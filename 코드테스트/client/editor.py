import tkinter as tk
from tkinter import scrolledtext
import tkinter.font as tkfont


from editors.editor_input import *
from editors.editor_output import *
from editors.editor_content import *
from editors.toolbar import *

from commu.client import *
from login.account import *

class PythonEditor:
    from login.account import Account
    
    def __init__(self, root):
        self.root = root
        self.root.title("파이썬 코드 에디터 (입력/출력 포함)")    
        
        self.level = 1   

        self.client = socketClient(self)
        # cli.run()
    
        account = Account()
        self.name, self.isRun = account.run(self.client)
        if self.isRun == False:
            return
        
        self.frame1=tk.Frame(self.root, width=140,relief="solid", bd=1)
        self.frame1.pack(padx=10, pady=(10, 0), fill="both", expand=1) 
        
        self.frame2=tk.Frame(self.root, width=140,relief="solid", bd=1)
        self.frame2.pack(padx=10, pady=(10, 0), fill="both")        
        
        self.frame3=tk.Frame(self.root, width=140,relief="solid", bd=1)
        self.frame3.pack(padx=10, pady=(10, 0), fill="both", expand=0)
        
        
        self.frame3_1=tk.Frame(self.frame3, relief="solid", bd=1)
        self.frame3_1.pack(side="left", fill="both", expand=1,padx=10, pady=(10, 0))
        
        self.frame3_2=tk.Frame(self.frame3, relief="solid", bd=1)
        self.frame3_2.pack(side="right", fill="both", expand=1,padx=10, pady=(10, 0))
        
        self.ed_input = EditorInput(self.frame1)
        self.ed_output = EditorOutput(self.frame3_1,self.ed_input)
        self.ed_content = EditorContent(self.frame3_2)
        self.toolbar = ToolBar(self.frame2,self.ed_output)
        
        self.ed_input.set_bind_frame(self.ed_output)
        self.ed_output.set_client(self.client)
        self.client.set_bind_output(self.ed_output)
        self.client.set_bind_content(self.ed_content)
        self.client.set_bind_input(self.ed_input)
        
        self.client.send_request('start')
        


if __name__ == "__main__":
    root = tk.Tk()
    app = PythonEditor(root)
    if app.isRun:
        root.mainloop()
