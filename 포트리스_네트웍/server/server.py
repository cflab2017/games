import asyncio
import json
import math
import time
import uuid

# --- 게임 상수 ---
HOST = '127.0.0.1'
PORT = 9994
TICK_RATE = 30
GRAVITY = 9.8 * 50
TURN_MOVE_DISTANCE = 100
MAP_WIDTH = 800
MAP_HEIGHT = 600
LAVA_LEVEL = 580

class GameRoom:
    def __init__(self, name, server):
        self.name = name
        self.server = server
        self.clients = {}
        self.game_state = {
            "phase": "waiting", "players": {},
            "projectiles": {},
            "current_turn": None, "winner": None
        }
        self.terrain_heights = self._create_terrain_heights()
        self.turn_order = []
        self.current_turn_index = 0
        self.physics_loop_task = None

    def _create_terrain_heights(self):
        heights = [0] * MAP_WIDTH
        for x in range(MAP_WIDTH):
            y1 = 50 * math.sin(x * 2 * math.pi / (MAP_WIDTH * 0.8))
            y2 = 25 * math.sin(x * 2 * math.pi / (MAP_WIDTH * 0.3))
            heights[x] = int(350 + y1 + y2)
        return heights

    async def broadcast(self, message):
        for writer in self.clients.keys():
            await self.server.send_message(writer, message)

    async def broadcast_room_state(self):
        await self.broadcast({"type": "room_state", "state": self.game_state})

    async def add_player(self, writer, player_id):
        if len(self.clients) >= 2: return
        self.clients[writer] = player_id
        spawn_x = 100 if len(self.clients) == 1 else 700
        spawn_y = self.terrain_heights[spawn_x] - 15
        self.game_state["players"][player_id] = {
            "id": player_id, "x": spawn_x, "y": spawn_y, "hp": 100,
            "vx": 0, "angle": 45 if spawn_x < 400 else 135,
            "move_left": TURN_MOVE_DISTANCE
        }
        await self.server.send_message(writer, {"type": "join_ok", "room_name": self.name, "terrain_heights": self.terrain_heights})
        await self.broadcast_room_state()
        if len(self.clients) == 2: await self.start_game()

    async def remove_player(self, writer):
        player_id = self.clients.pop(writer, None)
        if player_id and player_id in self.game_state["players"]:
            del self.game_state["players"][player_id]
            if not await self.check_for_winner(): # 플레이어 퇴장 후 승자 확인
                if not self.clients: # 방이 비었으면 게임 종료
                    self.game_state["phase"] = "game_over"
                    if self.physics_loop_task: self.physics_loop_task.cancel()
            await self.broadcast_room_state()
    async def start_game(self):
        self.turn_order = list(self.game_state["players"].keys())
        self.current_turn_index = 0
        self.game_state["phase"] = "playing"
        self.physics_loop_task = asyncio.create_task(self.physics_loop())
        await self.start_turn()

    async def start_turn(self):
        if self.game_state["phase"] != "playing" or not self.turn_order: return
        player_id = self.turn_order[self.current_turn_index]
        self.game_state["current_turn"] = player_id
        self.game_state["players"][player_id]["move_left"] = TURN_MOVE_DISTANCE
        await self.broadcast_room_state()

    async def next_turn(self):
        self.current_turn_index = (self.current_turn_index + 1) % len(self.turn_order)
        await self.start_turn()

    async def check_for_winner(self):
        alive_players = [p for p in self.game_state["players"].values() if p["hp"] > 0]
        if len(self.game_state["players"]) >= 2 and len(alive_players) <= 1:
            self.game_state["phase"] = "game_over"
            if alive_players:
                self.game_state["winner"] = alive_players[0]["id"]
            if self.physics_loop_task: self.physics_loop_task.cancel()
            await self.broadcast_room_state()
            return True
        return False

    async def physics_loop(self):
        while self.game_state["phase"] not in ["game_over", "waiting"]:
            try:
                state_changed = False

                # 1. 모든 플레이어의 y좌표를 지형에 맞게 항상 보정 (중력)
                for player in self.game_state["players"].values():
                    px = int(player["x"])
                    ground_y = self.terrain_heights[px]
                    expected_y = ground_y - 15
                    if abs(player["y"] - expected_y) > 1:
                        player["y"] = expected_y
                        state_changed = True
                    
                    # 용암 충돌 판정
                    if player["y"] + 15 >= LAVA_LEVEL:
                        player["hp"] = 0
                        state_changed = True

                # 2. 포탄 물리 계산 (포탄이 날아갈 때만)
                if self.game_state["phase"] == "projectile_flying":
                    proj_id, proj = next(iter(self.game_state["projectiles"].items()))
                    proj['vy'] += GRAVITY * (1 / TICK_RATE)
                    proj['x'] += proj['vx'] * (1 / TICK_RATE)
                    proj['y'] += proj['vy'] * (1 / TICK_RATE)

                    px, py = int(proj['x']), int(proj['y'])
                    collided = not (0 <= px < MAP_WIDTH and py < MAP_HEIGHT) or py >= self.terrain_heights[px]

                    if collided:
                        await self.handle_explosion(proj)
                        del self.game_state["projectiles"][proj_id]
                        self.game_state["phase"] = "playing"
                        if not await self.check_for_winner(): await self.next_turn()
                    state_changed = True # 포탄은 항상 움직이므로 상태 변경으로 간주
                
                # 3. 상태 변경이 있었으면 클라이언트에 알림
                if state_changed:
                    await self.broadcast_room_state()
                
                await asyncio.sleep(1 / TICK_RATE)
            except (asyncio.CancelledError, StopAsyncIteration):
                break

    async def handle_explosion(self, projectile):
        radius, ex, ey = 45, int(projectile["x"]), int(projectile["y"])
        for player in self.game_state["players"].values():
            if math.hypot(ex - player["x"], ey - player["y"]) < radius:
                player["hp"] = max(0, player["hp"] - int(50 * (1 - math.hypot(ex - player["x"], ey - player["y"]) / radius)))
        
        for i in range(max(0, ex - radius), min(MAP_WIDTH, ex + radius)):
            if abs(i - ex) < radius:
                depth = (radius**2 - (i - ex)**2)**0.5
                self.terrain_heights[i] = int(min(self.terrain_heights[i] + depth, LAVA_LEVEL))
        
        await self.broadcast({"type": "event", "event": "explosion", "x": ex, "y": ey, "radius": radius, "terrain_update": self.terrain_heights})

    async def handle_message(self, player_id, message):
        if self.game_state.get("current_turn") != player_id: return
        player = self.game_state["players"].get(player_id)
        if not player: return

        msg_type = message.get("type")
        if msg_type == "input":
            move = message.get("move", 0)
            dist = abs(move * (100 / TICK_RATE))
            if player["move_left"] > dist:
                player["x"] += move * (100 / TICK_RATE)
                player["x"] = max(15, min(MAP_WIDTH - 15, player["x"]))
                # y좌표 업데이트는 physics_loop로 이전됨
                player["move_left"] -= dist
        elif msg_type == "aim":
            player["angle"] = message.get("angle", 0)
        elif msg_type == "fire":
            angle = message.get("angle", player["angle"])
            rad = math.radians(angle if player['x'] < MAP_WIDTH / 2 else 180 - angle)
            self.game_state["projectiles"][f"p_{uuid.uuid4().hex[:4]}"] = {
                "owner_id": player_id, "x": player["x"], "y": player["y"] - 10,
                "vx": math.cos(rad) * message.get("power", 0), "vy": -math.sin(rad) * message.get("power", 0)
            }
            self.game_state["phase"] = "projectile_flying"
        
        await self.check_for_winner()
        await self.broadcast_room_state()

# --- 로비 서버 ---
class GameServer:
    def __init__(self): self.clients, self.players_in_room, self.rooms = {}, {}, {}
    async def start(self, host = None):
        if host is None:
            self.HOST = self.get_host_ip()
        else:
            self.HOST = host
        server = await asyncio.start_server(self.handle_client, self.HOST, PORT)
        print(f"[INFO] 로비 서버가 {HOST}:{PORT}에서 실행 중입니다...")
        await server.serve_forever()

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
            
    async def send_message(self, writer, message):
        try: writer.write((json.dumps(message) + '\n').encode()); await writer.drain()
        except ConnectionError: await self.remove_client(writer)
    async def remove_client(self, writer):
        if writer not in self.clients: return
        player_id = self.clients.pop(writer, None)
        if writer.can_write_eof(): writer.close()
        await writer.wait_closed()
        if not player_id: return
        room_name = self.players_in_room.pop(player_id, None)
        if room_name in self.rooms:
            await self.rooms[room_name].remove_player(writer)
            if not self.rooms[room_name].clients: del self.rooms[room_name]
    async def handle_client(self, reader, writer):
        player_id = None
        try:
            while True: # 클라이언트 연결 유지 및 메시지 처리 루프
                data = await reader.readline()
                if not data: break # 클라이언트 연결 종료

                message = json.loads(data.decode())

                if player_id is None: # 아직 로그인하지 않은 클라이언트
                    if message.get("type") == "login":
                        player_id = message.get("player_id", f"player_{uuid.uuid4().hex[:4]}")
                        self.clients[writer] = player_id
                        await self.send_message(writer, {"type": "login_ok", "id": player_id})
                        print(f"[INFO] {player_id} 로그인.")
                    else:
                        # 로그인하지 않은 클라이언트가 login 외의 메시지를 보낼 경우
                        await self.send_message(writer, {"type": "error", "message": "로그인 먼저 해주세요."})
                        # 선택적으로 연결을 끊을 수도 있음: break
                else: # 로그인한 클라이언트
                    await self.process_message(writer, player_id, message)

        except (asyncio.IncompleteReadError, ConnectionResetError): pass
        except Exception as e:
            print(f"[ERROR] {player_id or 'Unknown'} 처리 중 오류: {e}")
        finally:
            await self.remove_client(writer)
    async def process_message(self, writer, player_id, message):
        room_name = self.players_in_room.get(player_id)
        if room_name in self.rooms: await self.rooms[room_name].handle_message(player_id, message)
        else:
            msg_type = message.get("type")
            if msg_type == "list_rooms": await self.send_message(writer, {"type": "room_list", "rooms": list(self.rooms.keys())})
            elif msg_type == "create_room":
                room_name = message.get("room_name")
                if room_name and room_name not in self.rooms:
                    self.rooms[room_name] = GameRoom(room_name, self)
                    self.players_in_room[player_id] = room_name
                    await self.rooms[room_name].add_player(writer, player_id)
                else: await self.send_message(writer, {"type": "create_fail", "reason": "이미 존재하는 방 이름입니다."})
            elif msg_type == "join_room":
                room_name = message.get("room_name")
                if room_name in self.rooms:
                    self.players_in_room[player_id] = room_name
                    await self.rooms[room_name].add_player(writer, player_id)
                else: await self.send_message(writer, {"type": "join_fail", "reason": "존재하지 않는 방입니다."})
            elif msg_type == "leave_room": # 클라이언트가 로비에서 leave_room을 보낼 경우
                # 이 경우는 플레이어가 이미 방을 나갔거나 방에 없는 경우이므로 특별한 처리 불필요
                pass
if __name__ == "__main__":
    try: asyncio.run(GameServer().start())
    except KeyboardInterrupt: print("\n[INFO] 서버를 종료합니다.")