import pygame
from pygame import *
import random

class DrawImg(pygame.sprite.Sprite):
    def __init__(self, screen:Surface, cx:int, cy:int, ex:int, ey:int):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        image = pygame.image.load('./images/acorn.png').convert_alpha()
        self.image_src = pygame.transform.scale(image, (40, 50))
        self.image = self.image_src
        self.rect = self.image.get_rect()
        self.rect.centerx = cx
        self.rect.centery = cy
        self.ex = ex
        self.ey = ey - self.rect.height/2
        self.item_delay = pygame.time.get_ticks()
        self.is_finish = False
        
    def update(self):        
        if pygame.time.get_ticks() - self.item_delay > 300:
            if self.rect.centery < self.ey:
                self.rect.y += 5
                self.image = pygame.transform.rotate(self.image_src, random.randint(0,360))
                if self.rect.centerx < self.ex:
                    self.rect.x += random.randint(1,2)
                if self.rect.centerx > self.ex:
                    self.rect.x -= random.randint(1,2)
            else:
                self.is_finish = True
            