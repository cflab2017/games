import pygame
import random
import math
from src.paddle import Paddle
from src.ball import Ball
from src.brick import Brick
from src.item import Item
from src.bullet import Bullet
from src.particle import Particle # Import Particle class
from src.keyboard import Keyboard # Import Keyboard class

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.screen_width = 800
        self.screen_height = 600
        self.screen_title = "Breakout Game"
        self.border_size = 10

        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.gradient_start = (0, 0, 0)
        self.gradient_end = (50, 50, 50)

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption(self.screen_title)

        self.font = pygame.font.Font(None, 36)
        self.clock = pygame.time.Clock() # For FPS control

        # Load sounds
        try:
            self.brick_hit_sound = pygame.mixer.Sound("assets/brick_hit.wav")
            self.paddle_hit_sound = pygame.mixer.Sound("assets/paddle_hit.wav")
            self.bullet_sound = pygame.mixer.Sound("assets/bullet.wav") # New sound for bullet
            self.item_collect_sound = pygame.mixer.Sound("assets/item_collect.wav") # New sound for item collection
        except pygame.error as e:
            print(f"Could not load sound file: {e}")
            self.brick_hit_sound = None
            self.paddle_hit_sound = None
            self.bullet_sound = None
            self.item_collect_sound = None

        self.paddle = Paddle(self.screen_width, self.screen_height, self.border_size, self.white)
        self.ball = Ball(self.screen_width, self.screen_height, self.border_size, (255, 255, 0), 5, -5)

        self.brick_width = 60
        self.brick_height = 20
        self.brick_rows = 5
        self.brick_cols = 10
        self.brick_colors = [
            (255, 0, 0),    # Red
            (255, 165, 0),  # Orange
            (255, 255, 0),  # Yellow
            (0, 255, 0),    # Green
            (0, 0, 255)     # Blue
        ]

        self.bricks = []
        self.items = [] # List to hold falling items
        self.bullets = [] # List to hold active bullets
        self.particles = [] # List to hold active particles
        self.bullet_count = 0 # Initial bullet count

        self.score = 0
        self.lives = 3
        self.level = 1
        self.game_over = False
        self.game_state = "start" # "start", "playing", "game_over"
        self.bottom_border_red_timer = 0 # Timer for red bottom border effect
        self.red = (255, 0, 0)
        self.ball_lost_flag = False # Flag to indicate ball lost and delay reset

        # Initialize Keyboard for display
        keyboard_x = self.screen_width - 130 - 20 # Middle right
        keyboard_y = self.screen_height // 2 - 50 # Middle right
        self.keyboard = Keyboard(keyboard_x, keyboard_y)

        self.create_bricks()

    def create_bricks(self):
        self.bricks = []
        for row in range(self.brick_rows):
            for col in range(self.brick_cols):
                brick_x = col * (self.brick_width + 5) + self.border_size + 20
                brick_y = row * (self.brick_height + 5) + self.border_size + 30
                color_index = (row + self.level - 1) % len(self.brick_colors)
                self.bricks.append(Brick(brick_x, brick_y, self.brick_width, self.brick_height, self.brick_colors[color_index]))

    def reset_game_state(self):
        self.ball.reset()
        # Reset paddle position and angle
        self.paddle.center_x = self.screen_width // 2
        self.paddle.angle = 0
        self.items = [] # Clear items on reset
        self.bullets = [] # Clear bullets on reset
        self.particles = [] # Clear particles on reset

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                self.keyboard.handle_event(event) # Pass event to keyboard
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if self.game_state == "start" and event.key == pygame.K_SPACE:
                        self.game_state = "playing"
                    elif self.game_state == "game_over" and event.key == pygame.K_SPACE:
                        # Reset game for new start
                        self.score = 0
                        self.lives = 3
                        self.level = 1
                        self.game_over = False
                        self.bullet_count = 0 # Reset bullet count
                        self.create_bricks()
                        self.reset_game_state()
                        self.game_state = "playing"
                    elif self.game_state == "playing" and event.key == pygame.K_SPACE:
                        if self.bullet_count > 0:
                            bullet_x = self.paddle.rect.centerx - 2 # Adjust for bullet width
                            bullet_y = self.paddle.rect.top - 10 # Above the paddle
                            self.bullets.append(Bullet(bullet_x, bullet_y, self.white, 10))
                            self.bullet_count -= 1
                            if self.bullet_sound:
                                self.bullet_sound.play()

            keys = pygame.key.get_pressed()

            if self.game_state == "playing":
                # Only update ball position if not in ball lost delay
                if not self.ball_lost_flag:
                    self.ball.update()

                    # Only update other game logic if not in ball lost delay
                    
                    self.paddle.update(keys)

                    # Update and check items
                    for item in self.items[:]:
                        item.update()
                        # Create particles for item trail
                        for _ in range(5): # 5 particles per item per frame
                            self.particles.append(Particle(item.rect.centerx, item.rect.centery, item.color, random.randint(1, 3), 15, random.uniform(-1, 1), random.uniform(0, 2)))

                        if item.rect.top > self.screen_height: # Remove if off-screen
                            self.items.remove(item)
                        elif item.rect.colliderect(self.paddle.rect): # Item collected
                            if self.item_collect_sound:
                                self.item_collect_sound.play()
                            if item.item_type == 'life':
                                self.lives += 1
                            elif item.item_type == 'bullet':
                                self.bullet_count += 5
                            self.items.remove(item)

                    # Update and check bullets
                    for bullet in self.bullets[:]:
                        bullet.update()
                        if bullet.rect.bottom < self.border_size: # Remove if off-screen
                            self.bullets.remove(bullet)
                        else:
                            for brick in self.bricks[:]:
                                if bullet.rect.colliderect(brick.rect):
                                    # Create particles for bullet-brick collision
                                    for _ in range(5): # 5 particles
                                        self.particles.append(Particle(bullet.rect.centerx, bullet.rect.centery, brick.color, random.randint(2, 5), 30))

                                    self.bricks.remove(brick)
                                    self.score += 10
                                    if self.brick_hit_sound:
                                        self.brick_hit_sound.play()
                                    self.bullets.remove(bullet)
                                    break # Bullet hits only one brick

                    # Ball-paddle collision
                    if pygame.sprite.collide_mask(self.ball, self.paddle) and self.ball.speed_y > 0:
                        if self.paddle_hit_sound:
                            self.paddle_hit_sound.play()

                        # Reverse vertical direction
                        self.ball.speed_y *= -1

                        # --- Simplified & Robust Collision Physics ---

                        # 1. Factor in where the ball hit the paddle (minor effect)
                        diff = self.ball.rect.centerx - self.paddle.rect.centerx
                        normalized_diff = diff / (self.paddle.width / 2)
                        position_effect = normalized_diff * 2.0 # Reduced influence

                        # 2. Factor in the paddle's angle (major effect)
                        # The factor can be tuned for more/less effect
                        angle_effect = self.paddle.angle * -0.20 # Increased influence, and INVERTED SIGN

                        # 3. Combine effects to get new speed
                        new_speed_x = position_effect + angle_effect

                        # 4. Prevent ball from getting stuck in a vertical loop
                        if abs(new_speed_x) < 1.5:
                            new_speed_x = random.choice([-1.5, 1.5])
                        
                        self.ball.speed_x = new_speed_x
                        max_speed_x = abs(self.ball.initial_speed_x) * 1.7 # Allow a bit more speed from angle
                        self.ball.speed_x = max(-max_speed_x, min(max_speed_x, self.ball.speed_x))

                        # 5. Ensure the ball is moved out of the paddle to prevent "sticking"
                        # This is an approximation but is much safer
                        self.ball.rect.bottom = self.paddle.rect.top

                        # Create particles for ball-paddle collision
                        for _ in range(10):
                            self.particles.append(Particle(self.ball.rect.centerx, self.ball.rect.bottom, self.ball.color, random.randint(3, 6), 45, random.uniform(-3, 3), random.uniform(-1, -5)))

                    # Ball-brick collision
                    for brick in self.bricks[:]:
                        if self.ball.rect.colliderect(brick.rect):
                            self.ball.speed_y *= -1
                            # Create particles for ball-brick collision
                            for _ in range(7): # 7 particles
                                self.particles.append(Particle(self.ball.rect.centerx, self.ball.rect.centery, brick.color, random.randint(3, 6), 40))

                            self.bricks.remove(brick)
                            self.score += 10
                            if self.brick_hit_sound:
                                self.brick_hit_sound.play()
                            
                            # Item drop chance
                            if random.random() < 0.2: # 20% chance to drop an item
                                item_type = random.choice(['life', 'bullet'])
                                item_color = (0, 255, 0) if item_type == 'life' else (0, 0, 255) # Green for life, Blue for bullet
                                self.items.append(Item(brick.rect.centerx, brick.rect.centery, item_type, item_color))
                            break

                    # Ball-wall collision (particles for top/left/right walls)
                    if self.ball.rect.left < self.border_size:
                        for _ in range(5): self.particles.append(Particle(self.ball.rect.left, self.ball.rect.centery, self.ball.color, random.randint(2, 4), 20, x_vel=random.uniform(1, 3), y_vel=random.uniform(-2, 2)))
                    if self.ball.rect.right > self.screen_width - self.border_size:
                        for _ in range(5): self.particles.append(Particle(self.ball.rect.right, self.ball.rect.centery, self.ball.color, random.randint(2, 4), 20, x_vel=random.uniform(-3, -1), y_vel=random.uniform(-2, 2)))
                    if self.ball.rect.top < self.border_size:
                        for _ in range(5): self.particles.append(Particle(self.ball.rect.centerx, self.ball.rect.top, self.ball.color, random.randint(2, 4), 20, x_vel=random.uniform(-2, 2), y_vel=random.uniform(1, 3)))

                    # Level completion check
                    if not self.bricks:
                        self.level += 1
                        self.ball.speed_x *= 1.1
                        self.ball.speed_y *= 1.1
                        self.create_bricks()
                        self.reset_game_state()

                    # Ball goes out of bounds (bottom)
                    if self.ball.rect.bottom > self.screen_height - self.border_size:
                        self.bottom_border_red_timer = 30 # Set timer for red border
                        self.ball_lost_flag = True # Set flag to indicate ball lost
                        # Create particles for ball lost animation
                        for _ in range(20): # 20 particles for a more significant effect
                            self.particles.append(Particle(self.ball.rect.centerx, self.ball.rect.bottom, self.ball.color, random.randint(5, 10), 60, random.uniform(-5, 5), random.uniform(-10, 0)))

                # Update particles (always update when playing)
                for particle in self.particles[:]:
                    particle.update()
                    if particle.current_lifetime <= 0:
                        self.particles.remove(particle)

                # Handle ball lost delay and reset
                if self.ball_lost_flag and self.bottom_border_red_timer <= 0:
                    self.lives -= 1
                    if self.lives == 0:
                        self.game_over = True
                        self.game_state = "game_over"
                    else:
                        self.reset_game_state()
                    self.ball_lost_flag = False

            # Decrement bottom border red timer
            if self.bottom_border_red_timer > 0:
                self.bottom_border_red_timer -= 1

            # Drawing
            self.draw()

            pygame.display.flip()
            self.clock.tick(60) # Cap the frame rate at 60 FPS

        pygame.quit()

    def draw(self):
        # Draw gradient background
        for y in range(self.screen_height):
            r = self.gradient_start[0] + (self.gradient_end[0] - self.gradient_start[0]) * y / self.screen_height
            g = self.gradient_start[1] + (self.gradient_end[1] - self.gradient_start[1]) * y / self.screen_height
            b = self.gradient_start[2] + (self.gradient_end[2] - self.gradient_start[2]) * y / self.screen_height
            pygame.draw.line(self.screen, (r, g, b), (0, y), (self.screen_width, y))

        # Draw white borders
        pygame.draw.rect(self.screen, self.white, (0, 0, self.screen_width, self.border_size))  # Top border
        # Conditional drawing for bottom border
        bottom_border_color = self.red if self.bottom_border_red_timer > 0 else self.white
        pygame.draw.rect(self.screen, bottom_border_color, (0, self.screen_height - self.border_size, self.screen_width, self.border_size))  # Bottom border
        pygame.draw.rect(self.screen, self.white, (0, 0, self.border_size, self.screen_height))  # Left border
        pygame.draw.rect(self.screen, self.white, (self.screen_width - self.border_size, 0, self.border_size, self.screen_height))  # Right border

        if self.game_state == "playing":
            self.paddle.draw(self.screen)

            for brick in self.bricks:
                brick.draw(self.screen)

            for item in self.items:
                item.draw(self.screen)

            for bullet in self.bullets:
                bullet.draw(self.screen)

            for particle in self.particles:
                particle.draw(self.screen)

            # Display score and bullets on one line, slightly transparent
            info_text = self.font.render(f"Score: {self.score}   Bullets: {self.bullet_count}", True, (200, 200, 200)) # Desaturated white for transparency effect
            self.screen.blit(info_text, (self.border_size + 5, self.border_size + 5))

            # Display lives as a gauge (adjusted position)
            for i in range(self.lives):
                life_rect = pygame.Rect(self.screen_width - self.border_size - (i + 1) * 25, self.border_size + 5, 20, 20)
                color = (255, 150, 150) # Light Red (consistent color)
                pygame.draw.rect(self.screen, color, life_rect)

            # Display level (adjusted position)
            level_text = self.font.render(f"Level: {self.level}", True, self.white)
            level_rect = level_text.get_rect(center=(self.screen_width // 2, self.border_size + 15))
            self.screen.blit(level_text, level_rect)

            # Draw the virtual keyboard
            self.keyboard.draw(self.screen)

            # Draw the ball after all other elements in playing state
            self.ball.draw(self.screen)

        if self.game_state == "start":
            start_text = self.font.render("Press SPACE to Start", True, self.white)
            start_rect = start_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
            self.screen.blit(start_text, start_rect)
        elif self.game_state == "game_over":
            game_over_text = self.font.render("Game Over", True, self.white)
            game_over_rect = game_over_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
            self.screen.blit(game_over_text, game_over_rect)