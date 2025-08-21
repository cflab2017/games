
import tkinter as tk

class TextNumbers(tk.Listbox):
    def __init__(self, master, textwidget, **options):
        super().__init__(master, **options)

        self.textwidget = textwidget
        self.textwidget.bind("<Return>", self.update_num_list)
        self.textwidget.bind("<BackSpace>", self.update_num_list)
        
        self.textwidget.bind("<<Modified>>", self.update_num_list)
    
        self.number_var = tk.Variable(self, value=["1"])

        self.configure(listvariable=self.number_var, selectmode=tk.SINGLE)
        self.set_width(1)
        self.set_font()
        

    def set_font(self):
        font = self.textwidget.cget("font")
        self.configure(font = font)

    def set_width(self, num_len):
        self.configure(width=num_len+1)

    def update_num_list(self, event=None):
        linenums = self.get_num_lines()
        if event is not None:
            current_column = self.get_current_colomn()
            
            # if current_column != 0 and event.keycode != 13: return
            number_list = list(range(1, linenums)) if event.keycode == 13 else list(range(1, linenums-1))
        else:
            number_list = list(range(1, linenums))

        self.set_width(len(str(linenums)))
        self.number_var.set(number_list)
        self.yview("end")
        
    def get_num_lines(self):
        num_lines = int(self.textwidget.index("end").split(".")[0])
        return (num_lines)

    def get_current_colomn(self):
        curr_column = int(self.textwidget.index("insert").split(".")[1])
        return (curr_column)