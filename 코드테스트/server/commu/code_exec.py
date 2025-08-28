
import sys
from question import Questions
from commu.stdoutredirector import *
# from commu.server import socketServer
import multiprocessing

def run_code_in_process(code, input_list,queue):
    import io
    from contextlib import redirect_stdout

    output = io.StringIO()
    input_cnt = 0

    # print('---sssss---------')
    def custom_input(prompt="입력: "):
        nonlocal input_cnt
        response = ''
        try:
            if input_cnt < len(input_list):
                response = input_list[input_cnt]
            input_cnt += 1
        except:
            pass
        return response

    # sys.stdout = StdoutRedirector(output_list)
    # sys.stderr = StdoutRedirector(output_list)
    try:
        with redirect_stdout(output):
            exec(code, {"input": custom_input})
    except Exception as e:
        print("오류:", e, file=output)
    finally:
        pass
        # print('------------')
        # print('프로그램 종료', file=output)
        # print('------------')
    #     sys.stdout = sys.__stdout__
    #     sys.stderr = sys.__stderr__
    # print(output_list)
        
    # 결과를 큐에 넣기
    queue.put(output.getvalue())
    
class CodeExec:
    from editors.editor_connect import EditorConnect
    from editors.editor_highscore import EditorHighScore
    from editors.editor_input import EditorInput
    
    # from commu.server import socketServer
    
    def __init__(self,parent,identity,ed_input:EditorInput,ed_connect:EditorConnect):
        self.identity = identity
        self.parent = parent
        self.name = ''
        self.ed_input = ed_input
        self.ed_connect = ed_connect
        self.input_cnt = 0
        self.level = 1
            
    def check_must(self,level, code):
        code_lines = code.replace(' ', '')
        for mu in Questions.que[level-1]['must']:
            if isinstance(mu, list):
                for m in mu:
                    # print('==',m)
                    m = m.replace(' ', '')
                    if m in code_lines:
                        break
                else:
                    return mu[0]
            else:
                mu = mu.replace(' ', '')
                if mu not in code_lines:
                    return mu
        
        return None
    
    def check_not_used(self,level,code):
        
        if 'nused' not in Questions.que[level-1]:
            return None
        
        code_lines = code.replace(' ', '')
        # code_lines = code_lines.split('\n')
        
        for nused in Questions.que[level-1]['nused']:
            if nused in code_lines:
                return nused        
        return None
    # def check_not_used(self,level,code):
        
    #     code_lines = code.replace(' ', '')
    #     code_lines = code_lines.split('\n')
        
    #     for nused in Questions.que[level-1]['nused']:
    #         for line in code_lines:
    #             if nused in line:
    #                 return nused        
    #     return None
            
    def check_list(self, inputs):        
        if len(inputs) > 0:
            if isinstance(inputs[0], list):
                return True
        return False
    
    def safe_remove(self,lst, value):
        if value in lst:
            lst.remove(value)
            return True
        return False
            # lst = [x for x in lst if x != value]
            
    def check_line_same(self,output,cnt, line):
        result = None
        while output[cnt] == '\n':
            cnt += 1
                
        if str(output[cnt]).replace(' ', '') != str(line).replace(' ', ''):
            result = f'실패\n출력과 결과값이 다릅니다. \n\n출력:[{output[cnt]}]\n정답:[{line}]\n'
            return False,0,result
        cnt += 1
        return True,cnt,result
                    
    def run(self, code:str,level:int):
        self.level = level
        self.input_cnt = 0
        
        next_up = False
        result = '실패'
        
        mu = self.check_must(level, code)
        used = self.check_not_used(level, code)
        if mu is not None:
            result = f'실패 (반드시 사용되어야 하는 것 :{mu})'
        elif used is not None:
            result = f'실패 (사용하면 안되는 것 :{used})'
        else:
            output = []
            
            inputs = Questions.que[level - 1]['input']
            if self.check_list(inputs):
                for input_item in inputs:                            
                    queue = multiprocessing.Queue()                    
                    p = multiprocessing.Process(target=run_code_in_process, args=(code,input_item.copy(),queue))
                    p.start()
                    p.join(timeout=2)  # 5초 제한

                    if p.is_alive():
                        print("실행 시간 초과, 프로세스 종료")
                        p.terminate()
                        p.join()
                        
                    if not queue.empty():
                        # result = queue.get()
                        output += str(queue.get()).split('\n')
                        # print("실행결과:\n", result)
            else:
                queue = multiprocessing.Queue()
                p = multiprocessing.Process(target=run_code_in_process, args=(code,inputs.copy(),queue))
                p.start()
                p.join(timeout=2)  # 5초 제한

                if p.is_alive():
                    print("실행 시간 초과, 프로세스 종료")
                    p.terminate()
                    p.join()
                
                if not queue.empty():
                    # result = queue.get()
                    output = str(queue.get()).split('\n')
                    # print("실행결과:\n", result)
            
            # print(f'level:{self.level}')
            
            while self.safe_remove(output, ''):  # 빈 문자열 제거
                pass
            # self.safe_remove(output, '\n')  # 빈 문자열 제거
            # print(output)
            try:
                is_ok = True
                if len(Questions.que[level-1]['answ']) == 0:
                    if len(output) > 0 and len(output[0]):
                        is_ok = False
                        result = f'실패\n출력과 결과값이 다릅니다. \n\n출력:{output}'
                else:
                    cnt =0
                    for i,an in enumerate(Questions.que[level-1]['answ']):
                        if isinstance(an,list):
                            for res in an:
                                is_ok,cnt,result = self.check_line_same(output,cnt,res)
                                if is_ok == False:
                                    break
                        else:
                            is_ok,cnt,result = self.check_line_same(output,cnt,an)
                            
                        if is_ok == False:
                            break
                        
                if is_ok:
                    result = '정답입니다.'
                    msg = f'{self.name}님이 {level}번 문제를 해결했습니다.'
                    self.ed_input.add_msg(msg)
                    next_up = True                        
                    self.level += 1
                    
                        
            except Exception as ex:
                result = f'실패 (결과값:{ex})'
                    
                
        if self.level > len(Questions.que):
            self.level = 1
            
        return result, self.level,next_up

        
    # def editor_input(self,prompt="입력: "):
    #     response = ''
    #     try:
    #         if self.input_cnt < len(Questions.que[self.level-1]['input']):
    #             response = Questions.que[self.level-1]['input'][self.input_cnt]
    #         self.input_cnt += 1
    #     except Exception as e:
    #             pass
    #     return response
            
    # def run(self, code:str,level:int,start_level:int):
    #     self.level = level
    #     self.input_cnt = 0
        
    #     result = '실패'
    #     if code == 'start':
    #         result = '시작'
    #         self.level = start_level
    #     else:
    #         mu = self.check_must(level, code)
    #         if mu is not None:
    #             result = f'실패 (반드시 사용되어야 하는 것 :{mu})'
    #         else:
    #             output = []
    #             sys.stdout = StdoutRedirector(output)
    #             sys.stderr = StdoutRedirector(output)
                                
    #             try:
    #                 exec(code, {"input": self.editor_input})
    #                 # exec(code)
    #             except TimeoutError:
    #                 print('------------')
    #                 print("오류: Exec timed out!")
    #                 print('------------')
    #             except Exception as e:
    #                 print('------------')
    #                 print("오류:", e)
    #                 print('------------')
    #             finally:
    #                 # print()
    #                 print('------------')
    #                 print('프로그램 종료')
    #                 print('------------')
    #                 sys.stdout = sys.__stdout__
    #                 sys.stderr = sys.__stderr__
                    
    #             print(f'level:{self.level}')
    #             print(output)
    #             try:
    #                 cnt =0
    #                 for i,an in enumerate(Questions.que[level-1]['answ']):
    #                     while output[cnt] == '\n':
    #                         cnt += 1
                                
    #                     if output[cnt] != str(an):
    #                         result = f'실패 (결과값:{output[i]} != {an})'
    #                         break
    #                     cnt += 1
    #                 else:
    #                     result = '성공'
    #                     msg = f'{self.name}님이 {level}번 문제를 해결했습니다.'
    #                     self.ed_input.add_msg(msg)
    #                     self.level += 1
    #                     self.ed_connect.update_item(self.identity,self.name,self.level)
    #                     self.parent.score_sort(self.name,self.level)
    #             except Exception as ex:
    #                 result = f'실패 (결과값:{ex})'
                    
                
    #     if self.level > len(Questions.que):
    #         self.level = 1
            
    #     return result, self.level