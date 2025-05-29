from _thread import *
import socket
import time
import json
# import pyautogui
import traceback

from users import *

class socketClient():
    
    HOST = '127.0.0.1'
    PORT = 9998
    infor = {}
    
    def __init__(self, parent):
        self.parent = parent
        self.HOST = self.get_host_ip()
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.HOST, self.PORT))
        # self.user = user
        self.identity = None
        self.name = None
        self.response = None
        self.client_run()
        
    def get_host_ip(self):        
        with open("host.txt", "r") as f:
            lines = f.readlines()
            for line in lines:
                # print(line)
                return line
                
    def send_infor(self,user):
        arrows = []
        for arrow in user.arrow_group:
            # print(arrow.rect)
            arrows.append((arrow.rect.x,arrow.rect.y,arrow.direction))
        json_object = {
            "action":{
                "name": user.name,
                "score": user.score,
                "hp": user.hp,
                "char": user.character,
                'x':user.rect.x,
                'y':user.rect.y,
                'dir':user.direction,
                'arrow':arrows,
            }
        }
        json_string = json.dumps(json_object)
        self.client_socket.send(json_string.encode())
        
    def send_request(self, name):
        json_object = {
            "request":{
                "name": name
            }
        }        
        self.response = None
        json_string = json.dumps(json_object)
        self.client_socket.send(json_string.encode())
        
    def del_out_user(self,server_infor):  
        del_users = []      
        for identity in self.infor:#저장된 유저 정보
            if identity not in  server_infor: #서버에서 받은 유저 정보
                del_users.append(identity)
                
        for identity in  del_users:
            del self.infor[identity]
            for i, user in enumerate(self.parent.player_group):
                if user.identity == identity:
                    del self.parent.player_group[i]
                    break
                
    def update_infor(self,server_infor):   
        identitys = []
        for user in self.parent.player_group:
            identitys.append(user.identity)
        
        for identity in server_infor:
            
            if identity not in self.infor: #새로 접속한 유저 정보 추가.
                self.infor[identity] = {}
            
            user = server_infor[identity]
                
            for value in user:
                self.infor[identity].update({value:user[value]})
                
            if identity == '서버정보' or identity == self.identity:
                continue
            
            if 'char' not in user:
                continue
            
            if 'name' not in user:
                continue
            
            # print(f'[{type(identity)}][{type(self.identity)}]')
            # print(self.identity,identity,identitys,server_infor)
            if identity not in identitys: 
                user = Users(self.parent.screen,self.parent.img_player,self.parent.img_arrow,identity,self)
                self.parent.player_group.append(user)
                
    def client_run(self):
        #서버로부터 오는 메세지를 대기하는 쓰레드 생성
        start_new_thread(self.recv_data, (self.client_socket,))   
          
        # while self.identity is None:
        #     self.send_infor()
        #     time.sleep(0.1)
        
        # self.parent.user.identity = self.identity
        
        #클라이언트 무한 대기
        # while True:
        #     time.sleep(1)
        #     # msg = pyautogui.prompt('내용을 입력하세요','채팅입력')
        #     #문자를 encode해서 클라이언트에게 보낸다.
        #     self.client_socket.send(msg.encode())

    #서버로 부터 메세지를 받는다.    
    def recv_data(self,client_socket):
        while True:
            try:
                data = client_socket.recv(1024).decode()
                server_infor = json.loads(data)    
                # print(f"서버메세지1:{server_infor}")
                if 'response' in server_infor:
                    self.response = server_infor['response']
                    if 'identity' in self.response:
                        self.identity = self.response['identity']
                    if 'name' in self.response:
                        self.name = self.response['name']
                else:
                    if self.name is not None:
                        self.del_out_user(server_infor)#접속을 해제 한 유저 삭제.                    
                        self.update_infor(server_infor)
                
                # print(f"서버메세지:{server_infor}")
            except ConnectionResetError:
                break
            except Exception as ex:
                err_msg = traceback.format_exc()
                print('recv_data ',err_msg)
                pass