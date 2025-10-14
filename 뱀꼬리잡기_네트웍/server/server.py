import socket
import threading
import pickle
import random
import time
import uuid
import struct

from constants import *
from snake import Snake
from food import Food

# --- Network Protocol Helpers ---
def send_msg(sock, msg):
    """Prefixes a message with a 4-byte length before sending."""
    msg = pickle.dumps(msg)
    msg = struct.pack('>I', len(msg)) + msg
    sock.sendall(msg)

def recv_msg(sock):
    """Reads a message with a 4-byte length prefix."""
    raw_msglen = recvall(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    return pickle.loads(recvall(sock, msglen))

def recvall(sock, n):
    """Helper function to recv n bytes or return None if EOF is hit."""
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data

# --- Server Configuration ---
# SERVER_HOST = '127.0.0.1'
SERVER_PORT = 9993
MAX_PLAYERS = 10

# --- Global Server State ---
clients = {}
rooms = {}
player_to_room = {}
player_names = {}
next_player_id = 0
state_lock = threading.Lock()

class Room:
    def __init__(self, name="New Room"):
        self.id = str(uuid.uuid4())
        self.name = name
        self.snakes = {}
        self.food = Food()
        self.clients = {}
        self.running = True
        self.game_loop_thread = threading.Thread(target=self.game_loop)
        self.game_loop_thread.daemon = True
        self.started_with_multiple_players = False
        
        # Game state management
        self.game_state = "waiting" # waiting, countdown, running
        self.countdown = 3
        self.last_countdown_time = 0

        self.game_loop_thread.start()
        print(f"[ROOM CREATED] Room '{self.name}' ({self.id}) created.")

    def stop(self):
        self.running = False

    def reset_all_snakes(self):
        print(f"[ROOM] Resetting all snakes in room '{self.name}'.")
        for snake in self.snakes.values():
            snake.reset(random.randint(0, GRID_WIDTH-1)*GRID_SIZE, random.randint(0, GRID_HEIGHT-1)*GRID_SIZE + UI_PANEL_HEIGHT, random.choice([UP, DOWN, LEFT, RIGHT]))

    def add_player(self, player_id, client_socket, player_name):
        print(f"[ROOM] Adding player {player_id} ({player_name}) to room '{self.name}'.")
        self.clients[player_id] = client_socket
        rand_x = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
        rand_y = random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE + UI_PANEL_HEIGHT
        rand_color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
        self.snakes[player_id] = Snake(rand_x, rand_y, rand_color)
        self.snakes[player_id].name = player_name
        
        if len(self.snakes) > 1:
            self.started_with_multiple_players = True

        # When a new player joins, always reset the game and start a countdown
        # This will pause an ongoing game and restart it.
        self.game_state = "countdown"
        self.countdown = 3
        self.last_countdown_time = time.time()
        self.reset_all_snakes()

    def remove_player(self, player_id, keep_client_connection=False):
        if not keep_client_connection:
            if player_id in self.clients: del self.clients[player_id]
        if player_id in self.snakes: del self.snakes[player_id]
        print(f"[ROOM] Player {player_id} removed from room '{self.name}'.")
        
        # If a player leaves during countdown or waiting, reset to waiting
        if len(self.snakes) < 2 and self.game_state != "running":
            self.game_state = "waiting"

        if not self.snakes:
            print(f"[ROOM DELETED] Room '{self.name}' ({self.id}) is empty. Deleting.")
            return True
        return False

    def handle_command(self, player_id, command):
        # Only allow movement if the game is running
        if self.game_state == "running" and player_id in self.snakes:
            snake = self.snakes[player_id]
            if command == "left": snake.change_direction(LEFT)
            elif command == "right": snake.change_direction(RIGHT)
            elif command == "up": snake.change_direction(UP)
            elif command == "down": snake.change_direction(DOWN)

    def game_loop(self):
        self.food.spawn([])
        while self.running:
            time.sleep(1 / 10)
            
            state_to_send = None
            sockets_to_send_to = []
            winner_found = False

            with state_lock:
                # --- Game State Machine ---
                if self.game_state == "waiting":
                    # If enough players join, the add_player function will trigger the countdown
                    pass # Do nothing, just wait

                elif self.game_state == "countdown":
                    if time.time() - self.last_countdown_time > 1:
                        self.countdown -= 1
                        self.last_countdown_time = time.time()
                    if self.countdown <= 0:
                        self.game_state = "running"
                        self.food.spawn(list(self.snakes.values())) # Spawn initial food

                elif self.game_state == "running":
                    # --- Start of protected game logic ---
                    for snake in self.snakes.values(): snake.move()

                    for p_id, snake in list(self.snakes.items()):
                        if snake.body[0].colliderect(self.food.rect):
                            snake.grow_by(self.food.value)
                            self.food.spawn(list(self.snakes.values()))
                            break
                    
                    all_snake_ids = list(self.snakes.keys())
                    for i in range(len(all_snake_ids)):
                        for j in range(len(all_snake_ids)):
                            p_id1, p_id2 = all_snake_ids[i], all_snake_ids[j]
                            if p_id1 not in self.snakes or p_id2 not in self.snakes: continue
                            snake1, snake2 = self.snakes[p_id1], self.snakes.get(p_id2)
                            if i == j: snake1.check_self_collision()
                            elif snake2:
                                if snake1.body[0].colliderect(snake2.body[0]):
                                    snake1.reset(random.randint(0, GRID_WIDTH-1)*GRID_SIZE, random.randint(0, GRID_HEIGHT-1)*GRID_SIZE + UI_PANEL_HEIGHT, random.choice([UP, DOWN, LEFT, RIGHT]))
                                    snake2.reset(random.randint(0, GRID_WIDTH-1)*GRID_SIZE, random.randint(0, GRID_HEIGHT-1)*GRID_SIZE + UI_PANEL_HEIGHT, random.choice([UP, DOWN, LEFT, RIGHT]))
                                else:
                                    for index, seg in enumerate(snake2.body[1:], 1):
                                        if snake1.body[0].colliderect(seg):
                                            snake1.grow_by(len(snake2.body) - index)
                                            snake2.truncate(index)
                                            break
                    
                    dead_snakes = [p_id for p_id, s in self.snakes.items() if not s.alive or len(s.body) <= 1]
                    for p_id in dead_snakes: 
                        if self.remove_player(p_id, keep_client_connection=True):
                            self.stop()

                # --- Data to Send (Common for all states) ---
                winner_info = None
                if self.game_state == "running": # Only check for winners if game is running
                    for p_id, snake in self.snakes.items():
                        if len(snake.body) >= WIN_LENGTH:
                            winner_info = {"id": p_id, "name": snake.name}
                            break
                    
                    if not winner_info and self.started_with_multiple_players and len(self.snakes) == 1:
                        winner_id = list(self.snakes.keys())[0]
                        winner_info = {"id": winner_id, "name": self.snakes[winner_id].name}

                    if not self.snakes and self.running:
                         if self.started_with_multiple_players:
                             winner_info = {"id": None, "name": "Draw!"}
                         else:
                             winner_info = {"id": None, "name": "Game Over"}
                
                serializable_snakes = {p_id: {"body": [(seg.x, seg.y) for seg in s.body], "color": s.color, "name": s.name} for p_id, s in self.snakes.items()}
                
                # Only show food if game is running
                serializable_food = None
                if self.game_state == "running":
                    serializable_food = (self.food.rect.x, self.food.rect.y, self.food.color)

                state_to_send = {
                    "snakes": serializable_snakes, 
                    "food": serializable_food, 
                    "room_name": self.name, 
                    "winner": winner_info,
                    "game_state": self.game_state,
                    "countdown": self.countdown
                }
                
                sockets_to_send_to = list(self.clients.values())

                if winner_info:
                    winner_found = True
                    self.stop()
                    print(f"[GAME OVER] Room '{self.name}' game ended. Winner: {winner_info.get('name')}. Cleaning up.")
                    player_ids_in_room = list(self.clients.keys())
                    for p_id in player_ids_in_room:
                        if p_id in player_to_room:
                            del player_to_room[p_id]
                    
                    if self.id in rooms:
                        del rooms[self.id]
                # --- End of protected game logic ---

            # --- Network sending is now OUTSIDE the lock ---
            if state_to_send and sockets_to_send_to:
                for client_socket in sockets_to_send_to:
                    try:
                        send_msg(client_socket, state_to_send)
                    except socket.error:
                        # Client likely disconnected, will be cleaned up by its own thread
                        pass


def handle_client_connection(client_socket, addr):
    global next_player_id, rooms, player_to_room, player_names
    
    with state_lock:
        next_player_id += 1
        player_id = next_player_id
        clients[player_id] = client_socket
        player_names[player_id] = f"Player{player_id}"

    print(f"[NEW CONNECTION] {addr} connected as Player {player_id}.")
    send_msg(client_socket, {"id": player_id, "name": player_names[player_id]})

    while True:
        try:
            data = recv_msg(client_socket)
            if not data:
                print(f"[INFO] Client {player_id} closed connection gracefully.")
                break

            with state_lock:
                action = data.get("action")
                
                if action == "login":
                    name_to_check = data.get("name", "")
                    if not (0 < len(name_to_check) <= 10):
                        send_msg(client_socket, {"status": "login_failed", "message": "Name must be 1-10 characters."})
                    elif name_to_check in player_names.values():
                        send_msg(client_socket, {"status": "login_failed", "message": "Name already taken."})
                    else:
                        player_names[player_id] = name_to_check
                        send_msg(client_socket, {"status": "logged_in", "name": player_names[player_id]})

                elif action == "get_rooms":
                    room_list = [{"id": r_id, "name": room.name, "players": len(room.snakes)} for r_id, room in rooms.items()]
                    send_msg(client_socket, {"status": "room_list", "rooms": room_list})

                elif action == "create_room":
                    room_name_to_check = data.get("room_name", "")
                    existing_room_names = [r.name for r in rooms.values()]
                    if not (0 < len(room_name_to_check) <= 10):
                        send_msg(client_socket, {"status": "create_failed", "message": "Room name must be 1-10 characters."})
                    elif room_name_to_check in existing_room_names:
                        send_msg(client_socket, {"status": "create_failed", "message": "Room name already taken."})
                    else:
                        new_room = Room(name=room_name_to_check)
                        rooms[new_room.id] = new_room
                        new_room.add_player(player_id, client_socket, player_names[player_id])
                        player_to_room[player_id] = new_room.id
                        send_msg(client_socket, {"status": "joined_room", "room_id": new_room.id, "room_name": new_room.name})

                elif action == "join_room":
                    room_id = data.get("room_id")
                    if room_id in rooms:
                        target_room = rooms[room_id]
                        if len(target_room.snakes) < MAX_PLAYERS:
                            target_room.add_player(player_id, client_socket, player_names[player_id])
                            player_to_room[player_id] = room_id
                            send_msg(client_socket, {"status": "joined_room", "room_id": room_id, "room_name": target_room.name})
                        else:
                            send_msg(client_socket, {"status": "error", "message": "Room is full"})
                    else:
                        send_msg(client_socket, {"status": "error", "message": "Room not found"})

                elif action == "move":
                    room_id = player_to_room.get(player_id)
                    if room_id and room_id in rooms:
                        rooms[room_id].handle_command(player_id, data.get("direction"))

        except (ConnectionResetError, EOFError):
            print(f"[DISCONNECTED] Client {player_id} disconnected abruptly.")
            break
        except Exception as e:
            print(f"[ERROR] Unhandled exception for client {player_id}: {e}")
            break

    print(f"[CLEANUP] Cleaning up resources for Player {player_id}.")
    with state_lock:
        room_id = player_to_room.get(player_id)
        if room_id and room_id in rooms:
            if rooms[room_id].remove_player(player_id):
                rooms[room_id].stop()
                del rooms[room_id]

        if player_id in clients: del clients[player_id]
        if player_id in player_to_room: del player_to_room[player_id]
        if player_id in player_names: del player_names[player_id]
    
    client_socket.close()


        
def get_host_ip():        
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
            
def start_server(host = None):
    if host is None:
        host = get_host_ip()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, SERVER_PORT))
    server.listen(MAX_PLAYERS)
    print(f"[LISTENING] Server is listening on {host}:{SERVER_PORT}")

    while True:
        client_socket, addr = server.accept()
        thread = threading.Thread(target=handle_client_connection, args=(client_socket, addr))
        thread.daemon = True
        thread.start()

if __name__ == "__main__":
    start_server()