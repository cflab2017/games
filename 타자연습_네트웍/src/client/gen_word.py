
import pygame
import random

import pygame.time

class Gen_Workd():
    # game_words = ['if','for', 'while']
    game_words = []
    def __init__(self,parent) -> None:
        self.parent = parent
        self.screen = self.parent.screen
        
        self.mfont30 = pygame.font.SysFont("malgungothic", 30)
        self.speed = 1
        self.words = {}
        self.get_words()
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
        
        if len(self.words) >= self.parent.level:
            return
        
        while True:
            max_len = self.parent.level*3+26
            if max_len > len(self.game_words)-1:
                max_len = len(self.game_words)-1
            
            value = self.game_words[random.randint(0,max_len)]
            # if self.parent.level < 5:
            if value in "(){}[]/%&*!@#$?":
                continue
            if value not in self.words:
                break
        
        img = self.mfont30.render(value, 2, (0,255,255))
        rect = img.get_rect()
        rect.x = random.randint(0,self.screen.get_width() - rect.width-self.parent.msg_win_width)
        rect.y = 0
        speed = random.randint(1,2)
        self.words[value] = {'img':img, 'rect':rect, 'speed':speed}
        
    def clear_word(self):
        self.words.clear()
        self.creat_word()
        
    def match_word(self, key):
        centerx = None
        centery = None
        # display_words = []
        # for word in self.words:
        #     display_words.append(word.lower())
        # key = key.lower()
        # print(key, self.words)
        if key in self.words:
            centerx = self.words[key]['rect'].centerx
            centery = self.words[key]['rect'].centery
            del self.words[key]
            
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
            
        
    def draw(self, gamover):
        if gamover == False:
            self.create_word_uing_time()
        delet_keys = []
        is_drop = False
        for key in self.words:
            img = self.words[key]['img']
            rect = self.words[key]['rect']
            # rect.y += (self.speed+(self.parent.level - 1*0.2))
            rect.y += self.words[key]['speed']
            if rect.bottom > self.screen.get_height()-self.parent.inp_win_heigh:
                # del self.words[key]
                delet_keys.append(key)
                is_drop = True
            else:
                self.screen.blit(img,rect)
                
        for key in delet_keys:
            del self.words[key]
            
        if is_drop:
            self.creat_word()
            
        return is_drop