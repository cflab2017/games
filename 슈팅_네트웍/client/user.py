

import pygame
from pygame.locals import *
import pygame.time
from arrow import *

class User(pygame.sprite.Sprite):
        
    def __init__(self, screen,
                        client,
                        name,
                        character,
                        img_player,
                        img_arrow,
                        img_heart,
                        img_shield,
                        x, 
                        y):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.client = client
        self.img_src = img_player[character]
        self.image = self.img_src
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.img_heart = img_heart
        self.img_heart_rect = self.img_heart.get_rect()
        
        self.img_shield = img_shield
        self.img_shield_rects = []
        
        self.score = 0
        self.hp = 100
        self.name = name
        self.character = character
        self.is_press = True
        self.cycle_color = None
        self.cycle_color_tick = 0
        
        self.direction = 1 #-1 right to left, 1 left to right
        self.arrow_delay = 0
        self.img_arrow = img_arrow
        self.arrow_group = pygame.sprite.Group()
        self.arrow_cnt = 10
        self.arrow_cnt_tick = 0
        self.teleport_tick = 0
        self.healing_tick = 0
        self.mfont = pygame.font.SysFont("malgungothic", 18)
        
        # wav, ogg 가능
        self.snd_move = pygame.mixer.Sound(f'./sound/shoot.wav')
        self.snd_space = pygame.mixer.Sound(f'./sound/move.wav')
        self.snd_hit = pygame.mixer.Sound(f'./sound/hit.wav')
        self.snd_item = pygame.mixer.Sound(f'./sound/item.wav')
    
    def arrow_add(self):
        if pygame.time.get_ticks() - self.healing_tick > 1000:
            self.healing_tick = pygame.time.get_ticks()
            if self.hp < 200:
                self.hp += 2
                if self.hp > 200:
                    self.hp = 200
            
        if pygame.time.get_ticks() - self.arrow_cnt_tick > 700:
            self.arrow_cnt_tick = pygame.time.get_ticks()
            if self.arrow_cnt < 10:
                self.arrow_cnt += 1
        
    def setText(self):
        try:
            name = self.client.infor['서버정보']['최고점수']['name']
            score = self.client.infor['서버정보']['최고점수']['score']
            if name is not None:
                mtext = self.mfont.render(f'최고점수 ({name} : {score}점)  (순간이동 : 1,2,3,4 HP20 소모)', True, 'red')
                tRec = mtext.get_rect()
                tRec.x = 20
                tRec.y = 20
                self.screen.blit(mtext, tRec)
        except Exception as ex:
            pass
        
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
            
        mtext = self.mfont.render(f'[{self.name} / {self.arrow_cnt}]', True, 'blue')
        tRec = mtext.get_rect()
        tRec.x = self.rect.centerx - tRec.width/2
        tRec.y = self.rect.y - 65
        self.screen.blit(mtext, tRec)
    
    def check_collid_shield(self, x,y):        
        for rec in self.img_shield_rects:
            if rec.colliderect(self.rect):
                self.rect.x += x
                self.rect.y += y
                for i in range(3):
                    if rec.colliderect(self.rect):
                        self.rect.x += x
                        self.rect.y += y
                    else:
                        return
                break
                
    def event_key_pressed(self):
        key_pressed = pygame.key.get_pressed()
        is_press = False
        
        if key_pressed[pygame.K_SPACE]:
            if self.arrow_cnt > 0:
                ellip = pygame.time.get_ticks() - self.arrow_delay
                if(ellip > 200):
                    self.arrow_group.add(Arrow(self.screen, 
                                            self.client.identity, 
                                            self.img_arrow, 
                                            self.rect.x+10,
                                            self.rect.y+40,
                                            self.direction))
                    self.arrow_delay = pygame.time.get_ticks()
                    is_press = True
                    self.snd_space.play()
                    self.arrow_cnt -= 1
        move_step = 5
        
        if key_pressed[pygame.K_LEFT]:
            self.image = pygame.transform.flip(self.img_src, True, False)
            self.direction = -1
            self.rect.x -= move_step
            
            self.check_collid_shield(move_step,0)
            
            if self.rect.x < 0:
                self.rect.x = 0
                
            is_press = True
            if pygame.mixer.get_busy() == False:
                self.snd_move.play()
            
        elif key_pressed[pygame.K_RIGHT]:
            self.image = self.img_src
            self.direction = 1
            self.rect.x += move_step
            
            self.check_collid_shield(-move_step,0)
                
            if self.rect.x+self.rect.width > self.screen.get_width():
                self.rect.x = self.screen.get_width() - self.rect.width
            is_press = True
            if pygame.mixer.get_busy() == False:
                self.snd_move.play()
            
        elif key_pressed[pygame.K_UP]:
            self.rect.y -= move_step
            self.check_collid_shield(0,move_step)
                
            if self.rect.y < 0:
                self.rect.y = 0
                
            is_press = True
            if pygame.mixer.get_busy() == False:
                self.snd_move.play()
            
        elif key_pressed[pygame.K_DOWN]:
            self.rect.y += move_step
            self.check_collid_shield(0,-move_step)
                
            if self.rect.y+self.rect.height > self.screen.get_height():
                self.rect.y = self.screen.get_height() - self.rect.height
                
            is_press = True
            if pygame.mixer.get_busy() == False:
                self.snd_move.play()
            
        elif key_pressed[pygame.K_1]:
            if pygame.time.get_ticks()-self.teleport_tick > 500:
                self.teleport_tick = pygame.time.get_ticks()
                if self.hp > 50:
                    self.hp -= 20
                    self.rect.x = self.rect.width
                    self.rect.y = self.rect.height
                
            is_press = True
            if pygame.mixer.get_busy() == False:
                self.snd_move.play()
            
        elif key_pressed[pygame.K_2]:
            if pygame.time.get_ticks()-self.teleport_tick > 500:
                self.teleport_tick = pygame.time.get_ticks()
                if self.hp > 50:
                    self.hp -= 20
                    self.rect.x = self.screen.get_width()-self.rect.width
                    self.rect.y = self.rect.height
            
            is_press = True
            if pygame.mixer.get_busy() == False:
                self.snd_move.play()
            
            
        elif key_pressed[pygame.K_3]:
            if pygame.time.get_ticks()-self.teleport_tick > 500:
                self.teleport_tick = pygame.time.get_ticks()
                if self.hp > 50:
                    self.hp -= 20
                    self.rect.x = self.rect.width
                    self.rect.y = self.screen.get_height()-self.rect.height
            
            is_press = True
            if pygame.mixer.get_busy() == False:
                self.snd_move.play()
            
        elif key_pressed[pygame.K_4]:
            if pygame.time.get_ticks()-self.teleport_tick > 500:
                self.teleport_tick = pygame.time.get_ticks()
                if self.hp > 50:
                    self.hp -= 20
                    self.rect.x = self.screen.get_width()-self.rect.width
                    self.rect.y = self.screen.get_height()-self.rect.height
            
            is_press = True
            if pygame.mixer.get_busy() == False:
                self.snd_move.play()
            
            
            
        return is_press
                    
    def update(self,player_group):
        is_send = False
        
        self.arrow_add()
        
        if self.event_key_pressed():
            is_send = True
        
        if len(self.arrow_group) > 0:
            for player in player_group:
                if player.check_collide(self.arrow_group):
                    self.score += 2
                    
            self.arrow_group.update()
            self.arrow_group.draw(self.screen)
            is_send = True


        for identity in self.client.infor:
            
            if identity==self.client.identity:
                continue
            
            if identity == '서버정보':
                items = self.client.infor[identity]['아이템']
                for item in items:
                    if 'hp' == item:
                        for loc in items[item]:
                            self.img_heart_rect.x = loc[0]
                            self.img_heart_rect.y = loc[1]
                            self.screen.blit(self.img_heart, self.img_heart_rect)
                            if self.img_heart_rect.colliderect(self.rect):
                                self.hp += 1
                                if self.hp > 200:
                                    self.hp = 200
                                    
                                self.arrow_cnt +=1
                                if self.arrow_cnt > 10:
                                    self.arrow_cnt = 10
                                is_send = True
                                self.snd_item.play()
                                
                    if 'shield' == item:
                        img_shield_rects = []
                        for loc in items[item]:
                            rect = self.img_shield.get_rect()
                            rect.x = loc[0]
                            rect.y = loc[1]
                            self.screen.blit(self.img_shield, rect)
                            img_shield_rects.append(rect)
                            
                            for arrow in self.arrow_group:
                                if rect.colliderect(arrow.rect):
                                    arrow.kill()
                                    
                        self.img_shield_rects = img_shield_rects
            else:       
                if 'arrow' not in self.client.infor[identity]:
                    continue   
                  
                arrows = self.client.infor[identity]['arrow']
                for arrow in arrows:
                    rect_arrow = self.img_arrow.get_rect()
                    rect_arrow.x = arrow[0]
                    rect_arrow.y = arrow[1]
                    
                    if rect_arrow.colliderect(self.rect):
                        self.hp -= 15
                        self.score = -10
                        self.snd_hit.play()
                        if self.score < 0:
                            self.score = 0
                            
                        self.cycle_color = (255,0,0)
                        if self.hp < 1:
                            self.hp = 100
                            self.score = 0
                            self.arrow_cnt = 10
                            
                        is_send = True
                
        self.setText()
        if self.cycle_color is not None:
            pygame.draw.circle(self.screen, self.cycle_color,[self.rect.centerx,self.rect.centery],self.rect.width/2+5, 2)
            if self.cycle_color_tick == 0:
                self.cycle_color_tick = pygame.time.get_ticks()
                
            if pygame.time.get_ticks() - self.cycle_color_tick > 500:
                self.cycle_color = None
                self.cycle_color_tick = 0
                
        self.screen.blit(self.image, self.rect)
        
        if is_send and (self.client is not None):
            self.client.send_infor(self)
        # return self.is_press
        # return self.is_press