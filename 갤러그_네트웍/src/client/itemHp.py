import pygame
from pygame import *
import random

import pygame.time

class ItemHP(pygame.sprite.Sprite):
	
    def __init__(self,screen:Surface,cx,cy):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        image = pygame.image.load('./images/shield.png').convert_alpha()
        image = pygame.transform.scale(image, (40, 50))
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.centerx = cx
        self.rect.centery = cy
        self.item_delay = pygame.time.get_ticks()
        		 

    def update(self):
        if pygame.time.get_ticks() - self.item_delay > 300:   
            self.rect.y += 1          
        if self.rect.bottom < 0 or self.rect.bottom > self.screen.get_height():
            self.kill()