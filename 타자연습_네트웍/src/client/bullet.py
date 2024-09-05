import pygame
from pygame import *
import random

import pygame.time

class Bullet(pygame.sprite.Sprite):
	
    def __init__(self,screen:Surface,cx,cy,target_centery):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.direction = -10
        self.img_src = pygame.image.load('./images/bullet.png')
        self.image = pygame.transform.scale(self.img_src, (30, 60))
        self.image.set_alpha(150)
        # self.image = image
        self.speed = 1
        self.rect = self.image.get_rect()
        self.rect.centerx = cx
        self.rect.centery = cy
        # self.bullet_group = pygame.sprite.Group()
        # self.bullet_tick = 0
        self.target_centery = target_centery
        # self.bullet_delay = None
        # if self.bullet_target is not None:
        #     self.bullet_delay = pygame.time.get_ticks()
        #     self.direction += random.randint(0,int(level/10)+1)
        #     self.bullet_target += random.randint(-2,2)
		 

    def update(self):
        # if self.bullet_delay is not None:
        #     if pygame.time.get_ticks() - self.bullet_delay > 300:            
        #         self.rect.y += self.direction
        # else:
        #     self.rect.y += self.direction
            
        # if self.bullet_target is not None:
        self.rect.y += self.direction
        # if self.rect.x > self.bullet_target:
        #     self.rect.x -= self.speed
        # if self.rect.x < self.bullet_target:
        #     self.rect.x += self.speed
        if self.rect.bottom < self.target_centery or self.rect.bottom > self.screen.get_height():
            self.kill()