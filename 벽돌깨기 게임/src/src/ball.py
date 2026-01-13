import pygame
import random

class Ball(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height, border_size, color, initial_speed_x, initial_speed_y):
        super().__init__()
        self.radius = 10
        self.color = color
        self.initial_speed_x = initial_speed_x
        self.initial_speed_y = initial_speed_y
        self.speed_x = initial_speed_x
        self.speed_y = initial_speed_y
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.border_size = border_size

        # Create image and rect attributes
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        self.draw_ball_3d() # Draw the ball onto self.image
        self.rect = self.image.get_rect()
        
        # Create the mask for pixel-perfect collision
        self.mask = pygame.mask.from_surface(self.image)

        self.trail = [] # To store past positions for the tail effect
        self.trail_max_length = 8 # Number of positions to store
        self.reset()

    def draw_ball_3d(self):
        # Draw onto the self.image surface
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)
        light_color = (min(255, self.color[0] + 50), min(255, self.color[1] + 50), min(255, self.color[2] + 50))
        dark_color = (max(0, self.color[0] - 50), max(0, self.color[1] - 50), max(0, self.color[2] - 50))
        
        # Draw a smaller circle inside for highlight
        pygame.draw.circle(self.image, light_color, (self.radius - self.radius // 3, self.radius - self.radius // 3), self.radius // 2)
        # Draw a small arc for shadow
        pygame.draw.arc(self.image, dark_color, (0, 0, self.radius * 2, self.radius * 2), 0, 3.14159, 2)

    def reset(self):
        self.rect.center = (self.screen_width // 2, self.screen_height // 2)
        self.speed_y = -abs(self.speed_y) # Ensure ball goes up initially
        self.speed_x = random.choice([-1, 1]) * abs(self.initial_speed_x) # Random initial x direction
        self.trail = [] # Clear trail on reset

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Add current position to trail
        self.trail.append(self.rect.center)
        if len(self.trail) > self.trail_max_length:
            self.trail.pop(0) # Remove oldest position

        # Wall collision
        if self.rect.left < self.border_size:
            self.rect.left = self.border_size
            self.speed_x *= -1
        elif self.rect.right > self.screen_width - self.border_size:
            self.rect.right = self.screen_width - self.border_size
            self.speed_x *= -1
        
        if self.rect.top < self.border_size:
            self.rect.top = self.border_size
            self.speed_y *= -1

    def draw(self, surface):
        # Draw trail
        for i, pos in enumerate(self.trail):
            alpha = int(255 * (i / self.trail_max_length) * 0.5)
            size = int(self.radius * (i / self.trail_max_length) * 0.8)
            if size > 0 and alpha > 0:
                trail_color = self.color + (alpha,)
                s = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
                pygame.draw.circle(s, trail_color, (size, size), size)
                surface.blit(s, (pos[0] - size, pos[1] - size))

        # Draw the main ball image
        surface.blit(self.image, self.rect)