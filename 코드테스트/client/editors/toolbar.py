
import tkinter as tk
from tkinter import scrolledtext
import tkinter.font as tkfont



    
class ToolBar:
    def __init__(self,parent,frame):
        # self.frame = frame
        self.parent = parent
        
        self.frame=tk.Frame(frame, height=100,relief="solid", bd=0)
        self.frame.pack(padx=10, pady=(10, 10), fill="both", expand=1) 
        self.seconds = 0
                
        
    def set_bind_output(self,ed_output,name):
        self.label = tk.Label(self.frame, text="타이머: 0초", font=("Helvetica", 20,"bold"), foreground="green")
        self.label.pack(side="left", fill="none", expand=0, anchor='center')
        self.update_timer()
        
        self.ed_output = ed_output
        run_btn = tk.Button(self.frame, text="▶ 실행해보기(Alt+Enter)", command=self.ed_output.only_run_code_thread)
        run_btn.config(font=("malgungulim", 16, "bold"))  # 기본: 영어
        run_btn.configure(font=("malgungulim", 16, "normal", "bold"), foreground="blue")
        run_btn.pack(side="left", fill="none", expand=0, anchor='center',padx=10)
        
        
        run_btn = tk.Button(self.frame, text="▶ 확인받기(Shift+Enter)", command=self.ed_output.run_code_thread)
        run_btn.config(font=("malgungulim", 16, "bold"))  # 기본: 영어
        run_btn.configure(font=("malgungulim", 16, "normal", "bold"), foreground="red")
        run_btn.pack(side="left", padx=10,fill="none", expand=0, anchor='center')
        
        
        name_label = tk.Label(self.frame, text=f' 접속 : {name}')        
        name_label.config(font=("malgungulim", 16, "bold"))  # 기본: 영어
        name_label.configure(font=("malgungulim", 16, "normal", "bold"))
        name_label.pack(side="left", fill="none", expand=0, anchor='center',padx=10)
        
        
    def update_timer(self):
        self.seconds += 1
        hrs = self.seconds // 3600
        mins = (self.seconds % 3600) // 60
        secs = self.seconds % 60
        self.label.config(text=f"{hrs:02}:{mins:02}:{secs:02}")
        self.parent.root.after(1000, self.update_timer)  # 1초마다 반복