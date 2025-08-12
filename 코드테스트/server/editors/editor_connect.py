
import sys
import threading
import queue

import re
import tkinter as tk
from tkinter import scrolledtext
import tkinter.font as tkfont
from tkinter import Menu
from tkinter import messagebox
from tkinter import simpledialog, messagebox

from editors.stdoutredirector import *
    
class EditorConnect:
    def __init__(self,parent, frame, ed_input):
        self.frame = frame
        self.parent = parent
        self.ed_input = ed_input
        
        self.data = {
        }
        
        self.listbox = tk.Listbox(self.frame, 
                                  width=40,
                                  height=15,
                                font=("Consolas", 20), 
                                bg="#1E1E1E", 
                                fg="#D4D4D4", )
        self.listbox.config(font=("malgungulim", 20))  # 기본: 영어
        self.listbox.configure(font=("malgungulim", 20, "normal"))
        self.listbox.pack(padx=10, pady=(0, 10), fill="both", expand=1)
        self.refresh_listbox()
        
# 우클릭 메뉴 생성
        self.context_menu = Menu(self.frame, tearoff=0)
        self.context_menu.add_command(label="레벨", command=self.menu_action_level)
        
        self.listbox.bind('<<ListboxSelect>>', self.on_select)
        self.listbox.bind('<Button-3>', self.show_context_menu)  # Windows: Button-3, Mac: Button-2
        
    def menu_action_level(self):
        selection = self.listbox.curselection()
        if selection:
            value = self.listbox.get(selection[0])
            value = re.findall(r'\[(.*?)\]', value)
            
            # print(f"{value}")
            name = value[0]
            
            level = simpledialog.askinteger("레벨 입력", "레벨을 입력하세요:")
            # print(level)
            if level is not None:
                try:
                    level = int(level)
                    # print(name,level)
                    self.parent.server.send_client_level(name,level)
                except Exception as ex:
                    print(ex)
            #     messagebox.showinfo("입력 결과", f"입력한 숫자는 {num}입니다.")
            # else:
            #     messagebox.showwarning("입력 취소", "숫자 입력이 취소되었습니다.")
            
    def on_select(self,event):
        # 선택된 항목 확인
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            value = self.listbox.get(index)
            # print(f"선택된 항목: {value}")
        
    def show_context_menu(self,event):
        # 우클릭 위치에서 해당 항목 선택
        try:
            index = self.listbox.nearest(event.y)
            self.listbox.selection_clear(0, tk.END)
            self.listbox.selection_set(index)
            self.listbox.activate(index)
            
            # 팝업 메뉴 띄우기
            self.context_menu.post(event.x_root, event.y_root)
        except:
            pass
        
    def refresh_listbox(self):
        """딕셔너리 내용을 Listbox에 새로 표시"""
        self.listbox.delete(0, tk.END)  # 기존 항목 제거
        self.data = dict(sorted(self.data.items(), key=lambda x: x[1]['level'], reverse=True))
        # print(self.data)
        for key, value in self.data.items():
            self.listbox.insert(tk.END, f" [{value['name']}] : 레벨{value['level']}")

    def update_item(self,key,name,level):
        """새 항목 추가"""
        if key in self.data:
            self.data[key]['level'] = level
        else:
            self.data[key] = {
                'name':name,
                'level':level
            }
        self.refresh_listbox()

    def delete_item(self,key):
        if key in self.data:
            del self.data[key]
        self.refresh_listbox()
        
        
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
