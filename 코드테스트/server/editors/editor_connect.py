
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
    def __init__(self,parent, frame):
        self.frame = frame
        self.parent = parent
        
        self.data = {
        }
        
        self.color_bg = self.rgb_to_hex(208,223,211) 
        self.color_font = self.rgb_to_hex(36,53,40)  
        
        self.listbox = tk.Listbox(self.frame, 
                                  width=25,
                                #   height=15,
                                font=("Consolas", 20), 
                                bg="#1E1E1E", 
                                fg="#D4D4D4", )
        self.listbox.config(font=("malgungulim", 20))  # 기본: 영어
        self.listbox.configure(font=("malgungulim", 20, "normal"))
        self.listbox.pack(padx=10, pady=(10, 10), fill="both", expand=1)
        self.refresh_listbox()
        
# 우클릭 메뉴 생성
        self.context_menu = Menu(self.frame, tearoff=0)
        self.context_menu.add_command(label="레벨 이동", command=self.menu_action_level)
        self.context_menu.add_command(label="도전 레벨 & 시간", command=self.menu_action_Challenge_time)
        
        self.listbox.bind('<<ListboxSelect>>', self.on_select)
        self.listbox.bind('<Button-3>', self.show_context_menu)  # Windows: Button-3, Mac: Button-2
        
    def rgb_to_hex(self,r, g, b):
        return f'#{r:02x}{g:02x}{b:02x}'
    
    def set_bind_input(self, ed_input):
        self.ed_input = ed_input
        
    def set_bind_out_print(self, out_print):
        self.out_print = out_print
        
    def set_bind_server(self, server):
        self.server = server
    
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
            
    def menu_action_Challenge_time(self):
        selection = self.listbox.curselection()
        if selection:
            value = self.listbox.get(selection[0])
            value = re.findall(r'\[(.*?)\]', value)
            
            # print(f"{value}")
            name = value[0]
            
            # Challenge_time = simpledialog.askinteger("도전 시간 입력", "도전 시간을 입력하세요(분.초):")
            Challenge_values = simpledialog.askstring("도전 시간 입력", "도전 시간을 입력하세요(레벨.분.초):")
            # print(level)
            if Challenge_values is not None:
                try:
                    Challenge_values = str(Challenge_values).split('.')
                    
                    if len(Challenge_values)==3:
                        level = int(Challenge_values[0])
                        mi = int(Challenge_values[1])
                        se = int(Challenge_values[2])
                        
                        Challenge_time = mi*60 + se
                        
                        self.parent.server.send_client_level(name,level)
                        self.parent.server.send_client_challenge_time(name,Challenge_time)
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
            if index == 0:
                return 'break'
                
            self.listbox.selection_clear(0, tk.END)
            self.listbox.selection_set(index)
            self.listbox.activate(index)
            
            # 팝업 메뉴 띄우기
            self.context_menu.post(event.x_root, event.y_root)
        except:
            pass
        
    def add_highlight(self, msg):
        # self.listbox.config(state="normal")
        self.listbox.insert(tk.END, msg+"\n")
        # self.listbox.itemconfig(0, {'fg': 'blue', 'bg': 'lightyellow'})
        self.listbox.itemconfig(0, {'fg': self.color_font, 'bg': self.color_bg})
        # self.listbox.config(state="disabled")
        
    def refresh_listbox(self):
        """딕셔너리 내용을 Listbox에 새로 표시"""
        self.listbox.delete(0, tk.END)  # 기존 항목 제거
        self.add_highlight('접속자')
        self.data = dict(sorted(self.data.items(), key=lambda x: x[1]['level'], reverse=True))
        # print(self.data)
        for key, value in self.data.items():
            self.listbox.insert(tk.END, f" [{value['name']}] : 레벨{value['level']} {value['Challenge']}")

    def update_item(self,key,name,level,Challenge):
        if Challenge:
            Challenge = '도전'
        else:
            Challenge = '연습'
            
        if key not in self.data:
            self.data[key] = {
                'name':name,
                'level':level,
                'Challenge':Challenge
            }
        
        self.data[key]['level'] = level
        self.data[key]['Challenge'] = Challenge
        # print(self.data[key])
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
