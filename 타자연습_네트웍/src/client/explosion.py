import pygame
from pygame import *
import pygame.time

class Explosion(pygame.sprite.Sprite):
	
    def __init__(self,screen:Surface,cx,cy):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.img_size = 10
        self.img_src = pygame.image.load('./images/explosion.png')
        self.image = pygame.transform.scale(self.img_src, (self.img_size, self.img_size))
        self.image.set_alpha(150)
        self.rect = self.image.get_rect()
        self.cx = cx
        self.cy = cy
        self.rect.centerx = self.cx
        self.rect.centery = self.cy
        self.explosion_tick = pygame.time.get_ticks()
		 
    def update(self):
        ellip = pygame.time.get_ticks() - self.explosion_tick
        if ellip > 10:
            self.explosion_tick = pygame.time.get_ticks()
            self.img_size += 10
            if self.img_size > 100:
                self.kill()
            else:
                self.image = pygame.transform.scale(self.img_src, (self.img_size, self.img_size))
                self.image.set_alpha(150)
                self.rect = self.image.get_rect()
                self.rect.centerx = self.cx
                self.rect.centery = self.cy
            