import tkinter as tk
from tkinter import scrolledtext
import tkinter.font as tkfont


from editors.editor_input import *
from editors.editor_connect import *
from editors.editor_highscore import *
from editors.toolbar import *

from commu.server import *

class PythonEditor:

    def __init__(self, root, host = None):
        self.root = root
        self.root.title("파이썬 코드 에디터 (입력/출력 포함)")    
        
        self.level = 1   
        self.name = 'joseph'

        # cli.run()
    
        self.frame1=tk.Frame(self.root, width=140,relief="solid", bd=1)
        self.frame1.pack(padx=10, pady=(10, 0), fill="both", expand=1) 
        
        self.frame2=tk.Frame(self.root, width=140,relief="solid", bd=1)
        self.frame2.pack(padx=10, pady=(10, 0), fill="both")        
        
        self.frame3=tk.Frame(self.root, width=140,relief="solid", bd=1)
        self.frame3.pack(padx=10, pady=(10, 0), fill="both", expand=1)
        
        
        self.frame3_1=tk.Frame(self.frame3, relief="solid", bd=1)
        self.frame3_1.pack(side="left", fill="both", expand=1,padx=10, pady=(10, 0))
        
        self.frame3_2=tk.Frame(self.frame3, relief="solid", bd=1)
        self.frame3_2.pack(side="right", fill="both", expand=1,padx=10, pady=(10, 0))
        
        self.ed_input = EditorInput(self.frame1)
        self.ed_connect = EditorConnect(self.frame3_1,self.ed_input)
        self.ed_highscore = EditorHighScore(self,self.frame3_2)
        self.toolbar = ToolBar(self.frame2,self.ed_connect)
        
        self.server = socketServer(self.ed_input,host)
        self.ed_input.set_bind_frame(self.ed_connect)
        # self.ed_output.set_client(self.client)
        self.server.set_bind_input(self.ed_input)
        self.server.set_bind_toolbar(self.toolbar)
        self.server.set_bind_output(self.ed_connect)
        self.server.set_bind_score(self.ed_highscore)
        
        # self.client.send_request(self.name,'start')
        

if __name__ == "__main__":
    root = tk.Tk()
    app = PythonEditor(root)
    root.mainloop()
