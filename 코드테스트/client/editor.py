import tkinter as tk
from tkinter import scrolledtext
import tkinter.font as tkfont


from editors.editor_input import *
from editors.editor_output import *
from editors.editor_content import *
from editors.editor_rangking import *
from editors.toolbar import *

from commu.client import *
from login.account import *

class PythonEditor:
    from login.account import Account
    
    def __init__(self, root, host= None):
        self.root = root
        root.geometry("1800x860")
        self.root.title("코딩나우 코딩연습")    
        # self.bg_image = tk.PhotoImage(file="./images/bg2.png")
        
        self.font_size = 20
        
        self.level = 1   
        self.last_level = 0

        self.client = socketClient(self,host)
        # cli.run()
    
        account = Account()
        self.name, self.isRun = account.run(self.client)
        if self.isRun == False:
            return
#########################################################################        
        self.frame0=tk.Frame(self.root,relief="solid", bd=1)
        self.frame0.pack(padx=10, pady=(10, 0), fill="both")
              
        
        # bg_label = tk.Label(self.frame1, image=self.bg_image)
        # bg_label.place(x=0, y=0, relwidth=1, relheight=1)
           
        self.toolbar = ToolBar(self,self.frame0)        
#########################################################################
#########################################################################    
        self.frame1=tk.Frame(self.root)        
        self.frame1.pack(fill="both", expand=1) 
        
        # self.frame1_1=tk.Frame(self.frame1,relief="solid", bd=1)        
        # self.frame1_1.pack(side="left", padx=10, pady=(10, 10), fill="both", expand=1) 
        # self.frame1_1.pack_propagate(False)
#########################################################################  

        # self.frame1_2=tk.Frame(self.frame1,relief="solid", bd=1)        
        # self.frame1_2.pack(side="left", padx=10, pady=(10, 10), fill="both", expand=1) 
        # self.frame1_2.pack_propagate(False)
        
        # self.frame2_3=tk.Frame(self.frame1_2)
        # self.frame2_3.pack(fill="both", expand=1)  
        # self.frame2_3.pack_propagate(False)          
        # self.ed_ranking = EditorRanking(self,self.frame2_3)  
              
#########################################################################  
        self.frame1_1=tk.Frame(self.frame1,relief="solid", bd=1)        
        self.frame1_1.pack(side="left", padx=10, pady=(10, 10), fill="both", expand=1) 
        self.frame1_1.pack_propagate(False)
#########################################################################  
        self.frame2_1=tk.Frame(self.frame1_1)              
        self.frame2_1.pack(fill="both", expand=1)          
        self.frame2_1.pack_propagate(False)
        
        self.frame2_1_1=tk.Frame(self.frame2_1)              
        self.frame2_1_1.pack(side="left", fill="both", expand=1)          
        self.frame2_1_1.pack_propagate(False)        
        self.ed_input = EditorInput(self,self.frame2_1_1)
        
        self.frame2_1_2=tk.Frame(self.frame2_1)              
        self.frame2_1_2.pack(side="left", fill="both", expand=1)          
        self.frame2_1_2.pack_propagate(False)    
        self.ed_ranking = EditorRanking(self,self.frame2_1_2) 
        
        self.frame2_2=tk.Frame(self.frame1_1)   
        self.frame2_2.pack(fill="both", expand=1)    
        self.frame2_2.pack_propagate(False) 
        self.ed_output = EditorOutput(self,self.frame2_2)              
        
#########################################################################    
#########################################################################    
        self.frame3=tk.Frame(self.frame1, 
                        #      width=400,
                             relief="solid", bd=1)
        self.frame3.pack(side="right", padx=10, pady=(10, 10), fill="both", expand=1)  
        self.frame3.pack_propagate(False)  
#########################################################################   
        self.frame3_1=tk.Frame(self.frame3)
        self.frame3_1.pack(side="left", fill="both", expand=1)  
        self.frame3_1.pack_propagate(False)          
        self.ed_content = EditorContent(self,self.frame3_1) 
        
        
        # self.frame3_2=tk.Frame(self.frame3)
        # self.frame3_2.pack(side="left", fill="both", expand=1)  
        # self.frame3_2.pack_propagate(False)          
        # self.ed_ranking = EditorRanking(self,self.frame3_2)    
#########################################################################       
#########################################################################

        self.ed_input.set_bind_output(self.ed_output)
        self.ed_input.set_client(self.client)
        
        self.ed_output.set_bind_input(self.ed_input)
        self.ed_output.set_client(self.client)
        
        self.toolbar.set_bind_input(self.ed_input)
        self.toolbar.set_bind_output(self.ed_output,self.name)
        
        
        self.client.set_bind_output(self.ed_output)
        self.client.set_bind_content(self.ed_content)
        self.client.set_bind_input(self.ed_input)
        self.client.set_bind_Ranking(self.ed_ranking)
        
        self.client.send_request('start')
        self.client.send_request_ranking()
        
     
    def show_popup(self,message, duration=2000):  # duration은 밀리초(ms)
        popup = tk.Toplevel(self.root)
        popup.title("알림")
        popup.overrideredirect(True)  # ← 제목 표시줄 제거

        # 팝업 크기
        popup_width = 600
        popup_height = 400

        # root(메인 창)의 위치와 크기 가져오기
        self.root.update_idletasks()  # 위치 정보 갱신
        root_x = self.root.winfo_rootx()
        root_y = self.root.winfo_rooty()
        root_width = self.root.winfo_width()
        root_height = self.root.winfo_height()

        # 메인창 중심을 기준으로 팝업 위치 계산
        x = root_x + (root_width // 2) - (popup_width // 2)
        y = root_y + (root_height // 2) - (popup_height // 2)

        # 팝업 위치 설정
        popup.geometry(f"{popup_width}x{popup_height}+{x}+{y}")
        popup.resizable(False, False)

        # 내용 표시
        label = tk.Label(popup, text=message, font=("malgungulim", 30, "bold"), bg="white", fg="red")
        label.pack(expand=True)

        # 자동 종료 타이머
        popup.after(duration, popup.destroy)

if __name__ == "__main__":
    root = tk.Tk()
    app = PythonEditor(root)
    if app.isRun:
        root.mainloop()
