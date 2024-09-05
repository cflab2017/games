import pygame
import pygame.event
import pygame.image
import pygame.transform
import pygame.key

from player import *

class Game():
    isActive = True
    SCREEN_WIDTH = 400
    SCREEN_HEIGHT = 400
    
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("codingnow.co.kr")
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        cx = self.screen.get_width()/2
        cy = self.screen.get_height()/2
        self.player = Player(self.screen,cx,cy)

    def eventProcess(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                self.isActive = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pass
            
    def run(self):
        while self.isActive:
            self.screen.fill((0, 0, 0))
            self.eventProcess()
            
            self.player.draw()
            pygame.display.update()
            self.clock.tick(200)

if __name__ == '__main__':
    game = Game()
    game.run()