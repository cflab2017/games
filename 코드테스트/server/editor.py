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
        root.geometry("900x900")
        self.root.title("코딩나우 코딩연습")  
        
        self.level = 1   
        self.name = 'joseph'

        # cli.run()
    
        self.frame0=tk.Frame(self.root,relief="solid", bd=1)
        self.frame0.pack(padx=0, pady=(0, 0), fill="both")    
        # self.frame2.pack_propagate(False)    
        self.toolbar = ToolBar(self.frame0)
        
        self.frame1=tk.Frame(self.root,relief="solid", bd=1)
        self.frame1.pack(padx=0, pady=(0, 0), fill="both", expand=1) 
        self.frame1.pack_propagate(False)
        
        self.frame1_1=tk.Frame(self.frame1,relief="solid", bd=1
                           ,width = '100'
                               )
        self.frame1_1.pack(side="left", padx=0, pady=(0, 0), fill="both", expand=0
                           ) 
        # self.frame1_1.pack_propagate(False)
        
        
        self.frame3_1=tk.Frame(self.frame1_1, relief="solid", bd=1)
        self.frame3_1.pack(fill="both", expand=1,padx=0, pady=(0, 0))   
        # self.frame3_1.pack_propagate(False)
        self.ed_input = EditorInput(self,self.frame3_1)
        
        self.frame3_2=tk.Frame(self.frame1_1, relief="solid", bd=1)
        self.frame3_2.pack(fill="both", expand=1,padx=0, pady=(0, 0))   
        # self.frame3_2.pack_propagate(False)
        self.ed_connect = EditorConnect(self,self.frame3_2)
        
        
        
        self.frame1_2=tk.Frame(self.frame1,relief="solid", bd=1)
        self.frame1_2.pack(side="left", padx=0, pady=(0, 0), fill="both", expand=1) 
        self.frame1_2.pack_propagate(False)
        self.ed_highscore = EditorHighScore(self,self.frame1_2)  
        
                    
        self.server = socketServer(self.ed_input,host)
        
        
        self.ed_highscore.set_bind_server(self.server)
        # self.ed_input.set_bind_frame(self.ed_connect)
        self.server.set_bind_input(self.ed_input)
        self.server.set_bind_toolbar(self.toolbar)
        self.server.set_bind_output(self.ed_connect)
        self.server.set_bind_score(self.ed_highscore)        
        

if __name__ == "__main__":
    root = tk.Tk()
    app = PythonEditor(root)
    root.mainloop()
