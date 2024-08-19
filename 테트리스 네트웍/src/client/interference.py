
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
            'game_over':pygame.mixer.Sound('./sound/game_over.wav'),
        }

    def create_stone(self,idex):
        self.next_stone.append(self.shapes[idex])
        if len(self.stone)==0:
            self.new_stone()
        
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
        new_stone = self.rotate_clockwise()
        if not self.check_collision():
            self.stone = new_stone
        
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
            new_x = self.stone_x + delta_x
            if new_x < 0:
                new_x = 0
            if new_x > self.cols - len(self.stone[0]):
                new_x = self.cols - len(self.stone[0])
            if not self.check_collision():
                self.stone_x = new_x
        except Exception:            
            err_msg = traceback.format_exc()
            print(err_msg) 
    
###########################################################
    #한칸 내리기
    def drop(self):
        if (self.stone is not None) and len(self.stone):
            self.stone_y += 1
            if self.check_collision():
                self.join_matrixes()
                self.new_stone()
                cleared_rows = 0
                # while True:
                for i, row in enumerate(self.board.board):
                    if None not in row:
                        self.remove_row(i)
                        cleared_rows += 1
                        break
                    # else:
                    #     break
                
                self.add_cl_lines(cleared_rows)
                return True
            return False
        else:
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
        
        if self.mstone.score > self.mstone.score_high:
            self.mstone.score_high = self.mstone.score
            
        if n > 0:
            self.snd_dic['score'].play()
            
        # if self.mstone.lines >= self.mstone.level*6:
        #     self.mstone.level += 1
            # newdelay = 1000-50*(self.level-1)
            # newdelay = 100 if newdelay < 100 else newdelay
            # pygame.time.set_timer(pygame.USEREVENT+1, newdelay)
            
    #보드에 stone을 삽입하기
    def join_matrixes(self):
        for cy, row in enumerate(self.stone):
            for cx, val in enumerate(row):
                if val is not None:
                    self.board.board[cy+self.stone_y-1][cx+self.stone_x] = val