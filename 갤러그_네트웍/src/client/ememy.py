import pygame
from pygame import *
import pygame.time
import random
from bullet import *

class Ememy(pygame.sprite.Sprite):
	
    def __init__(self,screen:Surface,cx,cy,limit_x,level):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.limit_x = limit_x
        img = pygame.image.load('./images/enemy.png')
        img = pygame.transform.scale(img, (70, 70))
        self.image = pygame.transform.flip(img, False, True)
        self.rect = self.image.get_rect()
        self.rect.centerx = cx
        self.rect.centery = cy
        self.direction = 2
        self.move = 0
        self.bullet_group = pygame.sprite.Group()
        self.bullet_tick = 0
        self.bullet_time = random.randint(1000,2000)
        self.hp = level
        self.shield_on = False
        self.shield_tick = 0
        
        self.font15 = pygame.font.SysFont('malgungothic', 15)
        img = pygame.image.load('./images/bullet2.png')
        self.image_bullet = pygame.transform.scale(img, (20, 20))
        
    def draw_shield(self):
        
        if self.shield_on:
            self.shield_tick = pygame.time.get_ticks()
            self.shield_on = False
            
        if self.shield_tick > 0:
            ellip = pygame.time.get_ticks() - self.shield_tick
            if ellip < 500:
                temp_surface = pygame.Surface(self.image.get_size())
                temp_surface.fill((255, 0, 0))
                temp_surface.blit(self.image, (0, 0))
                temp_surface.set_alpha(100)
                self.screen.blit(temp_surface, self.rect)
            else:
                self.shield_tick = 0
                
    def draw_text_score(self):        
        msg = f'HP : {self.hp}'
        color = (0, 0, 0)
        img = self.font15.render(msg, True, color)        
        rect = img.get_rect()        
        rect.centerx = self.rect.centerx
        rect.y = self.rect.y-15
        color_offset = (100-self.hp*10)
        temp_surface = pygame.Surface(img.get_size())
        temp_surface.fill((192, 192-color_offset, 192-color_offset))
        temp_surface.blit(img, (0, 0))
        temp_surface.set_alpha(128+color_offset)

        self.screen.blit(temp_surface, rect)
             
    def update(self):
        self.draw_shield()
        self.draw_text_score()
        if pygame.time.get_ticks() - self.bullet_tick > self.bullet_time:
            if len(self.bullet_group) == 0 and random.randint(0,100) > 50:
                bullet = Bullet(self.screen,self.image_bullet,self.rect.centerx, self.rect.top,2)
                self.bullet_group.add(bullet)
            self.bullet_tick = pygame.time.get_ticks()
            self.bullet_time = random.randint(1000,2000)
        
        self.bullet_group.update()
        self.bullet_group.draw(self.screen)
        
        if abs(self.move + self.direction) > self.limit_x:
            if self.direction > 0:
                self.direction = -2
            else:
                self.direction = 2
        self.rect.x += self.direction
        self.move += self.direction
        # self.screen.blit(self.image, self.rect)