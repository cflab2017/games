from _thread import *
import socket
import time
import json
import traceback
import winsound

class socketClient():
    
    HOST = '127.0.0.1'
    PORT = 9995
    
    def __init__(self,parent,host):
        self.parent = parent 
        self.identity = None
        self.name = None
        self.response = None
        self.ed_ranking = None
        if host == None:
            self.HOST = self.get_host_ip()      
        else:
            self.HOST = host    
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.HOST, self.PORT))
        self.client_run()
        # self.send_request('test')
    
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
            
    def set_bind_Ranking(self,ed_ranking):
        self.ed_ranking = ed_ranking
        
    def set_bind_input(self, ed_input):
        self.ed_input = ed_input
        
    def set_bind_output(self, output):
        self.output = output
    def set_bind_content(self, content):
        self.content = content
        
    def send_request_ranking(self):        
        json_object = {
            'ranking':0
            }
        self.response = None
        json_string = json.dumps(json_object, ensure_ascii=False, default=str)
        self.client_socket.sendall(json_string.encode())
        
    def send_request_complete_level(self, level = 0):        
        json_object = {
            'levels':level
            }
        self.response = None
        json_string = json.dumps(json_object, ensure_ascii=False, default=str)
        self.client_socket.sendall(json_string.encode())
        
    def send_request_sign(self, name):        
        json_object = {
            'sign':{
                'name':name,
                }
            }
        self.response = None
        json_string = json.dumps(json_object, ensure_ascii=False, default=str)
        self.client_socket.sendall(json_string.encode())
        
    def send_request(self, code, input_list=[]):        
        json_object = {
            'request':{
                'name':self.name,
                'level':self.parent.level,
                'code':code,
                'input':input_list,
                }
            }
        self.response = None
        json_string = json.dumps(json_object, ensure_ascii=False, default=str)
        self.client_socket.sendall(json_string.encode())
        
    def client_run(self):
        #서버로부터 오는 메세지를 대기하는 쓰레드 생성
        start_new_thread(self.recv_data, (self.client_socket,))     
        
    def dingdong(self):
        winsound.PlaySound("./sounds/dingdong.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)

    def ttaeng(self):
        winsound.PlaySound("./sounds/ding.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
        
    #서버로 부터 메세지를 받는다.    
    def recv_data(self,client_socket):
        while True:
            try:
                data = client_socket.recv(1024).decode()
                # print(f"{data}")
                server_infor = json.loads(data)    
                # print(server_infor)     
                if 'sign' in server_infor:                    
                    if 'identity' in server_infor['sign']:
                        self.identity = server_infor['sign']['identity']
                        self.name = server_infor['sign']['name']
                        self.response = server_infor['sign']  
                        self.parent.last_level = server_infor['sign']['last']
                        # self.ed_input.clear_msg()
                        # self.ed_input.add_msg("#코드를 여기에 작성하세요")
                elif 'levels' in server_infor:   
                    # print(server_infor)
                    levels = server_infor['levels']['level']
                    code = server_infor['levels']['code']
                    if len(code)>0:
                        self.ed_input.add_code_msg(code)
                    else:
                        self.ed_input.levels_code_list(levels)
                    
                    
                elif 'ranking' in server_infor:   
                    # print(server_infor)
                    if self.ed_ranking is not None:
                        self.ed_ranking.refresh_listbox(server_infor['ranking'])
                elif 'response' in server_infor:                 
                    self.output.add_msg('\n')   
                    
                    # msg = '============================\n'
                    # msg += f"\t서버메세지\n"
                    # msg += '============================\n'
                    # self.output.add_msg(msg)            
                    # self.output.add_msg('\n')   
                    self.output.add_highlight('서버메세지')     
                    self.output.add_msg('\n')   
                    msg = server_infor['response']['result']
                    msg = str(msg)
                    self.output.add_msg(msg)     
                    if msg.find('실패')>-1:
                        # self.ttaeng()
                        start_new_thread(self.ttaeng,())
                    
                    if self.parent.level < server_infor['response']['level']:
                        self.parent.level = server_infor['response']['level']
                        self.parent.last_level = server_infor['response']['last']
                        self.ed_input.clear_msg()
                        self.ed_input.add_msg("#코드를 여기에 작성하세요")
                        self.ed_input.set_focus()
                        
                        
                        if msg.find('정답')>-1:
                            
                            start_new_thread(self.dingdong,())
                            # self.dingdong()
                            self.parent.show_popup(f'레벨업!! level : {self.parent.level}')
                        # self.output.add_msg(f'레벨업!! level : {self.parent.level}')
                        
                    self.content.clear_msg()
                    msg = '\n'
                    # msg = '============================\n'
                    # msg += f"\t\t 레벨 : [ {self.parent.level} ]\n"
                    # msg += '============================\n'
                    self.content.add_msg(str(msg))
                    for msg in server_infor['response']['question']:
                        msg = str(msg)
                        if msg.find('힌트')>-1:
                            self.content.add_msg('\n')
                            self.content.add_highlight('힌트')
                            self.content.add_msg('\n')
                        elif msg.find('출력 결과')>-1:
                            self.content.add_msg('\n')
                            self.content.add_highlight('아래와 같이 출력하세요.')
                            self.content.add_msg('\n')
                        else:
                            self.content.add_msg(str(msg))
                # print(f"서버메세제:{server_infor}")
            except Exception:
                err_msg = traceback.format_exc()
                print(err_msg) 
    
    def run(self):
        while True:
            pass


# if __name__ == '__main__':
#     cli = socketClient(None)
#     cli.run()
    