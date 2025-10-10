
import pygame
import socket
import json
import threading
import math

# --- 설정 ---
# SERVER_HOST = '127.0.0.1'
SERVER_PORT = 9994
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60
MAX_POWER = 700
LAVA_LEVEL = 580

# --- 색상 ---
WHITE = (255, 255, 255); BLACK = (0, 0, 0); RED = (255, 0, 0); GREEN = (0, 255, 0)
YELLOW = (255, 255, 0); SKY_BLUE = (135, 206, 235); BROWN = (139, 69, 19)
GREY = (200, 200, 200); DARK_GREY = (100, 100, 100)

class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = DARK_GREY
        self.text = text
        self.font = pygame.font.Font(None, 32)
        self.txt_surface = self.font.render(text, True, self.color)
        self.active = False

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

        self.sock = None
        self.is_connected = False
        self.screen_state = 'login'
        self.my_id = ""
        self.room_list = []
        self.game_state = None
        self.terrain_heights = None

        self.login_input = InputBox(300, 250, 200, 40)
        self.room_input = InputBox(300, 400, 200, 40)
        self.return_to_lobby_button = pygame.Rect(280, 400, 240, 50)
        self.lobby_error_message = "" # 로비 화면 오류 메시지

        self.angle = 90
        self.power = 0
        self.is_charging = False
        self.last_move_dir = 0

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
            print(f"[INFO] 로그인 성공: {self.my_id}")
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
        self.screen.blit(title, (340, 150))
        self.login_input.draw(self.screen)

    def handle_lobby_screen(self, events):
        for event in events:
            room_name = self.room_input.handle_event(event)
            if room_name:
                self.send_message({"type": "create_room", "room_name": room_name})
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, name in enumerate(self.room_list):
                    if pygame.Rect(300, 150 + i * 40, 200, 30).collidepoint(event.pos):
                        self.send_message({"type": "join_room", "room_name": name}); break

    def draw_lobby_screen(self):
        self.screen.fill(SKY_BLUE)
        self.screen.blit(self.big_font.render("Game Lobby", True, WHITE), (280, 50))
        for i, name in enumerate(self.room_list):
            rect = pygame.Rect(300, 150 + i * 40, 200, 30)
            pygame.draw.rect(self.screen, DARK_GREY, rect)
            self.screen.blit(self.font.render(name, True, WHITE), (310, 155 + i * 40))
        self.screen.blit(self.font.render("Create New Room:", True, WHITE), (320, 370))
        self.room_input.draw(self.screen)
        if self.lobby_error_message:
            error_text = self.font.render(self.lobby_error_message, True, RED)
            self.screen.blit(error_text, (300, 450))

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
        if move_dir != self.last_move_dir:
            self.send_message({"type": "input", "move": move_dir})
            self.last_move_dir = move_dir

        angle_changed = False
        if keys[pygame.K_w]: self.angle = min(180, self.angle + 1); angle_changed = True
        if keys[pygame.K_q]: self.angle = max(0, self.angle - 1); angle_changed = True
        if angle_changed: self.send_message({"type": "aim", "angle": self.angle})

        if keys[pygame.K_SPACE]:
            self.is_charging = True
            self.power = min(MAX_POWER, self.power + (MAX_POWER / FPS / 1.5))
        else:
            self.is_charging = False

    def draw_game_screen(self):
        self.screen.fill(SKY_BLUE)
        if not self.game_state: return

        if self.terrain_heights:
            points = [(0, SCREEN_HEIGHT)] + [(x, self.terrain_heights[x]) for x in range(len(self.terrain_heights))] + [(SCREEN_WIDTH - 1, SCREEN_HEIGHT)]
            pygame.draw.polygon(self.screen, BROWN, points)
            pygame.draw.rect(self.screen, RED, (0, LAVA_LEVEL, SCREEN_WIDTH, SCREEN_HEIGHT - LAVA_LEVEL)) # NEW: 용암 그리기

        for player in self.game_state.get("players", {}).values(): self.draw_player(player)
        for proj in self.game_state.get("projectiles", {}).values(): pygame.draw.circle(self.screen, BLACK, (int(proj['x']), int(proj['y'])), 5)
        
        self.draw_game_ui()

        if self.game_state.get("phase") == "game_over":
            winner = self.game_state.get("winner", "")
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            self.screen.blit(overlay, (0, 0))
            self.screen.blit(self.big_font.render("GAME OVER", True, RED), (280, 250))
            self.screen.blit(self.big_font.render(f"Winner: {winner}", True, YELLOW), (280, 310))
            pygame.draw.rect(self.screen, GREEN, self.return_to_lobby_button)
            self.screen.blit(self.big_font.render("Return to Lobby", True, BLACK), (self.return_to_lobby_button.x + 10, self.return_to_lobby_button.y + 10))

    def draw_player(self, player):
        color = GREEN if player["id"] == self.my_id else RED
        pos = (int(player["x"]), int(player["y"]))
        pygame.draw.circle(self.screen, color, pos, 15)
        hp_percent = player["hp"] / 100
        pygame.draw.rect(self.screen, RED, (pos[0] - 20, pos[1] - 30, 40, 5))
        pygame.draw.rect(self.screen, GREEN, (pos[0] - 20, pos[1] - 30, 40 * hp_percent, 5))
        self.screen.blit(self.font.render(player["id"], True, BLACK), (pos[0] - self.font.render(player["id"], True, BLACK).get_width() // 2, pos[1] - 50))
        
        angle_to_draw = self.angle if player["id"] == self.my_id else player['angle']
        rad = math.radians(angle_to_draw if player['x'] < 400 else 180 - angle_to_draw)
        end_pos = (pos[0] + 25 * math.cos(rad), pos[1] - 25 * math.sin(rad))
        pygame.draw.line(self.screen, BLACK, pos, end_pos, 4)

    def draw_game_ui(self):
        turn_text = f"Current Turn: {self.game_state.get('current_turn', '')}"
        self.screen.blit(self.big_font.render(turn_text, True, WHITE), (10, 10))
        if self.game_state.get("current_turn") == self.my_id:
            self.screen.blit(self.big_font.render("YOUR TURN", True, YELLOW), (280, 50))
            me = self.game_state["players"].get(self.my_id)
            if me: self.screen.blit(self.font.render(f"Move Left: {int(me['move_left'])}", True, WHITE), (10, 60))
        if self.is_charging:
            pygame.draw.rect(self.screen, BLACK, (248, 550, 304, 24), 2)
            pygame.draw.rect(self.screen, YELLOW, (250, 552, 300 * (self.power / MAX_POWER), 20))

if __name__ == '__main__':
    GameClient().run()
