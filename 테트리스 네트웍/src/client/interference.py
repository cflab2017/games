
import pygame
from random import randrange as rand

import traceback
import pickle
import os.path

class Interference():
    shapes = [    
        [[(100, 0,  100), (100, 0,  100), (100, 0,  100)],
         [None,(100, 0,  100),None]],

        [[None, (100, 0,  100), (100, 0,  100)],
        [(100, 0,  100), (100, 0,  100), None]],

        [[(100, 0,  100), (100, 0,  100), None],
        [None, (100, 0,  100), (100, 0,  100)]],

        [[(100, 0,  100), None, None],
        [(100, 0,  100), (100, 0,  100), (100, 0,  100)]],

        [[None, None, (100, 0,  100)],
        [(100, 0,  100),(100, 0,  100), (100, 0,  100)]],

        [[(100, 0,  100), (100, 0,  100), (100, 0,  100), (100, 0,  100)]],

        [[(100, 0,  100), (100, 0,  100)],
        [(100, 0,  100), (100, 0,  100)]]
    ]
    
    def __init__(self,stone,rows,cols,board,user_name):
        self.rows = rows
        self.cols = cols
        self.board = board
        self.mstone = stone
        
        self.user_name = user_name
                
        self.stone_x = 0
        self.stone_y = 0
        self.stone = None
        self.next_stone = []
        # self.next_stone.append(self.shapes[rand(len(self.shapes))])
        # self.next_stone.append(self.shapes[rand(len(self.shapes))])
            
        self.snd_dic = {
            'move':pygame.mixer.Sound('./sound/move.wav'),
            'score':pygame.mixer.Sound('./sound/score.wav'),
            'clear':pygame.mixer.Sound('./sound/clear.wav'),
            'game_over':pygame.mixer.Sound('./sound/game_over.wav'),
            'destory':pygame.mixer.Sound('./sound/destory.wav'),
            
        }

    def set_DrawMsg(self,DrawMsg):
        self.DrawMsg = DrawMsg#.status_msg
        
    def create_stone(self,idex):
        self.next_stone.append(self.shapes[idex])
        if len(self.stone)==0:
            self.new_stone()
            
    def del_stone(self):
        if self.mstone.item_cnt > 0:
            self.mstone.item_cnt -= 1
            self.stone = []
            self.new_stone()
            self.snd_dic['destory'].play()

    def new_stone(self):
        if len(self.next_stone):
            self.stone = self.next_stone.pop()
            # self.next_stone = self.shapes[rand(len(self.shapes))]
            
            self.stone_x = int(self.cols / 2 - len(self.stone[0])/2)
            self.stone_y = 0
        else:
            self.stone = []
    
    def check_collision(self):
        for cy, row in enumerate(self.stone):
            for cx, cell in enumerate(row):
                try:
                    if cell and self.board.board[cy + self.stone_y][cx + self.stone_x]:
                        return True
                except IndexError:
                    return True
        return False    

    def rotate_clockwise(self):
        result = []
        for x in range(len(self.stone[0]) - 1, -1, -1):
            col = []
            for y in range(len(self.stone)):
                col.append(self.stone[y][x])
            result.append(col)        
        return result

    def rotate_stone(self):
        if self.stone is None or (len(self.stone)<1):
            return
        
        pre_stone = self.stone
        
        self.stone = self.rotate_clockwise()
        if self.check_collision():
            self.stone = pre_stone
        
        while True:
            new_x = self.stone_x
            if new_x < 0:
                self.stone_x += 1
                continue
            if new_x > self.cols - len(self.stone[0]):
                self.stone_x -= 1
                continue
            break
        
    def move(self, delta_x):
        if self.stone is None or (len(self.stone)<1):
            return
        try:
            pre_x = self.stone_x
            self.stone_x = self.stone_x + delta_x
            if self.stone_x < 0:
                self.stone_x = 0
            if self.stone_x > self.cols - len(self.stone[0]):
                self.stone_x = self.cols - len(self.stone[0])
            if self.check_collision():
                self.stone_x = pre_x
        except Exception:            
            err_msg = traceback.format_exc()
            print(err_msg) 
    
###########################################################
    #한칸 내리기
    def drop(self):
        try:
            if (self.stone is not None) and len(self.stone):
                self.stone_y += 1
                if self.check_collision():
                    self.join_matrixes()
                    self.new_stone()
                    cleared_rows = 0
                    while True:
                        for i, row in enumerate(self.board.board):
                            if None not in row:
                                self.remove_row(i)
                                cleared_rows += 1
                                break
                        else:
                            break
                    
                    self.add_cl_lines(cleared_rows)
                    return True
                return False
            else:
                return True
        except Exception:       
            err_msg = traceback.format_exc()
            print(err_msg) 
            return True
        
    #내려갈 수 있는 곳까지 내려가기
    def insta_drop(self):
        while(not self.drop()):
            pass
        
    #한줄 지우고 새로 한줄 넣기
    def remove_row(self,row):
        del self.board.board[row]
        self.board.board = [[None for i in range(self.cols)]] + self.board.board

    #점수 계산하고 레벨업
    def add_cl_lines(self,n):
        linescores = [0, 40, 100, 300, 1200]
        self.mstone.lines += n
        self.mstone.score += linescores[n] * self.mstone.level
        
        # if n >= 1:
        #     self.mstone.item_cnt += int(n/1)
        if n >= 2:
            self.mstone.item_cnt += int(n/2)
            print(f'self.item_cnt : {self.mstone.item_cnt}')
            self.DrawMsg.status_msg.append(f'공격권 획득 {self.mstone.item_cnt}개')
            
        if self.mstone.score > self.mstone.score_high:
            self.mstone.score_high = self.mstone.score
            
        if n > 0:
            self.snd_dic['clear'].play()
            
        
            
        # if self.mstone.lines >= self.mstone.level*6:
        #     self.mstone.level += 1
            # newdelay = 1000-50*(self.level-1)
            # newdelay = 100 if newdelay < 100 else newdelay
            # pygame.time.set_timer(pygame.USEREVENT+1, newdelay)
            
    #보드에 stone을 삽입하기
    def join_matrixes(self):
        result_y = 0
        for cy, row in enumerate(self.stone):
            for cx, val in enumerate(row):
                if val is not None:
                    if cy+self.stone_y-1 >= len(self.board.board):
                        result_y -= 1
        # if result_y < 0:
        #     return result_y
        self.stone_y += result_y
        
        for cy, row in enumerate(self.stone):
            for cx, val in enumerate(row):
                if val is not None:
                    self.board.board[cy+self.stone_y-1][cx+self.stone_x] = val
        return 0