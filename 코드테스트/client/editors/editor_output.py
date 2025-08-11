
import sys
import threading
import queue


import tkinter as tk
from tkinter import scrolledtext
import tkinter.font as tkfont

from editors.stdoutredirector import *
    
class EditorOutput:
    def __init__(self, parent,frame):
        self.parent = parent
        self.frame = frame
        self.client = None
        
        self.input_mode = False
        self.input_prompt = ""
        self.input_response = ""
        self.input_ready = threading.Event()
        self.input_list = []
        
        self.text = scrolledtext.ScrolledText(
            self.frame, 
            # width=100, height=22, 
            font=("Consolas", 12), undo=True,
            bg="#1E1E1E", fg="#D4D4D4", insertbackground="white"
        )
        self.text.config(font=("malgungulim", 16))  # 기본: 영어
        self.text.configure(font=("malgungulim", 16, "normal"))
        
        self.text.tag_configure("title", font=("malgungulim", 16,'bold'), foreground="red", background="white",justify='center')   
        self.text.tag_configure("highlight", font=("malgungulim", 16,'bold'), foreground="blue", background="white",justify='center')   
        
        self.text.pack(padx=10, pady=(0, 10), fill="both", expand=1)
        # self.text.pack(side="left", fill="y", expand=1)
        # self.text.pack(fill="both", expand=1)
        self.text.bind("<Return>", self.capture_input)
        self.clear_msg()
        
    # def tab_pressed(self,event:tk.Event) -> str:
    #     # Insert the 4 spaces
    #     self.text.insert("insert", " "*4)
    #     # Prevent the default tkinter behaviour
    #     return "break"

    def capture_input(self, event=None):
        if self.input_mode:
            last_line = self.text.get("end-2l", "end-1c").split(self.input_prompt)[-1]
            self.input_response = last_line.strip()
            self.input_ready.set()
            self.text.insert(tk.END, "\n")
            return "break"
    
    def set_bind_input(self,ed_input):
        self.ed_input = ed_input
        
    def set_client(self,client):
        self.client = client

    def clear_msg(self,):
        self.text.config(state="normal")
        self.text.delete("1.0", tk.END)
        self.text.insert(tk.END, f"코드 실행 결과\n", "title")
        self.text.config(state="disabled")
        
        
    def add_highlight(self, msg):
        self.text.config(state="normal")
        self.text.insert(tk.END, msg+"\n", "highlight")
        self.text.config(state="disabled")
        
         
    def add_msg(self,msg):
        self.text.config(state="normal")
        self.text.insert(tk.END, msg+"\n")
        self.text.config(state="disabled")
        
    def only_run_code_thread(self,event=None):
        if self.input_mode == False:
            threading.Thread(target=self.run_code, daemon=True, args=(False,)).start()
        else:
            self.parent.show_popup('입력을 완료하세요',1000)
        
    def run_code_thread(self,event=None):
        if self.input_mode == False:
            threading.Thread(target=self.run_code, daemon=True, args=(True,)).start()
        else:
            self.parent.show_popup('입력을 완료하세요',1000)

    def rgb_to_hex(self,r, g, b):
        return f'#{r:02x}{g:02x}{b:02x}'

    def run_code(self, send_request):
        code = self.ed_input.text.get("1.0", tk.END)
        # self.text.delete("1.0", tk.END)
        self.clear_msg()
        self.add_msg('')
        self.input_list = []
        if send_request and self.client is not None:
            self.add_msg('')
            # self.add_highlight('서버로 코드를 전송합니다.')
            self.parent.show_popup("코드가 서버로 전송되었습니다.", duration=1000)
            self.client.send_request(code,self.input_list)
            return
        color = self.rgb_to_hex(47,47,47)
        self.text.configure(foreground="white", background=color)
        self.text.config(state="normal")
        # stdout redirect
        sys.stdout = StdoutRedirector(self.text)
        sys.stderr = StdoutRedirector(self.text)
        # input 대체 함수
        def editor_input(prompt="입력: "):
            self.text.see(tk.END)              # 스크롤을 마지막으로 이동
            self.text.mark_set("insert", tk.END)  # 커서를 마지막 위치로 이동
            self.text.focus()                  # 포커스 주기 (필요 시)
            self.input_mode = True
            self.input_prompt = prompt
            print(prompt, end="")
            self.input_ready.clear()
            self.input_ready.wait()  # 사용자 입력 기다림
            self.input_list.append(self.input_response)
            return self.input_response

        try:
            exec(code, {"input": editor_input})
            # print()
            # print('============================')
            print('프로그램 실행 종료.')
            # print('============================')
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__
            self.input_mode = False
            # if send_request and self.client is not None:
            #     self.add_msg('')
            #     # self.add_highlight('서버로 코드를 전송합니다.')
            #     self.parent.show_popup("코드가 서버로 전송되었습니다.", duration=1000)
            #     self.client.send_request(code,self.input_list)
        except Exception as e:
            print('============================')
            print("오류:", e)
            print('============================')
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__
            self.input_mode = False
        finally:
            # print()
            self.input_mode = False
            pass
        self.text.configure(foreground="white", background='black')
        self.text.config(state="disabled")
            
