import pygame
import sys
import winsound # Import winsound
from network import Network
from constants import *
from snake import Snake
from food import Food
from effects import FloatingText

# --- Helper Functions for Drawing ---

def get_snake_direction(body_segments):
    if len(body_segments) < 2: return RIGHT
    head, neck = body_segments[0], body_segments[1]
    if head[0] > neck[0]: return RIGHT
    if head[0] < neck[0]: return LEFT
    if head[1] > neck[1]: return DOWN
    if head[1] < neck[1]: return UP
    return RIGHT

def draw_grid(surface):
    for y in range(UI_PANEL_HEIGHT, SCREEN_HEIGHT, GRID_SIZE):
        for x in range(0, SCREEN_WIDTH, GRID_SIZE):
            pygame.draw.rect(surface, (50, 50, 50), pygame.Rect(x, y, GRID_SIZE, GRID_SIZE), 1)

def draw_gauge(surface, x, y, w, h, color, val, max_val):
    if val < 0: val = 0
    if val > max_val: val = max_val
    fill_w = (val / max_val) * w if max_val > 0 else 0
    bg_rect = pygame.Rect(x, y, w, h)
    pygame.draw.rect(surface, (50, 50, 50), bg_rect)
    pygame.draw.rect(surface, color, pygame.Rect(x, y, fill_w, h))
    pygame.draw.rect(surface, WHITE, bg_rect, 2)

# --- UI Elements ---
class Button:
    def __init__(self, x, y, width, height, text, color, text_color=BLACK, font_size=30):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.font = pygame.font.Font(None, font_size)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.rect(surface, WHITE, self.rect, 2) # Border
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)

class TextInputBox:
    def __init__(self, x, y, width, height, font_size=30, initial_text=''):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (150, 150, 150)
        self.active_color = WHITE
        self.text_color = BLACK
        self.font = pygame.font.Font(None, font_size)
        self.text = initial_text
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            self.color = self.active_color if self.active else (150, 150, 150)
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.active = False
                self.color = (150, 150, 150)
                return True # Indicate Enter was pressed
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif len(self.text) < 10:
                self.text += event.unicode
        return False

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, 0)
        pygame.draw.rect(surface, WHITE, self.rect, 2) # Border
        text_surface = self.font.render(self.text, True, self.text_color)
        surface.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))
        self.rect.w = max(self.rect.width, text_surface.get_width() + 10)

# --- Main Drawing Function for the Game ---

def redraw_game_window(surface, my_id, game_state, floating_texts, flip_display=True):
    surface.fill((30, 30, 30))
    game_area = pygame.Rect(0, UI_PANEL_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT - UI_PANEL_HEIGHT)
    surface.fill(BLACK, game_area)
    draw_grid(surface)

    food_data = game_state.get("food")
    if food_data:
        temp_food = Food()
        temp_food.rect.topleft = (food_data[0], food_data[1])
        temp_food.color = food_data[2]
        temp_food.draw(surface)

    snakes_data = game_state.get("snakes", {})
    for p_id, snake_data in snakes_data.items():
        body_coords = snake_data["body"]
        color = snake_data["color"]
        temp_snake = Snake(0, 0, color)
        temp_snake.body = [pygame.Rect(x, y, GRID_SIZE, GRID_SIZE) for x, y in body_coords]
        temp_snake.direction = get_snake_direction(body_coords)
        temp_snake.draw(surface)

    for effect in floating_texts:
        effect.draw(surface)

    # --- Draw player scores and gauges ---
    font = pygame.font.Font(None, 28)
    small_font = pygame.font.Font(None, 22)
    WIN_LENGTH = 10
    GAUGE_WIDTH, GAUGE_HEIGHT = 120, 12
    
    player_box_width = 180
    
    sorted_pids = sorted(snakes_data.keys())
    
    for i, p_id in enumerate(sorted_pids):
        snake_data = snakes_data[p_id]
        score = len(snake_data.get("body", []))
        player_name = snake_data.get("name", f"P{p_id}")
        
        start_x = 10 + i * player_box_width
        if start_x + player_box_width > SCREEN_WIDTH: break # Don't draw off-screen

        # Highlight the current player
        text_color = YELLOW if p_id == my_id else WHITE

        # Draw name and score
        name_text = small_font.render(player_name, True, text_color)
        surface.blit(name_text, (start_x, 10))
        
        score_text = font.render(f"Score: {score}", True, text_color)
        surface.blit(score_text, (start_x, 28))
        
        # Draw gauge
        gauge_y = 48
        gauge_color = snake_data.get("color", BLUE)
        draw_gauge(surface, start_x, gauge_y, GAUGE_WIDTH, GAUGE_HEIGHT, gauge_color, score, WIN_LENGTH)

    if flip_display:
        pygame.display.flip()

# --- Main Application ---

def main(host = None):
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Snake Online")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 50)
    small_font = pygame.font.Font(None, 32)
    error_font = pygame.font.Font(None, 28)

    # --- State Management ---
    game_screen_state = "login"
    username = ""
    login_input_box = TextInputBox(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 25, 300, 50, initial_text="")
    create_room_input_box = TextInputBox(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 100, 300, 50, initial_text="")
    create_room_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 160, 200, 50, "Create Room", (0, 200, 0), WHITE)

    network = None
    my_id = -1
    my_name = ""
    game_state = {}
    floating_texts = []
    last_my_score = 0
    room_list = []
    room_list_timer = 0 
    winner_info = None
    back_to_lobby_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50, 200, 50, "Back to Lobby", (0, 150, 200), WHITE)
    
    # Error message states
    login_error_message = ""
    lobby_error_message = ""

    # Sound related
    last_my_head_pos = None
    move_command_sent_this_frame = False

    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            
            if game_screen_state == "login":
                if login_input_box.handle_event(event):
                    if len(login_input_box.text) > 0:
                        username = login_input_box.text
                        try:
                            if not network: # Establish connection if not already connected
                                network = Network(host)
                                player_data = network.get_player_id()
                                if not player_data:
                                    login_error_message = "Failed to connect to server."
                                    network = None
                                    continue
                                my_id = player_data.get("id")

                            response = network.send_and_receive({"action": "login", "name": username})
                            if response and response.get("status") == "logged_in":
                                my_name = response.get("name", username)
                                game_screen_state = "lobby"
                                login_error_message = ""
                                print(f"Logged in as {my_name} (ID: {my_id})")
                            else:
                                login_error_message = response.get("message", "Unknown login error.")
                                print(f'Login failed: {login_error_message}')
                        except Exception as e:
                            login_error_message = "Network error during login."
                            print(f"Network error during login: {e}")
                            network = None

            elif game_screen_state == "lobby":
                create_room_input_box.handle_event(event)
                if create_room_button.is_clicked(event):
                    if len(create_room_input_box.text) > 0:
                        try:
                            response = network.send_and_receive({"action": "create_room", "room_name": create_room_input_box.text})
                            if response and response.get("status") == "joined_room":
                                game_screen_state = "game"
                                lobby_error_message = ""
                                print(f'Joined room: {response.get("room_name")}')
                                last_my_score = 0
                                floating_texts = []
                            else:
                                lobby_error_message = response.get("message", "Unknown create room error.")
                                print(f'Create room failed: {lobby_error_message}')
                        except Exception as e:
                            lobby_error_message = "Network error during room creation."
                            print(f"Network error during room creation: {e}")

                # Handle joining existing rooms
                room_y = 150
                for room_data in room_list:
                    join_button = Button(SCREEN_WIDTH - 120, room_y, 100, 30, "Join", (0, 150, 0), WHITE, font_size=20)
                    if join_button.is_clicked(event):
                        try:
                            response = network.send_and_receive({"action": "join_room", "room_id": room_data["id"]})
                            if response and response.get("status") == "joined_room":
                                game_screen_state = "game"
                                lobby_error_message = ""
                                print(f'Joined room: {response.get("room_name")}')
                                last_my_score = 0
                                floating_texts = []
                            else:
                                lobby_error_message = response.get('message', 'Unknown join room error.')
                                print(f"Join room failed: {lobby_error_message}")
                        except Exception as e:
                            lobby_error_message = "Network error during room join."
                            print(f"Network error during room join: {e}")
                        break  # Only process one join click per event
                    room_y += 40

            elif game_screen_state == "game_over":
                if back_to_lobby_button.is_clicked(event):
                    print("[CLIENT] 'Back to Lobby' button clicked.")
                    game_screen_state = "lobby"
                    print("[CLIENT] State changed to 'lobby'. Next loop will be in lobby screen.")
                    winner_info = None
                    game_state = {}
                    room_list_timer = 1001 # Force room list update in lobby

        # --- Screen-specific Logic and Drawing ---
        if game_screen_state == "login":
            screen.fill(BLACK)
            title_text = font.render("Enter Your Name", True, WHITE)
            screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 200))
            login_input_box.draw(screen)
            
            if login_error_message:
                error_text = error_font.render(login_error_message, True, (255, 80, 80))
                screen.blit(error_text, (SCREEN_WIDTH // 2 - error_text.get_width() // 2, 290))

            pygame.display.flip()

        elif game_screen_state == "lobby":
            if room_list_timer > 1000: # To avoid printing every frame
                print("[CLIENT] Entered lobby screen logic.")

            screen.fill(BLACK)
            lobby_title = font.render(f"Welcome, {my_name}!", True, WHITE)
            screen.blit(lobby_title, (SCREEN_WIDTH // 2 - lobby_title.get_width() // 2, 50))

            room_list_timer += clock.get_time()
            if room_list_timer > 1000: # Every 1 second
                try:
                    print("[CLIENT] In lobby, about to request room list...")
                    response = network.send_and_receive({"action": "get_rooms"})
                    print("[CLIENT] In lobby, received response for room list.")

                    if response and response.get("status") == "room_list":
                        room_list = response.get("rooms", [])
                        print(f"[CLIENT] Successfully updated room list: {len(room_list)} rooms.")
                    elif response:
                        print(f"[CLIENT] Failed to get room list: {response.get('message', 'Unknown error')}")
                    else:
                        print("[CLIENT] Failed to get room list: No response from server. Disconnecting.")
                        running = False
                        break
                except Exception as e:
                    print(f"[CLIENT] Network error getting room list: {e}")
                    running = False
                    break
                room_list_timer = 0

            room_y = 150
            if room_list:
                for room_data in room_list:
                    room_info = small_font.render(f"[{room_data['players']}/10] {room_data['name']}", True, WHITE)
                    screen.blit(room_info, (50, room_y))
                    join_button = Button(SCREEN_WIDTH - 120, room_y, 100, 30, "Join", (0, 150, 0), WHITE, font_size=20)
                    join_button.draw(screen)
                    room_y += 40
            else:
                no_rooms_text = small_font.render("No rooms available. Create one!", True, WHITE)
                screen.blit(no_rooms_text, (50, room_y))

            create_room_input_box.draw(screen)
            create_room_button.draw(screen)

            if lobby_error_message:
                error_text = error_font.render(lobby_error_message, True, (255, 80, 80))
                screen.blit(error_text, (SCREEN_WIDTH // 2 - error_text.get_width() // 2, SCREEN_HEIGHT // 2 + 225))

            pygame.display.flip()

        elif game_screen_state == "game":
            # On the first frame after joining, game_state is empty. Get the first state before proceeding.
            if not game_state:
                game_state = network.receive()
                if not game_state:
                    print("[CLIENT] Failed to receive initial game state.")
                    running = False
                    break
                continue

            # Reset flag for sound
            move_command_sent_this_frame = False

            # 1. Send player input to server (if any)
            command = None
            # Only process movement if the server says the game is running
            server_game_state = game_state.get("game_state")
            if server_game_state == "running":
                for event in events:
                    if event.type == pygame.KEYDOWN:
                        if event.key in (pygame.K_a, pygame.K_LEFT): command = {"action": "move", "direction": "left"}
                        elif event.key in (pygame.K_d, pygame.K_RIGHT): command = {"action": "move", "direction": "right"}
                        elif event.key in (pygame.K_w, pygame.K_UP): command = {"action": "move", "direction": "up"}
                        elif event.key in (pygame.K_s, pygame.K_DOWN): command = {"action": "move", "direction": "down"}
                
                if command:
                    network.send_only(command)
                    winsound.PlaySound("SystemAsterisk", winsound.SND_ASYNC) # Play move sound
                    move_command_sent_this_frame = True

            # 2. Receive game state from server (blocking)
            game_state = network.receive()
            if not game_state: 
                print("[CLIENT] Lost connection to server during game.")
                running = False; 
                break

            # --- Check for Winner ---
            winner_info = game_state.get("winner")
            if winner_info:
                print(f"[CLIENT] Winner found: {winner_info.get('name')}. Entering game_over state.")
                game_screen_state = "game_over"
                redraw_game_window(screen, my_id, game_state, floating_texts)
                continue

            # --- Update and Draw based on Server State ---
            server_game_state = game_state.get("game_state")
            
            # Detect collision/reset sound
            current_my_snake_data = game_state.get("snakes", {}).get(my_id)
            if current_my_snake_data:
                current_my_head_pos = current_my_snake_data["body"][0]
                if last_my_head_pos and current_my_head_pos != last_my_head_pos and not move_command_sent_this_frame:
                    winsound.PlaySound("SystemExclamation", winsound.SND_ASYNC) # Play collision sound
                last_my_head_pos = current_my_head_pos
            else:
                last_my_head_pos = None # My snake is gone

            # Always draw the basic background and player scores
            redraw_game_window(screen, my_id, game_state, floating_texts, flip_display=False)

            if server_game_state == "waiting":
                wait_text = font.render("Waiting for more players...", True, WHITE)
                screen.blit(wait_text, (SCREEN_WIDTH // 2 - wait_text.get_width() // 2, SCREEN_HEIGHT // 2 - wait_text.get_height() // 2))
            
            elif server_game_state == "countdown":
                countdown_val = game_state.get("countdown", 3)
                countdown_font = pygame.font.Font(None, 150)
                countdown_text = countdown_font.render(str(countdown_val), True, WHITE)
                screen.blit(countdown_text, (SCREEN_WIDTH // 2 - countdown_text.get_width() // 2, SCREEN_HEIGHT // 2 - countdown_text.get_height() // 2))

            pygame.display.flip()

            # Update local effects
            if current_my_snake_data:
                current_my_score = len(current_my_snake_data["body"])
                if current_my_score > last_my_score:
                    score_diff = current_my_score - last_my_score
                    my_head = current_my_snake_data["body"][0]
                    floating_texts.append(FloatingText(my_head[0], my_head[1], f"+{score_diff}", WHITE))
                last_my_score = current_my_score
            else:
                last_my_score = 0 # My snake is gone
            
            for effect in floating_texts: effect.update()
            floating_texts = [e for e in floating_texts if e.lifespan > 0]

        elif game_screen_state == "game_over":
            # Keep drawing the last game state in the background
            redraw_game_window(screen, my_id, game_state, floating_texts, flip_display=False)

            # Overlay with winner message
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180)) # Semi-transparent black overlay
            screen.blit(overlay, (0, 0))

            if winner_info:
                winner_name = winner_info.get("name", f"Player {winner_info.get('id')}")
                win_text = font.render(f"{winner_name} Wins!", True, YELLOW)
                screen.blit(win_text, (SCREEN_WIDTH // 2 - win_text.get_width() // 2, 200))
            
            back_to_lobby_button.draw(screen)
            pygame.display.flip()

        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()