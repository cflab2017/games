

import pygame
from pygame.locals import *
import pyautogui

class Users(pygame.sprite.Sprite):
    
    def __init__(self, screen,img_player,img_arrow,identity,client):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen        
        self.identity = identity
        self.client = client
        self.infor = self.client.infor[identity]
        
        self.name = self.infor['name']
        self.character = self.infor['char']
        self.img_src = img_player[self.character]
        self.image = self.img_src
        self.rect = self.image.get_rect()
        self.rect.x = self.infor['x']
        self.rect.y = self.infor['y']
        
        self.img_arrow = img_arrow
        self.rect_arrow = self.img_arrow.get_rect()
        
        self.score = self.infor['score']
        self.hp = self.infor['hp']
        self.cycle_color = None
        self.cycle_color_tick = 0
        
        self.mfont = pygame.font.SysFont("malgungothic", 18)
        
    def setText(self):
        mtext = self.mfont.render(f'{self.score}점', True, 'black')
        tRec = mtext.get_rect()
        tRec.x = self.rect.centerx - tRec.width/2
        tRec.y = self.rect.y - 25
        self.screen.blit(mtext, tRec)
        
        mtext = self.mfont.render(f'♥{self.hp}♥', True, 'red')
        tRec = mtext.get_rect()
        tRec.x = self.rect.centerx - tRec.width/2
        tRec.y = self.rect.y - 45
        self.screen.blit(mtext, tRec)
        
        mtext = self.mfont.render(f'{self.name}', True, 'blue')
        tRec = mtext.get_rect()
        tRec.x = self.rect.centerx - tRec.width/2
        tRec.y = self.rect.y - 65
        self.screen.blit(mtext, tRec)
        
    def check_collide(self,arrow_group):
        if pygame.sprite.spritecollide(self, arrow_group, True):
            self.cycle_color = (255,0,0)
            return True
        return False
                    
    def update(self):
        if self.identity in self.client.infor:
            self.score = self.infor['score']
            self.rect.x = self.infor['x']
            self.rect.y = self.infor['y']
            self.hp = self.infor['hp']
            arrows = self.infor['arrow']
            for arrow in arrows:
                self.rect_arrow.x = arrow[0]
                self.rect_arrow.y = arrow[1]
                    
                if arrow[2] == 1:
                    img = pygame.transform.flip(self.img_arrow, True, False)
                else:
                    img = self.img_arrow
                self.screen.blit(img, self.rect_arrow)   
            direction = self.infor['dir']
            if direction > 0:
                self.image = self.img_src
            else:
                self.image = pygame.transform.flip(self.img_src, True, False)
                
        self.setText()
        
        if self.cycle_color is not None:
            pygame.draw.circle(self.screen, self.cycle_color,[self.rect.centerx,self.rect.centery],self.rect.width/2+5, 2)
            if self.cycle_color_tick == 0:
                self.cycle_color_tick = pygame.time.get_ticks()
                
            if pygame.time.get_ticks() - self.cycle_color_tick > 500:
                self.cycle_color = None
                self.cycle_color_tick = 0
                
        self.screen.blit(self.image, self.rect)
        # return self.is_press
        # return self.is_press