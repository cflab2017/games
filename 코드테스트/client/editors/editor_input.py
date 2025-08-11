

import os
import tkinter as tk
from tkinter import scrolledtext
import tkinter.font as tkfont


try:
    import jedi
except:
    os.system('pip install jedi')
    import jedi
    
try:
    import pygments
except:
    os.system('pip install pygments')
    import pygments
    
import winsound  # 윈도우 전용
from _thread import *
import time as ott

from pygments import lex
from pygments.lexers import PythonLexer
from pygments.token import Token
from pygments.styles import get_style_by_name

from editors.textnumbers import *
# 1옥타브: C, C#, D, D#, E, F, F#, G, G#, A, A#, B
pitch = {'c_': 523, 'cs': 554, 'd_': 587, 'ds': 622, 'e_': 659,
         'f_': 698, 'fs': 740, 'g_': 784, 'gs': 831, 'a_': 880,
         'as': 932, 'b_': 988}
lasting = 40

class EditorInput:
    # from editor import PythonEditor
    play_memody = []
    def __init__(self,parent,frame):
        self.frame = frame
        self.parent = parent
        self.font_size = self.parent.font_size
        # self.style = get_style_by_name("monokai")
        
        self.scroll_text()
        self.number_widget()
        self.text.bind('<Shift-Return>', self.ignore_shift_enter_key)
        self.text.bind('<Alt-Return>', self.ignore_alt_enter_key)
        self.text.bind("<Key>", self.key_sound)
        self.text.bind("<KeyPress-BackSpace>", self.on_backspace)  # Backspace
        self.text.bind("<Delete>", self.on_delete_key)              # Delete 키
        self.text.bind("<Control-a>", self.on_ctrl_a)               # Ctrl+A 전체 선택
        self.text.bind("<MouseWheel>", self.on_ctrl_mousewheel) 

        color = self.rgb_to_hex(208,223,211) 
        color_font = self.rgb_to_hex(36,53,40) 
        
        self.text.tag_configure("highlight", font=("malgungulim", self.font_size,'bold'), foreground=color_font, background=color,justify='center')   
        
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
            
        
        start_new_thread(self.thread_play, (self.play_memody, ))
        self.ini_input_value()
        
            
    def on_ctrl_mousewheel(self,event):
        if event.state & 0x0004:  # Ctrl key mask
            delta = 1 if event.delta > 0 else -1
            self.font_size = max(8, self.font_size + delta)  # 최소 글꼴 크기 8
            if self.font_size > 30:
                self.font_size = 30
            self.text.configure(font=("malgungulim", self.font_size, "normal"))
        # else:
        #     print("Regular scroll")   
        
    def ini_input_value(self):
        self.clear_msg()
        self.add_msg("#코드를 여기에 작성하세요")
        self.set_focus()
        
    def on_backspace(self,event):
        # 현재 커서 위치가 첫 줄이라면 삭제 막기
        idx = self.text.index(tk.INSERT)  # 현재 커서 위치 (ex: '1.0', '2.3')
        line, col = map(int, idx.split('.'))
        if line == 1 or (line==2 and col == 0):
            return "break"  # 이벤트 차단(Backspace 무시)

    def on_delete(self,event):
        # 삭제 키도 첫 줄에서 막기 (선택 삭제 등)
        try:
            start = self.text.index("sel.first")
            line, col = map(int, start.split('.'))
            # print(line)
            if line == 1:
                # 선택 영역에 첫 줄 포함되면 삭제 못 하게 막기
                # return "break"
                self.ini_input_value()
        except tk.TclError:
            # 선택 영역 없으면 무시
            pass

    def on_ctrl_a(self,event):
        # Ctrl + A 처리 (전체 선택)
        self.text.tag_add(tk.SEL, "1.0", tk.END)
        return "break"

    def on_delete_key(self,event):
        # Delete 키도 첫 줄 포함 선택 삭제 못 하게 막기
        return self.on_delete(event)
        
    def add_highlight(self, msg):
        self.clear_msg()
        self.text.insert(tk.END, msg+"\n", "highlight")
        self.text.insert(tk.END, "\n")
        
    def thread_play(self,play_memody):
        
        while True:
            ott.sleep(0.1)
            if len(play_memody):
                # print(play_memody)
                for memody in play_memody:
                    winsound.Beep(pitch[memody], lasting)
                    # self.key_sound(memody)
                play_memody.clear()
                
    def key_sound(self,event):
        # keycode를 기반으로 주파수 생성 (100~2000Hz 범위)
        # freq = 200 + (event.keycode * 10) % 1800
        # winsound.Beep(freq, 50)  # 0.05초 재생
        # print(f"키: {event.keysym}, 코드: {event.keycode}, 주파수: {freq}Hz")
        self.play_memody.append('g_')
        
    def set_bind_output(self,ed_output):
        self.ed_output = ed_output
        
    def clear_msg(self):
        self.text.delete("1.0", tk.END)

    def add_msg(self,msg:str):
        if msg.find('코드를')>-1:
            self.add_highlight(msg)
        else:
            self.text.insert(tk.END, msg+"\n")
    
    def rgb_to_hex(self,r, g, b):
        return f'#{r:02x}{g:02x}{b:02x}'
    
    def set_focus(self):        
        self.text.see(tk.END)              # 스크롤을 마지막으로 이동
        self.text.mark_set("insert", tk.END)  # 커서를 마지막 위치로 이동
        self.text.focus()                  # 포커스 주기 (필요 시)
                        
    def ignore_shift_enter_key(self,event):
        self.ed_output.run_code_thread()
        return "break"
    
    def ignore_alt_enter_key(self,event):
        self.ed_output.only_run_code_thread()
        return "break"
    
    def scroll_both(self, action, position):
        self.text.yview_moveto(position)
        self.linenumber.yview_moveto(position)
    
    def update_scroll_both(self, first, last, type=None):
        self.text.yview_moveto(first)
        self.linenumber.yview_moveto(first)
        self.uniscrollbar.set(first, last)
        
    def scroll_text(self):

        self.uniscrollbar = tk.Scrollbar(self.frame, width=20, relief="flat")
        self.uniscrollbar.pack(side="right",fill="y", expand=0,padx=0, pady=(10, 10))       
        
        self.text = tk.Text(self.frame,  wrap=tk.WORD,
                            # width=5, 
                            height=22, font=("Consolas", 12),  undo=True,
   
                            bg="#1E1E1E", fg="#D4D4D4", insertbackground="white", relief="flat")
        self.text.config(font=("malgungulim", 16))  # 기본: 영어
        self.text.configure(font=("malgungulim", 16, "normal"))
        self.text.bind("<KeyRelease>", self.on_key_release)
        self.text.bind("<Control-space>", self.show_autocomplete)
        self.text.bind("<<Modified>>", self.on_text_modified)
        
        font = tkfont.Font(font=self.text['font'])
        tab = font.measure('    ')
        self.text.config(tabs=tab)
        self.text.config(spacing1=0, spacing2=1, spacing3=1)

        self.uniscrollbar["command"] = self.scroll_both
        self.text["yscrollcommand"] = self.update_scroll_both

        self.text.pack(side="left", fill="both", expand=1,padx=10, pady=(10, 10))
        
    def number_widget(self):
        pass
        self.linenumber = TextNumbers(self.frame, self.text,  width=20,relief="flat", state="disabled", justify="right",)

        self.uniscrollbar["command"] = self.scroll_both
        self.linenumber["yscrollcommand"] = self.update_scroll_both
        self.linenumber.pack(side="right", fill="y", expand=0,padx=00, pady=(10, 0))
        
    def on_text_modified(self, event=None):
        self.text.edit_modified(False)  # 중요: 플래그 초기화
        self.highlight_code()
    
    def on_key_release(self, event=None):
        self.highlight_code()

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
            
            # print(code, row,col)
            # delete_start = f"{row}.{0}"
            delete_start = f"{row}.0"
            delete_end = f"{row}.end"  # 현재 줄의 끝까지만 삭제
            self.text.delete(delete_start, delete_end)
            
            # cursor_index = self.text.index(tk.INSERT)
            # line_number = cursor_index.split('.')[0]

            # # 해당 줄의 텍스트 가져오기
            # line_start = f"{line_number}.0"
            # line_end = f"{line_number}.end"
            # line_text = self.text.get(line_start, line_end)

            # # 마지막 공백 위치 찾기
            # last_space_pos = line_text.rfind(" ")

            # if last_space_pos != -1:
            #     # 공백 앞 단어 삭제
            #     word_start = line_text.rfind(" ", 0, last_space_pos - 1) + 1
            #     delete_start = f"{line_number}.{word_start}"
            #     delete_end = f"{line_number}.{last_space_pos}"
            #     self.text.delete(delete_start, delete_end)

            #     # 공백 다음 위치에 삽입
            #     insert_index = f"{line_number}.{last_space_pos + 1}"
            # else:
            #     # 공백이 없으면 줄 전체 삭제 후 맨 앞에 삽입
            #     self.text.delete(line_start, line_end)
            #     insert_index = f"{line_number}.0"

            self.text.insert(delete_start, selected)
            # self.text.insert(tk.INSERT, selected)
            popup.destroy()

        listbox.bind("<Return>", insert_completion)
        listbox.bind("<Escape>", lambda e: popup.destroy())
        listbox.focus_set()