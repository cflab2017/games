import socket
from _thread import *
import json
import time
import random
import pickle
import os.path
import datetime

class socketServer():
    client_sockets = [] #클라이언트 목록
    HOST = '127.0.0.1'
    PORT = 9998
    
    user_file_name = 'user_score.pickle'
    high_score_dict = {
    'name':None,
    'score':0,
    }
    
    infor = {
        '서버정보': 
            {
                '최고점수':high_score_dict,
                '아이템':{
                    'hp':[],
                    'shield':[],
                    },                    
            },
        }

    def __init__(self):
        print('>> Server Start')
        
        self.HOST = self.get_host_ip()
        self.update_store_dic('r')
                                
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.HOST, self.PORT))
        self.server_socket.listen()
        self.server_run()
    
    def get_host_ip(self):        
        with open("host.txt", "r") as f:
            lines = f.readlines()
            for line in lines:
                print(line)
                return line
            
    def update_store_dic(self, state):
        if state == 'r':
            #저장된 파일 불러오기
            if os.path.isfile(self.user_file_name): #불러올 파일이 있는가?
                with open(self.user_file_name, 'rb') as fr:
                    self.high_score_dict = pickle.load(fr) #딕셔너리로 변환
                    self.infor['서버정보'].update({'최고점수' : self.high_score_dict})
                            
        if state == 'w':  
            with open(self.user_file_name, 'wb') as fw:
                self.high_score_dict = self.infor['서버정보']['최고점수']
                pickle.dump(self.high_score_dict,fw)
                
    #접속한 모든 유저에게 새로 접속한 정보를 보낸다.
    def send_infor_to_all(self):        
        json_string = json.dumps(self.infor)
        
        # print(self.infor)
        for client in self.client_sockets:
            client.send(json_string.encode())
            
    def add_infor(self, identity):
        if identity not in self.infor:
            self.infor[identity] = {}
                        
    def update_infor(self,values,identity):     
        for value in values:                    
            self.infor[identity].update({value:values[value]})
            
    
    def update_high_score(self,identity):
        
        name = self.infor[identity]['name']
        score = self.infor[identity]['score']
        if self.infor['서버정보']['최고점수']['score'] < score:
            self.infor['서버정보']['최고점수']['name'] = name
            self.infor['서버정보']['최고점수']['score'] = score           

            #파일에 저장하기
            self.update_store_dic('w')
                    
    #client가 접속되는지 기다리고 쓰레드를 생서한다.
    def server_run(self):
        start_new_thread(self.thread_server, ())
        while True:
            print('>>클라이언트 접속 대기')
            client_socket, addr = self.server_socket.accept()
            self.client_sockets.append(client_socket) #접속된 클라이언트를 리스트에 추가한다.
            print('>> Connected by :', addr[0], ':', addr[1])
            print("연결된 수 : ", len(self.client_sockets))            
            
            start_new_thread(self.thread_client, (client_socket, addr[1])) #클라이언트 쓰레드 생성
                        
    def thread_server(self):
        item_gen_time_tick = 0
        item_gen_time = 5#random.randint(5)
        while True:
            time.sleep(1)
            item_gen_time_tick += 1
            # if item_gen_time_tick >= 2:
            #     if self.infor['서버정보']['아이템']['hp'] is not None or self.infor['서버정보']['아이템']['shield'] is not None:
            #         self.infor['서버정보']['아이템']['hp'] = None
            #         self.infor['서버정보']['아이템']['shield'] = None
            #         self.send_infor_to_all()
            is_send = False
            for i, hp in enumerate(self.infor['서버정보']['아이템']['hp']):
                hp[2] += 1
                if hp[2] > 2:
                    del self.infor['서버정보']['아이템']['hp'][i]
                    is_send = True
            
            for i, shield in enumerate(self.infor['서버정보']['아이템']['shield']):
                shield[2] += 1
                if shield[2] > random.randint(5,10):
                    del self.infor['서버정보']['아이템']['shield'][i]
                    is_send = True
                    
            if item_gen_time_tick > item_gen_time:
                item_gen_time = 2#random.randint(3,15)
                item_gen_time_tick = 0
                
                for i in range(3):
                    per = random.randint(0,100)
                    if per < 30 and len(self.infor['서버정보']['아이템']['hp'])<3:
                        x = random.randint(300,700)
                        y = random.randint(20,980)
                        self.infor['서버정보']['아이템']['hp'].append([x,y,0])
                        is_send = True
                    
                for i in range(6):
                    per = random.randint(0,100)
                    if per < 90 and len(self.infor['서버정보']['아이템']['shield'])<8:
                        x = random.randint(300,700)
                        y = random.randint(20,980)
                        self.infor['서버정보']['아이템']['shield'].append([x,y,0])
                        is_send = True
                    
            # if is_send:
            #     self.send_infor_to_all()
                
            
            
    #접속된 client마다 각각 쓰레드가 생성된다.
    def thread_client(self,client_socket, identity):
        identity = str(identity)
        self.add_infor(identity)
        self.send_infor_to_all()
        
        while True:
            try:
                data = client_socket.recv(1024*10).decode()
                # print(f"클라이언트에서 받은 메세지 : {data}")
                
                values = json.loads(data)
                if 'action' in values:
                    self.update_infor(values['action'],identity)
                    self.update_high_score(identity)
                    self.send_infor_to_all()
                if 'request' in values:
                    name = None
                    if 'name' in values['request']:
                        name = values['request']['name']
                        for key in self.infor:
                            if key == '서버정보' or key == identity:
                                continue
                            if 'name' not in self.infor[key]:
                                continue
                            if name == self.infor[key]['name']:
                                name = None
                                break
                                
                    json_object = {
                        "response":{
                            'identity':identity,
                            'name':name,
                        }
                    }
                    if name is not None:
                        self.infor[key].update({'name':name})
                        
                    json_string = json.dumps(json_object)
                    client_socket.send(json_string.encode())
                    
                    
            except ConnectionResetError: #클라이언트 연결을 끊어지면..
                if 'name' in self.infor[identity]:
                    print(f"{self.infor[identity]['name']} 님이 종료했습니다.")
                del self.infor[identity]
                client_socket.close()
                self.client_sockets.remove(client_socket)
                self.send_infor_to_all()
                break
            except Exception as ex:
                print(ex)                
                            
server = socketServer()