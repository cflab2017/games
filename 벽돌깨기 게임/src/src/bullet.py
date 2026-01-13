import pygame

class Bullet:
    def __init__(self, x, y, color, speed):
        self.rect = pygame.Rect(x, y, 5, 10) # Bullet size
        self.color = color
        self.speed = speed

    def update(self):
        self.rect.y -= self.speed # Bullets move upwards

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
