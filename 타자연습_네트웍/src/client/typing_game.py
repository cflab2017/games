import pygame
import pygame.key
from pygame.locals import *
import pygame.time
import winsound
from _thread import *
import time
from client import *
import pyautogui
from account import *

from keyboardDraw import *

from gen_word import *
# 1옥타브: C, C#, D, D#, E, F, F#, G, G#, A, A#, B
pitch = {'c_': 523, 'cs': 554, 'd_': 587, 'ds': 622, 'e_': 659,
         'f_': 698, 'fs': 740, 'g_': 784, 'gs': 831, 'a_': 880,
         'as': 932, 'b_': 988}
lasting = 80

class game_main():
    
    isActive = True
    WIDTH = 1000-110
    HEIGHT = 1000
    msg_inbox = ''
    score = 0
    score_high = 0
    hp_max = 5
    hp = hp_max
    level = 1
    match_cnt = 0
    is_game_over = False
    is_game_init = True
    com_bo_tick = 0
    com_bo_tick_limit = 2000
    com_bo_ellip = 0
    com_bo_bonus = 3
    com_bo_position = []
    play_memody = []
    msg_win_width = 400
    inp_win_heigh = 80
    
    
    
    
    def __init__(self) -> None:
        pygame.init() #pygame 초기화
        pygame.display.set_caption("codingnow.co.kr") #타이틀
        self.clock = pygame.time.Clock() #프레임을 처리 하기위해
        
        self.mfont30 = pygame.font.SysFont("malgungothic", 20)
        self.mfont18 = pygame.font.SysFont("malgungothic", 18)
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        # self.creat_name()
        self.client = socketClient()
        account = Account(self.screen)
        self.user_name,self.isActive = account.run(self.client)
        
        self.keyboardDraw = KeyboardDraw(self.screen)
        self.snd_space = pygame.mixer.Sound(f'./sound/shoot.wav')
        self.snd_hit = pygame.mixer.Sound(f'./sound/hit.wav')
        self.snd_item = pygame.mixer.Sound(f'./sound/item.wav')
        self.snd_gameover = pygame.mixer.Sound(f'./sound/game_over.wav')
        self.gen_word = Gen_Workd(self,self.client.words)
        start_new_thread(self.thread_play, (self.play_memody, ))
        
    def creat_name(self):
        msg = '이름을 입력하세요'
        while True:
            name = pyautogui.prompt(msg,'게임시작')
            
            if name is None or len(name.replace(" ","")) < 1:
                msg = '이름을 입력해야 합니다.'
                continue
            self.user_name = name
            break           

    def thread_play(self,play_memody):
        
        while True:
            time.sleep(0.1)
            if len(play_memody):
                # print(play_memody)
                for memody in play_memody:
                    winsound.Beep(pitch[memody], lasting)
                play_memody.clear()
        
    #이벤트 확인 및 처리 함수
    def eventProcess(self):
        for event in pygame.event.get():#이벤트 가져오기
            self.keyboardDraw.update_key(event)
            if event.type == QUIT: #종료버튼?
                self.isActive = False
                    
            if event.type == pygame.TEXTINPUT:
                if self.is_game_over == False:
                    self.msg_inbox += event.text
                    # winsound.Beep(pitch['g_'], lasting)
                    self.play_memody.append('g_')
                    
            if event.type == pygame.KEYDOWN:#키 눌림?
                if event.key == pygame.K_ESCAPE:#ESC 키?
                    self.isActive = False
                if event.key == pygame.K_SPACE:#space?
                    if self.is_game_over:
                        self.is_game_init = True
                elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    # self.msg_inbox = ''
                    # winsound.Beep(pitch['g_'], lasting)
                    if self.is_game_over == False:
                        centerx, centery = self.gen_word.match_word(self.msg_inbox)
                        if centerx is not None:
                            if self.com_bo_ellip > 0:
                                self.score += (len(self.msg_inbox)+3)*self.com_bo_bonus*self.level
                                self.com_bo_position.append([centerx, centery,self.com_bo_tick,self.com_bo_bonus])
                                self.com_bo_bonus += 1
                                if(self.com_bo_bonus > 10):
                                    self.com_bo_bonus = 10
                                
                                # self.snd_space.play()
                                self.snd_hit.play()
                            else:
                                self.score += (len(self.msg_inbox)+3)*self.level
                                self.snd_hit.play()
                            self.msg_inbox = ''
                            
                            if self.score > self.score_high:
                                self.score_high = self.score                                
                                # self.snd_item.play()
                                
                            self.client.send_score(self.user_name, self.score)
                            if self.hp < self.hp_max:
                                self.hp += 1
                            self.match_cnt += 1
                            if self.match_cnt % 10 == 0:
                                self.level += 1
                            self.com_bo_tick = pygame.time.get_ticks()
                        else:
                            self.play_memody.append('b_')
                            
                        self.msg_inbox = ''
                    else:
                        pass
            
                
            if event.type == pygame.USEREVENT+1:#사용자 이벤트            
                key_event = pygame.key.get_pressed()    
                if key_event[pygame.K_BACKSPACE]:
                    self.msg_inbox = self.msg_inbox[0:-1] 
                    self.play_memody.append('g_')
                    
            if event.type == pygame.USEREVENT+2:#사용자 이벤트  
                self.gen_word.drop()
                
    def check_combo(self):
        
        if self.com_bo_tick != 0:
            self.com_bo_ellip = pygame.time.get_ticks() - self.com_bo_tick
            if self.com_bo_ellip > self.com_bo_tick_limit:
                self.com_bo_tick = 0
                self.com_bo_ellip = 0
                self.com_bo_bonus = 3
                    
    def game_init(self):
        if self.is_game_init:
            self.is_game_init = False
            self.is_game_over = False
            self.client.send_score(self.user_name, self.score)
            self.gen_word.clear_word()
            self.hp = self.hp_max
            self.match_cnt = 0
            self.level = 1
            self.score = 0
            self.com_bo_tick = 0
            self.com_bo_ellip = 0
            self.com_bo_bonus = 3
            
    def display_users_score(self):
        users, high = self.client.get_score()
        if len(users):
            # print(users)
            
            width = self.msg_win_width
            x = self.screen.get_width() - width
            x += 4
            y = 150+300
            
            img = self.mfont30.render(f'최고점수', 1, (255,0,0))
            self.screen.blit(img,(x, y))
            y+= 40
            if len(high)>1:
                img = self.mfont30.render(f' {high[1]:7,d} {high[0]}', 1, (0,255,255))
                self.screen.blit(img,(x, y))
            y+= 60
            
            img = self.mfont30.render(f'나의기록', 1, (255,0,0))
            self.screen.blit(img,(x, y))
            y+= 40
            img = self.mfont30.render(f' {self.score_high:7,d}', 1, (0,255,255))
            self.screen.blit(img,(x, y))
            y+= 60

            
            img = self.mfont30.render(f'접속순위', 1, (255,0,0))
            self.screen.blit(img,(x, y))
            y+= 40
            for i,user in enumerate(users):
                img = self.mfont30.render(f' {user[1]:7,d} {user[0]}', 1, (255,255,255))
                self.screen.blit(img,(x, y))
                y+= 40
    
    def display_box(self):
        
        width = self.msg_win_width
        height = self.screen.get_height()
        x = self.screen.get_width() - width
        y = 0+300
        pygame.draw.rect(self.screen, (255,255,255),(x,y, width,height), 1)
        
        x += 2#self.screen.get_width()/2 -  width/2
        y = 20+300
        
        img = self.mfont30.render(f' 레벨: {self.level}', 1, (0,0,255))
        self.screen.blit(img,(x, y+2))
        
        y += 40
        img = self.mfont30.render(f' HP: {self.hp}/{self.hp_max}', 1, (255,0,0))
        self.screen.blit(img,(x, y+2))
                
        y += 40
        img = self.mfont30.render(f' 점수: {self.score}', 1, (255,255,255))
        self.screen.blit(img,(x, y+2))
        
        y = self.screen.get_height()-60
        img = self.mfont30.render(f' 콤보타임: {self.com_bo_tick_limit - self.com_bo_ellip}: x{self.com_bo_bonus}', 1, (255,255,0))
        self.screen.blit(img,(x, y+2))
        
        if self.is_game_over:
            img = self.mfont30.render(f'Game Over!! [재시작 : 스페이스 누르기]', 1, (255,255,255))
            rect = img.get_rect()
            rect.centerx = (self.screen.get_width()-self.msg_win_width)/2
            rect.centery = self.screen.get_height()/2
            self.screen.blit(img,rect)
        
        # print(self.com_bo_position)
        for i,com in enumerate(self.com_bo_position):
            if pygame.time.get_ticks()- com[2] > 3000:
                del self.com_bo_position[i]
            else:
                img = self.mfont30.render(f'COMBO x {com[3]}', 1, (255,0,0))
                rect = img.get_rect()
                rect.centerx = com[0]
                rect.centery = com[1]
                if rect.right > self.screen.get_width() - rect.width - self.msg_win_width:
                    rect.x = self.screen.get_width() - rect.width - self.msg_win_width
                if rect.x < 0 :
                    rect.x = 0
                    
                self.screen.blit(img,rect)
            
        width = self.screen.get_width()-self.msg_win_width
        height = self.inp_win_heigh
        x = 0
        y = self.screen.get_height()-height
        pygame.draw.rect(self.screen, (255,255,255),(x,y, width,height), 1)
        
        width = self.screen.get_width()-self.msg_win_width-40
        height = 60
        
        x = 20
        y = self.screen.get_height() - height - 10
        # pygame.draw.rect(self.screen, (  0,  0,  0),(x,y, width,height), 0)#검정 사각형 채움
        # pygame.draw.rect(self.screen, (255,255,255),(x,y, width,height), 1)#흰색 사각형 라인        
        img = self.mfont30.render(' 입력: '+self.msg_inbox, 1, (255,255,255))
        self.screen.blit(img,(x, y+10))
                
    def run(self):
        pygame.time.set_timer(pygame.USEREVENT+1, 50)
        pygame.time.set_timer(pygame.USEREVENT+2, 10)
        while self.isActive:
            self.screen.fill((0, 0, 0)) #화면을 흰색으로 채우기
            self.game_init()
            self.display_users_score()
            self.eventProcess()
            self.check_combo()
            self.display_box()
            if self.is_game_over == False:
                if self.gen_word.draw(self.is_game_over):
                    self.hp -= 1
                    if self.hp <= 0:
                        self.hp = 0
                        self.is_game_over = True
                        self.snd_gameover.play()
            self.keyboardDraw.draw(self.gen_word.words)
            pygame.display.update() #화면 갱신
            self.clock.tick(30) #초당 60프레임 갱신을 위한 잠시 대기

if __name__ == "__main__":
    game = game_main()
    game.run()
# pyinstaller -w -F test.py