
import tkinter as tk
from tkinter import scrolledtext
import tkinter.font as tkfont



    
class ToolBar:
    def __init__(self,frame):
        # self.frame = frame
        
        self.frame=tk.Frame(frame, height=100,relief="solid", bd=0)
        self.frame.pack(padx=10, pady=(10, 10), fill="both", expand=1) 
                
        
    def set_bind_output(self,ed_output):
        self.ed_output = ed_output
        run_btn = tk.Button(self.frame, text="▶ 실행(Shift+Enter)", command=self.ed_output.run_code_thread)
        run_btn.pack(side="left", fill="none", expand=0, anchor='center')