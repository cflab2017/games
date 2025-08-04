import tkinter as tk
from tkinter import scrolledtext
import tkinter.font as tkfont
from pygments import lex
from pygments.lexers import PythonLexer
from pygments.token import Token
import jedi
import sys
import threading
import queue

class TextNumbers(tk.Listbox):
    def __init__(self, master, textwidget, **options):
        super().__init__(master, **options)

        self.textwidget = textwidget
        self.textwidget.bind("<Return>", self.update_num_list)
        self.textwidget.bind("<BackSpace>", self.update_num_list)
    
        self.number_var = tk.Variable(self, value=["1"])

        self.configure(listvariable=self.number_var, selectmode=tk.SINGLE)
        self.set_width(1)
        self.set_font()

    def set_font(self):
        font = self.textwidget.cget("font")
        self.configure(font = font)

    def set_width(self, num_len):
        self.configure(width=num_len+1)

    def update_num_list(self, event):
        linenums = self.get_num_lines()
        current_column = self.get_current_colomn()
        
        if current_column != 0 and event.keycode != 13: return
        number_list = list(range(1, linenums)) if event.keycode == 13 else list(range(1, linenums-1))

        self.set_width(len(str(linenums)))
        self.number_var.set(number_list)
        self.yview("end")
        
    def get_num_lines(self):
        num_lines = int(self.textwidget.index("end").split(".")[0])
        return (num_lines)

    def get_current_colomn(self):
        curr_column = int(self.textwidget.index("insert").split(".")[1])
        return (curr_column)

class StdoutRedirector:
    def __init__(self, widget):
        self.widget = widget

    def write(self, string):
        self.widget.insert(tk.END, string)
        self.widget.see(tk.END)
        self.widget.update()

    def flush(self):
        pass

class PythonEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("파이썬 코드 에디터 (입력/출력 포함)")

        root.bind('<Shift-Return>', self.run_code_thread)
        
        self.input_mode = False
        self.input_prompt = ""
        self.input_response = ""
        self.input_ready = threading.Event()

        self.frame1=tk.Frame(self.root, width=140,relief="solid", bd=1)
        self.frame1.pack(padx=10, pady=(10, 0), fill="both", expand=1)
 
        self.scroll_text()
        self.number_widget()
        
        self.frame2=tk.Frame(self.root, width=140,relief="solid", bd=0)
        self.frame2.pack(padx=10, pady=(10, 0), fill="both")        
        # 실행 버튼
        run_btn = tk.Button(self.frame2, text="▶ 실행", command=self.run_code_thread)
        run_btn.pack(side="right", fill="none", expand='YES')
        
        
        self.frame3=tk.Frame(self.root, width=140,relief="solid", bd=1)
        self.frame3.pack(padx=10, pady=(10, 0), fill="both", expand=0)
        # self.frame3.pack()
        
        self.output = scrolledtext.ScrolledText(
            self.frame3, width=100, height=22, font=("malgungulim", 12), undo=True,
            bg="#1E1E1E", fg="#D4D4D4", insertbackground="white"
        )
        self.output.pack(padx=10, pady=(0, 10), fill="both")
        # self.output.pack(side="left", fill="y", expand=1)
        # self.output.pack(fill="both", expand=1)
        self.output.bind("<Return>", self.capture_input)

        self.token_tags = {
            Token.Keyword: {"foreground": "#569CD6"},
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
        
    def scroll_both(self, action, position):
        self.text.yview_moveto(position)
        self.linenumber.yview_moveto(position)
    
    def update_scroll_both(self, first, last, type=None):
        self.text.yview_moveto(first)
        self.linenumber.yview_moveto(first)
        self.uniscrollbar.set(first, last)
        
    def scroll_text(self):

        self.uniscrollbar = tk.Scrollbar(self.frame1, width=20, relief="flat")
        self.uniscrollbar.pack(side="right",fill="y", expand=0,padx=10, pady=(10, 0))       
        # 코드 입력 영역
        # self.text = scrolledtext.ScrolledText(
        #     self.frame1, width=100, height=22, font=("malgungulim", 12), undo=True,
        #     bg="#1E1E1E", fg="#D4D4D4", insertbackground="white", relief="flat"
        # )
        self.text = tk.Text(self.frame1,  
                            width=100, height=22, font=("malgungulim", 12),  undo=True,
                            bg="#1E1E1E", fg="#D4D4D4", insertbackground="white", relief="flat")
        self.text.bind("<KeyRelease>", self.on_key_release)
        self.text.bind("<Control-space>", self.show_autocomplete)
        
        font = tkfont.Font(font=self.text['font'])
        tab = font.measure('    ')
        self.text.config(tabs=tab)
        # self.text.bind("<Tab>", self.tab_pressed)
        self.text.config(spacing1=0, spacing2=1, spacing3=1)
        
        # self.text = tk.Text(self.root, relief="flat")

        self.uniscrollbar["command"] = self.scroll_both
        self.text["yscrollcommand"] = self.update_scroll_both

        self.text.pack(side="right", fill="both", expand=1,padx=10, pady=(10, 0))
        # self.text.pack(padx=10, pady=(10, 0))
        
    def number_widget(self):
        self.linenumber = TextNumbers(self.frame1, self.text,  width=20,relief="flat", state="disabled", justify="right",)

        self.uniscrollbar["command"] = self.scroll_both
        self.linenumber["yscrollcommand"] = self.update_scroll_both
        self.linenumber.pack(side="right", fill="y", expand=0,padx=00, pady=(10, 0))
        
    def tab_pressed(self,event:tk.Event) -> str:
        # Insert the 4 spaces
        self.text.insert("insert", " "*4)
        # Prevent the default tkinter behaviour
        return "break"

    def on_key_release(self, event=None):
        self.highlight_code()

    def highlight_code(self):
        code = self.text.get("1.0", tk.END)
        self.text.tag_remove("Token", "1.0", tk.END)
        for tag in self.token_tags:
            self.text.tag_remove(str(tag), "1.0", tk.END)

        idx = "1.0"
        for token, content in lex(code, PythonLexer()):
            end_idx = self.text.index(f"{idx}+{len(content)}c")
            self.text.tag_add(str(token), idx, end_idx)
            idx = end_idx

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

        popup = tk.Toplevel(self.root)
        popup.overrideredirect(True)
        popup.geometry(f"+{self.root.winfo_pointerx()}+{self.root.winfo_pointery()}")

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

    def run_code_thread(self,event=None):
        threading.Thread(target=self.run_code, daemon=True).start()

    def run_code(self):
        code = self.text.get("1.0", tk.END)
        self.output.delete("1.0", tk.END)

        # stdout redirect
        sys.stdout = StdoutRedirector(self.output)
        sys.stderr = StdoutRedirector(self.output)

        # input 대체 함수
        def editor_input(prompt="입력: "):
            self.input_mode = True
            self.input_prompt = prompt
            print(prompt, end="")
            self.input_ready.clear()
            self.input_ready.wait()  # 사용자 입력 기다림
            return self.input_response

        try:
            exec(code, {"input": editor_input})
        except Exception as e:
            print("오류:", e)
        finally:
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__
            self.input_mode = False

    def capture_input(self, event=None):
        if self.input_mode:
            last_line = self.output.get("end-2l", "end-1c").split(self.input_prompt)[-1]
            self.input_response = last_line.strip()
            self.input_ready.set()
            self.output.insert(tk.END, "\n")
            return "break"

if __name__ == "__main__":
    root = tk.Tk()
    app = PythonEditor(root)
    root.mainloop()
