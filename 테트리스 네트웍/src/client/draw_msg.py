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
        self.msg_start = rlim+cell_size - 30
        # self.defFont = pygame.font.Font(pygame.font.get_default_font(), 18)
        self.defFont40 = pygame.font.SysFont('malgungothic', 40)
        self.defFont = pygame.font.SysFont('malgungothic', 20)
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
    
    def disp_msg_f40(self,msg, topleft,color=(255, 255, 255)):
        x, y = topleft
        img = self.defFont40.render(msg,False,color,(0, 0, 0))
        img.set_alpha(100)
        pos = self.screen.blit(img,(x, y))        
        return pos
    
    def disp_msg(self,msg, topleft,color=(255, 255, 255)):
        x, y = topleft
        img = self.defFont.render(msg,False,color,(0, 0, 0))
        img.set_alpha(150)
        pos = self.screen.blit(img,(x, y))        
        return pos
    
    def disp_msg_s(self,msg, topleft,color=(255, 255, 255)):
        x, y = topleft
        img = self.defFont18.render(msg,False,color,(0, 0, 0))
        img.set_alpha(150)
        pos = self.screen.blit(img,(x, y))       
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
        # name = self.client.infor['최고점수']['name']
        # score = self.client.infor['최고점수']['score']
        # self.disp_msg(f"최고점수",(self.msg_start, self.cell_size*(line)),(255, 255, 255))  
        # self.disp_msg(f" {score:7,} ({name})",(self.msg_start+100, self.cell_size*(line)),(0, 255, 0)) 
        
        start_y = self.cell_size*(line) - 20
        self.disp_msg(f"[최고점수]",(self.msg_start, start_y),(255, 255, 255))  
        start_y += 30
        for i,key in enumerate(self.client.infor['최고점수']):
            name = self.client.infor['최고점수'][key]['name']
            score = self.client.infor['최고점수'][key]['score']
            date = self.client.infor['최고점수'][key]['date']
            self.disp_msg(f"{i+1}위 : {score:,}",(self.msg_start+4, start_y),(0, 255, 0)) 
            start_y += 30
            self.disp_msg(f"{name}({date})",(self.msg_start+40, start_y),(255, 255, 255)) 
            start_y += 30
            # self.disp_msg(f"{date}",(self.msg_start+40, start_y),(255, 255, 255)) 
            # start_y += 30
        
    def disp_msg_users(self,line):
        users = self.client.get_score()
        user_cnt = 0
        start_x = self.msg_start+250        
        start_y = self.cell_size*(line+user_cnt) - 20        
        pos = self.disp_msg(f"[접속자 순위]",(start_x, start_y),(255,255,255))
        start_y += 30
        user_cnt += 1
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
                        status = ' 공격'                        
                    elif ellip > 1000:
                        self.attack_msg_tick = pygame.time.get_ticks()
                else:
                    color = (255, 255, 255)
                
            pos = self.disp_msg(f" {user_cnt}위: {score:,} {name} {status}",(start_x, start_y),color)
            start_y += 30
            if name != self.client.name:
                self.click_draw.append([pos,name])
            user_cnt += 1
        
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
                    
    def disp_msg_score(self):
        msg = f"(level : {self.stone.level}) (score : {self.stone.score:,}) "
        img = self.defFont.render(msg,False,(0, 0, 0),(255, 255, 255))
        img.set_alpha(150)
        rect = img.get_rect()
        rect.x = 10
        rect.y = 10
        self.screen.blit(img,rect)
    
    def draw(self,is_pause,pause_cnt,interf_next_stone):
        if self.stone.gameover:
            self.center_msg("Game Over!! (Re-start : Enter)")
        else:
                
            #게임화면 구분선
            msg_add = ' Next Attck'
            if len(interf_next_stone) > 3:
                msg_add += f' + {len(interf_next_stone)-3}'            
            self.disp_msg(msg_add, (self.msg_start+self.cell_size*5,2))
                
            self.disp_msg("Next:", (self.msg_start,2))
            
            self.disp_msg_server_high_score(6)
            self.disp_msg_users(6)
                
            msg_idex = 15
            self.disp_msg(f"최고점수: {self.stone.score_high:,}",(self.msg_start, self.cell_size*msg_idex))
            
            msg_idex += 1
            if self.stone.item_cnt>0:
                color = (255, 0, 0)
            else:
                color = (255, 255, 255)
            self.disp_msg(f"공격가능: {self.stone.item_cnt:,}개 (방어)",(self.msg_start, self.cell_size*msg_idex),color)
            
            msg_idex += 1            
            if is_pause:
                color = (255, 0, 0)
            else:
                color = (255, 255, 255)
            self.disp_msg(f"일지정지: {pause_cnt}번 남음",(self.msg_start, self.cell_size*msg_idex),color)
            self.check_click()