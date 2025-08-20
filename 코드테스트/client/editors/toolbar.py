
import tkinter as tk
from tkinter import scrolledtext
import tkinter.font as tkfont
import winsound

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tipwindow = None
        widget.bind("<Enter>", self.show_tip)
        widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event=None):
        if self.tipwindow or not self.text:
            return
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 10
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)   # 창 테두리 제거
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, background="#ffffe0",
                         relief="solid", borderwidth=1,
                         font=("맑은 고딕", 9))
        label.pack(ipadx=5, ipady=2)

    def hide_tip(self, event=None):
        if self.tipwindow:
            self.tipwindow.destroy()
            self.tipwindow = None

    
class ToolBar:
    def __init__(self,parent,frame):
        # self.frame = frame
        self.parent = parent
        self.font_size = self.parent.font_size
        
        self.frame=tk.Frame(frame, height=100,relief="solid", bd=0)
        self.frame.pack(padx=10, pady=(10, 10), fill="both", expand=1) 
        self.seconds = 0
                
    def set_bind_input(self,ed_input):
        self.ed_input = ed_input
        
        
    def set_bind_output(self,ed_output,name):
        
        color = self.rgb_to_hex(208,223,211) 
        color_font = self.rgb_to_hex(36,53,40)
        color_font2 = self.rgb_to_hex(94,43,56)
        color_font3 = self.rgb_to_hex(196,26,81)
        
        self.label = tk.Label(self.frame, text="타이머: 0초", font=("Helvetica", 20,"bold"), foreground=color_font3)
        self.label.pack(side="left", fill="none", expand=0, anchor='center')
        
        self.ed_output = ed_output
        run_btn = tk.Button(self.frame, text="실행해보기", command=self.ed_output.only_run_code_thread)
        run_btn.config(font=("malgungulim", self.font_size, "bold"))  # 기본: 영어
        run_btn.configure(font=("malgungulim", self.font_size, "normal", "bold"), foreground=color_font, background=color)
        run_btn.pack(side="left", fill="none", expand=0, anchor='center',padx=10)
        ToolTip(run_btn, "작성한 코드의 실행 결과를 볼 수 있습니다.")
        
        
        run_btn = tk.Button(self.frame, text="확인받기", command=self.ed_output.run_code_thread)
        run_btn.config(font=("malgungulim", self.font_size, "bold"))  # 기본: 영어
        run_btn.configure(font=("malgungulim", self.font_size, "normal", "bold"), foreground=color_font2, background=color)
        run_btn.pack(side="left", padx=10,fill="none", expand=0, anchor='center')
        ToolTip(run_btn, "작성한 코드를 서버에 보내 채점을 받습니다.")
                
        name_label = tk.Label(self.frame, text=f' | ')        
        name_label.config(font=("malgungulim", self.font_size, "bold"))  # 기본: 영어
        name_label.configure(font=("malgungulim", self.font_size, "normal", "bold"), foreground=color_font)
        name_label.pack(side="left", fill="none", expand=0, anchor='center',padx=10)
                
        self.train_btn = tk.Button(self.frame, text="연습하기", command=self.btn_train)
        self.train_btn.config(font=("malgungulim", self.font_size, "bold"))  # 기본: 영어
        self.train_btn.configure(font=("malgungulim", self.font_size, "normal", "bold"), foreground=color_font2, background=color)
        self.train_btn.pack(side="left", padx=10,fill="none", expand=0, anchor='center')
        ToolTip(self.train_btn, "연습모드로 문제를 연습할 수 있습니다.")
        
        self.challenge_btn = tk.Button(self.frame, text="도전하기", command=self.btn_Challenge)
        self.challenge_btn.config(font=("malgungulim", self.font_size, "bold"))  # 기본: 영어
        self.challenge_btn.configure(font=("malgungulim", self.font_size, "normal", "bold"), foreground=color_font2, background=color)
        self.challenge_btn.pack(side="left", padx=10,fill="none", expand=0, anchor='center')
        ToolTip(self.challenge_btn, "도전모드로 서버에 순위가 기록됩니다.")
        
        name_label = tk.Label(self.frame, text=f' | ')        
        name_label.config(font=("malgungulim", self.font_size, "bold"))  # 기본: 영어
        name_label.configure(font=("malgungulim", self.font_size, "normal", "bold"), foreground=color_font)
        name_label.pack(side="left", fill="none", expand=0, anchor='center',padx=10)
        
        run_btn = tk.Button(self.frame, text="제출한 코드", command=self.btn_load_code)
        run_btn.config(font=("malgungulim", self.font_size, "bold"))  # 기본: 영어
        run_btn.configure(font=("malgungulim", self.font_size, "normal", "bold"), foreground=color_font2, background=color)
        run_btn.pack(side="left", padx=10,fill="none", expand=0, anchor='center')
        ToolTip(run_btn, "서버에 등록된 나의 정답을 코드를 확인 할 수 있습니다.")
        
        name_label = tk.Label(self.frame, text=f' 접속 : ▶ {name}')        
        name_label.config(font=("malgungulim", self.font_size, "bold"))  # 기본: 영어
        name_label.configure(font=("malgungulim", self.font_size, "normal", "bold"), foreground=color_font)
        name_label.pack(side="left", fill="none", expand=0, anchor='center',padx=10)
        self.update_timer()
        
    def btn_load_code(self):
        if self.parent.Challenge == 1:
            self.parent.show_popup('도전 중에는 안되요!!',1000)
        else:
            self.ed_input.get_user_code()
            
    def popup_challenge_stop(self,prompt="도전을 중지할까요?"):

        def on_ok(event=None):
            self.stop_Challenge('도전을 중지 했습니다.')
            self.win.destroy()
            
        value = None
        self.win = tk.Toplevel(self.parent.root)

        # 화면 크기 구하기
        screen_width = self.win.winfo_screenwidth()
        screen_height = self.win.winfo_screenheight()

        # 팝업 크기 예상값 (약 300x100)
        popup_w, popup_h = 300, 100
        x = (screen_width // 2) - (popup_w // 2)
        y = (screen_height // 2) - (popup_h // 2)
        
        self.win.geometry(f"300x100+{x}+{y}")  # 위치 지정
        self.win.title("선택")

        tk.Label(self.win, text=prompt).pack(pady=10)

        # 버튼 영역 프레임
        frame_btn = tk.Frame(self.win)
        frame_btn.pack(pady=10)

        tk.Button(frame_btn, text="중지", command=on_ok, width=10).pack(side="left", padx=5)
        tk.Button(frame_btn, text="계속", command=self.win.destroy, width=10).pack(side="left", padx=5)


        self.win.lift()
        self.win.focus_force()
        
        # print('level1')
        # self.win.mainloop()
        # 팝업이 닫힐 때까지 대기
        self.parent.root.wait_window(self.win)        
        
        # print('level2')
        return value
    
    def popup_input(self,prompt="레벨을 입력하세요:"):
            
        prompt += f'[{1} ~ {self.parent.last_level-1}]'
        def on_ok(event=None):
            nonlocal value
            value = entry.get()
            # print(value)
            self.win.destroy()

        value = None
        self.win = tk.Toplevel(self.parent.root)

        # 화면 크기 구하기
        screen_width = self.win.winfo_screenwidth()
        screen_height = self.win.winfo_screenheight()

        # 팝업 크기 예상값 (약 300x100)
        popup_w, popup_h = 300, 100
        x = (screen_width // 2) - (popup_w // 2)
        y = (screen_height // 2) - (popup_h // 2)
        
        self.win.geometry(f"300x100+{x}+{y}")  # 위치 지정
        self.win.title("레벨 입력")

        tk.Label(self.win, text=prompt).pack(pady=5)
        entry = tk.Entry(self.win)
        entry.pack(pady=5)
        entry.focus()
        entry.bind("<Return>", on_ok)

        tk.Button(self.win, text="확인", command=on_ok).pack(pady=5)

        self.win.lift()
        self.win.focus_force()
        self.win.after(50, lambda: entry.focus())
        entry.focus()                  # 포커스 주기 (필요 시)
        
        # print('level1')
        # self.win.mainloop()
        # 팝업이 닫힐 때까지 대기
        self.parent.root.wait_window(self.win)        
        
        # print('level2')
        return value
    
    def stop_Challenge(self, prompt = '도전을 종료합니다.'):
        self.parent.Challenge = 0 
        self.dingdong()
        self.parent.show_popup('도전을 중지했습니다.',1000)
        self.parent.client.send_request_code('start',Challenge=self.parent.Challenge)
        self.seconds = 0
       
        
    def btn_train(self):
        if self.parent.Challenge == 1:
            # self.parent.show_popup('도전 중에는 안되요!!',1000)
            self.popup_challenge_stop()
        else:
            level = self.popup_input()
            if len(level) < 1:
                return
            try:
                level = int(level)
            except Exception as ex:
                return
                
            if level < 1:
                level = 1
            elif level > self.parent.last_level-1:
                level = self.parent.last_level-1
                
            self.parent.level = level   
            # self.parent.last_level = 0
            self.parent.client.send_request_code('train',Challenge=self.parent.Challenge)
        self.seconds = 0
            
    def btn_Challenge(self):
        if self.parent.Challenge == 0:
            self.parent.Challenge = 1
            self.parent.level = 1   
            # self.parent.last_level = 0
            self.parent.client.send_request_code('start',Challenge=self.parent.Challenge)
            self.parent.show_popup(f'도전을 시작합니다.\n도전시간은 {self.parent.Challenge_time}분입니다.',2000)
            # self.seconds = 60 * 30
            self.seconds = self.parent.Challenge_time*60+2
        else:
            # self.parent.show_popup('도전 중입니다.',1000)
            self.popup_challenge_stop()
        
    def rgb_to_hex(self,r, g, b):
        return f'#{r:02x}{g:02x}{b:02x}'
    
    def dingdong(self):
        winsound.PlaySound("./sounds/complet.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
        
    def update_timer(self):

        if self.seconds % 2 == 0:
            color_font2 = self.rgb_to_hex(255,255,255)
            color_font1 = self.rgb_to_hex(196,26,81)
        else:
            color_font1 = self.rgb_to_hex(255,255,255)
            color_font2 = self.rgb_to_hex(196,26,81)
            
            
        if self.parent.Challenge == 1:
            self.challenge_btn.configure(foreground=color_font2, background=color_font1)
            self.label.configure(foreground=color_font2, background=color_font1)
            self.challenge_btn.config(text='도전중')
            
            color_font1 = self.rgb_to_hex(255,255,255)
            color_font2 = self.rgb_to_hex(196,26,81)
            self.train_btn.configure(foreground=color_font2, background=color_font1)
            self.train_btn.config(text='연습하기')
        else:
            self.train_btn.configure(foreground=color_font2, background=color_font1)
            self.train_btn.config(text='연습중')
            
            color_font1 = self.rgb_to_hex(255,255,255)
            color_font2 = self.rgb_to_hex(196,26,81)
            self.challenge_btn.configure(foreground=color_font2, background=color_font1)
            self.label.configure(foreground=color_font2, background=color_font1)
            self.challenge_btn.config(text='도전하기')
            
        if self.parent.Challenge == 1:
            self.seconds -= 1
            if self.seconds <= 0:
                self.stop_Challenge()
        else:
            self.seconds += 1
        
        hrs = self.seconds // 3600
        mins = (self.seconds % 3600) // 60
        secs = self.seconds % 60
        self.label.config(text=f"{hrs:02}:{mins:02}:{secs:02}")
        
        self.parent.root.after(1000, self.update_timer)  # 1초마다 반복