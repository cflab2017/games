

import tkinter as tk
from tkinter import scrolledtext
import tkinter.font as tkfont

import jedi
from pygments import lex
from pygments.lexers import PythonLexer
from pygments.token import Token
from pygments.styles import get_style_by_name

from editors.textnumbers import *
    
class EditorContent:
    # from editor import PythonEditor
    def __init__(self,parent,frame):
        self.parent = parent
        self.frame = frame
        # self.style = get_style_by_name("monokai")
        
        self.scroll_text()
        self.text.bind('<Shift-Return>', self.ignore_a_key)   
        self.text.tag_configure("title", font=("malgungulim", 16, "bold"), foreground="red", background="yellow",justify='center')   
        self.text.tag_configure("highlight", font=("malgungulim", 16, "bold"), foreground="blue", background="yellow",justify='center')   
        
        
        self.token_tags = {
            Token.Keyword: {"foreground": "#569CD6"},
            # Token.Name: {"foreground": "#9CDCFE"},
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
            
    def clear_msg(self,):
        self.text.config(state="normal")
        self.text.delete("1.0", tk.END)
        self.text.insert(tk.END, f"문제 [레벨:{self.parent.level}]\n", "title")
        
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
        
    def scroll_text(self):

        self.uniscrollbar = tk.Scrollbar(self.frame, width=20, relief="flat")
        self.uniscrollbar.pack(side="right",fill="y", expand=0,padx=10, pady=(10, 10))       
        
        self.text = tk.Text(self.frame,  wrap=tk.WORD,
                            # width=100, height=22, 
                            font=("Consolas", 12),  undo=True,
                            bg="#1E1E1E", fg="#D4D4D4", insertbackground="white", relief="flat")
        self.text.config(font=("malgungulim", 16, "bold"))  # 기본: 영어
        self.text.configure(font=("malgungulim", 16, "normal", "bold"))
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
        # self.highlight_code()
    
    def on_key_release(self, event=None):
        pass
        # self.highlight_code()

    # def highlight_code(self):
    #     code = self.text.get("1.0", tk.END)
    #     self.text.tag_remove("Token", "1.0", tk.END)
    #     for tag in self.token_tags:
    #         self.text.tag_remove(str(tag), "1.0", tk.END)

    #     idx = "1.0"
    #     for token, content in lex(code, PythonLexer()):
    #         end_idx = self.text.index(f"{idx}+{len(content)}c")
    #         self.text.tag_add(str(token), idx, end_idx)
    #         idx = end_idx
    
    # def highlight_code(self, event=None):
    #     code = self.text.get("1.0", tk.END)
    #     self.text.tag_remove("Token", "1.0", tk.END)
    #     for tag in self.token_tags:
    #         self.text.tag_remove(str(tag), "1.0", tk.END)

    #     index = "1.0"
    #     for token, content in lex(code, PythonLexer()):
    #         # 토큰이 비어있으면 스킵
    #         if not content.strip():
    #             index = self.text.index(f"{index}+{len(content)}c")
    #             continue

    #         lines = content.split('\n')
    #         for i, line in enumerate(lines):
    #             if line:
    #                 start_idx = index
    #                 end_idx = self.text.index(f"{start_idx}+{len(line)}c")
    #                 if token in self.token_tags:
    #                     self.text.tag_add(str(token), start_idx, end_idx)
    #                 index = end_idx

    #             if i < len(lines) - 1:
    #                 index = self.text.index(f"{index} +1line linestart")

    def highlight_code(self, event=None):
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
    
    def show_autocomplete(self, event=None):
        index = self.text.index(tk.INSERT)
        row, col = map(int, index.split("."))
        code = self.text.get("1.0", tk.END)

        try:
            script = jedi.Script(code)
            completions = script.complete(line=row, column=col)
        except Exception:
            return

        if not completions:
            return

        popup = tk.Toplevel(self.frame)
        popup.overrideredirect(True)
        popup.geometry(f"+{self.frame.winfo_pointerx()}+{self.frame.winfo_pointery()}")

        listbox = tk.Listbox(popup, font=("Consolas", 12), height=min(6, len(completions)))
        listbox.pack()

        for c in completions:
            listbox.insert(tk.END, c.name)

        def insert_completion(event):
            selected = listbox.get(tk.ACTIVE)
            self.text.insert(tk.INSERT, selected)
            popup.destroy()

        listbox.bind("<Return>", insert_completion)
        listbox.bind("<Escape>", lambda e: popup.destroy())
        listbox.focus_set()