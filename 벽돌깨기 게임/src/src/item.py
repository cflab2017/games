import pygame

class Item:
    def __init__(self, x, y, item_type, color):
        self.size = 30 # New size (20 * 1.5 = 30)
        self.rect = pygame.Rect(x - self.size // 2, y - self.size // 2, self.size, self.size) # Adjust rect for center
        self.item_type = item_type # 'life' or 'bullet'
        self.color = color
        self.speed = 3

    def update(self):
        self.rect.y += self.speed

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.rect.center, self.size // 2)
        # Optionally draw a symbol for the item type
        font = pygame.font.Font(None, 20)
        if self.item_type == 'life':
            text = font.render("+", True, (0,0,0)) # Black plus sign
        elif self.item_type == 'bullet':
            text = font.render("B", True, (0,0,0)) # Black 'B'
        text_rect = text.get_rect(center=self.rect.center)
        surface.blit(text, text_rect)
