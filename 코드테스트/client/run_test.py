import tkinter as tk


if __name__ == "__main__":
    from editor import PythonEditor
    app = PythonEditor('127.0.0.1')
    app.root.mainloop()