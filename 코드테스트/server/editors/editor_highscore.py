
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
        self.listbox.pack(padx=10, pady=(10, 10), fill="both", expand=1)
        self.high_score_dict = None
        
# 우클릭 메뉴 생성
        self.context_menu = Menu(self.frame, tearoff=0)
        self.context_menu.add_command(label="코드제출", command=self.menu_action_level)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="비밀번호 초기화", command=self.menu_action_remove_password)
        self.context_menu.add_command(label="삭제", command=self.menu_action_remove)
        
        self.listbox.bind('<<ListboxSelect>>', self.on_select)
        self.listbox.bind('<Button-3>', self.show_context_menu)  # Windows: Button-3, Mac: Button-2

        # self.refresh_listbox()
        

    def set_bind_server(self, server):
        self.server = server
        
    def refresh_listbox(self, data):
        self.listbox.delete(0, tk.END)  # 기존 항목 제거
        # self.data = dict(sorted(self.data.items(), key=lambda x: x[1]['level'], reverse=True))
        self.high_score_dict = data
        keys = list(self.high_score_dict.keys())
        keys.sort()
        
        
        for key in keys:
            value = self.high_score_dict[key]
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
    
    def open_popup(self,name):
        # print(self.server.users)
        if name not in self.server.users:
            messagebox.showinfo("검색 결과", f"검색된 내용이 없습니다.")
            return
        self.code_sel_name = name
        popup = tk.Toplevel(self.parent.root)
        popup.title(f"{name}님의 코드 제출 결과")
        
                # 화면 크기 구하기
        screen_width = self.parent.root.winfo_screenwidth()
        screen_height = self.parent.root.winfo_screenheight()

        # 팝업 크기 예상값 (약 300x100)
        popup_w, popup_h = 300, 100
        x = (screen_width // 2) - (popup_w // 2)
        y = (screen_height // 2) - (popup_h // 2)
        
        popup.geometry(f"800x800+{x}+{y}")  # 위치 지정
        
        
        popup.attributes('-topmost', True)

        # 좌측 Listbox
        list_frame = tk.Frame(popup, width = 150)
        list_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)    
        list_frame.pack_propagate(False)

        self.listbox_code = tk.Listbox(list_frame,
                                font=("Consolas", 20), 
                                bg="#1E1E1E", 
                                fg="#D4D4D4",  )
        
        self.listbox_code.bind('<<ListboxSelect>>', self.on_select_code)
        self.listbox_code.pack(side=tk.LEFT, fill=tk.Y)

        # 스크롤바 연결
        scrollbar = tk.Scrollbar(list_frame, orient="vertical", command=self.listbox_code.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox_code.config(yscrollcommand=scrollbar.set)

        levels = list(self.server.users[name].keys())
        levels.sort()
        
        
        for level in levels:
            self.listbox_code.insert(tk.END, f" 레벨 {level}")

        # 우측 Text
        self.text_code = tk.Text(popup, wrap="word",
                                font=("Consolas", 20), 
                                bg="#1E1E1E", 
                                fg="#D4D4D4", )
        self.text_code.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def on_select_code(self,event):
        # 선택된 항목 확인
        selection = self.listbox_code.curselection()
        if selection:
            index = selection[0]
            value = self.listbox_code.get(index)
            value = str(value).replace('레벨','')
            value = value.replace(' ','')
            level = int(value)
            name  = self.code_sel_name
            code = self.server.users[name][level]['code']
            self.clear_code_msg()
            self.add_code_msg(code)
            
            # print(f"선택된 항목: {value}")
            
    def clear_code_msg(self,):
        self.text_code.config(state="normal")
        self.text_code.delete("1.0", tk.END)
        self.text_code.config(state="disabled")
        
    def add_code_msg(self,msg):
        self.text_code.config(state="normal")
        self.text_code.insert(tk.END, msg+"\n")
        self.text_code.config(state="disabled")
        
    def menu_action_level(self):
        selection = self.listbox.curselection()
        if selection:
            value = self.listbox.get(selection[0])
            value = str(value).replace(']','').split("[")
            # print(f"{value}")
            name = value[3]
            self.open_popup(name)
            
            # level = simpledialog.askinteger("레벨 입력", "레벨을 입력하세요:")
            # # print(level)
            # if level is not None:
            #     try:
            #         level = int(level)
            #         self.parent.server.send_client_level(name,level)
            #     except Exception as ex:
            #         print(ex)
                    
            #     messagebox.showinfo("입력 결과", f"입력한 숫자는 {num}입니다.")
            # else:
            #     messagebox.showwarning("입력 취소", "숫자 입력이 취소되었습니다.")
            
    def menu_action_remove_password(self): 
        if self.check_password('0000') is False:
            return       
        selection = self.listbox.curselection()
        if selection:
            value = self.listbox.get(selection[0])
            value = str(value).replace(']','').split("[")
            # print(f"{value}")
            name = value[3]
            if name in self.parent.server.login_dict:
                del self.parent.server.login_dict[name]
                self.parent.server.update_login_dic('w')
            
    def menu_action_remove(self):
        
        if self.check_password('0000') is False:
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
                        
                        self.parent.server.high_score_refresh()
                        self.refresh_listbox(self.high_score_dict)
                        
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
