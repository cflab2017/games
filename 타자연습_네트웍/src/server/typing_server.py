import socket
from _thread import *
import json

import pickle
import os.path

class socketServer():
    client_sockets = [] #클라이언트 목록
    HOST = '127.0.0.1'
    PORT = 9997
    
    user_file_name = 'user_score.pickle'
    high_score_dict = {
    'name':None,
    'score':0,
    }
    
    infor = {
        '최고점수':high_score_dict
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
                line = line.replace('\n','')
                line = line.replace(' ','')
                if line.find('#')>=0:
                    continue
                if len(line.split('.')) != 4:
                    print(line)
                    continue
                print(line)
                return line
            
    def update_store_dic(self, state):
        if state == 'r':
            #저장된 파일 불러오기
            if os.path.isfile(self.user_file_name): #불러올 파일이 있는가?
                with open(self.user_file_name, 'rb') as fr:
                    self.high_score_dict = pickle.load(fr) #딕셔너리로 변환
                    self.infor.update({'최고점수' : self.high_score_dict})
                    print('최고점수')
                    print(self.high_score_dict)
                    # self.infor = pickle.load(fr)
                    
        
        if state == 'w':  
            with open(self.user_file_name, 'wb') as fw:
                # pickle.dump(self.infor,fw)
                self.high_score_dict = self.infor['최고점수']
                pickle.dump(self.high_score_dict,fw)
                print('최고점수')
                print(self.high_score_dict)
                
    #접속한 모든 유저에게 새로 접속한 정보를 보낸다.
    def send_infor_to_all(self):        
        json_string = json.dumps(self.infor)
        
        for client in self.client_sockets:
            client.send(json_string.encode())
            
    def add_infor(self, identity):
        if identity not in self.infor:
            self.infor[identity] = {'name':None, 'score':0}
                        
    def update_infor(self,values,identity):
        for value in values:                    
            self.infor[identity].update({value:values[value]})
            
        if ('score' in self.infor[identity]) and ('name' in self.infor[identity]):
            name = self.infor[identity]['name']
            if name is not None:
                score = self.infor[identity]['score']
                self.update_high_score(name,score)   
        print(self.infor)
    
    def update_high_score(self,name, score):
        if self.infor['최고점수']['score'] < score:
            self.infor['최고점수']['name'] = name
            self.infor['최고점수']['score'] = score           

            #파일에 저장하기
            self.update_store_dic('w')
                    
    #client가 접속되는지 기다리고 쓰레드를 생서한다.
    def server_run(self):
        while True:
            print('>>클라이언트 접속 대기')
            client_socket, addr = self.server_socket.accept()
            self.client_sockets.append(client_socket) #접속된 클라이언트를 리스트에 추가한다.
            print('>> Connected by :', addr[0], ':', addr[1])
            print("연결된 수 : ", len(self.client_sockets))            
            
            start_new_thread(self.thread_client, (client_socket, addr[1])) #클라이언트 쓰레드 생성
                        
    #접속된 client마다 각각 쓰레드가 생성된다.
    def thread_client(self,client_socket, identity):
        
        self.add_infor(identity)
        self.send_infor_to_all()
        
        while True:
            try:
                data = client_socket.recv(1024*10).decode()
                print(f"클라이언트에서 받은 메세지 : {data}")
                
                values = json.loads(data)
                if 'request' in values:
                    response = {
                        'response':{
                            'identity':identity
                            }
                        }                    
                    json_string = json.dumps(response)
                    client_socket.send(json_string.encode())
                    print(f"response : {json_string}")
                else:
                    self.update_infor(values,identity)                
                    self.send_infor_to_all()
                
                # if ('score' in self.infor[identity]) and ('name' in self.infor[identity]):
                #     name = self.infor[identity]['name']
                #     score = self.infor[identity]['score']
                #     self.update_high_score(name,score)    
                #     # self.infor = dict(sorted(self.infor.items(), key=lambda x: x[1]['score'],reverse=True))
                #     # print("정렬\n",self.infor)            
                #     self.send_infor_to_all()
                        
            except ConnectionResetError: #클라이언트 연결을 끊어지면..
                if 'name' in self.infor[identity]:
                    print(f"{self.infor[identity]['name']} 님이 종료했습니다.")
                    self.update_store_dic('w')
                else:
                    print(f"{identity} 님이 종료했습니다.")
                
                del self.infor[identity]
                client_socket.close()
                self.client_sockets.remove(client_socket)
                
                break
            except Exception as ex:
                print("--------------",ex)
                            
server = socketServer()