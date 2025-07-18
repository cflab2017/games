import pygame
from pygame.locals import *
import pygame.time
import random
import re

class Account():
    def __init__(self, screen,imgs) -> None:
        self.screen = screen
        self.imgs = imgs
        self.clock = pygame.time.Clock()
        self.msg_inbox = ''
        self.isRun = True
        self.select = random.randint(0,len(imgs)-1)
        self.isQuit = False
        
    def contains_special_char(self,text):
        # 특수문자 정규표현식: 영어, 숫자, 공백을 제외한 나머지
        # return bool(re.search(r'[^a-zA-Z0-9\s]', text))
        return bool(re.search(r'[^\uAC00-\uD7A3a-zA-Z0-9\s]', text))

    def eventProcess(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.isQuit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.msg_inbox = self.msg_inbox[0:-1]
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    if self.msg_inbox is not None:
                        if self.contains_special_char(self.msg_inbox):
                            self.lable = '특수문자는 입력 할 수 없어요.'  
                        elif len(self.msg_inbox.replace(" ","")) <= 1:
                            self.lable = '한글자 이상 입력하세요.'   
                        elif len(self.msg_inbox) > 6:
                            self.lable = '너무 긴 이름은 입력 할 수 없어요'   
                        else:
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
        
        #검정 사각형 채움
        pygame.draw.rect(self.screen, (  0,  0,  0),(x,y, width,height), 0)
        #흰색 사각형 라인
        pygame.draw.rect(self.screen, (255,255,255),(x,y, width,height), 1)
        
        msg = font.render('이름:'+self.msg_inbox, 1, (255,255,255))
        self.screen.blit(msg,(x+2, y+10))
        
    def select_img(self):
        length = len(self.imgs)
        rect = self.imgs[0].get_rect()
        gap = ((self.screen.get_width()-40)-(rect.width*length))/length#여백/이미지수
        #마우스 좌표
        pos = pygame.mouse.get_pos()
        
        for i, img in enumerate(self.imgs):
            
            rect = img.get_rect()
            rect.x = 20+ i*(rect.width + gap)
            rect.y = 100
            if rect.collidepoint(pos):
                if pygame.mouse.get_pressed()[0]:
                    self.select = i
                img_s = pygame.transform.scale(img, (100, 100))
                self.screen.blit(img_s, rect)
            else:
                self.screen.blit(img, rect)

        img = self.imgs[self.select]
        rect = img.get_rect()
        rect.x = self.screen.get_width()/2 - rect.width/2
        rect.y = self.screen.get_height()/2 - rect.height/2 - 100
        self.screen.blit(img, rect)
        
    def run(self,client):
        while self.isRun:
            self.screen.fill((0, 0, 0))
            self.eventProcess()
            if self.isQuit:
                return None,None,False
            self.display_box()
            self.select_img()
            pygame.display.update() #화면 갱신
            if self.isRun == False:
                client.send_request(self.msg_inbox)
                while client.response == None:
                    pygame.time.wait(100)
                if client.name == None:
                    self.isRun = True
                    self.msg_inbox = '같은 이름 있음'            
            self.clock.tick(100)            
        return self.msg_inbox,self.select,True