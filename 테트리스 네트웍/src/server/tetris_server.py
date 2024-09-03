import socket
from _thread import *
import json
import traceback

import pickle
import os.path
import datetime as dt

class socketServer():
    client_sockets = {} #클라이언트 목록
    HOST = '127.0.0.1'
    PORT = 9999
    
    user_file_name = 'user_score.pickle'
    high_score_dict = {
        0:{
            'name':None,
            'score':0,
            'date':None},
        1:{
            'name':None,
            'score':0,
            'date':None},
        2:{
            'name':None,
            'score':0,
            'date':None},
    }
    
    infor = {
        '최고점수':high_score_dict
        }

    def __init__(self):
        print('>> Server Start 버전02')
        
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
                    high_score_dict = pickle.load(fr) #딕셔너리로 변환
                    if 0 in high_score_dict:
                        self.high_score_dict = high_score_dict
                    else:
                        if 'name' in high_score_dict:
                            self.high_score_dict[0]['name'] = high_score_dict['name']
                            self.high_score_dict[0]['score'] = high_score_dict['score']
                    self.infor.update({'최고점수' : self.high_score_dict})
                    
        
        if state == 'w':  
            with open(self.user_file_name, 'wb') as fw:
                self.high_score_dict = self.infor['최고점수']
                pickle.dump(self.high_score_dict,fw)
                print('최고점수')
                print(self.high_score_dict)
                
    #접속한 모든 유저에게 새로 접속한 정보를 보낸다.
    def send_infor_to_all(self):        
        json_string = json.dumps(self.infor)
        
        for identity in self.client_sockets:
            client = self.client_sockets[identity]
            client.send(json_string.encode())
            
    def add_infor(self, identity):
        identity = int(identity)
        if identity not in self.infor:
            self.infor[identity] = {}
                        
    def update_infor(self,values,identity):
        identity = int(identity)
        for value in values:                    
            self.infor[identity].update({value:values[value]})
            
        if ('score' in self.infor[identity]) and ('name' in self.infor[identity]):
            name = self.infor[identity]['name']
            if name is not None:
                score = self.infor[identity]['score']
                self.update_high_score(name,score)   
        print(self.infor)
    
    
    def score_sort(self, name, score):        
        is_find = 0 
        date = dt.datetime.now()
        for key in self.infor['최고점수']:
            if self.infor['최고점수'][key]['score'] < score:
                is_find = 1
                # break
            if self.infor['최고점수'][key]['name'] == name:
                if self.infor['최고점수'][key]['score'] < score:
                    date_str = f'{date.year}.{date.month}.{date.day}'
                    self.infor['최고점수'][key]['score'] = score
                    self.infor['최고점수'][key]['date'] = date_str
                    is_find = 2
                else:
                    is_find = 0
                break
            
        if is_find:
            score_temp = []
            for key in self.infor['최고점수']:
                score_temp.append(list(self.infor['최고점수'][key].values()))
                
            if is_find == 1:
                date_str = f'{date.year}.{date.month}.{date.day}'
                score_temp.append([name,score,date_str])
            score_temp.sort(key=lambda x:-x[1])
            
            for i,key in enumerate(self.infor['최고점수']):
                self.infor['최고점수'][key]['name'] = score_temp[i][0]
                self.infor['최고점수'][key]['score'] = score_temp[i][1]
                self.infor['최고점수'][key]['date'] = score_temp[i][2]
            
        #     #파일에 저장하기
            self.update_store_dic('w')
                
    def update_high_score(self,name, score):
        self.score_sort(name, score)
        # is_find = False
        # for key in self.infor['최고점수']:
        #     if self.infor['최고점수'][key]['score'] < score:
        #         is_find = False
        #         break
            
        # if is_find:
        #     score_temp = []
        #     for key in self.infor['최고점수']:
        #         score_temp.append(self.infor['최고점수'][key].values())
                
        # if self.infor['최고점수']['score'] < score:
        #     self.infor['최고점수']['name'] = name
        #     self.infor['최고점수']['score'] = score           

        #     #파일에 저장하기
        #     self.update_store_dic('w')
            
    def check_same_name(self,identity,name):
        identity = int(identity)
        if len(name) < 1 or (name is None):
            return None
        
        name_check = name.replace(" ", "")
        
        for key in self.infor:
            if key == '최고점수' or identity == key:
                continue
            print(self.infor,self.infor[key])
            if 'name' not in self.infor[key]:
                continue
            if self.infor[key]['name'] is None:
                continue
            if name_check == self.infor[key]['name'].replace(' ', ''):
                return None
            
        return name
    
    def sendAttack(self,target,shape):
        target = int(target)
        if target in self.client_sockets:
            json_object = {
                "attack": {
                    'shape':shape
                    },
            }
            json_string = json.dumps(json_object)
            self.client_sockets[target].send(json_string.encode())
            
    #client가 접속되는지 기다리고 쓰레드를 생서한다.
    def server_run(self):
        while True:
            print('>>클라이언트 접속 대기')
            client_socket, addr = self.server_socket.accept()
            self.client_sockets[addr[1]] = client_socket #접속된 클라이언트를 리스트에 추가한다.
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
                    name = None
                    if 'name' in values['request']:
                        name = values['request']['name']
                        name = self.check_same_name(identity,name)
                        
                    response = {
                        'response':{
                            'identity':identity,
                            'name':name
                            }
                        }                    
                    json_string = json.dumps(response)
                    client_socket.send(json_string.encode())
                    print(f"response : {json_string}")
                elif 'attack' in values:
                    self.sendAttack(values['attack']['identity'],
                                    values['attack']['shape'])
                else:
                    self.update_infor(values,identity)                
                    self.send_infor_to_all()
                        
            except ConnectionResetError: #클라이언트 연결을 끊어지면..
                if 'name' in self.infor[identity]:
                    print(f"{self.infor[identity]['name']} 님이 종료했습니다.")
                else:
                    print(f"{identity} 님이 종료했습니다.")
                    
                del self.infor[identity]
                client_socket.close()
                del self.client_sockets[identity]
                print("연결된 수 : ", len(self.client_sockets))   
                break
            except Exception:
                err_msg = traceback.format_exc()
                print(err_msg)  
                            
server = socketServer()