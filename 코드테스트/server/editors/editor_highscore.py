
import sys
import threading
import queue

from tkinter import Menu
from tkinter import messagebox
import tkinter as tk
from tkinter import scrolledtext
import tkinter.font as tkfont
from tkinter import simpledialog, messagebox

from editors.stdoutredirector import *

class PasswordPopup(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("비밀번호 입력")
        self.geometry("250x100")
        self.resizable(False, False)
        self.password = None

        tk.Label(self, text="비밀번호를 입력하세요:").pack(pady=5)

        self.entry = tk.Entry(self, show="*")
        self.entry.pack(pady=5)
        self.entry.focus()

        tk.Button(self, text="확인", command=self.submit).pack(pady=5)

        self.entry.bind("<Return>", lambda e: self.submit())

        # 부모 창을 비활성화
        self.grab_set()
        self.transient(parent)

    def submit(self):
        self.password = self.entry.get()
        self.destroy()
        
class EditorHighScore:
    def __init__(self, parent,frame):
        self.frame = frame
        self.parent = parent
                
        self.listbox = tk.Listbox(self.frame, 
                                  width=40,
                                  height=15,
                                font=("Consolas", 20), 
                                bg="#1E1E1E", 
                                fg="#D4D4D4", )
        self.listbox.config(font=("malgungulim", 20))  # 기본: 영어
        self.listbox.configure(font=("malgungulim", 20, "normal"))
        self.listbox.pack(padx=10, pady=(0, 10), fill="both", expand=1)
        self.high_score_dict = None
        
# 우클릭 메뉴 생성
        self.context_menu = Menu(self.frame, tearoff=0)
        self.context_menu.add_command(label="레벨", command=self.menu_action_level)
        self.context_menu.add_command(label="삭제", command=self.menu_action_remove)
        
        self.listbox.bind('<<ListboxSelect>>', self.on_select)
        self.listbox.bind('<Button-3>', self.show_context_menu)  # Windows: Button-3, Mac: Button-2

        # self.refresh_listbox()
        

    def refresh_listbox(self, data):
        self.listbox.delete(0, tk.END)  # 기존 항목 제거
        # self.data = dict(sorted(self.data.items(), key=lambda x: x[1]['level'], reverse=True))
        self.high_score_dict = data
        
        for key, value in self.high_score_dict.items():
            if value['name'] is not None:
                self.listbox.insert(tk.END, f" {key+1}. [{value['date']}] [레벨: {value['score']:03}] [{value['name']}]")

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
        
    def check_password(self,password=None):
        popup = PasswordPopup(self.parent.root)
        self.parent.root.wait_window(popup)

        if popup.password == password:
            # messagebox.showinfo("성공", "비밀번호 일치")
            return True
        else:
            messagebox.showerror("오류", "비밀번호 불일치")
            return False
        
    def menu_action_level(self):
        selection = self.listbox.curselection()
        if selection:
            value = self.listbox.get(selection[0])
            value = str(value).replace(']','').split("[")
            # print(f"{value}")
            name = value[3]
            
            level = simpledialog.askinteger("레벨 입력", "레벨을 입력하세요:")
            # print(level)
            if level is not None:
                try:
                    level = int(level)
                    self.parent.server.send_client_level(name,level)
                except Exception as ex:
                    print(ex)
            #     messagebox.showinfo("입력 결과", f"입력한 숫자는 {num}입니다.")
            # else:
            #     messagebox.showwarning("입력 취소", "숫자 입력이 취소되었습니다.")
         
    def menu_action_remove(self):
        
        if self.check_password('4321') is False:
            return
            
        selection = self.listbox.curselection()
        if selection:
            value = self.listbox.get(selection[0])
            value = str(value).replace(']','').split("[")
            # print(f"{value}")
            name = value[3]
            
            # print(f"{name}")
            # print(self.high_score_dict)
            try:
                for key in self.high_score_dict:
                    if self.high_score_dict[key]['name'] == name:
                        del self.high_score_dict[key]
                        last_key = list(self.high_score_dict.keys())[-1]
                        for i in range(key, last_key):
                            # print(f"i: {i}, last_key: {last_key}")
                            self.high_score_dict[i] = self.high_score_dict.pop(i + 1)
                        self.refresh_listbox(self.high_score_dict)
                        self.parent.server.update_store_dic('w')
                        break
            except Exception as e:
                print(f"Error: {e}")
        
    # def delete_item(self):
    #     """선택한 항목 삭제"""
    #     selection = self.listbox.curselection()
    #     if selection:
    #         item_text = self.listbox.get(selection[0])
    #         key = item_text.split(" : ")[0]  # key만 추출
    #         if key in self.high_score_dict:
    #             del self.high_score_dict[key]
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
