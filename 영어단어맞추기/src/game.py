import pygame

from createEng import *
# pip install pygame


class GuessingEng:   
    
    def __init__(self) -> None:        
        #pygame 초기화
        pygame.init() #pygame 초기화
        pygame.display.set_caption("codingnow.co.kr")
        self.screen = pygame.display.set_mode((800, 800))
        self.clock = pygame.time.Clock()        
        self.creatEng = CreateEng(self.screen)
        self.img_bg = pygame.image.load('./images/bg.png')
        self.img_bg = pygame.transform.scale(self.img_bg, (self.screen.get_width(), self.screen.get_height()))
        
    def checkQuit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True
            
    def run(self):
        while self.checkQuit():
            self.screen.fill((255, 255, 255))
            self.screen.blit(self.img_bg, (0,0))
            self.creatEng.draw()
            pygame.display.update()
            self.clock.tick(60)   

if __name__ == '__main__':
    game = GuessingEng()
    game.run()