import pygame
from pygame import Surface
import pygame.surface
import pygame.time

class Msg_draw():
    
    msg_win_width = 400
    def __init__(self,screen:Surface,game_line_start,game_line_end) -> None:
        self.screen = screen
        self.game_line_start = game_line_start
        self.game_line_end = game_line_end
        
        self.mfont100 = pygame.font.SysFont("malgungothic", 100)
        self.mfont60 = pygame.font.SysFont("malgungothic", 60)
        self.mfont40 = pygame.font.SysFont("malgungothic", 40)
        self.mfont30 = pygame.font.SysFont("malgungothic", 20)
        self.mfont18 = pygame.font.SysFont("malgungothic", 18)
    
        img = pygame.image.load('./images/heart.png')
        self.img_heart = pygame.transform.scale(img,((30, 30)))
        self.img_heart.set_alpha(200)
        
        self.status_msg_tick = 0
        self.status_msg_disp = ''   
        self.status_msg = []
        self.game_start_msg_tick = 0
        self.game_over_msg_tick = 0
        self.game_timout_msg_tick = 0
        
        self.snd_count = pygame.mixer.Sound(f'./sound/shoot.wav')
        
    def drawStatusMsg(self):           
        if self.status_msg_tick == 0:
            if len(self.status_msg):
                self.status_msg_disp = self.status_msg.pop()
                self.status_msg_tick = pygame.time.get_ticks()
        else:
            ellip = pygame.time.get_ticks() - self.status_msg_tick
            if ellip < 2000:
                if ellip < 400 or (800 < ellip < 1200)or (1600 < ellip):                    
                    img = self.mfont40.render(self.status_msg_disp, 1, (255,0,0))
                    img.set_alpha(150)
                    rect = img.get_rect()
                    rect.centerx = (self.screen.get_width()/2 -rect.width)-50
                    rect.centery = self.screen.get_height()/2
                    self.screen.blit(img,rect)
            else:
                self.status_msg_tick = 0
                self.status_msg_disp = ''   
    
    def display_users_score(self,parent):
        users, high = parent.client.get_score()
        if len(users):
            # print(users)
            
            width = self.msg_win_width
            x = self.screen.get_width() - width
            x += 4
            y = self.game_line_start+10
            
            img = self.mfont30.render(f'최고점수', 1, (255,0,0))
            self.screen.blit(img,(x, y))
            y+= 40
            if len(high)>1:
                for i,hi in enumerate(high):
                    name = hi[0]
                    score = hi[1]
                    date = hi[2]
                    img = self.mfont30.render(f' {i+1}위 {score:,d} ({name} : {date})', 1, (0,255,255))
                    rect = img.get_rect()
                    rect.x = x
                    rect.y = y
                    self.screen.blit(img,(x, y))
                    y = rect.bottom+5
            
            img = self.mfont30.render(f'나의기록', 1, (255,0,0))
            rect = self.screen.blit(img,(x, y))
            y = rect.bottom+5
            
            img = self.mfont30.render(f' {parent.score_high:7,d}', 1, (0,255,255))
            rect = self.screen.blit(img,(x, y))
            y = rect.bottom+5

            
            img = self.mfont30.render(f'접속순위', 1, (255,0,0))
            self.screen.blit(img,(x, y))
            y+= 40
            for i,user in enumerate(users):
                if parent.user_name == user[0]:
                    color = (0,255,0)
                    img = self.mfont30.render(f' {i+1}위 {user[1]:7,d} {user[0]}', 1, color,(0,0,0))
                    rect = img.get_rect()
                    rect.x = x
                    rect.y = y
                    # temp_surface = pygame.Surface((rect.width,rect.height))
                    # temp_surface.fill((0,0,0))
                    self.screen.blit(img,rect)
                else:
                    color = (255,255,255)
                    img = self.mfont30.render(f' {i+1}위 {user[1]:7,d} {user[0]}', 1, color)
                    self.screen.blit(img,(x, y))
                y+= 40
                
    def display_startGame(self,parent):
        if len(parent.game_start_msg):
            msg = parent.game_start_msg[parent.game_start_msg_idex]
            img = self.mfont100.render(f'{msg}', 1, (255,255,255))
            rect = img.get_rect()
            rect.centerx = (self.screen.get_width()-self.msg_win_width)/2
            rect.centery = self.screen.get_height()/3
            
            self.screen.blit(img,rect)
            
            if self.game_start_msg_tick == 0:
                self.game_start_msg_tick = pygame.time.get_ticks()
            if pygame.time.get_ticks() - self.game_start_msg_tick > 500:
                self.game_start_msg_tick = pygame.time.get_ticks()
                parent.game_start_msg_idex += 1
                self.snd_count.play()
                if len(parent.game_start_msg) <= parent.game_start_msg_idex:
                    parent.game_start_msg.clear()
                    parent.game_start_msg_idex = 0
                    self.game_start_msg_tick = 0                    
                    parent.is_game_over = False
                    parent.game_play_time = pygame.time.get_ticks() + 1000*60*2
            
    def display_gameover(self,parent):
        if parent.is_game_over and self.game_start_msg_tick==0:
            ellip = pygame.time.get_ticks() - self.game_over_msg_tick
            if ellip < 500:
                color = (255,255,255)
            elif ellip < 1000:
                color = (255,0,0)
            else:
                self.game_over_msg_tick = pygame.time.get_ticks()
                color = (255,0,0)
                
            img1 = self.mfont40.render(f'Game Over!!', 1, color)
            rect1 = img1.get_rect()
            
            img2 = self.mfont30.render(f'[재시작 : 스페이스 누르기]', 1, (255,255,255))
            rect2 = img2.get_rect()
            rect2.y = rect1.bottom
            
            temp_surface = pygame.Surface((rect2.width,rect1.height*2))
            temp_surface.set_alpha(200)
            temp_surface.blit(img1,rect1)
            temp_surface.blit(img2,rect2)
            
            # self.screen.blit(temp_surface, rect)
            
            # img = self.mfont30.render(f'Game Over!! [재시작 : 스페이스 누르기]', 1, (255,255,255))
            rect = temp_surface.get_rect()
            rect.centerx = (self.screen.get_width()-self.msg_win_width)/2
            rect.centery = self.screen.get_height()/3
            self.screen.blit(temp_surface,rect)
            
    def display_timeout(self,parent):
        if parent.is_game_over==False:
            millis = parent.game_play_time-pygame.time.get_ticks()
            color = (255,255,255)
            if millis < 1000*10:
                ellip = pygame.time.get_ticks() - self.game_timout_msg_tick
                if ellip < 500:
                    color = (255,255,255)
                elif ellip < 1000:
                    color = (255,0,0)
                else:
                    self.game_timout_msg_tick = pygame.time.get_ticks()
                    color = (255,0,0)
                
            sec = int((millis/1000)%60)
            minute = int((millis/1000)/60)
            millis = int(millis%1000)
            
            img = self.mfont60.render(f'{minute}:{sec}:{millis:03}', 1, color)
            rect = img.get_rect()
            rect.centerx = (self.screen.get_width()-self.msg_win_width)/2
            rect.centery = self.screen.get_height()/3+100
            # self.screen.blit(img,rect)
            
            temp_surface = pygame.Surface((rect.width,rect.height))
            temp_surface.fill((0,0,0))
            temp_surface.set_alpha(100)
            temp_surface.blit(img,(0,0))
            self.screen.blit(temp_surface,rect)
            
    def display_combo(self,parent):        
        if parent.com_bo_ellip > 0:
            
            img = self.mfont30.render(f' 콤보시간: {parent.com_bo_tick_limit - parent.com_bo_ellip}: 점수{parent.com_bo_bonus}배', 1, (255,255,0))
            img.set_alpha(150)
            rect = img.get_rect()
            rect.centerx = (self.screen.get_width()-rect.width)-50
            rect.y = self.game_line_end - rect.height - 10
            self.screen.blit(img,rect)
            
        for i,com in enumerate(parent.com_bo_position):
            if pygame.time.get_ticks()- com[2] > 3000:
                del parent.com_bo_position[i]
            else:
                img = self.mfont40.render(f'점수 {com[3]}배', 1, (255,0,0))
                img.set_alpha(150)
                rect = img.get_rect()
                rect.centerx = (self.screen.get_width()-self.msg_win_width)/2
                rect.centery = self.screen.get_height()-200
                    
                self.screen.blit(img,rect)
                
    def display_box(self,parent):
        
        width = self.msg_win_width
        height = self.game_line_end#self.screen.get_height()
        x = self.screen.get_width() - width
        y = 0+self.game_line_start
        pygame.draw.rect(self.screen, (255,255,255),(x,y, width,height), 1)
        
            
        img = self.mfont30.render(' 입력: '+parent.msg_inbox, 1, (255,255,255))
        rect = img.get_rect()
        rect.x = 20
        rect.y = self.game_line_end - rect.height - 10
        rect.width = self.screen.get_width()-self.msg_win_width-40
        self.screen.blit(img,rect)
        
    def draw_heart(self,parent):        
        
        rect = self.img_heart.get_rect()
        rect.x = 20
        rect.y = self.game_line_start+2
        for i in range(parent.hp):
            self.screen.blit(self.img_heart,rect)
            rect.x += rect.width+10
        
        img = self.mfont30.render(f' 레벨: {parent.level}', 1, (255,255,255))
        img.set_alpha(150)
        rect = img.get_rect()
        rect.x = 220
        rect.y = self.game_line_start+2
        self.screen.blit(img,rect)
        
        img = self.mfont30.render(f' 점수: {parent.score}', 1, (255,255,255))
        img.set_alpha(150)
        rect = img.get_rect()
        rect.x = 220+100
        rect.y = self.game_line_start+2
        self.screen.blit(img,rect)
    
    def draw(self,parent):        
        self.draw_heart(parent)
        self.display_users_score(parent)
        self.display_gameover(parent)
        self.display_combo(parent)
        self.display_box(parent)
        self.drawStatusMsg()
        self.display_startGame(parent)
        self.display_timeout(parent)