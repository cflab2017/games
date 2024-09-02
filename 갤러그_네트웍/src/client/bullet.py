import pygame
from pygame import *
import random

import pygame.time

class Bullet(pygame.sprite.Sprite):
	
    def __init__(self,screen:Surface,image,cx,y, direction,player_centerx=None,level = 0):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.direction = direction
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.centerx = cx
        self.rect.y = y
        self.bullet_group = pygame.sprite.Group()
        self.bullet_tick = 0
        self.bullet_target = player_centerx
        self.bullet_delay = None
        if self.bullet_target is not None:
            self.bullet_delay = pygame.time.get_ticks()
            self.direction += random.randint(0,int(level/10)+1)
            self.bullet_target += random.randint(-2,2)
		 

    def update(self):
        if self.bullet_delay is not None:
            if pygame.time.get_ticks() - self.bullet_delay > 300:            
                self.rect.y += self.direction
        else:
            self.rect.y += self.direction
            
        if self.bullet_target is not None:
            if self.rect.x > self.bullet_target:
                self.rect.x -= 1
            if self.rect.x < self.bullet_target:
                self.rect.x += 1
        if self.rect.bottom < 0 or self.rect.bottom > self.screen.get_height():
            self.kill()