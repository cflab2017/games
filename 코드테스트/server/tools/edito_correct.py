import tkinter as tk

def 변환하기():
    str_input = str_source.get("1.0", tk.END).strip()   # str_source에서 문자열 가져오기
    
    str_input = str(str_input).split('\n')
    str_output = ''
    for s in str_input:
        s = s.replace('\t', '\\t')
        str_output += f"\"{s}\",\n"
    
    # str_output = str_input.upper()                   # 변환 (여기서는 대문자로)
    
    str_result.delete("1.0", tk.END)                  # str_result 초기화
    str_result.insert(tk.END, str_output)               # 변환 결과 출력
    
    # root.clipboard_clear()        # 클립보드 비우기
    # root.clipboard_append(str_output)   # 클립보드에 텍스트 추가
    # root.update()                 # 클립보드 내용이 유지되도록 업데이트
    

def on_change(event=None):
    변환하기()
    
# 메인 윈도우 생성
root = tk.Tk()
root.title("문자 편집 툴")

# str_source
입력라벨 = tk.Label(root, text="입력 문자열")
입력라벨.pack()

str_source = tk.Text(root, height=20, width=60)
str_source.bind("<KeyRelease>", on_change)
str_source.pack()

# 변환 버튼
변환버튼 = tk.Button(root, text="변환하기", command=변환하기)
변환버튼.pack(pady=5)

# str_result
출력라벨 = tk.Label(root, text="출력 문자열")
출력라벨.pack()

str_result = tk.Text(root, height=20, width=60)
str_result.pack()

root.mainloop()
