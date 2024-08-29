import pygame
from pygame.locals import *
from player import *
from army import *
# pip install pygame

class SpaceWar():
    
    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 1000
    game_over = False
    
    def __init__(self) -> None:
        self.is_run = True
        pygame.init() #pygame 초기화
        self.setCaption()
        self.clock = pygame.time.Clock() #프레임을 처리 하기위해
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT)) #화면생성
        self.loadBackground()
        
        self.snd_dic = {
            'shoot':pygame.mixer.Sound('./sound/shoot.wav'),
            # 'score':pygame.mixer.Sound('./sound/score.wav'),
            'gameover':pygame.mixer.Sound('./sound/game_over.wav'),
            'hit':pygame.mixer.Sound('./sound/hit.wav'),
            'shock':pygame.mixer.Sound('./sound/shock.wav'),
        }
        self.player = Player(self.screen,self.snd_dic)
        self.army = Army(self.screen)
        self.player.set_army(self.army)
        
    def setCaption(self):
        pygame.display.set_caption("codingnow.co.kr")   
        icon = pygame.image.load('./images/spaceship.png')
        icon = pygame.transform.scale(icon, (80, 80))
        pygame.display.set_icon(icon)
    
    def loadBackground(self):
        img = pygame.image.load('./images/background.png')
        self.img_bg = pygame.transform.scale(img, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
    
    def gameRestart(self):
        self.game_over = False
        self.player.restart()
        self.army.create_ememy(self.player.level)
        # self.army.create_ememy(45)
        
    #이벤트 확인 및 처리 함수
    def eventProcess(self):
        for event in pygame.event.get():#이벤트 가져오기
            if event.type == QUIT: #종료버튼?
                self.is_run = False
            if event.type == pygame.KEYDOWN:#키 눌림?
                if event.key == pygame.K_SPACE:#space?
                    pass
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:#space?
                    if self.player.hp == 0:
                        self.gameRestart()
                
    def run(self):
        
        self.gameRestart()
        
        while self.is_run:
            self.screen.fill((255, 255, 255)) #화면을 흰색으로 채우기
            self.screen.blit(self.img_bg, (0, 0)) #이미지 넣기
            
            self.eventProcess() #이벤트 함수 호출
            self.player.draw()
            self.army.draw()
            
            if self.player.hp <= 0:
                if self.game_over == False:
                    self.snd_dic['gameover'].play()
                    self.game_over = True
            else:               
                for em in self.army.army_group:                
                    if pygame.sprite.spritecollide(self.player, em.bullet_group, True):
                        self.snd_dic['shock'].play()
                        self.player.hp -= 10
                        self.player.shield_on = True
                        if self.player.hp <=0:
                            self.player.hp = 0
                    else:
                        if pygame.sprite.spritecollide(em, self.player.bullet_group, True):
                            self.snd_dic['hit'].play()
                            em.hp -= 1
                            if em.hp < 1:
                                self.player.score += 30
                                em.kill()
                            else:
                                em.shield_on = True
                                self.player.score += 10
                                
                if len(self.army.army_group)==0 and self.player.level_up_tick==0:
                    self.player.level += 1
                    self.player.level_up = True
                    
                
            pygame.display.update() #화면 갱신
            self.clock.tick(200) #초당 60프레임 갱신을 위한 잠시 대기

if __name__ == '__main__':
    main = SpaceWar()
    main.run()