import pygame
from pygame import *
from pygame.locals import *
import pygame.time
import pygame.font
import random
import re
import tkinter as tk
from tkinter import simpledialog

class Account():
    from commu.client import socketClient
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 800
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.msg_inbox = ''
        self.isRun = True
        self.isQuit = False
        self.font = pygame.font.SysFont("malgungothic", 30)
        img_bg = pygame.image.load('./images/bg1.jpg')
        self.img_bg = pygame.transform.scale(img_bg,(self.screen.get_width(), self.screen.get_height()))
        self.cursor_tick = pygame.time.get_ticks()

    
    def popup_input(self,prompt="비밀번호를 입력하세요:"):
        def on_ok(event=None):
            nonlocal value
            value = entry.get()
            win.destroy()

        value = None
        win = tk.Tk()

        # 화면 크기 구하기
        screen_width = win.winfo_screenwidth()
        screen_height = win.winfo_screenheight()

        # 팝업 크기 예상값 (약 300x100)
        popup_w, popup_h = 300, 100
        x = (screen_width // 2) - (popup_w // 2)
        y = (screen_height // 2) - (popup_h // 2)
        
        win.geometry(f"300x100+{x}+{y}")  # 위치 지정
        win.title("비밀번호")

        tk.Label(win, text=prompt).pack(pady=5)
        entry = tk.Entry(win)
        entry.pack(pady=5)
        entry.focus()
        entry.bind("<Return>", on_ok)

        tk.Button(win, text="확인", command=on_ok).pack(pady=5)

        win.lift()
        win.focus_force()
        win.after(50, lambda: entry.focus())
        entry.focus()                  # 포커스 주기 (필요 시)
        
        win.mainloop()
        return value

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
                        elif len(self.msg_inbox) > 10:
                            self.lable = '너무 긴 이름은 입력 할 수 없어요'   
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
                
    def run(self,client:socketClient):
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
                self.password = self.popup_input()
                if self.contains_special_char(self.password):
                    self.lable = '특수문자는 입력 할 수 없어요.'  
                    self.isRun = True
                elif len(self.password.replace(" ","")) <= 1:
                    self.lable = '한글자 이상 입력하세요.'   
                    self.isRun = True
                elif len(self.password) > 10:
                    self.lable = '너무 긴 비밀번호는 입력 할 수 없어요' 
                    self.isRun = True
                else:                  
                    client.send_request_sign(self.msg_inbox,self.password)
                    while client.response == None:
                        pygame.time.wait(100)
                    if client.name == None:
                        self.isRun = True
                        self.lable = '같은 ID가 게임 중입니다.'      
                        self.msg_inbox = '' 
                    if client.password_ok == 0:
                        self.isRun = True
                        self.lable = '비밀번호가 다릅니다.'      
                        # self.msg_inbox = '' 
            self.clock.tick(100)          
        pygame.quit()  
        return self.msg_inbox,True


