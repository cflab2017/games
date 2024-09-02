import pygame
from pygame import *
import random

import pygame.time

class BtnDraw():
	
    def __init__(self,screen:Surface):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        
        image = pygame.image.load('./images/btn_space.png').convert_alpha()
        self.btn_space = pygame.transform.scale(image, (100, 40))
        self.btn_space_rect = self.btn_space.get_rect()
        self.btn_space.set_alpha(100)
        self.btn_space_rect.right = self.screen.get_width() - 10 - (40+10)*3
        self.btn_space_rect.bottom = self.screen.get_height() - 10
        
        

        image = pygame.image.load('./images/btn_left.png').convert_alpha()
        self.btn_left = pygame.transform.scale(image, (40, 40))
        self.btn_left_rect = self.btn_left.get_rect()
        self.btn_left.set_alpha(100)
        self.btn_left_rect.right = self.screen.get_width() - 10 - (40+10)*2
        self.btn_left_rect.bottom = self.screen.get_height() - 10
        
        image = pygame.image.load('./images/btn_up.png').convert_alpha()
        self.btn_up = pygame.transform.scale(image, (40, 40))
        self.btn_up_rect = self.btn_up.get_rect()
        self.btn_up.set_alpha(100)
        self.btn_up_rect.right = self.screen.get_width() - 10 - (40+10)*1
        self.btn_up_rect.bottom = self.screen.get_height() - 10 - (40+10)*1
        
        image = pygame.image.load('./images/btn_down.png').convert_alpha()
        self.btn_down = pygame.transform.scale(image, (40, 40))
        self.btn_down_rect = self.btn_down.get_rect()
        self.btn_down.set_alpha(100)        
        self.btn_down_rect.right = self.screen.get_width() - 10 - (40+10)*1
        self.btn_down_rect.bottom = self.screen.get_height() - 10
        
        image = pygame.image.load('./images/btn_right.png').convert_alpha()
        self.btn_right = pygame.transform.scale(image, (40, 40))
        self.btn_right.set_alpha(100)
        self.btn_right_rect = self.btn_right.get_rect()        
        self.btn_right_rect.right = self.screen.get_width() - 10 - (40+10)*0
        self.btn_right_rect.bottom = self.screen.get_height() - 10
        

    def draw(self):
                    
        self.screen.blit(self.btn_space,self.btn_space_rect)
        self.screen.blit(self.btn_up,self.btn_up_rect)
        self.screen.blit(self.btn_down,self.btn_down_rect)
        self.screen.blit(self.btn_left,self.btn_left_rect)
        self.screen.blit(self.btn_right,self.btn_right_rect)