import pygame
import pygame.image
import pygame.image
import pygame.key
from pygame.locals import *
import pygame.time
import pygame.time
import pygame.transform
import pygame.key

from board import *
from stone import *
from interference import *

from client import *
from account import *
from draw_msg import *

from draw_button import *
from draw_line import *
import pickle
import os.path

# import pyautogui
# pip install pygame
class Tetris():
    isActive = True
    design_mode = 0
    cell_size = 42
    cols = 10
    rows = 23
    rlim = cell_size*cols
    is_pause = False
    is_freeze = False
    freeze_tick_start = 0
    freeze_tick_end = 0
    pause_cnt = 0
    SCREEN_WIDTH = cell_size*cols + 520
    SCREEN_HEIGHT = cell_size*rows
    
    LANG_KOREAN = 0x0412  # 한국어
    LANG_ENGLISH = 0x0409  # 영어
    
    def __init__(self) -> None:                            
        #1.초기화 하기
        pygame.init() #pygame 초기화
        self.clock = pygame.time.Clock() #프레임을 처리 하기위해

        #3.스크린 생성하기
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT)) #화면생성

        img_bg = pygame.image.load('./images/bg.jpg')
        self.img_bg = pygame.transform.scale(img_bg,(self.screen.get_width(), self.screen.get_height()))
        #4.클래스 생성
        self.client = socketClient()

        self.account = Account(self.screen)
        self.user_name,self.isActive = self.account.run(self.client)

        pygame.display.set_caption(f"codingnow.co.kr 버전02 (접속자 : {self.user_name})") #타이틀
        self.board = Board(self.rows,self.cols)
        self.stone = Stone(self.rows,self.cols,self.board,self.user_name)
        self.interf = Interference(self.stone,self.rows,self.cols,self.board,self.user_name)
        self.msg = DrawMsg(self.screen,self.stone,self.user_name,self.client,self.rlim,self.cell_size)

        self.btnDraw = Draw_button(self.screen)
        self.draw_line = Draw_line(self.screen,self.cell_size,self.rlim,self.cols)

        self.stone.set_DrawMsg(self.msg)
        self.interf.set_DrawMsg(self.msg)

        self.client.set_interf(self.interf)
        self.init_game()
        self.set_event_dict()    
        
    def init_game(self):
        self.stone.gameover = False
        self.is_pause = False
        self.pause_cnt = 5
        self.board.new_board()
        self.stone.new_stone()
        self.interf.new_stone()
        self.stone.item_cnt = 2
        pygame.time.set_timer(pygame.USEREVENT+1, 1000)#1초마다 "USEREVENT+1" 이벤트 발생
        pygame.time.set_timer(pygame.USEREVENT+2, 1000)

#이벤트 처리함수
    def eventProcess(self):
        for event in pygame.event.get():#이벤트 가져오기
            
            # print(event)
            if event.type == QUIT: #종료버튼?
                self.isActive = False
            if event.type == pygame.KEYDOWN:#키 눌림?                    
                if self.stone.gameover:
                    if event.key == pygame.K_RETURN:#재시작
                        self.init_game()
                self.key_process_stone(event.key,True)
                        
            if event.type == pygame.KEYUP:
                self.key_process_stone(event.key,False)
                
            if event.type == pygame.TEXTINPUT:
                print(event.text)                
                if event.text in 'ㅈㅁㄴㅇ':
                    if len(self.msg.status_msg)==0:
                        self.msg.status_msg.append(f'키보드 변경!! 영문으로 변경!!')
                    self.stone.snd_dic['destory'].play()  
                                
            if self.is_pause == False and self.is_freeze == False:
                if event.type == pygame.USEREVENT+2:#사용자 이벤트
                        self.interf.drop()                    
                if event.type == pygame.USEREVENT+1:#사용자 이벤트
                        self.stone.drop()            
                        
        key_pressed = pygame.key.get_pressed()
        for key in self.event_dic:
            if key_pressed[key] and self.event_dic[key]['long']:
                if self.event_dic[key]['tick'] > 0:
                    if pygame.time.get_ticks()-self.event_dic[key]['tick']>140:
                        self.key_process_stone(key,True)
                        self.event_dic[key]['tick'] = pygame.time.get_ticks()
                
    def key_event(self,key):        
        if key == pygame.K_F5:
            self.draw_line.design_mode += 1
            self.draw_line.design_mode %= 3
                
        if key == pygame.K_1:
            if self.is_pause or self.is_freeze:
                return
            self.interf.snd_dic['move'].play()
            msg_temp = self.interf.del_stone()
            if msg_temp is not None:
                self.msg.status_msg.append(f'{msg_temp}')
        
        if key == pygame.K_2:
            if self.is_pause or self.is_freeze:
                return
            self.interf.snd_dic['move'].play()
            msg_temp = self.stone.change_boom()
            if msg_temp is not None:
                self.msg.status_msg.append(f'{msg_temp}')
                
        if key == pygame.K_3:
            
            if self.is_pause:
                self.msg.status_msg.append(f'일시정지 중에는 사용할 수 없음')
            elif self.stone.item_cnt <= 0:
                self.msg.status_msg.append(f'얼음 교환 권 없음')
                self.stone.item_cnt = 0
            else:
                self.stone.item_cnt -= 1
                self.is_freeze = True
                if self.freeze_tick_start == 0:
                    self.freeze_tick_start = pygame.time.get_ticks()
                    self.freeze_tick_end = self.freeze_tick_start + 3000
                else:
                    self.freeze_tick_end += 1000
            
                
        if key == pygame.K_p:
            if self.is_freeze:
                self.msg.status_msg.append(f'얼음 중에는 사용할 수 없음')
            else:
                if self.is_pause:
                    self.is_pause = False
                else:
                    if self.pause_cnt > 0:
                        self.is_pause = True                    
                        self.pause_cnt -= 1      
                        self.msg.status_msg.append(f'일시정지 남은 횟수 {self.pause_cnt}개')
                                
    def key_process_stone(self,key,is_press):    
        if key in self.event_dic:
            if self.is_pause and key != pygame.K_p and self.is_freeze==False:
                pass
            elif is_press:
                self.event_dic[key]['btnDraw'].set_alpha(200)
                if (self.event_dic[key]['ctrl'] is not None) and (self.stone.gameover==False):                    
                    if self.event_dic[key]['long']:
                        if self.event_dic[key]['tick'] == 0:
                            self.event_dic[key]['tick'] = pygame.time.get_ticks()
                    self.event_dic[key]['ctrl'].key_event(key)
            else:
                self.event_dic[key]['btnDraw'].set_alpha(100)
                self.event_dic[key]['tick'] = 0
                            
    def set_event_dict(self):
        self.event_dic = {
            pygame.K_SPACE:{'btnDraw':self.btnDraw.btn_space,'ctrl':self.stone,'long':False, 'tick':0},
            pygame.K_UP:{'btnDraw':self.btnDraw.btn_up,'ctrl':self.stone,'long':False, 'tick':0},
            pygame.K_DOWN:{'btnDraw':self.btnDraw.btn_down,'ctrl':self.stone,'long':True, 'tick':0},
            pygame.K_LEFT:{'btnDraw':self.btnDraw.btn_left,'ctrl':self.stone,'long':True, 'tick':0},
            pygame.K_RIGHT:{'btnDraw':self.btnDraw.btn_right,'ctrl':self.stone,'long':True, 'tick':0},
            #####################################
            pygame.K_LSHIFT:{'btnDraw':self.btnDraw.btn2_space,'ctrl':self.interf,'long':False, 'tick':0},
            pygame.K_w:{'btnDraw':self.btnDraw.btn2_up,'ctrl':self.interf,'long':False, 'tick':0},
            pygame.K_s:{'btnDraw':self.btnDraw.btn2_down,'ctrl':self.interf,'long':True, 'tick':0},
            pygame.K_a:{'btnDraw':self.btnDraw.btn2_left,'ctrl':self.interf,'long':True, 'tick':0},
            pygame.K_d:{'btnDraw':self.btnDraw.btn2_right,'ctrl':self.interf,'long':True, 'tick':0},
            #####################################
            pygame.K_F5:{'btnDraw':self.btnDraw.btn_stone,'ctrl':self,'long':False, 'tick':0},
            pygame.K_p:{'btnDraw':self.btnDraw.btn_pause,'ctrl':self,'long':False, 'tick':0},
            pygame.K_1:{'btnDraw':self.btnDraw.btn_shield,'ctrl':self,'long':False, 'tick':0},
            pygame.K_2:{'btnDraw':self.btnDraw.btn_boom,'ctrl':self,'long':False, 'tick':0},
            pygame.K_3:{'btnDraw':self.btnDraw.btn_freeze,'ctrl':self,'long':False, 'tick':0},
        }
    
    def run(self):
        while self.isActive:
            self.screen.fill((0, 0, 0)) #화면을 흰색으로 채우기
            self.screen.blit(self.img_bg,(0,0))
            self.eventProcess() #이벤트 처리
            self.btnDraw.draw()
            self.msg.draw(self.is_pause,self.pause_cnt,self.interf.next_stone)
            
                
            if self.is_pause and len(self.msg.status_msg)==0:
                self.msg.status_msg.append(f'일시정지 남은 횟수 {self.pause_cnt}개')
                            
            if self.stone.gameover == False:
                self.draw_line.draw(self.board, self.stone, self.interf,self.is_freeze)
                self.msg.disp_msg_score()
                if self.stone.score != self.stone.score_pre:
                    self.client.send_score(self.user_name, self.stone.score)
                    self.stone.score_pre = self.stone.score
            self.msg.drawStatusMsg()

            if self.is_freeze:
                ellip = self.freeze_tick_end - pygame.time.get_ticks()
                if ellip < 0:
                    self.is_freeze=False
                    self.freeze_tick_start = 0
                    self.freeze_tick_end = 0
                else:
                    self.msg.disp_msg_f40(f'얼음 남은시간 {ellip}',(self.cell_size, self.cell_size*7),(255,0,0))
                    
            pygame.display.update() #화면 갱신
            self.clock.tick(100) #초당 30프레임 

if __name__ == '__main__':
    game = Tetris()
    game.run()
# pyinstaller -w -F .\tetris.py
# pyinstaller --onefile --debug=all test.py
# pyinstaller -w -F --debug=all game.py