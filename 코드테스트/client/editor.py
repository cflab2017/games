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
        self.ed_output = EditorOutput(self,self.frame3_1,self.ed_input)
        self.ed_content = EditorContent(self,self.frame3_2)
        self.toolbar = ToolBar(self.frame2,self.ed_output)
        
        self.ed_input.set_bind_frame(self.ed_output)
        self.ed_output.set_client(self.client)
        self.client.set_bind_output(self.ed_output)
        self.client.set_bind_content(self.ed_content)
        self.client.set_bind_input(self.ed_input)
        
        self.client.send_request('start')
        
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
