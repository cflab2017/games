import pygame
import random

class Particle:
    def __init__(self, x, y, color, size, lifetime, x_vel=0, y_vel=0):
        self.x = x
        self.y = y
        self.color = color
        self.size = size
        self.lifetime = lifetime
        self.current_lifetime = lifetime
        self.x_vel = x_vel if x_vel != 0 else random.uniform(-2, 2)
        self.y_vel = y_vel if y_vel != 0 else random.uniform(-2, 2)

    def update(self):
        self.x += self.x_vel
        self.y += self.y_vel
        self.current_lifetime -= 1

    def draw(self, surface):
        if self.current_lifetime > 0:
            alpha = int(255 * (self.current_lifetime / self.lifetime))
            color_with_alpha = self.color + (alpha,)
            s = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
            pygame.draw.circle(s, color_with_alpha, (self.size, self.size), self.size)
            surface.blit(s, (self.x - self.size, self.y - self.size))
