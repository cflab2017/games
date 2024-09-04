import pygame
from pygame import *
from pygame.locals import *
import pygame.time
import pygame.font
import random

class Account():
    def __init__(self, screen:Surface) -> None:
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.msg_inbox = ''
        self.isRun = True
        self.isQuit = False
        self.font = pygame.font.SysFont("malgungothic", 30)
        img_bg = pygame.image.load('./images/bg.jpg')
        self.img_bg = pygame.transform.scale(img_bg,(screen.get_width(), screen.get_height()))
        self.cursor_tick = pygame.time.get_ticks()
        
    def eventProcess(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.isQuit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.msg_inbox = self.msg_inbox[0:-1]
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    if self.msg_inbox is not None:
                        if len(self.msg_inbox.replace(" ","")) <= 1:
                            self.lable = '한글자 이상 입력하세요.'   
                        else:
                            self.isRun = False
                else:
                    pass
            if event.type == pygame.TEXTINPUT:
                self.msg_inbox += event.text
                
    def display_box(self):
                
        img = self.font.render(self.lable, 1, (255,0,255),(0,0,0))
        img.set_alpha(200)
        rect = img.get_rect()
        rect.centerx = self.screen.get_width()/2
        rect.centery = self.screen.get_height()/2-200
        self.screen.blit(img,rect)
        
        # #검정 사각형 채움
        # pygame.draw.rect(self.screen, (  0,  0,  0),(x,y, width,height), 0)
        # #흰색 사각형 라인
        # pygame.draw.rect(self.screen, (255,255,255),(x,y, width,height), 1)
        ellip = pygame.time.get_ticks() - self.cursor_tick
        msg = f'[{self.msg_inbox}◁](enter)'
        if ellip < 400:
            pass
        elif ellip < 800:
            msg = f'[{self.msg_inbox}◀](enter)'
        else:
            self.cursor_tick = pygame.time.get_ticks()
        img = self.font.render(msg, 1, (255,255,255),(0,0,0))
        img.set_alpha(200)
        rect = img.get_rect()
        rect.centerx = self.screen.get_width()/2
        rect.centery = self.screen.get_height()/2
        self.screen.blit(img,rect)
                
    def run(self,client):
        self.lable = 'ID를 입력하세요.'
        while self.isRun:
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.img_bg,(0,0))
            self.eventProcess()
            if self.isQuit:
                return None,None,False
            self.display_box()
            pygame.display.update() #화면 갱신
            if self.isRun == False:
                client.send_request(self.msg_inbox)
                while client.response == None:
                    pygame.time.wait(100)
                if client.name == None:
                    self.isRun = True
                    self.lable = '같은 ID가 게임 중입니다.'      
                    self.msg_inbox = '' 
            self.clock.tick(100)            
        return self.msg_inbox,True