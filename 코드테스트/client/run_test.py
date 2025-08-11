import tkinter as tk


if __name__ == "__main__":
    from editor import PythonEditor
    root = tk.Tk()
    app = PythonEditor(root,'127.0.0.1')
    root.mainloop()