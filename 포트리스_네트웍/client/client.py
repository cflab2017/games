
import pygame
import socket
import json
import threading
import math
import time

# --- 설정 ---
# SERVER_HOST = '127.0.0.1'
SERVER_PORT = 9994
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 900
FPS = 60
MAX_POWER = 875
LAVA_LEVEL = SCREEN_HEIGHT-10

# --- 색상 ---
WHITE = (255, 255, 255); BLACK = (0, 0, 0); RED = (255, 0, 0); GREEN = (0, 255, 0)
YELLOW = (255, 255, 0); SKY_BLUE = (135, 206, 235); BROWN = (139, 69, 19)
GREY = (200, 200, 200); DARK_GREY = (100, 100, 100); DARK_BROWN = (101, 67, 33)

class InputBox:
    def __init__(self, x, y, w, h, text='', max_length=10):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = DARK_GREY
        self.text = text
        self.font = pygame.font.Font(None, 32)
        self.txt_surface = self.font.render(text, True, self.color)
        self.active = False
        self.max_length = max_length

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            self.color = WHITE if self.active else DARK_GREY
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    return self.text
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if len(self.text) < self.max_length:
                        self.text += event.unicode
                self.txt_surface = self.font.render(self.text, True, WHITE)
        return None

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 2)
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))

class GameClient:
    def __init__(self):
        pygame.init()
        pygame.mixer.init() # NEW: Mixer 초기화
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Turn-based Artillery Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        self.big_font = pygame.font.Font(None, 48)
        self.huge_font = pygame.font.Font(None, 96)

        self.sock = None
        self.is_connected = False
        self.screen_state = 'login'
        self.my_id = ""
        self.room_list = []
        self.game_state = None
        self.terrain_heights = None

        self.login_input = InputBox(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, 200, 40, max_length=10)
        self.room_input = InputBox(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 230, 200, 40, max_length=10)
        self.return_to_lobby_button = pygame.Rect(SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 50, 240, 50)
        self.lobby_error_message = "" # 로비 화면 오류 메시지
        self.explosions = []
        self.hp_gain_effects = []

        self.angle = 90
        self.power = 0
        self.is_charging = False
        self.last_move_dir = 0
        
        self.lobby_listRooms_ret = None

        # 사운드 로드
        self.fire_sound = None
        self.explosion_sound = None
        try:
            self.fire_sound = pygame.mixer.Sound("./sound/fire_sound.wav")
        except pygame.error:
            print("[WARNING] fire_sound.wav 파일을 찾을 수 없거나 로드할 수 없습니다.")
        try:
            self.explosion_sound = pygame.mixer.Sound("./sound/explosion_sound.wav")
        except pygame.error:
            print("[WARNING] explosion_sound.wav 파일을 찾을 수 없거나 로드할 수 없습니다.")

    def connect(self,HOST):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((HOST, SERVER_PORT))
            self.is_connected = True
            threading.Thread(target=self.receive_messages, daemon=True).start()
            print(f"[INFO] 서버({HOST}:{SERVER_PORT})에 연결되었습니다.")
            return True
        except ConnectionRefusedError:
            print("[ERROR] 서버에 연결할 수 없습니다. 서버가 실행 중인지 확인하세요.")
            return False

    def send_message(self, message):
        if self.is_connected:
            try: self.sock.sendall((json.dumps(message) + '\n').encode('utf-8'))
            except (ConnectionResetError, BrokenPipeError): self.is_connected = False

    def receive_messages(self):
        buffer = ""
        while self.is_connected:
            try:
                data = self.sock.recv(8192).decode('utf-8')
                if not data: break
                buffer += data
                while '\n' in buffer:
                    line, buffer = buffer.split('\n', 1)
                    if line: self.process_server_message(json.loads(line))
            except Exception as e:
                print(f"[ERROR] 메시지 수신 중 오류 발생: {e}")
                break
        self.is_connected = False
        print("[INFO] 서버와의 연결이 끊어졌습니다.")

    def process_server_message(self, msg):
        msg_type = msg.get("type")
        if msg_type == "login_ok":
            self.my_id = msg["id"]
            self.screen_state = 'lobby'
            self.send_message({"type": "list_rooms"})
            self.lobby_error_message = "" # Clear error message on successful login
            print(f"[INFO] 로그인 성공: {self.my_id}")
        elif msg_type == "login_fail": # NEW
            self.lobby_error_message = msg.get("reason", "로그인 실패")
            print(f"[ERROR] 로그인 실패: {self.lobby_error_message}")
        elif msg_type == "room_list":
            self.room_list = msg.get("rooms", [])
            self.lobby_error_message = "" # 방 목록 갱신 시 오류 메시지 초기화
            print(f"[INFO] 방 목록 수신: {self.room_list}")
        elif msg_type == "create_fail":
            self.lobby_error_message = msg.get("reason", "방 생성 실패")
        elif msg_type == "join_ok":
            self.terrain_heights = msg.get("terrain_heights")
            self.screen_state = 'in_game'
        elif msg_type == "room_state":
            self.game_state = msg.get("state")
        elif msg_type == "event" and msg.get("event") == "explosion":
            if "terrain_update" in msg:
                self.terrain_heights = msg["terrain_update"]
            if self.explosion_sound: # NEW: 폭발 사운드 재생
                self.explosion_sound.play()
            self.explosions.append({
                "x": msg["x"],
                "y": msg["y"],
                "max_radius": msg["radius"],
                "start_time": time.time()
            })
        elif msg_type == "hp_gain_effect":
            player_id = msg.get("player_id")
            player = self.game_state.get("players", {}).get(player_id)
            if player:
                self.hp_gain_effects.append({
                    "text": f"+{msg.get('amount', 0)}",
                    "pos": (player['x'], player['y']),
                    "start_time": time.time()
                })


    def get_host_ip(self):        
        with open("host.txt", "r") as f:
            lines = f.readlines()
            for line in lines:
                line = line.replace('\n','')
                line = line.replace(' ','')
                if line.find('#')>=0:
                    continue
                if len(line.split('.')) != 4:
                    print(line)
                    continue
                print(line)
                return line
            
    def run(self, host = None):
        if host is None:
            HOST = self.get_host_ip()
        else:
            HOST = host
            
        if not self.connect(HOST):
            print("[ERROR] 서버 연결 실패. 서버를 먼저 실행하세요.")
            return

        print("[INFO] 클라이언트 메인 루프 시작.")
        while self.is_connected:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT: self.is_connected = False
            
            if self.screen_state == 'login':
                self.handle_login_screen(events)
                self.draw_login_screen()
            elif self.screen_state == 'lobby':
                self.handle_lobby_screen(events)
                self.draw_lobby_screen()
            elif self.screen_state == 'in_game':
                if self.game_state and self.game_state.get("phase") == "game_over":
                    self.handle_game_over_screen(events)
                else:
                    self.handle_game_input(events)
                self.draw_game_screen()

            pygame.display.flip()
            self.clock.tick(FPS)
        
        self.sock.close()
        pygame.quit()

    def handle_login_screen(self, events):
        for event in events:
            player_id = self.login_input.handle_event(event)
            if player_id:
                self.send_message({"type": "login", "player_id": player_id})

    def draw_login_screen(self):
        self.screen.fill(SKY_BLUE)
        title = self.big_font.render("Login", True, WHITE)
        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 150))
        self.login_input.draw(self.screen)

    def handle_lobby_screen(self, events):
        for event in events:
            room_name = self.room_input.handle_event(event)
            # print(room_name)
            if room_name:
                self.send_message({"type": "create_room", "room_name": room_name})
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, name in enumerate(self.room_list):
                    if pygame.Rect(SCREEN_WIDTH // 2 - 100, 150 + i * 40, 200, 30).collidepoint(event.pos):
                        self.send_message({"type": "join_room", "room_name": name}); break
                if self.lobby_listRooms_ret.collidepoint(event.pos):
                    self.send_message({"type": "list_rooms"})

    def draw_lobby_screen(self):
        self.screen.fill(SKY_BLUE)
        title = self.big_font.render("Game Lobby", True, WHITE)
        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))
        for i, name in enumerate(self.room_list):
            rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, 150 + i * 40, 200, 30)
            pygame.draw.rect(self.screen, DARK_GREY, rect)
            self.screen.blit(self.font.render(name, True, WHITE), (rect.x + 10, rect.y + 5))
        
        create_room_text = self.font.render("Create New Room:", True, WHITE)
        self.screen.blit(create_room_text, (SCREEN_WIDTH // 2 - create_room_text.get_width() // 2, SCREEN_HEIGHT - 260))
        self.room_input.draw(self.screen)
        if self.lobby_error_message:
            error_text = self.font.render(self.lobby_error_message, True, RED)
            self.screen.blit(error_text, (SCREEN_WIDTH // 2 - error_text.get_width() // 2, SCREEN_HEIGHT - 180))
        
        img = self.big_font.render("List Rooms", True, BLACK)
        img_ret = img.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))
        self.screen.blit(img, img_ret)
        
        self.lobby_listRooms_ret = img_ret.inflate(10, 10)
        pygame.draw.rect(self.screen, GREEN, self.lobby_listRooms_ret, 1)

    def handle_game_over_screen(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.return_to_lobby_button.collidepoint(event.pos):
                    self.send_message({"type": "leave_room"})
                    self.screen_state = 'lobby'
                    self.game_state = None
                    self.room_list = []
                    self.send_message({"type": "list_rooms"})

    def handle_game_input(self, events):
        is_my_turn = self.game_state and self.game_state.get("current_turn") == self.my_id and self.game_state.get("phase") == "playing"
        if not is_my_turn:
            self.is_charging = False
            self.last_move_dir = 0
            return

        for event in events:
            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                if self.is_charging:
                    self.send_message({"type": "fire", "angle": self.angle, "power": self.power})
                    self.power = 0
                    self.is_charging = False
                    if self.fire_sound: # NEW: 발사 사운드 재생
                        self.fire_sound.play()

        keys = pygame.key.get_pressed()
        move_dir = 0
        if keys[pygame.K_LEFT]: move_dir = -1
        elif keys[pygame.K_RIGHT]: move_dir = 1
        
        if move_dir != 0 or self.last_move_dir != 0:
            self.send_message({"type": "input", "move": move_dir})
        
        self.last_move_dir = move_dir

        angle_changed = False
        if keys[pygame.K_w] or keys[pygame.K_UP]: self.angle = min(180, self.angle + 1); angle_changed = True
        if keys[pygame.K_q] or keys[pygame.K_DOWN]: self.angle = max(0, self.angle - 1); angle_changed = True
        if angle_changed: self.send_message({"type": "aim", "angle": self.angle})

        if keys[pygame.K_SPACE]:
            self.is_charging = True
            self.power = min(MAX_POWER, self.power + (MAX_POWER / FPS / 1.5))
        else:
            self.is_charging = False

    def draw_game_ui(self):
        turn_text = f"Current Turn: {self.game_state.get('current_turn', '')}"
        self.screen.blit(self.big_font.render(turn_text, True, WHITE), (10, 10))

        # Draw timer
        if "turn_remaining_time" in self.game_state and self.game_state["phase"] == "playing":
            remaining = int(self.game_state["turn_remaining_time"])
            if remaining >= 0:
                color = RED if remaining <= 5 else WHITE
                timer_text = self.huge_font.render(str(remaining), True, color)
                self.screen.blit(timer_text, (SCREEN_WIDTH // 2 - timer_text.get_width() // 2, 200))

        if self.game_state.get("current_turn") == self.my_id:
            your_turn_text = self.big_font.render("YOUR TURN", True, YELLOW)
            self.screen.blit(your_turn_text, (SCREEN_WIDTH // 2 - your_turn_text.get_width() // 2, 10))
            me = self.game_state["players"].get(self.my_id)
            if me: self.screen.blit(self.font.render(f"Move Left: {int(me['move_left'])}", True, WHITE), (10, 60))
        
        # Display all player HPs on the left side
        players = sorted(list(self.game_state.get("players", {}).values()), key=lambda p: p.get("team", 0))
        hp_display_y = 90 # Start below other UI elements
        for player in players:
            hp_text = f"{player['id']}: {player['hp']} HP"
            rendered_text = self.font.render(hp_text, True, WHITE)
            text_rect = rendered_text.get_rect(topleft=(10, hp_display_y))
            self.screen.blit(rendered_text, text_rect)
            hp_display_y += 25

        if self.is_charging:
            pygame.draw.rect(self.screen, BLACK, (SCREEN_WIDTH // 2 - 152, SCREEN_HEIGHT - 50, 304, 24), 2)
            pygame.draw.rect(self.screen, YELLOW, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT - 48, 300 * (self.power / MAX_POWER), 20))

        self.draw_keyboard_status()

    def draw_keyboard_status(self):
        keys = pygame.key.get_pressed()
        
        base_x = SCREEN_WIDTH - 180
        base_y = 20

        key_rects = {
            "UP": pygame.Rect(base_x + 60, base_y, 50, 30),
            "LEFT": pygame.Rect(base_x, base_y + 40, 50, 30),
            "DOWN": pygame.Rect(base_x + 60, base_y + 40, 50, 30),
            "RIGHT": pygame.Rect(base_x + 120, base_y + 40, 50, 30),
            "SPACE": pygame.Rect(base_x, base_y + 80, 170, 30)
        }

        key_states = {
            "UP": keys[pygame.K_UP] or keys[pygame.K_w],
            "DOWN": keys[pygame.K_DOWN] or keys[pygame.K_q],
            "LEFT": keys[pygame.K_LEFT],
            "RIGHT": keys[pygame.K_RIGHT],
            "SPACE": keys[pygame.K_SPACE]
        }

        for key_name, rect in key_rects.items():
            color = YELLOW if key_states[key_name] else GREY
            
            key_surface = pygame.Surface(rect.size, pygame.SRCALPHA)
            key_surface.fill((*color, 128)) # 50% opaque
            self.screen.blit(key_surface, rect.topleft)

            pygame.draw.rect(self.screen, BLACK, rect, 1) # Border

            if key_name == "SPACE":
                text = self.font.render(key_name, True, BLACK)
                text_rect = text.get_rect(center=rect.center)
                self.screen.blit(text, text_rect)
            else: # Draw arrow polygons
                cx, cy = rect.center
                if key_name == "UP":
                    points = [(cx, cy - 8), (cx - 8, cy + 4), (cx + 8, cy + 4)]
                elif key_name == "DOWN":
                    points = [(cx, cy + 8), (cx - 8, cy - 4), (cx + 8, cy - 4)]
                elif key_name == "LEFT":
                    points = [(cx - 8, cy), (cx + 4, cy - 8), (cx + 4, cy + 8)]
                elif key_name == "RIGHT":
                    points = [(cx + 8, cy), (cx - 4, cy - 8), (cx - 4, cy + 8)]
                
                pygame.draw.polygon(self.screen, BLACK, points)

    def draw_explosions(self):
        now = time.time()
        for explosion in self.explosions[:]:
            elapsed = now - explosion["start_time"]
            if elapsed > 0.5: # Animation duration
                self.explosions.remove(explosion)
                continue
            
            progress = elapsed / 0.5
            current_radius = int(explosion["max_radius"] * progress)
            
            if progress < 0.5:
                color = YELLOW
            else:
                color = RED
                
            alpha = int(255 * (1 - progress))
            
            surface = pygame.Surface((current_radius * 2, current_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(surface, (*color, alpha), (current_radius, current_radius), current_radius)
            self.screen.blit(surface, (explosion["x"] - current_radius, explosion["y"] - current_radius))

    def draw_minerals(self):
        minerals = self.game_state.get("minerals", [])
        for mineral in minerals:
            x, y = int(mineral["x"]), int(mineral["y"])
            # Draw a simple diamond shape
            points = [(x, y - 8), (x + 8, y), (x, y + 8), (x - 8, y)]
            pygame.draw.polygon(self.screen, (0, 255, 255), points) # Cyan color
            pygame.draw.polygon(self.screen, WHITE, points, 1)

    def draw_player(self, player):
        color = GREEN if player["id"] == self.my_id else RED
        pos = (int(player["x"]), int(player["y"]))
        pygame.draw.circle(self.screen, color, pos, 15)
        hp_percent = player["hp"] / 100
        pygame.draw.rect(self.screen, RED, (pos[0] - 20, pos[1] - 30, 40, 5))
        pygame.draw.rect(self.screen, GREEN, (pos[0] - 20, pos[1] - 30, 40 * hp_percent, 5))
        self.screen.blit(self.font.render(player["id"], True, BLACK), (pos[0] - self.font.render(player["id"], True, BLACK).get_width() // 2, pos[1] - 50))
        
        angle_to_draw = self.angle if player["id"] == self.my_id else player['angle']
        rad = math.radians(angle_to_draw if player['x'] < SCREEN_WIDTH // 2 else 180 - angle_to_draw)
        end_pos = (pos[0] + 25 * math.cos(rad), pos[1] - 25 * math.sin(rad))
        pygame.draw.line(self.screen, BLACK, pos, end_pos, 4)

    def draw_roulette_screen(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        title_text = self.big_font.render("Determining First Player...", True, WHITE)
        self.screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 200))

        players = list(self.game_state.get("players", {}).values())
        selected_player_id = self.game_state.get("roulette_selection")

        for i, player in enumerate(players):
            player_name = player["id"]
            is_selected = (player_name == selected_player_id)
            color = YELLOW if is_selected else WHITE
            text = self.big_font.render(player_name, True, color)
            
            x_pos = SCREEN_WIDTH // 2 - text.get_width() // 2
            y_pos = 300 + i * 60
            self.screen.blit(text, (x_pos, y_pos))

            if is_selected:
                # Draw a simple indicator
                pygame.draw.rect(self.screen, YELLOW, (x_pos - 20, y_pos, 10, text.get_height()), 0)
                pygame.draw.rect(self.screen, YELLOW, (x_pos + text.get_width() + 10, y_pos, 10, text.get_height()), 0)

    def draw_hp_gain_effects(self):
        now = time.time()
        for effect in self.hp_gain_effects[:]:
            elapsed = now - effect["start_time"]
            if elapsed > 1.0: # Effect lasts for 1 second
                self.hp_gain_effects.remove(effect)
                continue
            
            # Position floats up
            pos_x, pos_y = effect["pos"]
            pos_y -= elapsed * 30 # Move up

            # Alpha fades out
            alpha = 255 * (1 - elapsed)
            
            text_surface = self.big_font.render(effect["text"], True, GREEN)
            text_surface.set_alpha(alpha)
            
            text_rect = text_surface.get_rect(center=(int(pos_x), int(pos_y - 50))) # Start above player head
            self.screen.blit(text_surface, text_rect)

    def draw_game_screen(self):
        self.screen.fill(SKY_BLUE)
        if not self.game_state: return

        if self.terrain_heights:
            # Then draw terrain
            points = [(0, LAVA_LEVEL)] + [(x, self.terrain_heights[x]) for x in range(len(self.terrain_heights))] + [(SCREEN_WIDTH - 1, LAVA_LEVEL)]
            pygame.draw.polygon(self.screen, BROWN, points)

            # Paint the wall area
            wall_x_center = SCREEN_WIDTH // 2
            wall_width = 10
            wall_start_x = wall_x_center - wall_width // 2
            
            for i in range(wall_start_x, wall_start_x + wall_width):
                if i < len(self.terrain_heights):
                    pygame.draw.line(self.screen, DARK_BROWN, (i, self.terrain_heights[i]), (i, SCREEN_HEIGHT))

            pygame.draw.rect(self.screen, RED, (0, LAVA_LEVEL, SCREEN_WIDTH, SCREEN_HEIGHT - LAVA_LEVEL)) # NEW: 용암 그리기

        self.draw_minerals()
        for player in self.game_state.get("players", {}).values():
            if 'x' in player: # Only draw players that have been assigned a position
                self.draw_player(player)
        for proj in self.game_state.get("projectiles", {}).values(): pygame.draw.circle(self.screen, BLACK, (int(proj['x']), int(proj['y'])), 5)
        
        self.draw_explosions()
        self.draw_hp_gain_effects()
        self.draw_game_ui()

        if self.game_state.get("phase") == "roulette":
            self.draw_roulette_screen()

        if self.game_state.get("phase") == "game_over":
            winner = self.game_state.get("winner", "")
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            self.screen.blit(overlay, (0, 0))
            game_over_text = self.big_font.render("GAME OVER", True, RED)
            winner_text = self.big_font.render(f"Winner: {winner}", True, YELLOW)
            self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
            self.screen.blit(winner_text, (SCREEN_WIDTH // 2 - winner_text.get_width() // 2, SCREEN_HEIGHT // 2 + 10))
            pygame.draw.rect(self.screen, GREEN, self.return_to_lobby_button)
            self.screen.blit(self.big_font.render("Return to Lobby", True, BLACK), (self.return_to_lobby_button.x + 10, self.return_to_lobby_button.y + 10))

        pygame.draw.rect(self.screen, WHITE, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 4)

if __name__ == '__main__':
    GameClient().run()
