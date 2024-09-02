import pygame
from pygame import *
import pygame.sprite
import pygame.time
from itemHp import *
import random

class Items():
	
    def __init__(self,screen:Surface):
        self.screen = screen
        self.hp_group = pygame.sprite.Group()
    
    def reset(self):
        self.hp_group.clear()
        
    def createHP(self,centerx,centery):
        # if random.randint(0,100) < 10:
        hp = ItemHP(self.screen,centerx,centery)
        self.hp_group.add(hp)
        
    def draw(self):            
        self.hp_group.update()
        self.hp_group.draw(self.screen)