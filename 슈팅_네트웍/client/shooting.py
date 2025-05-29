import pygame
from pygame.locals import *
import pygame.time
import random

from client import *
from user import *
from users import *
from account import *
import pickle
import os.path

class game_main():
    isActive = True
    WIDTH = 1000
    HEIGHT = 1000
    def __init__(self) -> None:
        #pygame 초기화
        pygame.init() #pygame 초기화
        pygame.display.set_caption("codingnow.co.kr") #타이틀
        self.clock = pygame.time.Clock() #프레임을 처리 하기위해
        
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        # pygame.mixer.music.load(f'./sound/happyday.mp3')
        # pygame.mixer.music.play(-1)

        self.img_player = []
        self.load_player_img()
        
        self.client = socketClient(self)
        
        account = Account(self.screen,self.img_player)
        name,character,self.isActive = account.run(self.client)
        
        if self.isActive==False:
            return
        
        pygame.display.set_caption(f"사용자:{name}")
        
        self.player_group = []
        self.user = User(self.screen,
                            self.client,
                            name,
                            character,
                            self.img_player,
                            self.img_arrow,
                            self.img_heart,
                            self.img_shield,
                            random.randint(0, self.WIDTH),                           
                            random.randint(0, self.HEIGHT))    
        self.client.send_infor(self.user)    
        # self.player_group.append(self.user)
        
        # self.user.setClient(self.client)
        # print(self.client.identity)
        
    def load_player_img(self):
        file_names = [
            "player_army.png",    "player_dinosaur.png",
            "player_ninja.png",   "player_penguin.png",
            "player_Pirate.png",  "player_police.png",
            "player_samurai.png", "player_soldier.png",
            "player_warrior.png",
            ]
        
        self.img_player = []
        for file in file_names:
            image = pygame.image.load(f"./images/{file}").convert_alpha()
            image = pygame.transform.scale(image, (80, 80))
            self.img_player.append(image)  

        img_arrow = pygame.image.load(f"./images/arrow.png").convert_alpha()
        self.img_arrow = pygame.transform.scale(img_arrow, (60, 20))
        
        img_heart = pygame.image.load(f"./images/heart.png").convert_alpha()
        self.img_heart = pygame.transform.scale(img_heart, (40, 40))
        
        img_shield = pygame.image.load(f"./images/shield.png").convert_alpha()
        self.img_shield = pygame.transform.scale(img_shield, (int(50*1.5), int(60*1.5)))
        
        img_bg = pygame.image.load(f"./images/bg.png").convert_alpha()
        self.img_bg = pygame.transform.scale(img_bg, (self.screen.get_width()+100, self.screen.get_height()+100))
                
    #이벤트 확인 및 처리 함수
    def eventProcess(self):
        for event in pygame.event.get():#이벤트 가져오기
            if event.type == QUIT: #종료버튼?
                self.isActive = False
            if event.type == pygame.KEYDOWN:#키 눌림?
                if event.key == pygame.K_ESCAPE:#ESC 키?
                    self.isActive = False
                if event.key == pygame.K_SPACE:#space?
                    pass
    
    def run(self):
        bg_time_tick = pygame.time.get_ticks()
        bg_rec = [0,0]
        while self.isActive:
            # self.screen.fill((255, 255, 255)) #화면을 흰색으로 채우기
            # self.screen.blit(self.img_bg, (0+random.randint(-100,100),0+random.randint(-100,100)))
            if pygame.time.get_ticks() - bg_time_tick > 200:
                bg_time_tick = pygame.time.get_ticks()
                bg_rec = [-50+random.randint(-50,50),-50+random.randint(-50,50)]
                
            self.screen.blit(self.img_bg, bg_rec)
            self.eventProcess() #이벤트 함수 호출
            
            self.user.update(self.player_group)   
                 
            for player in self.player_group:
                player.update()
                
            pygame.display.update() #화면 갱신
            self.clock.tick(200) #초당 60프레임 갱신을 위한 잠시 대기

# print(__name__)
if __name__ == "__main__":
    game = game_main()
    game.run()
    
# pyinstaller -w -F .\shooting.py
# pyinstaller --onefile --debug=all test.py
# pyinstaller -w -F --debug=all game.py