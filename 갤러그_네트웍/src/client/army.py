import pygame
from pygame import *
import pygame.sprite
import pygame.time
from bullet import *
from ememy import *

class Army():
	
    def __init__(self,screen:Surface):
        self.screen = screen
        self.army_group = pygame.sprite.Group()
        
        
    def create_ememy(self,level):
        self.army_group.empty()
        nums = []
        max_line = level
        max_line += 2
        
        if max_line > 45:
            max_line = 45
            
        while max_line >= 9 :
            nums.append(9) 
            max_line -= 9

        if max_line > 0:
            nums.append(max_line)
            
        cy = 40+20
        for i in nums:
            limit_x = self.screen.get_width()/2 - (i)*90/2 - 90/2 +90
            for k in range(i):
                offsetx = i*90/2 - k*90 - 90/2
                cx = self.screen.get_width()/2-offsetx                
                em = Ememy(self.screen,cx,cy,limit_x,level)
                self.army_group.add(em)
            cy += 90
            # limit_x = self.screen.get_width()/2 - ((i*2)+1)*90/2 - 90/2 +90
            # for k in range((i*2)+1):
            #     offsetx = ((i*2)+1)*90/2 - k*90 - 90/2
            #     cx = self.screen.get_width()/2-offsetx
            #     cy = i*90+40+20
            #     em = Ememy(self.screen,cx,cy,limit_x)
            #     self.army_group.add(em)
                
        # for i in range(max_line):
        #     limit_x = self.screen.get_width()/2 - ((i*2)+1)*90/2 - 90/2 +90
        #     for k in range((i*2)+1):
        #         offsetx = ((i*2)+1)*90/2 - k*90 - 90/2
        #         cx = self.screen.get_width()/2-offsetx
        #         cy = i*90+40+20
        #         em = Ememy(self.screen,cx,cy,limit_x)
        #         self.army_group.add(em)
        
    def draw(self,player_centerx, level):
        limit = {}
        for em in self.army_group:
            if em.rect.centery not in limit:
                limit[em.rect.centery] = {
                    'left':[],
                    'right':[],
                    }
            limit[em.rect.centery]['left'].append(em.rect.left)
            limit[em.rect.centery]['right'].append(em.rect.right)
        for key in limit:
            limit[key]['left'] = min(limit[key]['left'])
            limit[key]['right'] = self.screen.get_width() - max(limit[key]['right'])
            
        # print(limit)
        for em in self.army_group:
            left_limit = limit[em.rect.centery]['left']
            right_limit = limit[em.rect.centery]['right']
            em.set_limit(left_limit,right_limit)
            
            
        self.army_group.update(player_centerx, level)
        self.army_group.draw(self.screen)