
import tkinter as tk

class StdoutRedirector:
    def __init__(self, widget:list):
        self.widget = widget

    def write(self, string):
        self.widget.append(string)

    def flush(self):
        pass