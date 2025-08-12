import socket
from _thread import *
import json
import traceback

import sys
import queue

import pickle
import os.path
import datetime as dt

from commu.stdoutredirector import *
from commu.code_exec import CodeExec
from question import *
import threading

class socketServer():
    from editors.editor_connect import EditorConnect
    from editors.editor_highscore import EditorHighScore
    from editors.editor_input import EditorInput
    from editors.toolbar import ToolBar
    client_sockets = {} #클라이언트 목록
    HOST = '127.0.0.1'
    PORT = 9995
    
    # infor = {
    #     'name':'coding'
    #     }
    
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
        3:{
            'name':None,
            'score':0,
            'date':None},
        4:{
            'name':None,
            'score':0,
            'date':None},
        5:{
            'name':None,
            'score':0,
            'date':None},
        6:{
            'name':None,
            'score':0,
            'date':None},
        7:{
            'name':None,
            'score':0,
            'date':None},
        8:{
            'name':None,
            'score':0,
            'date':None},
        9:{
            'name':None,
            'score':0,
            'date':None},
    }
    
    infor = {
        # '최고점수':high_score_dict
        }
    
    def __init__(self,ed_input,host):
        # print('>> Server Start 버전02')     
        if host == None:
            self.HOST = self.get_host_ip()     
        else:
            self.HOST = host
        self.update_store_dic('r')                      
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.HOST, self.PORT))
        self.server_socket.listen()
        threading.Thread(target=self.server_run, daemon=True).start()
        self.ed_input = ed_input
        self.last = len(Questions.que)
        # self.server_run()
    
    def get_host_ip(self):        
        with open("./commu/host.txt", "r") as f:
            lines = f.readlines()
            for line in lines:
                line = line.replace('\n','')
                line = line.replace(' ','')
                if line.find('#')>=0:
                    continue
                if len(line.split('.')) != 4:
                    # print(line)
                    continue
                # print(line)
                return line
    
    def check_same_name(self,identity,name):
        identity = int(identity)
        if len(name) < 1 or (name is None):
            return None
        
        name_check = name.replace(" ", "")
        
        for key in self.infor:
            if key == '최고점수' or identity == key:
                continue
            # print(self.infor,self.infor[key])
            if 'name' not in self.infor[key]:
                continue
            if self.infor[key]['name'] is None:
                continue
            if name_check == self.infor[key]['name'].replace(' ', ''):
                return None
            
        return name
    
    def update_store_dic(self, state):
        if state == 'r':
            #저장된 파일 불러오기
            if os.path.isfile(self.user_file_name): #불러올 파일이 있는가?
                with open(self.user_file_name, 'rb') as fr:
                    high_score_dict = pickle.load(fr) #딕셔너리로 변환
                    for key in high_score_dict:
                        self.high_score_dict[key] = high_score_dict[key]
                        if 'name' not in self.high_score_dict[key]:
                            self.high_score_dict[key]['name'] = None
                        if 'score' not in self.high_score_dict[key]:
                            self.high_score_dict[key]['score'] = 0
                        if 'date' not in self.high_score_dict[key]:
                            self.high_score_dict[key]['date'] = None
                        if key in self.high_score_dict:
                            if 'name' in self.high_score_dict[key]:
                                name = self.high_score_dict[key]['name']
                                if name is not None and len(name)>10:
                                    self.high_score_dict[key]['name'] = name[0:10]                            
                    # self.infor.update({'최고점수' : self.high_score_dict})      
                    # print(self.high_score_dict)              
        
        if state == 'w':  
            with open(self.user_file_name, 'wb') as fw:
                # self.high_score_dict = self.high_score_dict
                pickle.dump(self.high_score_dict,fw)
                # print('최고점수')
                # print(self.high_score_dict)
                
    def add_infor(self, identity):
        identity = int(identity)
        if identity not in self.infor:
            self.infor[identity] = {}
            self.infor[identity]['exec'] = CodeExec(self,identity,self.ed_input,self.ed_connect)
            
    def score_sort(self, name, score):
        if score <= 1:
            return
               
        score -=1 
        is_find = 0 
        date = dt.datetime.now()
        for key in self.high_score_dict:
            if self.high_score_dict[key]['score'] < score:
                is_find = 1
                # break
            if self.high_score_dict[key]['name'] == name:
                if self.high_score_dict[key]['score'] < score:
                    date_str = f'{date.year%100}.{date.month:02}.{date.day:02}'
                    self.high_score_dict[key]['score'] = score
                    self.high_score_dict[key]['date'] = date_str
                    is_find = 2
                else:
                    is_find = 0
                break
            
        if is_find:
            score_temp = []
            for key in self.high_score_dict:
                score_temp.append(list(self.high_score_dict[key].values()))
                
            if is_find == 1:
                date_str = f'{date.year%100}.{date.month:02}.{date.day:02}'
                score_temp.append([name,score,date_str])
            score_temp.sort(key=lambda x:-x[1])
            
            for i,key in enumerate(self.high_score_dict):
                self.high_score_dict[key]['name'] = score_temp[i][0]
                self.high_score_dict[key]['score'] = score_temp[i][1]
                self.high_score_dict[key]['date'] = score_temp[i][2]
            
        #     #파일에 저장하기
            self.update_store_dic('w')
            self.ed_score.refresh_listbox(self.high_score_dict)
            
    def set_bind_input(self, ed_input:EditorInput):
        self.ed_input = ed_input
        
    def set_bind_toolbar(self, ed_toolbar:ToolBar):
        self.ed_toolbar = ed_toolbar
        
    def set_bind_output(self, ed_connect:EditorConnect):
        self.ed_connect = ed_connect
        
    def set_bind_score(self, ed_score:EditorHighScore):
        self.ed_score = ed_score
        self.ed_score.refresh_listbox(self.high_score_dict)
        
    #접속한 모든 유저에게 새로 접속한 정보를 보낸다.
    def send_infor_to_all(self):        
        json_string = json.dumps(self.infor)        
        for identity in self.client_sockets:
            client = self.client_sockets[identity]
            client.send(json_string.encode())
    
    def send_client_level(self, name,level):
        for identity in self.infor:
            try:
                if self.infor[identity]['name'] == name:
                    client = self.client_sockets[identity]
                    self.send_to_level_client(client,name,level)
                    break
            except Exception as ex:
                print(ex)
                    
    #client가 접속되는지 기다리고 쓰레드를 생서한다.
    def server_run(self):
        while True:
            print('>>클라이언트 접속 대기')
            client_socket, addr = self.server_socket.accept()
            self.client_sockets[addr[1]] = client_socket #접속된 클라이언트를 리스트에 추가한다.
            print('>> Connected by :', addr[0], ':', addr[1])
            print("연결된 수 : ", len(self.client_sockets))            
            
            start_new_thread(self.thread_client, (client_socket, addr[1])) #클라이언트 쓰레드 생성
            
    def check_must(self,level, code):
        for mu in Questions.que[level-1]['must']:
            if mu not in code:
                return mu
        
        return None
    
    # def handler_exec(signum, frame):
    #     raise TimeoutError("Execution timed out!")
    def send_to_level_client(self, client,name, level):
                            
        json_object = {
            'response':{
                'name':name,
                'level':level,
                'result':'',
                'last':self.last,
                'question':Questions.que[level-1]['ques']
                }
            }
        print(json_object)
        self.response = None
        json_string = json.dumps(json_object)
        client.send(json_string.encode())
            
    def send_to_client(self, client, values,identity,start_level):
        if 'request' in values:
            name = values['request']['name']
            level = values['request']['level']
            code = values['request']['code']
            
            result,level = self.infor[identity]['exec'].run(code,level,start_level)
                            
            json_object = {
                'response':{
                    'name':name,
                    'level':level,
                    'result':result,
                    'last':self.last,
                    'question':Questions.que[level-1]['ques']
                    }
                }
            self.response = None
            json_string = json.dumps(json_object)
            client.send(json_string.encode())
            
    
    #접속된 client마다 각각 쓰레드가 생성된다.
    def thread_client(self,client_socket, identity):
        name = None
        try:
            start_level = int(self.ed_toolbar.get_level())
        except Exception as ex:
            start_level = 1
            
        self.add_infor(identity)
        while True:
            try:
                data = client_socket.recv(1024*10).decode()
                # print(f"클라이언트에서 받은 메세지 : {data}")
                
                values = json.loads(data)
                if 'sign' in values:
                    name = values['sign']['name']
                    name = self.check_same_name(identity,name)
                    response = {
                        'sign':{
                            'identity':identity,
                            'name':name,
                            'last':self.last,
                            }
                        }
                    self.infor[identity]['name'] = name
                    self.infor[identity]['exec'].name = name
                    json_string = json.dumps(response)
                    client_socket.send(json_string.encode())
                
                if 'request' in values:
                    name = values['request']['name']                    
                    level = values['request']['level']
                    # self.ed_input.add_msg(name)
                    self.ed_connect.update_item(identity,name,level)                    
                    self.send_to_client(client_socket,values,identity,start_level)
                # print(values)
                # self.send_infor_to_all()
                        
            except ConnectionResetError: #클라이언트 연결을 끊어지면..
                if 'name' in self.infor[identity]:
                    print(f"{self.infor[identity]['name']} 님이 종료했습니다.")
                else:
                    print(f"{identity} 님이 종료했습니다.")
                self.ed_connect.delete_item(identity)
                del self.infor[identity]
                client_socket.close()
                del self.client_sockets[identity]
                print("연결된 수 : ", len(self.client_sockets))   
                break
            except Exception:
                err_msg = traceback.format_exc()
                print(err_msg)  
                            
# server = socketServer()