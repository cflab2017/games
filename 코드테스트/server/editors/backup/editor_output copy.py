
import sys
import threading
import queue


import tkinter as tk
from tkinter import scrolledtext
import tkinter.font as tkfont

from editors.stdoutredirector import *
    
class EditorOutput:
    def __init__(self, frame, ed_input):
        self.frame = frame
        self.ed_input = ed_input
        self.client = None
        
        self.input_mode = False
        self.input_prompt = ""
        self.input_response = ""
        self.input_ready = threading.Event()
        
        self.output = scrolledtext.ScrolledText(
            self.frame, 
            # width=100, height=22, 
            font=("Consolas", 12), undo=True,
            bg="#1E1E1E", fg="#D4D4D4", insertbackground="white"
        )
        self.output.config(font=("malgungulim", 12))  # 기본: 영어
        self.output.configure(font=("malgungulim", 12, "normal"))
        self.output.pack(padx=10, pady=(0, 10), fill="both", expand=1)
        # self.output.pack(side="left", fill="y", expand=1)
        # self.output.pack(fill="both", expand=1)
        self.output.bind("<Return>", self.capture_input)
        
    def tab_pressed(self,event:tk.Event) -> str:
        # Insert the 4 spaces
        self.text.insert("insert", " "*4)
        # Prevent the default tkinter behaviour
        return "break"

    def capture_input(self, event=None):
        if self.input_mode:
            last_line = self.output.get("end-2l", "end-1c").split(self.input_prompt)[-1]
            self.input_response = last_line.strip()
            self.input_ready.set()
            self.output.insert(tk.END, "\n")
            return "break"
    
    def set_client(self,client):
        self.client = client
        
    def add_msg(self,msg):
        self.output.insert(tk.END, msg+"\n")
        
    def run_code_thread(self,event=None):
        threading.Thread(target=self.run_code, daemon=True).start()

    def run_code(self):
        code = self.ed_input.text.get("1.0", tk.END)
        self.output.delete("1.0", tk.END)

        # stdout redirect
        sys.stdout = StdoutRedirector(self.output)
        sys.stderr = StdoutRedirector(self.output)
        # input 대체 함수
        def editor_input(prompt="입력: "):
            self.input_mode = True
            self.input_prompt = prompt
            print(prompt, end="")
            self.input_ready.clear()
            self.input_ready.wait()  # 사용자 입력 기다림
            return self.input_response

        try:
            exec(code, {"input": editor_input})
            print('------------')
            print('프로그램 종료')
            print('------------')
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__
            self.input_mode = False
            if self.client is not None:
                self.client.send_request('joseph', code)
        except Exception as e:
            print('------------')
            print("오류:", e)
            print('------------')
            print('프로그램 종료')
            print('------------')
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__
            self.input_mode = False
        finally:
            # print()
            pass
            
