

import tkinter as tk
from tkinter import scrolledtext
import tkinter.font as tkfont

import jedi
from pygments import lex
from pygments.lexers import PythonLexer
from pygments.token import Token
from pygments.styles import get_style_by_name

from editors.textnumbers import *
    
class EditorRanking:
    # from editor import PythonEditor
    def __init__(self,parent,frame):
        self.parent = parent
        self.frame = frame
        self.font_size = 16#self.parent.font_size
        # self.style = get_style_by_name("monokai")
        
        color = self.rgb_to_hex(208,223,211) 
        color_font = self.rgb_to_hex(36,53,40) 
        
        self.scroll_text()
        self.text.tag_configure("title", font=("malgungulim", 20,'bold'), foreground=color_font, background=color,justify='center')   
        self.text.tag_configure("highlight", font=("malgungulim", 20,'bold'), foreground=color_font, background=color,justify='center')   
        
        self.text.bind('<Shift-Return>', self.ignore_a_key)  
        self.text.bind("<MouseWheel>", self.on_ctrl_mousewheel) 
                    
    def on_ctrl_mousewheel(self,event):
        if event.state & 0x0004:  # Ctrl key mask
            delta = 1 if event.delta > 0 else -1
            self.font_size = max(8, self.font_size + delta)  # 최소 글꼴 크기 8
            if self.font_size > 30:
                self.font_size = 30
            self.text.configure(font=("malgungulim", self.font_size, "normal"))
        # else:
        #     print("Regular scroll")   
        
    def clear_msg(self,):
        self.text.config(state="normal")
        self.text.delete("1.0", tk.END)
        self.text.insert(tk.END, f"문제 [레벨:{self.parent.level} / {self.parent.last_level}]\n", "title")
        
        self.text.config(state="disabled")
        
    def add_highlight(self, msg):
        self.text.config(state="normal")
        self.text.insert(tk.END, msg+"\n", "highlight")
        self.text.config(state="disabled")
        
    def add_msg(self,msg):  
        self.text.config(state="normal")
        self.text.insert(tk.END, msg+"\n")  
        self.text.config(state="disabled")

        
    def set_bind_frame(self,ed_output):
        self.ed_output = ed_output
        
    def ignore_a_key(self,event):
        self.ed_output.run_code_thread()
        return "break"
    
    def scroll_both(self, action, position):
        self.text.yview_moveto(position)
    
    def update_scroll_both(self, first, last, type=None):
        self.text.yview_moveto(first)
        self.uniscrollbar.set(first, last)
        
    def refresh_listbox(self, data):
        self.add_highlight("순위")
        self.text.config(state="normal")
        self.text.delete("0.0", tk.END)
        # self.data = dict(sorted(self.data.items(), key=lambda x: x[1]['level'], reverse=True))
        self.high_score_dict = data
        # print(self.high_score_dict)
        keys = list(self.high_score_dict.keys())
        keys.sort()        
        
        for key in keys:
            value = self.high_score_dict[key]
            if value['name'] is not None:
                self.text.insert(tk.END, f" {int(key)+1}. [레벨: {int(value['score']):02}] [{value['name']}]\n")
        self.text.config(state="disabled")
        
    def scroll_text(self):

        self.uniscrollbar = tk.Scrollbar(self.frame, width=20, relief="flat")
        self.uniscrollbar.pack(side="right",fill="y", expand=0,padx=0, pady=(10, 10))       
        
        self.text = tk.Text(self.frame,  wrap=tk.WORD,
                            # width=100, height=22, 
                            font=("Consolas", 12),  undo=True,
                            bg="#410303", fg="#D4D4D4", insertbackground="white", relief="flat")
        self.text.config(font=("malgungulim", self.font_size))  # 기본: 영어
        self.text.configure(font=("malgungulim", self.font_size, "normal"))
        self.text.bind("<<Modified>>", self.on_text_modified)
        
        font = tkfont.Font(font=self.text['font'])
        tab = font.measure('    ')
        self.text.config(tabs=tab)
        self.text.config(spacing1=0, spacing2=1, spacing3=1)

        self.uniscrollbar["command"] = self.scroll_both
        self.text["yscrollcommand"] = self.update_scroll_both

        self.text.pack(side="right", fill="both",expand=1,padx=10, pady=(10, 10))
        
        
    def on_text_modified(self, event=None):
        self.text.edit_modified(False)  # 중요: 플래그 초기화
    
    def on_key_release(self, event=None):
        pass

    def rgb_to_hex(self,r, g, b):
        return f'#{r:02x}{g:02x}{b:02x}'
    