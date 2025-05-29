

import pygame
from pygame.locals import *

class Arrow(pygame.sprite.Sprite):
    
    def __init__(self, screen,identity,img,x,y,direction):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.direction = direction
        if self.direction > 0:
            img = pygame.transform.flip(img, True, False)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.identity = identity
                
    def update(self):
        if self.rect.x < 0 or self.rect.x > self.screen.get_width():
            self.kill()
            return
            
        self.rect.x += (self.direction*3)
        self.screen.blit(self.image, self.rect)