import asyncio
import json
import math
import time
import uuid
import random
from values import *

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
            heights[x] = int(700 + y1 + y2)

        # Add a wall in the middle
        wall_x = MAP_WIDTH // 2
        wall_width = 10
        wall_top_y = MAP_HEIGHT // 2
        for i in range(wall_x - wall_width // 2, wall_x + wall_width // 2):
            heights[i] = min(heights[i], wall_top_y)

        return heights

    async def broadcast(self, message):
        for writer in self.clients.keys():
            await self.server.send_message(writer, message)

    async def broadcast_room_state(self):
        await self.broadcast({"type": "room_state", "state": self.game_state})

    async def add_player(self, writer, player_id):
        
        # print(self.rooms)
        if len(self.clients) >= 2: return
        self.clients[writer] = player_id
        spawn_x = MAP_WIDTH // 8 if len(self.clients) == 1 else MAP_WIDTH * 7 // 8
        spawn_y = self.terrain_heights[spawn_x] - 15
        self.game_state["players"][player_id] = {
            "id": player_id, "x": spawn_x, "y": spawn_y, "hp": 100,
            "vx": 0, "angle": 45 if spawn_x < MAP_WIDTH / 2 else 135,
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
        random.shuffle(self.turn_order)
        self.game_state["phase"] = "roulette"
        self.game_state["roulette_selection"] = None
        await self.broadcast_room_state()
        asyncio.create_task(self.run_roulette())

    async def run_roulette(self):
        start_time = time.time()
        roulette_duration = 3
        player_ids = self.turn_order

        i = 0
        while time.time() - start_time < roulette_duration:
            self.game_state["roulette_selection"] = player_ids[i % len(player_ids)]
            await self.broadcast_room_state()
            await asyncio.sleep(0.1)
            i += 1

        # Final selection
        self.game_state["current_turn"] = self.turn_order[0]
        self.current_turn_index = 0
        del self.game_state["roulette_selection"]
        self.game_state["phase"] = "playing"
        self.physics_loop_task = asyncio.create_task(self.physics_loop())
        await self.start_turn()

    async def start_turn(self):
        if self.game_state["phase"] != "playing" or not self.turn_order: return
        player_id = self.turn_order[self.current_turn_index]
        self.game_state["current_turn"] = player_id
        self.game_state["players"][player_id]["move_left"] = TURN_MOVE_DISTANCE
        self.game_state["turn_start_time"] = time.time()
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
                
                # 3. 턴 타이머 계산
                if self.game_state["phase"] == "playing":
                    turn_start_time = self.game_state.get("turn_start_time", 0)
                    elapsed = time.time() - turn_start_time
                    remaining = TURN_DURATION - elapsed
                    self.game_state["turn_remaining_time"] = remaining
                    if remaining <= 0:
                        await self.next_turn()
                    state_changed = True

                # 4. 상태 변경이 있었으면 클라이언트에 알림
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
                original_x = player["x"]
                new_x = original_x + move * (100 / TICK_RATE)
                
                wall_x_center = MAP_WIDTH // 2
                wall_half_width = 5
                player_radius = 15
                
                left_boundary = wall_x_center - wall_half_width - player_radius
                right_boundary = wall_x_center + wall_half_width + player_radius

                # If player is on the left and tries to cross
                if original_x <= left_boundary and new_x > left_boundary:
                    new_x = left_boundary
                
                # If player is on the right and tries to cross
                elif original_x >= right_boundary and new_x < right_boundary:
                    new_x = right_boundary
                
                player["x"] = new_x
                player["x"] = max(player_radius, min(MAP_WIDTH - player_radius, player["x"]))
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