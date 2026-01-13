import pygame
import math

class Paddle(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height, border_size, color):
        super().__init__()
        self.width = 100
        self.height = 15
        self.speed = 7
        self.color = color
        
        # Angle properties
        self.angle = 0
        self.max_angle = 45
        self.angle_speed = 2

        # Create the original, unrotated image of the paddle
        self.original_image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.draw_paddle_3d(self.original_image, (0, 0, self.width, self.height))
        
        # Store the original center position
        self.center_x = (screen_width - self.width) // 2 + self.width / 2
        self.center_y = screen_height - border_size - self.height - 30 + self.height / 2

        # The 'image' will be the rotated version of 'original_image'
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(self.center_x, self.center_y))
        
        # Create the mask for pixel-perfect collision
        self.mask = pygame.mask.from_surface(self.image)

        self.border_size = border_size
        self.screen_width = screen_width

    def draw_paddle_3d(self, surface, rect):
        """Draws the 3D-effect paddle onto a given surface."""
        pygame.draw.rect(surface, self.color, rect, border_radius=3)
        light_color = (min(255, self.color[0] + 50), min(255, self.color[1] + 50), min(255, self.color[2] + 50))
        dark_color = (max(0, self.color[0] - 50), max(0, self.color[1] - 50), max(0, self.color[2] - 50))
        r = pygame.Rect(rect)
        pygame.draw.line(surface, light_color, (r.left + 2, r.top), (r.right - 2, r.top), 2)
        pygame.draw.line(surface, light_color, (r.left, r.top + 2), (r.left, r.bottom - 2), 2)
        pygame.draw.line(surface, dark_color, (r.left + 2, r.bottom -1), (r.right - 2, r.bottom-1), 2)
        pygame.draw.line(surface, dark_color, (r.right -1, r.top + 2), (r.right-1, r.bottom - 2), 2)

    def update(self, keys):
        # Handle angle changes
        if keys[pygame.K_UP]:
            self.angle += self.angle_speed
        if keys[pygame.K_DOWN]:
            self.angle -= self.angle_speed
        
        self.angle = max(-self.max_angle, min(self.max_angle, self.angle))

        # Handle horizontal movement
        if keys[pygame.K_LEFT]:
            self.center_x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.center_x += self.speed

        # Rotate the paddle and update its rect
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=(self.center_x, self.center_y))
        
        # *** Update the mask AFTER rotation ***
        self.mask = pygame.mask.from_surface(self.image)

        # Boundary check
        if self.rect.left < self.border_size:
            self.rect.left = self.border_size
            self.center_x = self.rect.centerx
        if self.rect.right > self.screen_width - self.border_size:
            self.rect.right = self.screen_width - self.border_size
            self.center_x = self.rect.centerx

    def draw(self, surface):
        surface.blit(self.image, self.rect)
