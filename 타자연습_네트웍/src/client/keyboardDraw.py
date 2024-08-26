
import argparse

import keyboardlayout as kl
import keyboardlayout.pygame as klp
from keyboardlayout.pygame.key import *
import pygame
import pygame.event
import pygame.locals
# https://pypi.org/project/keyboardlayout/
# pip install keyboardlayout

class KeyboardDraw():
    
    grey = pygame.Color('grey')
    dark_grey = ~pygame.Color('grey')
    key_disp = []
    key_disp_pre = []
    
    def __init__(self,screen) -> None: 
        self.screen = screen
        parser = argparse.ArgumentParser()
        parser.add_argument(
            'layout_name',
            nargs='?',
            type=kl.LayoutName,
            default=kl.LayoutName.QWERTY,
            help='the layout_name to use',
        )
        args = parser.parse_args()
           
        key_size = 60
        self.released_key_info = kl.KeyInfo(
            margin=10,
            color=self.grey,
            txt_color=self.dark_grey,
            txt_font=pygame.font.SysFont('Arial', key_size//4),
            txt_padding=(key_size//6, key_size//10),
        )
        self.keyboard = self.get_keyboard(args.layout_name, key_size, self.released_key_info)
        

        self.pressed_key_info = kl.KeyInfo(
            margin=14,
            color=pygame.Color('red'),
            txt_color=pygame.Color('white'),
            txt_font=pygame.font.SysFont('Arial', key_size//4),
            txt_padding=(key_size//6, key_size//10)
        )
    
        self.words_key_info = kl.KeyInfo(
            margin=14,
            color=pygame.Color(0,255,255),
            txt_color=pygame.Color('black'),
            txt_font=pygame.font.SysFont('Arial', key_size//4),
            txt_padding=(key_size//6, key_size//10)
        )
        
    def get_keyboard(self,
        layout_name: kl.LayoutName,
        key_size: int,
        key_info: kl.KeyInfo
    ) -> klp.KeyboardLayout:
        keyboard_info = kl.KeyboardInfo(
            position=(0, 0),
            padding=2,
            color=~self.grey
        )
        letter_key_size = (key_size, key_size)  # width, height
        keyboard_layout = klp.KeyboardLayout(
            layout_name,
            keyboard_info,
            letter_key_size,
            key_info
        )
        return keyboard_layout
    
    def pykey_2_key(self,key):
        try:
            key = KEY_MAP_BY_LAYOUT[self.keyboard.layout_name][key]
            actual_key = self.keyboard._key_to_actual_key.get(key, key)
            self.keyboard._key_to_sprite_group[actual_key]
            return key
        except KeyError:
            return None
    
    def update_key(self,event):
        if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            key_name = pygame.key.name(event.key)
            key = self.keyboard.get_key(event)
            if key is None:
                return            
            if event.type == pygame.KEYDOWN:
                self.keyboard.update_key(key, self.pressed_key_info)
            elif event.type == pygame.KEYUP:
                self.keyboard.update_key(key, self.released_key_info)
            
    def draw(self, words):
        self.key_disp = []
        for word in words:
            for w in word:
                # test = getattr(pygame.locals, "K_" + w.lower())
                key = pygame.key.key_code(w)       
                key = self.pykey_2_key(key)
                self.keyboard.update_key(key, self.words_key_info)
                self.key_disp.append(key)
                        
        for key in self.key_disp_pre:
            if key not in self.key_disp:
                print('aaa')
                self.keyboard.update_key(key, self.released_key_info)
                
        self.key_disp_pre = self.key_disp[:]
        
        self.keyboard.draw(self.screen)