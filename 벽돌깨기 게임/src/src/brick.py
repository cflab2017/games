import pygame

class Brick:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        # Add 3D effect (simple shading)
        light_color = (min(255, self.color[0] + 30), min(255, self.color[1] + 30), min(255, self.color[2] + 30))
        dark_color = (max(0, self.color[0] - 30), max(0, self.color[1] - 30), max(0, self.color[2] - 30))

        # Top and left highlights
        pygame.draw.line(surface, light_color, (self.rect.left, self.rect.top), (self.rect.right, self.rect.top), 2)
        pygame.draw.line(surface, light_color, (self.rect.left, self.rect.top), (self.rect.left, self.rect.bottom), 2)
        # Bottom and right shadows
        pygame.draw.line(surface, dark_color, (self.rect.left, self.rect.bottom), (self.rect.right, self.rect.bottom), 2)
        pygame.draw.line(surface, dark_color, (self.rect.right, self.rect.top), (self.rect.right, self.rect.bottom), 2)
