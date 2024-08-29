import pygame
from pygame import *

class Bullet(pygame.sprite.Sprite):
	
    def __init__(self,screen:Surface,image,cx,y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.direction = direction
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.centerx = cx
        self.rect.y = y
        self.bullet_group = pygame.sprite.Group()
        self.bullet_tick = 0
		 

    def update(self):
        self.rect.y += self.direction
        if self.rect.bottom < 0 or self.rect.bottom > self.screen.get_height():
            self.kill()