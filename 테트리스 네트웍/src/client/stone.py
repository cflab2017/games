
import pygame
from random import randrange as rand

import pickle
import os.path
import traceback

class Stone():
    shapes = [    
        [[1, 1, 1],
         [None,1,None]],

        [[None, 2, 2],
        [2, 2, None]],

        [[3, 3, None],
        [None, 3, 3]],

        [[4, None, None],
        [4, 4, 4]],

        [[None, None, 5],
        [5, 5, 5]],

        [[6, 6, 6, 6]],

        [[7, 7],
        [7, 7]]
    ]
    
    def __init__(self,  rows,cols,board,user_name):
        self.rows = rows
        self.cols = cols
        self.board = board
        
        self.level = 1
        self.score = 0
        self.score_pre = -1
        self.user_name = user_name
        self.item_cnt = 1
        
        #저장할 딕셔너리
        self.load_dict = {}
        self.score_high = self.update_user_dic('r')
        self.lines = 0
        
        self.gameover = False
        self.stone_x = 0
        self.stone_y = 0
        self.stone = []
        self.next_stone = []
        self.next_stone = self.shapes[rand(len(self.shapes))]
            
        self.snd_dic = {
            'move':pygame.mixer.Sound('./sound/move.wav'),
            'score':pygame.mixer.Sound('./sound/score.wav'),
            'game_over':pygame.mixer.Sound('./sound/game_over.wav'),
            'clear':pygame.mixer.Sound('./sound/clear.wav'),
            'destory':pygame.mixer.Sound('./sound/destory.wav'),
        }
        
    def set_DrawMsg(self,DrawMsg):
        self.DrawMsg = DrawMsg#.status_msg
        
    def game_init(self):
        self.level = 1
        self.score = 0
        self.lines = 0
        self.item_cnt = 0
        
    def update_user_dic(self,state,high_score=None):
        user_file_name = 'user.pickle'
        
        if state == 'r':
            #저장된 파일 불러오기
            if os.path.isfile(user_file_name): #불러올 파일이 있는가?
                with open(user_file_name, 'rb') as fr:
                    self.load_dict = pickle.load(fr) #딕셔너리로 변환                  
            if self.user_name not in self.load_dict:
                self.load_dict[self.user_name] = {'score':0}
                
            return self.load_dict[self.user_name]['score']
            
        if state == 'w':
            if high_score > self.load_dict[self.user_name]['score']:
                self.load_dict[self.user_name]['score'] = high_score
                with open(user_file_name, 'wb') as fw:
                    pickle.dump(self.load_dict,fw)
                    
    def new_stone(self):        
        self.stone = self.next_stone[:]
        self.next_stone = self.shapes[rand(len(self.shapes))]
        
        self.stone_x = int(self.cols / 2 - len(self.stone[0])/2)
        self.stone_y = 0
        
        if self.check_collision():
            if self.gameover== False:
                self.snd_dic['game_over'].play()
                #파일에 저장하기
                self.update_user_dic('w',self.score_high)
                self.game_init()
                
            self.gameover = True
    
    def check_collision(self):
        for cy, row in enumerate(self.stone):
            for cx, cell in enumerate(row):
                try:
                    if cell and self.board.board[cy + self.stone_y][cx + self.stone_x]:
                        return True
                except IndexError:
                    # err_msg = traceback.format_exc()
                    # print(err_msg) 
                    # print(cx , self.stone_x,cy , self.stone_y,len(self.board.board)) 
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
        pre_x = self.stone_x
        self.stone_x = self.stone_x + delta_x
        if self.stone_x < 0:
            self.stone_x = 0
        if self.stone_x > self.cols - len(self.stone[0]):
            self.stone_x = self.cols - len(self.stone[0])
        if self.check_collision():
            self.stone_x = pre_x
    
###########################################################
    #한칸 내리기
    def drop(self):  
        try:
            self.stone_y += 1
            if self.check_collision():
                # self.stone_y +=  self.join_matrixes() #마지막 라인에서 회전하면 overfllow
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
        self.lines += n
        self.score += linescores[n] * self.level
        
        # if n >= 1:
        #     self.item_cnt += int(n/1)
        if n >= 2:
            self.item_cnt += int(n/2)
            # print(f'self.item_cnt : {self.item_cnt}')
            self.DrawMsg.status_msg.append(f'공격권 획득 {self.item_cnt}개')
        
        if self.score > self.score_high:
            self.score_high = self.score
            

        if n > 0:
            self.snd_dic['clear'].play()
            
        if self.lines >= self.level*6:
            self.level += 1
            newdelay = 1000-50*(self.level-1)
            newdelay = 100 if newdelay < 100 else newdelay
            pygame.time.set_timer(pygame.USEREVENT+1, newdelay)
            
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