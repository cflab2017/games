
import tkinter as tk

class StdoutRedirector:
    def __init__(self, widget):
        self.widget = widget

    def write(self, string):
        self.widget.insert(tk.END, string)
        self.widget.see(tk.END)
        self.widget.update()

    def flush(self):
        pass