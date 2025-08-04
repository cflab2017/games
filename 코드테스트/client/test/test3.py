import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
from tkinter import filedialog
from pygments import lex
from pygments.lexers import PythonLexer
from pygments.styles import get_style_by_name
from pygments.token import Token
import sys
import io

class PythonEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Python 코드 에디터 (VSCode 스타일)")
        self.root.geometry("900x600")
        self.style = get_style_by_name("monokai")

        # 에디터 프레임
        self.text = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Consolas", 13), undo=True, background="#272822", foreground="white", insertbackground="white")
        self.text.pack(expand=True, fill=tk.BOTH)

        # 실행 결과 출력창
        self.output = tk.Text(root, height=10, bg="#1e1e1e", fg="white", font=("Consolas", 11), state=tk.DISABLED)
        self.output.pack(fill=tk.BOTH)

        # 버튼 프레임
        button_frame = tk.Frame(root, bg="#1e1e1e")
        button_frame.pack(fill=tk.X)

        run_btn = tk.Button(button_frame, text="▶ 실행", command=self.run_code, bg="#007acc", fg="white", padx=10)
        run_btn.pack(side=tk.LEFT, padx=5, pady=5)

        open_btn = tk.Button(button_frame, text="📂 열기", command=self.open_file, bg="#333", fg="white")
        open_btn.pack(side=tk.LEFT, padx=5)

        save_btn = tk.Button(button_frame, text="💾 저장", command=self.save_file, bg="#333", fg="white")
        save_btn.pack(side=tk.LEFT, padx=5)

        # 키 입력 시 하이라이팅
        self.text.bind('<KeyRelease>', self.on_key_release)

    def on_key_release(self, event=None):
        self.highlight()

    def highlight(self):
        code = self.text.get("1.0", tk.END)
        self.text.mark_set("range_start", "1.0")
        self.text.tag_remove("Token", "1.0", tk.END)

        for token, content in lex(code, PythonLexer()):
            self.text.mark_set("range_end", "range_start + %dc" % len(content))
            self.text.tag_add(str(token), "range_start", "range_end")
            self.text.mark_set("range_start", "range_end")

        for ttype, style in self.style:
            if style['color']:
                self.text.tag_configure(str(ttype), foreground="#" + style['color'])

    def run_code(self):
        code = self.text.get("1.0", tk.END)
        old_stdout = sys.stdout
        redirected_output = sys.stdout = io.StringIO()

        try:
            exec(code, {})
            result = redirected_output.getvalue()
        except Exception as e:
            result = str(e)

        sys.stdout = old_stdout
        self.output.config(state=tk.NORMAL)
        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, result)
        self.output.config(state=tk.DISABLED)

    def open_file(self):
        path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
        if path:
            with open(path, "r", encoding="utf-8") as file:
                self.text.delete("1.0", tk.END)
                self.text.insert(tk.END, file.read())
            self.highlight()

    def save_file(self):
        path = filedialog.asksaveasfilename(defaultextension=".py", filetypes=[("Python Files", "*.py")])
        if path:
            with open(path, "w", encoding="utf-8") as file:
                file.write(self.text.get("1.0", tk.END))


if __name__ == "__main__":
    root = tk.Tk()
    app = PythonEditor(root)
    root.mainloop()
