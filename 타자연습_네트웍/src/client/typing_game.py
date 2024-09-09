import pygame
import pygame.image
import pygame.key

from pygame import *
import pygame.font
from pygame.locals import *
# import pygame.time
import winsound
from _thread import *
import time as ott

import pygame.sprite
import pygame.sprite
import pygame.transform
from client import *
from account import *

from keyboardDraw import *
from explosion import *
from gen_word import *
from bullet import *
from msg_draw import *
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
    com_bo_tick = 0
    com_bo_tick_limit = 5000
    com_bo_ellip = 0
    com_bo_bonus = 3
    com_bo_position = []
    play_memody = []
    inp_win_heigh = 80
    game_start_msg = []
    game_start_msg_idex = 0
    game_play_time = 5000
    
    game_line_start = 0
    game_line_end = 630+75
    game_line_dead = game_line_end - 90
    
    
    def __init__(self) -> None:
        pygame.init() #pygame 초기화
        pygame.display.set_caption("codingnow.co.kr") #타이틀
        self.clock = pygame.time.Clock() #프레임을 처리 하기위해
        
        img = pygame.image.load('./images/background.png')
        self.img_bg = pygame.transform.scale(img,((self.WIDTH, self.game_line_end)))        
        
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

        self.client = socketClient()
        account = Account(self.screen)
        self.user_name,self.isActive = account.run(self.client)        
        
        self.msg_draw = Msg_draw(self.screen,self.game_line_start,self.game_line_end)
        self.keyboardDraw = KeyboardDraw(self.screen,self.game_line_end)
        self.snd_drop = pygame.mixer.Sound(f'./sound/shoot.wav')
        self.snd_hit = pygame.mixer.Sound(f'./sound/hit.wav')
        self.snd_item = pygame.mixer.Sound(f'./sound/item.wav')
        self.snd_gameover = pygame.mixer.Sound(f'./sound/game_over.wav')
        self.gen_word = Gen_Workd(self,self.client.words,self.game_line_start,self.game_line_end,self.game_line_dead)
        self.ExplosionGroup = pygame.sprite.Group()
        self.bulletGroup = pygame.sprite.Group()
        start_new_thread(self.thread_play, (self.play_memody, ))

    def thread_play(self,play_memody):
        
        while True:
            ott.sleep(0.1)
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
                    if self.is_game_over and len(self.game_start_msg)==0:
                        self.game_init()
                        self.game_start_msg = [5,4,3,2,1, 'go']
                elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    if self.is_game_over == False:
                        centerx, centery = self.gen_word.match_word(self.msg_inbox)
                        if centerx is not None:
                            if self.com_bo_ellip > 0:
                                self.score += (len(self.msg_inbox)+3)*self.com_bo_bonus*self.level
                                self.com_bo_position.append([centerx, centery,self.com_bo_tick,self.com_bo_bonus])
                                self.com_bo_bonus += 1
                                if(self.com_bo_bonus > 10):
                                    self.com_bo_bonus = 10
                            else:
                                self.score += (len(self.msg_inbox)+3)*self.level
                            self.ExplosionGroup.add(Explosion(self.screen,centerx, centery,self.snd_hit))
                            self.bulletGroup.add(Bullet(self.screen,100,self.game_line_dead,centerx,centery))
                            self.msg_inbox = ''
                            
                            if self.score > self.score_high:
                                self.score_high = self.score        
                                
                            self.client.send_score(self.user_name, self.score)
                            self.match_cnt += 1
                            if self.match_cnt % (self.level*2) == 0:
                                self.level += 1
                                self.msg_draw.status_msg.append(f'레벨업 {self.level}!!')
                                
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
        self.gen_word.clear_word()
        self.hp = self.hp_max
        self.match_cnt = 0
        self.level = 1
        self.score = 0
        self.com_bo_tick = 0
        self.com_bo_ellip = 0
        self.com_bo_bonus = 3        
        self.client.send_score(self.user_name, self.score)            
        
    def run(self):
        pygame.time.set_timer(pygame.USEREVENT+1, 50)
        pygame.time.set_timer(pygame.USEREVENT+2, 10)
        self.game_init()
        self.is_game_over = True
        while self.isActive:
            self.screen.fill((0, 0, 0)) #화면을 흰색으로 채우기
            self.screen.blit(self.img_bg,(0,0))
            self.eventProcess()
            self.check_combo()
            self.msg_draw.draw(self)
            self.ExplosionGroup.update()
            self.ExplosionGroup.draw(self.screen)
                
            self.bulletGroup.update()
            self.bulletGroup.draw(self.screen)
            if self.is_game_over == False:
                drops = self.gen_word.draw(self.is_game_over)
                if len(drops):
                    self.hp -= len(drops)
                    self.snd_drop.play()
                    for drop in drops:
                        self.ExplosionGroup.add(Explosion(self.screen,drop.centerx, drop.centery,self.snd_hit))
                    if self.hp <= 0:
                        self.hp = 0
                        self.is_game_over = True
                        self.snd_gameover.play()
                else:
                    if self.game_play_time <= pygame.time.get_ticks():
                        self.is_game_over = True
                        self.snd_gameover.play()
                        
            self.keyboardDraw.draw(self.gen_word.words)
            pygame.display.update() #화면 갱신
            self.clock.tick(200) #초당 60프레임 갱신을 위한 잠시 대기

if __name__ == "__main__":
    game = game_main()
    game.run()
# pyinstaller -w -F test.py