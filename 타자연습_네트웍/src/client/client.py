from _thread import *
import socket
import time
import json
# import pyautogui

class socketClient():
    
    HOST = '127.0.0.1'
    PORT = 9997
    infor = {}
    words = None
    
    def __init__(self):        
        self.HOST = self.get_host_ip()
        self.name = None
        self.identity = None
        self.response = None
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.HOST, self.PORT))
        self.client_run()
        
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
                
    def send_score(self, name,score):        
        json_object = {
            "name": name,
            "score": score,
        }
        json_string = json.dumps(json_object)
        self.client_socket.send(json_string.encode())
        
    def del_out_user(self,server_infor):  
        del_users = []      
        for identity in self.infor:#저장된 유저 정보
            if identity not in  server_infor: #서버에서 받은 유저 정보
                del_users.append(identity)
                
        for identity in  del_users:
            del self.infor[identity]
            
    def get_score(self):
        result = []
        high = []
        # print( self.infor)
        if '최고점수' in self.infor:
            for idex in self.infor['최고점수']:
                name = self.infor['최고점수'][idex]['name']
                score = self.infor['최고점수'][idex]['score']
                date = self.infor['최고점수'][idex]['date']
                high.append((name,score,date))
            
        for identity in self.infor:
            if 'name' not in self.infor[identity]:
                continue
            name = self.infor[identity]['name']
            if name is None:
                continue                
            score = self.infor[identity]['score']
            
            if identity == '최고점수':
                # high = (name,score)
                continue
            else:
                result.append([name,score])
        result = sorted(result, key=lambda x:x[1],reverse=True)
        return result,high
        
    def update_infor(self,server_infor):
        for identity in server_infor:
            if identity not in self.infor: #새로 접속한 유저 정보 추가.
                self.infor[identity] = {}
                
            user = server_infor[identity]
            for value in server_infor[identity]:
                self.infor[identity].update({value:user[value]})
                
    def request_words(self):
        json_object = {
            'request':{
                'words':None
                }
            }
        while True:
            json_string = json.dumps(json_object)
            self.client_socket.send(json_string.encode())
            time.sleep(0.1)
            if self.words is not None:
                break
        print(f'response {self.words}')
        
    def send_request(self, name):        
        json_object = {
            'request':{
                'name':name
                }
            }
        self.response = None
        json_string = json.dumps(json_object)
        self.client_socket.send(json_string.encode())
        
    def client_run(self):
        #서버로부터 오는 메세지를 대기하는 쓰레드 생성
        start_new_thread(self.recv_data, (self.client_socket,))   
        
        # json_object = {
        #     'request':{
        #         'name':self.name
        #         }
        #     }
        
        # while True:
        #     json_string = json.dumps(json_object)
        #     self.client_socket.send(json_string.encode())
        #     time.sleep(0.1)
        #     if self.identity is not None:
        #         break
        # print(f'response {self.identity}')
        self.request_words()
        
        #클라이언트 무한 대기
        # while True:
        #     time.sleep(1)
        #     # msg = pyautogui.prompt('내용을 입력하세요','채팅입력')
        #     #문자를 encode해서 클라이언트에게 보낸다.
        #     self.client_socket.send(msg.encode())

    #서버로 부터 메세지를 받는다.    
    def recv_data(self,client_socket):
        while True:
            data = client_socket.recv(1024).decode()
            
            server_infor = json.loads(data)     
            if 'response' in server_infor:
                if 'identity' in server_infor['response']:
                    self.identity = server_infor['response']['identity']
                    self.name = server_infor['response']['name']
                    self.response = server_infor['response']   
                if 'words' in server_infor['response']:
                    self.words = server_infor['response']['words']
            else:
                self.del_out_user(server_infor)#접속을 해제 한 유저 삭제.                    
                self.update_infor(server_infor)
            
            # print(f"서버메세제:{server_infor}")