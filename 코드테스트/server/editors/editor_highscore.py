
import sys
import threading
import queue


import tkinter as tk
from tkinter import scrolledtext
import tkinter.font as tkfont

from editors.stdoutredirector import *
    
class EditorHighScore:
    def __init__(self, frame):
        self.frame = frame
                
        self.listbox = tk.Listbox(self.frame, 
                                  width=40,
                                  height=15,
                                font=("Consolas", 20), 
                                bg="#1E1E1E", 
                                fg="#D4D4D4", )
        self.listbox.config(font=("malgungulim", 20))  # 기본: 영어
        self.listbox.configure(font=("malgungulim", 20, "normal"))
        self.listbox.pack(padx=10, pady=(0, 10), fill="both", expand=1)
        # self.refresh_listbox()
        

    def refresh_listbox(self, data):
        self.listbox.delete(0, tk.END)  # 기존 항목 제거
        # self.data = dict(sorted(self.data.items(), key=lambda x: x[1]['level'], reverse=True))
        
        for key, value in data.items():
            if value['name'] is not None:
                self.listbox.insert(tk.END, f" {key+1}. [{value['date']}] [레벨: {value['score']:03}] {value['name']}")

    # def update_item(self,key,name,level):
    #     """새 항목 추가"""
    #     if key in self.data:
    #         self.data[key]['level'] = level
    #     else:
    #         self.data[key] = {
    #             'name':name,
    #             'level':level
    #         }
    #     self.refresh_listbox()

    # def delete_item(self):
    #     """선택한 항목 삭제"""
    #     selection = self.listbox.curselection()
    #     if selection:
    #         item_text = self.listbox.get(selection[0])
    #         key = item_text.split(" : ")[0]  # key만 추출
    #         if key in self.data:
    #             del self.data[key]
    #         self.refresh_listbox()

    # def update_item(self):
    #     """선택한 항목의 값 업데이트"""
    #     selection = self.listbox.curselection()
    #     if selection:
    #         item_text = self.listbox.get(selection[0])
    #         key = item_text.split(" : ")[0]
    #         if key in self.data:
    #             self.data[key] = self.data[key] + " (수정됨)"
    #         self.refresh_listbox()
