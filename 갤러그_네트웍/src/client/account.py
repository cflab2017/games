import pygame
from pygame.locals import *
import pygame.time
import random

class Account():
    def __init__(self, screen) -> None:
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.msg_inbox = ''
        self.isRun = True
        self.isQuit = False
        
    def eventProcess(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.isQuit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.msg_inbox = self.msg_inbox[0:-1]
                if event.key == pygame.K_RETURN:
                    if self.msg_inbox is not None and len(self.msg_inbox.replace(" ","")) > 1:
                        if self.msg_inbox != '같은 이름 있음':
                            self.isRun = False
                else:
                    pass
            if event.type == pygame.TEXTINPUT:
                # print(event.text)
                self.msg_inbox += event.text
                
    def display_box(self):
        font = pygame.font.SysFont("malgungothic", 18)

        width = 200
        height = 40
        x = self.screen.get_width()/2 -  width/2
        y = self.screen.get_height()/2 - height/2
                
        msg = font.render(self.lable, 1, (255,255,255))
        self.screen.blit(msg,(x, y-100))
        
        #검정 사각형 채움
        pygame.draw.rect(self.screen, (  0,  0,  0),(x,y, width,height), 0)
        #흰색 사각형 라인
        pygame.draw.rect(self.screen, (255,255,255),(x,y, width,height), 1)
        
        msg = font.render('ID:'+self.msg_inbox, 1, (255,255,255))
        self.screen.blit(msg,(x+2, y+10))
                
    def run(self,client):
        self.lable = 'ID를 입력하세요.'
        while self.isRun:
            self.screen.fill((0, 0, 0))
            self.eventProcess()
            if self.isQuit:
                return None,None,False
            self.display_box()
            pygame.display.update() #화면 갱신
            if self.isRun == False:
                if client is not None:
                    client.send_request(self.msg_inbox)
                    while client.response == None:
                        pygame.time.wait(100)
                    if client.name == None:
                        self.isRun = True
                        self.lable = '같은 ID가 게임 중입니다.'      
                        self.msg_inbox = '' 
            self.clock.tick(100)            
        return self.msg_inbox,True