

import tkinter as tk

import tkinter.font as tkfont

import jedi
from pygments import lex
from pygments.lexers import PythonLexer
from pygments.token import Token
from pygments.styles import get_style_by_name

from editors.textnumbers import *
class PopupCode:
    code_level = -1
    def __init__(self, parent,is_correct):
        self.parent = parent
        self.client = self.parent.client
        
        self.font_size = self.parent.font_size
        name = parent.name
        self.is_correct = is_correct
        self.code_sel_name = name
        self.popup = tk.Toplevel(self.parent.root)
        if self.is_correct:
            self.popup.title(f"정답 코드 확인")
        else:
            self.popup.title(f"{name}님의 코드 제출 결과")
        self.popup.geometry("800x800")
        self.popup.attributes('-topmost', True)
        
        # 좌측 Listbox
        list_frame = tk.Frame(self.popup, width = 150)
        list_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)    
        list_frame.pack_propagate(False)

        self.listbox_code = tk.Listbox(list_frame,
                                font=("Consolas", self.font_size), 
                                bg="#1E1E1E", 
                                fg="#D4D4D4", )
        
        self.listbox_code.bind('<<ListboxSelect>>', self.on_select_code)
        self.listbox_code.pack(side=tk.LEFT, fill=tk.Y)

        # 스크롤바 연결
        scrollbar = tk.Scrollbar(list_frame, orient="vertical", command=self.listbox_code.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox_code.config(yscrollcommand=scrollbar.set)

        # for level in self.server.users[name]:
        #     self.listbox_code.insert(tk.END, f"레벨 {level}")

        # 우측 Text
        # self.text = tk.Text(self.popup, wrap="word",
        #                         font=("Consolas", 20), 
        #                         bg="#1E1E1E", 
        #                         fg="#D4D4D4", )
        # self.text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.scroll_text()
        
        
        self.token_tags = {
            Token.Keyword: {"foreground": "#569CD6"},
            Token.Name: {"foreground": "#9CDCFE"},
            Token.Name.Variable: {"foreground": "#569CD6"},
            Token.Name.Function: {"foreground": "#DCDCAA"},
            Token.Name.Class: {"foreground": "#4EC9B0"},
            Token.Comment: {"foreground": "#6A9955"},
            Token.String: {"foreground": "#CE9178"},
            Token.Number: {"foreground": "#B5CEA8"},
            Token.Operator: {"foreground": "#D4D4D4"},
            Token.Name.Builtin: {"foreground": "#C586C0"},
        }
        for tag, conf in self.token_tags.items():
            self.text.tag_configure(str(tag), **conf)
        
        self.client.send_request_complete_level(level=0,is_correct = is_correct)
    
    def scroll_both(self, action, position):
        self.text.yview_moveto(position)
        self.linenumber.yview_moveto(position)
    
    def update_scroll_both(self, first, last, type=None):
        self.text.yview_moveto(first)
        self.linenumber.yview_moveto(first)
        self.uniscrollbar.set(first, last)
        
    def scroll_text(self):

        self.uniscrollbar = tk.Scrollbar(self.popup, width=20, relief="flat")
        self.uniscrollbar.pack(side="right",fill="y", expand=0,padx=0, pady=(10, 10))       
        
        
        
        self.text = tk.Text(self.popup,  wrap=tk.WORD,
                            # width=5, 
                            height=22, font=("Consolas", self.font_size),  undo=True,   
                            bg="#1E1E1E", fg="#D4D4D4", insertbackground="white", relief="flat")
        
        self.number_widget()
        
        
        self.text.config(font=("malgungulim", self.font_size))  # 기본: 영어
        self.text.configure(font=("malgungulim", self.font_size, "normal"))
        self.text.bind("<KeyRelease>", self.on_key_release)
        # self.text.bind("<Control-space>", self.show_autocomplete)
        self.text.bind("<<Modified>>", self.on_text_modified)
        
        font = tkfont.Font(font=self.text['font'])
        tab = font.measure('    ')
        self.text.config(tabs=tab)
        self.text.config(spacing1=0, spacing2=1, spacing3=1)


        self.uniscrollbar["command"] = self.scroll_both
        self.text["yscrollcommand"] = self.update_scroll_both
        self.text.pack(side="left", fill="both", expand=1,padx=0, pady=(10, 10))

        
    def number_widget(self):
        pass
        self.linenumber = TextNumbers(self.popup, self.text,  width=20,relief="flat", state="disabled", justify="right",)
        self.linenumber.configure(font=("malgungulim", self.font_size, "normal"))
        self.linenumber.configure(bg="#1E1E1E", fg="#D4D4D4")

        self.uniscrollbar["command"] = self.scroll_both
        self.linenumber["yscrollcommand"] = self.update_scroll_both
        self.linenumber.pack(side="left", fill="both", expand=1,padx=0, pady=(10, 10))
        
    def on_text_modified(self, event=None):
        self.text.edit_modified(False)  # 중요: 플래그 초기화
        self.highlight_code()
    
    def on_key_release(self, event=None):
        self.highlight_code()

    def highlight_code(self, event=None):
        self.linenumber.update_num_list()
        code = self.text.get("1.0", tk.END)

        # ✅ 첫 줄이 \n만 있는 경우 보정
        codetemp = code.split('\n')
        if len(codetemp[0])==0 and len(codetemp)>1:
            code = " " + code
            self.text.insert("1.0", " ")
        if len(codetemp[0])>1 and len(codetemp)>1:
            if codetemp[0][0]==' ':
                self.text.delete("1.0", "1.1")
                # print('aaaaa')

        code = code.rstrip()
        if not code.strip():
            self.text.tag_remove("Token", "1.0", tk.END)
            return

        self.text.mark_set("range_start", "1.0")
        self.text.tag_remove("Token", "1.0", tk.END)
        
        for tag in self.token_tags:
            self.text.tag_remove(str(tag), "1.0", tk.END)
        self.text.tag_remove("DefinedVariable", "1.0", tk.END)
            
        # 기본 하이라이팅
        for token, content in lex(code, PythonLexer()):
            self.text.mark_set("range_end", f"range_start + {len(content)}c")
            if token in self.token_tags:
                self.text.tag_add(str(token), "range_start", "range_end")
            self.text.mark_set("range_start", "range_end")

        # 변수 목록 추출 (jedi 사용)
        try:
            script = jedi.Script(code)
            definitions = script.get_names(all_scopes=True, definitions=True)
            variables = [d for d in definitions if d.type == 'statement']
            variable_names = set(d.name for d in variables)
        except Exception:
            variable_names = set()

        # 변수 색 적용
        for var_name in variable_names:
            start = "1.0"
            while True:
                pos = self.text.search(rf'\y{var_name}\y', start, tk.END, regexp=True)
                if not pos:
                    break
                end = f"{pos}+{len(var_name)}c"
                self.text.tag_add("DefinedVariable", pos, end)
                if pos == end:
                    break  # 무한 루프 방지
                start = end

        # 변수 색상 정의
        self.text.tag_configure("DefinedVariable", foreground="#9CDCFE")  # VSCode 하늘색
        
    def levels_code_list(self, levels):        
        self.listbox_code.delete(0, tk.END)  # 기존 항목 제거
        levels.sort()
        for level in levels:
            self.listbox_code.insert(tk.END, f"레벨 {level}")
            
    def on_select_code(self,event):
        selection = self.listbox_code.curselection()
        if selection:
            index = selection[0]
            value = self.listbox_code.get(index)
            value = str(value).replace('레벨','')
            value = value.replace(' ','')
            level = int(value)
            print(level,self.code_level)
            if self.code_level == level:
                # print('pass')
                return
            
            self.code_level = level
            name  = self.code_sel_name
            # code = self.server.users[name][level]['code']
            self.clear_code_msg()
            self.client.send_request_complete_level(level,self.is_correct)
            # self.add_code_msg(code)            
            # print(f"선택된 항목: {value}")
            
    def clear_code_msg(self):
        self.text.config(state="normal")
        self.text.delete("1.0", tk.END)
        self.text.config(state="disabled")
        
    def add_code_msg(self,msg):
        self.text.config(state="normal")
        self.text.insert(tk.END, msg+"\n")
        self.text.config(state="disabled")