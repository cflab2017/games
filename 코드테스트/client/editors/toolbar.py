
import tkinter as tk
from tkinter import scrolledtext
import tkinter.font as tkfont



    
class ToolBar:
    def __init__(self,frame):
        # self.frame = frame
        
        self.frame=tk.Frame(frame, height=100,relief="solid", bd=0)
        self.frame.pack(padx=10, pady=(10, 10), fill="both", expand=1) 
                
        
    def set_bind_output(self,ed_output,name):
        self.ed_output = ed_output
        run_btn = tk.Button(self.frame, text="▶ 실행해보기(Alt+Enter)", command=self.ed_output.only_run_code_thread)
        run_btn.config(font=("malgungulim", 16, "bold"))  # 기본: 영어
        run_btn.configure(font=("malgungulim", 16, "normal", "bold"), foreground="blue")
        run_btn.pack(side="left", fill="none", expand=0, anchor='center')
        
        
        run_btn = tk.Button(self.frame, text="▶ 확인받기(Shift+Enter)", command=self.ed_output.run_code_thread)
        run_btn.config(font=("malgungulim", 16, "bold"))  # 기본: 영어
        run_btn.configure(font=("malgungulim", 16, "normal", "bold"), foreground="red")
        run_btn.pack(side="left", padx=10,fill="none", expand=0, anchor='center')
        
        
        name_label = tk.Label(self.frame, text=f' 로그인 : {name}')        
        name_label.config(font=("malgungulim", 16, "bold"))  # 기본: 영어
        name_label.configure(font=("malgungulim", 16, "normal", "bold"))
        name_label.pack(side="left", fill="none", expand=0, anchor='center')