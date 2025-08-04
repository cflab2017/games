
import tkinter as tk
from tkinter import scrolledtext
import tkinter.font as tkfont



    
class ToolBar:
    def __init__(self,frame, output):
        # self.frame = frame
        self.out_print = output
        
        self.frame=tk.Frame(frame, height=80,relief="solid", bd=0)
        self.frame.pack(padx=10, pady=(10, 10), fill="both", expand=1) 
        
        label = tk.Label(self.frame, text="시작레벨")
        label.config(font=("malgungulim", 20))  # 기본: 영어
        label.configure(font=("malgungulim", 20, "normal"))
        label.place(x=10, y=10, width=150, height=60)
        # label.pack(side="left", 
        #                       fill="none", expand=0, anchor='center')
        
        self.entry_level = tk.Entry(self.frame, justify='center')
        self.entry_level.place(x=160, y=10, width=60, height=60)
        # self.entry_level.pack(side="left",
        #                       fill="none", expand=0, anchor='center')        
        self.entry_level.config(font=("malgungulim", 20))  # 기본: 영어
        self.entry_level.configure(font=("malgungulim", 20, "normal"))
        
        # run_btn = tk.Button(self.frame, text="▶ 실행(Shift+Enter)", command=self.out_print.run_code_thread)
        # run_btn.pack(side="left", fill="none", expand=0, anchor='center')
        self.set_level(1)
        
    def get_level(self):
        level = self.entry_level.get()
        print(f"입력된 값: {level}")
        # self.entry_level.delete(0, tk.END) # 입력 필드 초기화
        return level
    
    def set_level(self, level):
        self.entry_level.delete(0, tk.END)  # 기존 텍스트 삭제
        self.entry_level.insert(0, f"{level}")  # 새로운 값 추가
