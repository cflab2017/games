
import tkinter as tk
from tkinter import scrolledtext
import tkinter.font as tkfont



    
class ToolBar:
    def __init__(self,frame):
        # self.frame = frame
        
        self.frame=tk.Frame(frame, height=80,relief="solid", bd=0)
        self.frame.pack(padx=10, pady=(10, 10), fill="both", expand=1) 
        
        label = tk.Label(self.frame, text="시작레벨")
        label.config(font=("malgungulim", 20))  # 기본: 영어
        label.configure(font=("malgungulim", 20, "normal",'bold'))
        label.place(x=10, y=10, width=150, height=60)
        
        self.entry_level = tk.Entry(self.frame, justify='center')
        self.entry_level.place(x=160, y=10, width=60, height=60)      
        self.entry_level.config(font=("malgungulim", 20))  # 기본: 영어
        self.entry_level.configure(font=("malgungulim", 20, "normal",'bold'))
        
        
        label = tk.Label(self.frame, text="도전시간")
        label.config(font=("malgungulim", 20))  # 기본: 영어
        label.configure(font=("malgungulim", 20, "normal",'bold'))
        label.place(x=220, y=10, width=150, height=60)
        
        self.entry_challenge_time = tk.Entry(self.frame, justify='center')
        self.entry_challenge_time.place(x=380, y=10, width=60, height=60)      
        self.entry_challenge_time.config(font=("malgungulim", 20))  # 기본: 영어
        self.entry_challenge_time.configure(font=("malgungulim", 20, "normal",'bold'))
        
        self.set_level(1)
        self.set_challenge_time(30)
        
    def set_bind_input(self, ed_input):
        self.ed_input = ed_input
        
    def set_bind_out_print(self, out_print):
        self.out_print = out_print
                
    def get_level(self):
        level = self.entry_level.get()
        
        try:
            level = int(level)
        except Exception as ex:
            level = 1
            
        if level < 1:
            level = 1
            
        return level
    
    def set_level(self, level):
        self.entry_level.delete(0, tk.END)
        self.entry_level.insert(0, f"{level}")
        
    
    def get_challenge_time(self):
        time = self.entry_challenge_time.get()
        
        try:
            time = int(time)
        except Exception as es:
            time = 30
        
        if time < 1:
            time = 1
            
        return time
    
    def set_challenge_time(self, time):
        self.entry_challenge_time.delete(0, tk.END)
        self.entry_challenge_time.insert(0, f"{time}")
