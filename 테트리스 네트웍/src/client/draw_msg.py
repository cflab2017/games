import pygame
from pygame.locals import *

import pickle
import os.path

from random import randrange as rand
import pygame.mouse
import pygame.rect
import pygame.time

class DrawMsg():
    
    def __init__(self,screen,stone,user_name,client,rlim,cell_size) -> None:
        self.screen = screen
        self.stone = stone
        self.user_name = user_name
        self.client = client
        self.rlim = rlim
        self.cell_size = cell_size
        self.msg_start = rlim+cell_size
        # self.defFont = pygame.font.Font(pygame.font.get_default_font(), 18)
        self.defFont = pygame.font.SysFont('malgungothic', 25)
        self.defFont18 = pygame.font.SysFont('malgungothic', 18)
        self.click_draw=[]
        self.status_msg = []
        self.status_msg_disp = ''
        self.status_msg_tick = 0
        self.attack_delay_tick = 0
        self.attack_msg_tick = 0
        self.snd_dic = {
            'shoot':pygame.mixer.Sound('./sound/shoot.wav'),
        }
    
    def disp_msg(self,msg, topleft,color=(255, 255, 255)):
        x, y = topleft
        pos = self.screen.blit(self.defFont.render(msg,False,color,(0, 0, 0)),(x, y))        
        return pos
    
    def disp_msg_s(self,msg, topleft,color=(255, 255, 255)):
        x, y = topleft
        pos = self.screen.blit(self.defFont18.render(msg,False,color,(0, 0, 0)),(x, y))        
        return pos
    
    def center_msg(self,msg):
        for i, line in enumerate(msg.splitlines()):
            msg_image = self.defFont.render(line, False,(255, 255, 255), (0, 0, 0))
            center_x, center_y = msg_image.get_size()
            center_x /= 2
            center_y /= 2
            self.screen.blit(msg_image, (self.screen.get_width() / 2-center_x,self.screen.get_height() / 2-center_y+i*22))
            
    def disp_msg_server_high_score(self,line):
        if '최고점수'  not in self.client.infor:
            return           
        name = self.client.infor['최고점수']['name']
        score = self.client.infor['최고점수']['score']
        self.disp_msg(f"최고점수: {score:7,} {name}",(self.msg_start, self.cell_size*(line)),(0, 255, 0))   
        
    def disp_msg_users(self,line):
        users, high = self.client.get_score()
        
        user_cnt = 0
        self.click_draw = []
        for user in users:
            name  = user[0]
            score = user[1]
            status = ''
            if name == self.client.name:
                color = (0, 255, 255)
            else:
                if self.stone.item_cnt>0:
                    color = (255, 0, 255)
                    ellip = pygame.time.get_ticks()-self.attack_msg_tick
                    
                    if ellip < 500:
                        status = ' 공격!! (마우스 클릭)'                        
                    elif ellip > 1000:
                        self.attack_msg_tick = pygame.time.get_ticks()
                else:
                    color = (255, 255, 255)
                
            pos = self.disp_msg(f"{user_cnt+1}등: {score:7,} {name} {status}",(self.msg_start, self.cell_size*(line+user_cnt)),color)
            if name != self.client.name:
                self.click_draw.append([pos,name])
            user_cnt += 1
            
        
        # user_cnt = 0
        # for value in self.client.infor:
        #     info = self.client.infor[value]
        #     if 'name'  not in info:
        #         continue            
        #     if 'score' not in info:
        #         continue
        #     if value=='최고점수':
        #         continue            
        #     if self.user_name == info['name']:
        #         continue
            
        #     name  = info['name']
        #     score = info['score']
        #     self.disp_msg(f"상대점수: {score:7,} {name}",(self.msg_start, self.cell_size*(line+user_cnt)))
        #     user_cnt += 1
        
    def check_click(self):
        mous = pygame.mouse.get_pos()
        for value in self.click_draw:
            pos = value[0]
            if pos.collidepoint(mous):
                if self.stone.item_cnt>0:
                    print(self.stone.item_cnt)
                    pygame.draw.rect(self.screen, (255,255,255),pos, 1)
                    if pygame.mouse.get_pressed()[0]:
                        ellip = pygame.time.get_ticks() - self.attack_delay_tick
                        if ellip > 300:
                            self.stone.item_cnt -= 1
                            name = value[1]
                            shape = rand(len(self.stone.shapes))
                            self.client.send_attack(name,shape)
                            self.snd_dic['shoot'].play()
                            self.attack_delay_tick = pygame.time.get_ticks()
                        
                    
    def drawStatusMsg(self):
        if not self.stone.gameover:                
            if self.status_msg_tick == 0:
                if len(self.status_msg):
                    self.status_msg_disp = self.status_msg.pop()
                    self.status_msg_tick = pygame.time.get_ticks()
            else:
                ellip = pygame.time.get_ticks() - self.status_msg_tick
                if ellip < 2000:
                    if ellip < 400 or (800 < ellip < 1200)or (1600 < ellip):
                        self.disp_msg(f"{self.status_msg_disp}",(self.cell_size, self.cell_size*10),(200, 0, 0))
                else:
                    self.status_msg_tick = 0
                    self.status_msg_disp = ''
    
    def draw(self,is_pause,pause_cnt,interf_next_stone):
        if self.stone.gameover:
            self.center_msg("Game Over!! (Re-start : Enter)")
        else:
                
            #게임화면 구분선
            if len(interf_next_stone):
                self.disp_msg(f" Next Attck", (self.msg_start+self.cell_size*5,2))
                self.disp_msg(f" X : {len(interf_next_stone)}", (self.msg_start+self.cell_size*9,self.cell_size*2))
                
            self.disp_msg("Next:", (self.msg_start,2))
            
            self.disp_msg_server_high_score(5)
            self.disp_msg(f"나의점수: {self.stone.score:7,} {self.user_name}",(self.msg_start, self.cell_size*6),(0, 255, 255))
            self.disp_msg_users(7)
            status = ''
            if self.stone.item_cnt>0:
                status = '(공격상대 클릭!!)'
                
            msg_idex = 13
            self.disp_msg(f"공격가능: {self.stone.item_cnt:,} {status}",(self.msg_start, self.cell_size*msg_idex),(200, 0, 0))
            msg_idex += 1
            self.disp_msg(f"현재레벨: {self.stone.level}",(self.msg_start, self.cell_size*msg_idex))
            msg_idex += 1
            self.disp_msg(f"제거라인: {self.stone.lines}",(self.msg_start, self.cell_size*msg_idex))
            msg_idex += 1
            self.disp_msg(f"최고점수: {self.stone.score_high:,}",(self.msg_start, self.cell_size*msg_idex))
            msg_idex += 1
            
            if is_pause:
                color = (255, 0, 0)
            else:
                color = (255, 255, 255)
            self.disp_msg(f"일지정지(P) 남은 횟수({pause_cnt})",(self.msg_start, self.cell_size*msg_idex),color)
            msg_idex += 1
            
            color = (0, 0, 255)
            self.disp_msg_s(f"[스톤제어]",(self.msg_start, self.cell_size*msg_idex),color)
            msg_idex += 1
            color = (255, 255, 255)
            self.disp_msg_s(f"왼쪽:←, 오른쪽:→, 회전:↑, 내리기:↓, 한번에내리기: space",(self.msg_start, self.cell_size*msg_idex),color)
            msg_idex += 1
            color = (0, 0, 255)
            self.disp_msg_s(f"[공격받은 스톤제어]",(self.msg_start, self.cell_size*msg_idex),color)
            msg_idex += 1
            color = (255, 0, 255)
            self.disp_msg_s(f"왼쪽:A, 오른쪽:D, 회전:W, 내리기:S, 한번에내리기: x",(self.msg_start, self.cell_size*msg_idex),color)
            msg_idex += 1
            color = (255, 0, 255)
            self.disp_msg_s(f"공격소멸: 1",(self.msg_start, self.cell_size*msg_idex),color)
            msg_idex += 1

            self.check_click()