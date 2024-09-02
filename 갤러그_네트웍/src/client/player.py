import pygame
from pygame import *
import pygame.image
import pygame.time
import pygame.transform
from bullet import *

from btnDraw import *
import pickle
import os.path

class Player():
	
    def __init__(self,screen:Surface,snd_dic,user_name,btnDraw:BtnDraw):
        self.screen = screen
        self.snd_dic = snd_dic
        self.btnDraw = btnDraw
        img = pygame.image.load('./images/player.png').convert_alpha()
        self.image = pygame.transform.scale(img, (80, 80))
        self.rect = self.image.get_rect()
        self.rect.centerx = self.screen.get_width()/2
        self.rect.bottom = self.screen.get_height()-80
        self.bullet_group = pygame.sprite.Group()
        self.bullet_tick = 0
        img = pygame.image.load('./images/bullet.png').convert_alpha()
        self.image_bullet = pygame.transform.scale(img, (30, 40))
        
        img = pygame.image.load('./images/engine.png').convert_alpha()
        self.image_engine = pygame.transform.scale(img, (40, 40))
        self.rect_engine = self.image_engine.get_rect()
        
        self.font60 = pygame.font.SysFont('malgungothic', 60)
        self.font30 = pygame.font.SysFont('malgungothic', 30)
        self.font20 = pygame.font.SysFont('malgungothic', 20)
        self.user_name = user_name
        self.load_dict = {}
        self.score_high = self.update_user_dic('r')
        
        self.level = 1
        self.hp = 100
        self.score = 0
        self.shield_on = False
        self.shield_tick = 0
        
        self.level_up = False
        self.level_up_tick = 0
        
    def set_army(self,army):
        self.army = army
    
    def update_user_dic(self,state,high_score=None):
        user_file_name = 'user.pickle'
        
        if state == 'r':
            #저장된 파일 불러오기
            if os.path.isfile(user_file_name): #불러올 파일이 있는가?
                with open(user_file_name, 'rb') as fr:
                    self.load_dict = pickle.load(fr) #딕셔너리로 변환                  
            if self.user_name not in self.load_dict:
                self.load_dict[self.user_name] = {'score':0}
                
            return self.load_dict[self.user_name]['score']
            
        if state == 'w':
            if high_score > self.load_dict[self.user_name]['score']:
                self.score_high = high_score
                self.load_dict[self.user_name]['score'] = high_score
                with open(user_file_name, 'wb') as fw:
                    pickle.dump(self.load_dict,fw)
                    
    def restart(self):
        self.level = 1
        self.hp = 100
        self.score = 0
        self.rect.centerx = self.screen.get_width()/2
        self.rect.bottom = self.screen.get_height()-80
		 
    def event_key_pressed(self):
        key_pressed = pygame.key.get_pressed()
        
        if key_pressed[pygame.K_SPACE]:
            if pygame.time.get_ticks() - self.bullet_tick > 200:
                bullet = Bullet(self.screen,self.image_bullet,self.rect.centerx, self.rect.top,-2)
                self.bullet_group.add(bullet)
                self.bullet_tick = pygame.time.get_ticks()
                self.snd_dic['shoot'].play()
            self.btnDraw.btn_space.set_alpha(200)
        else:
            self.btnDraw.btn_space.set_alpha(100)
            
        if key_pressed[pygame.K_LEFT]:
            self.rect.x -= 2
            self.rect_engine.left = self.rect.right-40
            self.rect_engine.centery = self.rect.centery
            img = pygame.transform.rotate(self.image_engine,90)
            self.screen.blit(img, self.rect_engine)
            self.btnDraw.btn_left.set_alpha(200)
        else:
            self.btnDraw.btn_left.set_alpha(100)
            
        if key_pressed[pygame.K_RIGHT]:
            self.rect.x += 2
            self.rect_engine.right = self.rect.left+40
            self.rect_engine.centery = self.rect.centery
            img = pygame.transform.rotate(self.image_engine,-90)
            self.screen.blit(img, self.rect_engine)
            self.btnDraw.btn_right.set_alpha(200)
        else:
            self.btnDraw.btn_right.set_alpha(100)
            
        if key_pressed[pygame.K_UP]:
            self.rect.y -= 2
            self.rect_engine.centerx = self.rect.centerx
            self.rect_engine.top = self.rect.bottom
            self.screen.blit(self.image_engine, self.rect_engine)
            self.btnDraw.btn_up.set_alpha(200)
        else:
            self.btnDraw.btn_up.set_alpha(100)
                        
        if key_pressed[pygame.K_DOWN]:
            self.rect.y += 2
            self.rect_engine.centerx = self.rect.centerx
            self.rect_engine.bottom = self.rect.top+30
            img = pygame.transform.flip(self.image_engine,False,True)
            self.screen.blit(img, self.rect_engine)
            self.btnDraw.btn_down.set_alpha(200)
        else:
            self.btnDraw.btn_down.set_alpha(100)
            
            
        if self.rect.left < 0:
            self.rect.left = 0
            
        if self.rect.top < self.screen.get_height()/2:
            self.rect.top = self.screen.get_height()/2
            
        if self.rect.right > self.screen.get_width():
            self.rect.right = self.screen.get_width()
            
        if self.rect.bottom > self.screen.get_height():
            self.rect.bottom = self.screen.get_height()
            
    def draw_shield(self):
        
        if self.shield_on:
            self.shield_tick = pygame.time.get_ticks()
            self.shield_on = False
            
        if self.shield_tick > 0:
            ellip = pygame.time.get_ticks() - self.shield_tick
            if ellip < 500:
                temp_surface = pygame.Surface(self.image.get_size())
                temp_surface.fill((0, 255, 255))
                temp_surface.blit(self.image, (0, 0))
                temp_surface.set_alpha(100)
                self.screen.blit(temp_surface, self.rect)
            else:
                self.shield_tick = 0
                
    def draw_text_levelup(self):
        
        if self.level_up:
            self.level_up_tick = pygame.time.get_ticks()
            self.level_up = False
            
        if self.level_up_tick > 0:
            ellip = pygame.time.get_ticks() - self.level_up_tick
            if ellip < 2000:
                
                if ellip < 400 or (800 < ellip < 1200)or (1600 < ellip):
                    msg = f'Level {self.level}'
                    color = (255, 0, 255)
                    img = self.font60.render(msg, True, color)        
                    rect = img.get_rect()        
                    rect.centerx = self.screen.get_width()/2
                    rect.centery = self.screen.get_height()/2
                    temp_surface = pygame.Surface(img.get_size())
                    temp_surface.fill((0, 0, 0))
                    temp_surface.blit(img, (0, 0))
                    temp_surface.set_alpha(128)

                    self.screen.blit(temp_surface, rect)
            else:
                self.level_up_tick = 0
                self.army.create_ememy(self.level)
        
    def draw_text_gameover(self):        
        msg = f'Game over!! (Enter)'
        color = (255, 0, 0)
        img = self.font60.render(msg, True, color)        
        rect = img.get_rect()        
        rect.centerx = self.screen.get_width()/2
        rect.centery = self.screen.get_height()/2
        temp_surface = pygame.Surface(img.get_size())
        temp_surface.fill((0, 0, 0))
        temp_surface.blit(img, (0, 0))
        temp_surface.set_alpha(128)

        self.screen.blit(temp_surface, rect)
        
    def draw_text_score(self):        
        msg = f'SCORE : {self.score}'
        color = (0, 255, 0)
        img = self.font30.render(msg, True, color)        
        rect = img.get_rect()        
        rect.x = 10
        rect.y = 10
        temp_surface = pygame.Surface(img.get_size())
        temp_surface.fill((0, 0, 0))
        temp_surface.blit(img, (0, 0))
        temp_surface.set_alpha(128)
        self.screen.blit(temp_surface, rect)
        
    def draw_text_highscore(self):        
        msg = f'HIGH-SCORE : {self.score_high}'
        color = (0, 255, 0)
        img = self.font30.render(msg, True, color)        
        rect = img.get_rect()        
        rect.x = 10
        rect.y = 10+50
        temp_surface = pygame.Surface(img.get_size())
        temp_surface.fill((0, 0, 0))
        temp_surface.blit(img, (0, 0))
        temp_surface.set_alpha(128)
        self.screen.blit(temp_surface, rect)
        
    def draw_text_hp(self):        
        msg = f'HP : {self.hp}'
        color = (0, 255, 255)
        img = self.font20.render(msg, True, color)        
        rect = img.get_rect()        
        rect.centerx = self.rect.centerx
        rect.y = self.rect.bottom+5
        temp_surface = pygame.Surface(img.get_size())
        temp_surface.fill((0, 0, 0))
        temp_surface.blit(img, (0, 0))
        temp_surface.set_alpha(128)

        self.screen.blit(temp_surface, rect)
        
    def draw(self):
        if self.hp <= 0:
            self.draw_text_gameover()
        else:
            self.event_key_pressed()
        self.bullet_group.update()
        self.bullet_group.draw(self.screen)
        self.draw_text_score()
        self.draw_text_highscore()
        self.draw_text_hp()
        self.draw_shield()
        self.draw_text_levelup()
        self.screen.blit(self.image, self.rect)