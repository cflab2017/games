import asyncio
import json
import math
import time
import uuid

from values import *
from gameRoom import *


# --- 로비 서버 ---
class GameServer:
    def __init__(self): 
        self.clients = {} 
        self.players_in_room = {}
        self.rooms = {}
        
    async def start(self, host = None):
        if host is None:
            host = self.get_host_ip()
            
        server = await asyncio.start_server(self.handle_client, host, PORT)
        print(f"[INFO] 로비 서버가 {host}:{PORT}에서 실행 중입니다...")
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
        try:
            if writer not in self.clients: return
            player_id = self.clients.pop(writer, None)
            if not player_id: return
            room_name = self.players_in_room.pop(player_id, None)
            if room_name in self.rooms:
                await self.rooms[room_name].remove_player(writer)
                if not self.rooms[room_name].clients: del self.rooms[room_name]
            if writer.can_write_eof(): writer.close()
            await writer.wait_closed()
            
        except Exception as e:
            print(f"[ERROR] remove_client 처리 중 오류: {e}")
            
    async def handle_client(self, reader, writer):
        player_id = None
        try:
            while True: # 클라이언트 연결 유지 및 메시지 처리 루프
                data = await reader.readline()
                if not data: break # 클라이언트 연결 종료

                message = json.loads(data.decode())
                # print(message,player_id)
                if player_id is None: # 아직 로그인하지 않은 클라이언트
                    if message.get("type") == "login":
                        requested_player_id = message.get("player_id", "").strip()

                        # Check length limit
                        if not requested_player_id or len(requested_player_id) > 10:
                            await self.send_message(writer, {"type": "login_fail", "reason": "아이디는 1~10자 이내여야 합니다."})
                            return # Stop processing this login attempt

                        # Check for duplicate ID
                        if requested_player_id in [client_id for client_id in self.clients.values()]:
                            await self.send_message(writer, {"type": "login_fail", "reason": "이미 사용 중인 아이디입니다."})
                            return # Stop processing this login attempt
                        
                        player_id = requested_player_id
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
        # room_name = self.players_in_room.get(player_id)
        # if room_name in self.rooms: 
        #     await self.rooms[room_name].handle_message(player_id, message)
        # else:
        msg_type = message.get("type")
        if msg_type == "list_rooms": 
            await self.send_message(writer, {"type": "room_list", "rooms": list(self.rooms.keys())})
        elif msg_type == "create_room":
            room_name = message.get("room_name", "").strip()

            # Check length limit
            if not room_name or len(room_name) > 10:
                await self.send_message(writer, {"type": "create_fail", "reason": "방 이름은 1~10자 이내여야 합니다."})
                return # Stop processing this room creation attempt

            if room_name and room_name not in self.rooms:
                self.rooms[room_name] = GameRoom(room_name, self)
                self.players_in_room[player_id] = room_name
                await self.rooms[room_name].add_player(writer, player_id)
            else: await self.send_message(writer, {"type": "create_fail", "reason": "이미 존재하는 방 이름입니다."})
            # print('bbbb:',self.rooms)
        elif msg_type == "join_room":
            room_name = message.get("room_name")
            if room_name in self.rooms:
                self.players_in_room[player_id] = room_name
                await self.rooms[room_name].add_player(writer, player_id)
            else: await self.send_message(writer, {"type": "join_fail", "reason": "존재하지 않는 방입니다."})
        elif msg_type == "leave_room": # 클라이언트가 로비에서 leave_room을 보낼 경우
            # 이 경우는 플레이어가 이미 방을 나갔거나 방에 없는 경우이므로 특별한 처리 불필요
            room_name = self.players_in_room.pop(player_id, None)
            if room_name in self.rooms:
                await self.rooms[room_name].remove_player(writer)
                if not self.rooms[room_name].clients: 
                    del self.rooms[room_name]
            # del self.players_in_room[player_id]
            # print(self.players_in_room)
        else:                
            room_name = self.players_in_room.get(player_id)
            if room_name in self.rooms: 
                await self.rooms[room_name].handle_message(player_id, message)
                    
if __name__ == "__main__":
    try: asyncio.run(GameServer().start())
    except KeyboardInterrupt: print("\n[INFO] 서버를 종료합니다.")