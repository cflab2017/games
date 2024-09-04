import pygame
from pygame import *
import random

import pygame.time

class Draw_button():
	
    def __init__(self,screen:Surface):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.defFont18 = pygame.font.SysFont('malgungothic', 18)
        ####################################################################
        image = pygame.image.load('./images/btn_space.png').convert_alpha()
        self.btn_space = pygame.transform.scale(image, (40*3, 40))
        self.btn_space_rect = self.btn_space.get_rect()
        self.btn_space.set_alpha(100)
        self.btn_space_rect.right = self.screen.get_width() - 20 - (40+10)*0
        self.btn_space_rect.bottom = self.screen.get_height() - 10                

        image = pygame.image.load('./images/btn_left.png').convert_alpha()
        self.btn_left = pygame.transform.scale(image, (40, 40))
        self.btn_left_rect = self.btn_left.get_rect()
        self.btn_left.set_alpha(100)
        self.btn_left_rect.right = self.screen.get_width() - 10 - (40+10)*2
        self.btn_left_rect.bottom = self.screen.get_height() - 10 - (40+10)*1
        
        image = pygame.image.load('./images/btn_up.png').convert_alpha()
        self.btn_up = pygame.transform.scale(image, (40, 40))
        self.btn_up_rect = self.btn_up.get_rect()
        self.btn_up.set_alpha(100)
        self.btn_up_rect.right = self.screen.get_width() - 10 - (40+10)*1
        self.btn_up_rect.bottom = self.screen.get_height() - 10 - (40+10)*2
        
        image = pygame.image.load('./images/btn_down.png').convert_alpha()
        self.btn_down = pygame.transform.scale(image, (40, 40))
        self.btn_down_rect = self.btn_down.get_rect()
        self.btn_down.set_alpha(100)        
        self.btn_down_rect.right = self.screen.get_width() - 10 - (40+10)*1
        self.btn_down_rect.bottom = self.screen.get_height() - 10 - (40+10)*1
        
        image = pygame.image.load('./images/btn_right.png').convert_alpha()
        self.btn_right = pygame.transform.scale(image, (40, 40))
        self.btn_right.set_alpha(100)
        self.btn_right_rect = self.btn_right.get_rect()        
        self.btn_right_rect.right = self.screen.get_width() - 10 - (40+10)*0
        self.btn_right_rect.bottom = self.screen.get_height() - 10 - (40+10)*1
        #################################################################
        
        image = pygame.image.load('./images/btn2_space.png').convert_alpha()
        self.btn2_space = pygame.transform.scale(image, (40*3, 40))
        self.btn2_space_rect = self.btn2_space.get_rect()
        self.btn2_space.set_alpha(100)
        self.btn2_space_rect.right = self.screen.get_width() - 20 - (40+10)*(0+4)
        self.btn2_space_rect.bottom = self.screen.get_height() - 10                

        image = pygame.image.load('./images/btn2_left.png').convert_alpha()
        self.btn2_left = pygame.transform.scale(image, (40, 40))
        self.btn2_left_rect = self.btn2_left.get_rect()
        self.btn2_left.set_alpha(100)
        self.btn2_left_rect.right = self.screen.get_width() - 10 - (40+10)*(2+4)
        self.btn2_left_rect.bottom = self.screen.get_height() - 10 - (40+10)*1
        
        image = pygame.image.load('./images/btn2_up.png').convert_alpha()
        self.btn2_up = pygame.transform.scale(image, (40, 40))
        self.btn2_up_rect = self.btn2_up.get_rect()
        self.btn2_up.set_alpha(100)
        self.btn2_up_rect.right = self.screen.get_width() - 10 - (40+10)*(1+4)
        self.btn2_up_rect.bottom = self.screen.get_height() - 10 - (40+10)*2
        
        image = pygame.image.load('./images/btn2_down.png').convert_alpha()
        self.btn2_down = pygame.transform.scale(image, (40, 40))
        self.btn2_down_rect = self.btn_down.get_rect()
        self.btn2_down.set_alpha(100)        
        self.btn2_down_rect.right = self.screen.get_width() - 10 - (40+10)*(1+4)
        self.btn2_down_rect.bottom = self.screen.get_height() - 10 - (40+10)*1
        
        image = pygame.image.load('./images/btn2_right.png').convert_alpha()
        self.btn2_right = pygame.transform.scale(image, (40, 40))
        self.btn2_right.set_alpha(100)
        self.btn2_right_rect = self.btn2_right.get_rect()        
        self.btn2_right_rect.right = self.screen.get_width() - 10 - (40+10)*(0+4)
        self.btn2_right_rect.bottom = self.screen.get_height() - 10 - (40+10)*1

        #################################################################
        image = pygame.image.load('./images/btn_shield.png').convert_alpha()
        self.btn_shield = pygame.transform.scale(image, (40, 40))
        self.btn_shield.set_alpha(100)
        self.btn_shield_rect = self.btn_shield.get_rect()        
        self.btn_shield_rect.right = self.screen.get_width() - 10 - (40+10)*(0+4+5)
        self.btn_shield_rect.bottom = self.screen.get_height() - 10 - ((40+10)*3-20)
        #################################################################
        image = pygame.image.load('./images/btn_boom.png').convert_alpha()
        self.btn_boom = pygame.transform.scale(image, (40, 40))
        self.btn_boom.set_alpha(100)
        self.btn_boom_rect = self.btn_boom.get_rect()        
        self.btn_boom_rect.right = self.screen.get_width() - 10 - (40+10)*(0+4+5)
        self.btn_boom_rect.top = self.btn_shield_rect.bottom+5
        #################################################################
        image = pygame.image.load('./images/btn_pause.png').convert_alpha()
        self.btn_pause = pygame.transform.scale(image, (40, 40))
        self.btn_pause.set_alpha(100)
        self.btn_pause_rect = self.btn_pause.get_rect()        
        self.btn_pause_rect.right = self.screen.get_width() - 10 - (40+10)*(0+4+5)
        self.btn_pause_rect.top = self.btn_boom_rect.bottom+5
        #################################################################
        image = pygame.image.load('./images/btn_stone.png').convert_alpha()
        self.btn_stone = pygame.transform.scale(image, (40, 40))
        self.btn_stone.set_alpha(100)
        self.btn_stone_rect = self.btn_stone.get_rect()        
        self.btn_stone_rect.right = self.screen.get_width() - 10 - (40+10)*(0+4+5)
        self.btn_stone_rect.top = self.btn_pause_rect.bottom+5
        
    def disp_msg_1(self,msg, topleft,color=(255, 255, 255)):
        img = self.defFont18.render(msg,False,color,(0, 0, 0))
        rect = img.get_rect()
        rect.centerx, rect.top = topleft
        pos = self.screen.blit(img,rect)        
        return pos
    
    def disp_msg_2(self,msg, topleft,color=(255, 255, 255)):
        img = self.defFont18.render(msg,False,color,(0, 0, 0))
        rect = img.get_rect()
        rect.x, rect.centery = topleft
        pos = self.screen.blit(img,rect)        
        return pos
    
    def draw(self):
        self.disp_msg_1('[스톤제어]',(self.btn_up_rect.centerx,self.btn_up_rect.top-30),(192,192,192))
        self.screen.blit(self.btn_space,self.btn_space_rect)
        self.screen.blit(self.btn_up,self.btn_up_rect)
        self.screen.blit(self.btn_down,self.btn_down_rect)
        self.screen.blit(self.btn_left,self.btn_left_rect)
        self.screen.blit(self.btn_right,self.btn_right_rect)
        
        
        self.disp_msg_1('[공격 스톤제어]',(self.btn2_up_rect.centerx,self.btn2_up_rect.top-30),(192,192,192))
        self.screen.blit(self.btn2_space,self.btn2_space_rect)
        self.screen.blit(self.btn2_up,self.btn2_up_rect)
        self.screen.blit(self.btn2_down,self.btn2_down_rect)
        self.screen.blit(self.btn2_left,self.btn2_left_rect)
        self.screen.blit(self.btn2_right,self.btn2_right_rect)
        
        
        self.disp_msg_2('-일시정지',(self.btn_pause_rect.right+2,self.btn_pause_rect.centery),(192,192,192))
        self.screen.blit(self.btn_pause,self.btn_pause_rect)
        
        self.disp_msg_2('-공격 방어',(self.btn_shield_rect.right+2,self.btn_shield_rect.centery),(192,192,192))
        self.screen.blit(self.btn_shield,self.btn_shield_rect)
        
        self.disp_msg_2('-폭탄 변경',(self.btn_boom_rect.right+2,self.btn_boom_rect.centery),(192,192,192))
        self.screen.blit(self.btn_boom,self.btn_boom_rect)
        
        self.disp_msg_2('-스톤 변경',(self.btn_stone_rect.right+2,self.btn_stone_rect.centery),(192,192,192))
        self.screen.blit(self.btn_stone,self.btn_stone_rect)