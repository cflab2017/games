
import pygame
import random

import pygame.time

class Gen_Workd():
    # game_words = ['if','for', 'while']
    game_words = []
    def __init__(self,parent, game_words,game_line_start,game_line_end,game_line_dead) -> None:
        self.parent = parent
        self.screen = self.parent.screen
        self.game_line_start = game_line_start
        self.game_line_end = game_line_end
        self.game_line_dead = game_line_dead
        
        img = pygame.image.load('./images/boom.png')
        self.img_boom = pygame.transform.scale(img,((40, 40)))
        self.rect_boom = self.img_boom.get_rect()
        
        self.creat_delay_tick = 0
        self.mfont30 = pygame.font.SysFont("malgungothic", 30)
        self.speed = 1
        self.words = {}
        if game_words is None:
            self.get_words()
        else:
            self.game_words = game_words
            
        self.creat_word_time_tick = 0
        # self.creat_word()
    
    def get_words(self):        
        with open("word.txt", "r") as f:
            lines = f.readlines()
            for line in lines:
                if len(line.replace(" ","")):
                    word = line.replace("\n","")
                    word = word.replace(" ","")
                    # word = word.lower()
                    
                    self.game_words.append(word)
            self.game_words = sorted(self.game_words, key=lambda x:len(x))
            
    def creat_word(self):
        
        if len(self.words) > 0 and pygame.time.get_ticks() - self.creat_delay_tick < 1000:
            return
        
        self.creat_delay_tick = pygame.time.get_ticks()
        
        limit_num = self.parent.level
        if limit_num > 10:
            limit_num = 10
        
        if len(self.words) >= limit_num:
            return
        
        while True:
            max_len = 26-1
            
            if self.parent.level > 10:
                max_len += self.parent.level
                
            if max_len > len(self.game_words)-1:
                max_len = len(self.game_words)-1
            
            value = self.game_words[random.randint(0,max_len)]
            if self.parent.level > 10 and (random.randint(0,max_len)<50):
                temp = value + self.game_words[random.randint(0,max_len)]
                if len(temp) <= 2:
                    value = temp
            if self.parent.level > 20 and (random.randint(0,max_len)<50):
                temp = value + self.game_words[random.randint(0,max_len)]
                if len(temp) <= 3:
                    value = temp
            if self.parent.level > 30 and (random.randint(0,max_len)<50):
                temp = value + self.game_words[random.randint(0,max_len)]
                if len(temp) <= 4:
                    value = temp
                
            # if self.parent.level < 5:
            if value in "(){}[]/%&*!@#$?":
                continue
            if value not in self.words:
                break
        
        img = self.mfont30.render(value, 2, (255,255,255))
        rect = img.get_rect()
        
        is_ok = False
        cnt = 0
        while is_ok==False and cnt < 10:
            rect.x = random.randint(0,self.screen.get_width() - rect.width-self.parent.msg_draw.msg_win_width)
            rect.y = self.game_line_start+40#0+300 +40
            rect2 = rect.copy()
            rect2.height += 40
            
            is_ok = True
            for word in self.words:
                if rect2.colliderect(self.words[word]['rect']):
                    is_ok = False
                    cnt+=1
                    break
                
        start_speed = 9
        end_speed = 10
        offset_speed = 0
        if self.parent.level > 10:
            offset_speed = int(self.parent.level/10)
            if offset_speed > 8:
                offset_speed = 8
            start_speed -= offset_speed
            
        if self.parent.level > 20:
            offset_speed = int(self.parent.level/20)
            if offset_speed > 8:
                offset_speed = 8
            end_speed -= offset_speed
            if start_speed >= end_speed:
                end_speed = start_speed + 1
            
        speed = random.randint(start_speed,end_speed)
        self.words[value] = {'img':img, 'rect':rect, 'speed':speed, 'speed_cnt':0,'blink_tick':0,'blink_color':0}
        
    def clear_word(self):
        self.words.clear()
        self.creat_word()
        
    def match_word(self, key):
        centerx = None
        centery = None
        # display_words = []
        # for word in self.words:
        #     display_words.append(word.lower())
        key = key.lower()
        # print(key, self.words)
        for word in self.words:
            temp = word.replace(' ','')
            temp = temp.replace('\n','')
            temp = temp.lower()
            if key == temp:
                centerx = self.words[word]['rect'].centerx
                centery = self.words[word]['rect'].bottom
                del self.words[word]
                break
            
        # if key in self.words:
        #     centerx = self.words[key]['rect'].centerx
        #     centery = self.words[key]['rect'].centery
        #     del self.words[key]
            
        if centerx is not None:
            # self.creat_word()
            self.creat_word_time_tick = pygame.time.get_ticks()-1000 + 500
            
        return centerx,centery
            
    def update(self):
        pass
    
    def create_word_uing_time(self):
        
        ellip = pygame.time.get_ticks() - self.creat_word_time_tick
        if ellip > (1000 - self.parent.level*10):
            self.creat_word_time_tick = pygame.time.get_ticks()
            self.creat_word()
    
    def drop(self):
        for key in self.words:
            rect = self.words[key]['rect']
            # rect.y += (self.speed+(self.parent.level - 1*0.2))
            if self.words[key]['speed_cnt'] > self.words[key]['speed']:
                rect.y += 1
                self.words[key]['speed_cnt'] = 0
            else:
                self.words[key]['speed_cnt'] += 1
        
    def draw(self, gamover):
        if gamover == False:
            self.create_word_uing_time()
        delet_keys = []
        is_drop = False
        drops = []
        for key in self.words:
            img = self.words[key]['img']
            rect = self.words[key]['rect']
            # rect.y += (self.speed+(self.parent.level - 1*0.2))
            # rect.y += self.words[key]['speed']
            if rect.bottom > self.game_line_dead:#self.screen.get_height()-self.parent.inp_win_heigh:
                # del self.words[key]
                delet_keys.append(key)
                drops.append(rect)
                is_drop = True
            else:
                size = img.get_size()
                w = rect.width+4
                h = rect.height+4
                rect_img = pygame.Rect(0,0,w,h)
                temp_surface = pygame.Surface((w,h))
                ellip = pygame.time.get_ticks() - self.words[key]['blink_tick']
                if ellip > 200:
                    self.words[key]['blink_tick'] = pygame.time.get_ticks()
                    if self.words[key]['blink_color'] == 0:
                        self.words[key]['blink_color'] = 1
                    else:
                        self.words[key]['blink_color'] = 0
                if self.words[key]['blink_color']:
                    temp_surface.fill((0, 0, 0))
                else:
                    temp_surface.fill((255, 0, 0))
                temp_surface.blit(img, (2, 2))
                temp_surface.set_alpha(100)
                
                # img_boom = pygame.transform.scale(self.img_boom,((rect.width*2, rect.height*2)))
                # rect_boom = img_boom.get_rect()
                self.rect_boom.centerx = rect.centerx
                self.rect_boom.top  = rect.bottom
                self.screen.blit(self.img_boom,self.rect_boom)
                
                self.screen.blit(temp_surface, rect)
                
        for key in delet_keys:
            del self.words[key]
            
        if is_drop:
            self.creat_word()
            
        return drops