import pygame
import pygame.image
import pygame.image
from pygame.locals import *
import pygame.transform

from board import *
from stone import *
from client import *
from account import *
from draw_msg import *
from interference import *
from shapeLoad import *

from btnDraw import *
import pickle
import os.path

# import pyautogui
# pip install pygame

#이벤트 처리함수
def eventProcess():
    global isActive,design_mode
    global is_pause, pause_cnt
    for event in pygame.event.get():#이벤트 가져오기
        if event.type == QUIT: #종료버튼?
            isActive = False
        if event.type == pygame.KEYDOWN:#키 눌림?
            if event.key == pygame.K_ESCAPE:#ESC 키?
                isActive = False
            if event.key == pygame.K_F5:
                btnDraw.btn_stone.set_alpha(200)
                design_mode += 1
                
                if design_mode>2:
                    design_mode = 0
                
            if stone.gameover:
                if event.key == pygame.K_RETURN:#재시작
                    init_game()
            else:
                if event.key == pygame.K_1:#삭제
                    btnDraw.btn_shield.set_alpha(200)
                    interf.snd_dic['move'].play()
                    msg_temp = interf.del_stone()
                    if msg_temp is not None:
                        msg.status_msg.append(f'{msg_temp}')   
                    
                if event.key == pygame.K_p:
                    btnDraw.btn_pause.set_alpha(200)
                    if stone.gameover:
                        pass
                    elif is_pause:
                        is_pause = False
                    else:
                        if pause_cnt > 0:
                            is_pause = True
                            
                            pause_cnt -= 1      
                            msg.status_msg.append(f'일시정지 남은 횟수 {pause_cnt}개')              
                if is_pause == False:
                    key_process_stone(event.key)
                    key_process_inter(event.key)
                    
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_F5:
                btnDraw.btn_stone.set_alpha(100)
                
            if event.key == pygame.K_p:
                btnDraw.btn_pause.set_alpha(100)
                
            if event.key == pygame.K_1:
                btnDraw.btn_shield.set_alpha(100)
                
            if event.key == pygame.K_SPACE:
                btnDraw.btn_space.set_alpha(100)
                
            if event.key == pygame.K_LEFT:
                btnDraw.btn_left.set_alpha(100)
                
            if event.key == pygame.K_RIGHT:
                btnDraw.btn_right.set_alpha(100)
                
            if event.key == pygame.K_UP:
                btnDraw.btn_up.set_alpha(100)
                
            if event.key == pygame.K_DOWN:
                btnDraw.btn_down.set_alpha(100)
                
            if event.key == pygame.K_LSHIFT:
                btnDraw.btn2_space.set_alpha(100)
                
            if event.key == pygame.K_a:
                btnDraw.btn2_left.set_alpha(100)
                
            if event.key == pygame.K_d:
                btnDraw.btn2_right.set_alpha(100)
                
            if event.key == pygame.K_w:
                btnDraw.btn2_up.set_alpha(100)
                
            if event.key == pygame.K_s:
                btnDraw.btn2_down.set_alpha(100)
                
        if event.type == pygame.USEREVENT+3:
            interf.create_stone(2)
            
        if event.type == pygame.USEREVENT+2:#사용자 이벤트
            if is_pause == False:
                interf.drop()
                
        if event.type == pygame.USEREVENT+1:#사용자 이벤트
            if is_pause == False:
                stone.drop()
            pass
        
def key_process_stone( key):
    if key == pygame.K_SPACE:#한번에 내리기
        stone.snd_dic['move'].play()
        stone.insta_drop()
        btnDraw.btn_space.set_alpha(200)
                
    if key == pygame.K_LEFT:
        stone.snd_dic['move'].play()
        stone.move(-1)
        btnDraw.btn_left.set_alpha(200)
        
    if key == pygame.K_RIGHT:
        stone.snd_dic['move'].play()
        stone.move(+1)
        btnDraw.btn_right.set_alpha(200)
        
    if key == pygame.K_DOWN:#한칸내리기
        stone.snd_dic['move'].play()
        stone.drop()
        btnDraw.btn_down.set_alpha(200)
        
    if key == pygame.K_UP:#회전하기
        stone.snd_dic['move'].play()
        stone.rotate_stone()
        btnDraw.btn_up.set_alpha(200)
    
def key_process_inter( key):
    if key == pygame.K_LSHIFT:#한번에 내리기
        interf.snd_dic['move'].play()
        interf.insta_drop()
        btnDraw.btn2_space.set_alpha(200)
        
    if key == pygame.K_a:
        interf.snd_dic['move'].play()
        interf.move(-1)
        btnDraw.btn2_left.set_alpha(200)
        
    if key == pygame.K_d:
        interf.snd_dic['move'].play()
        interf.move(+1)
        btnDraw.btn2_right.set_alpha(200)
        
    if key == pygame.K_s:#한칸내리기
        interf.snd_dic['move'].play()
        interf.drop()
        btnDraw.btn2_down.set_alpha(200)
        
    if key == pygame.K_w:#회전하기
        interf.snd_dic['move'].play()
        interf.rotate_stone()
        btnDraw.btn2_up.set_alpha(200)
        
        
def draw_rect(p_x,p_y,color,Thickness,outline,divide = 1):
    
    pygame.draw.rect(
        screen,
        color,
        pygame.Rect(p_x,p_y,cell_size/divide,cell_size/divide), 
        Thickness)
    
    if outline:
        pygame.draw.rect(
            screen,
            (200,200,200),
            # (24,5,194),
            pygame.Rect(p_x,p_y,cell_size/divide,cell_size/divide), 
            1)
        
def draw_guide_line():
    rect = pygame.Rect(rlim,0,screen.get_width()-rlim,220)
    pygame.draw.rect(screen,(255,255,255),rect, 1)
    
    rect.top = rect.bottom
    rect.height = 360
    pygame.draw.rect(screen,(255,255,255),rect, 1)
    
    rect.top = rect.bottom
    rect.height = 200
    pygame.draw.rect(screen,(255,255,255),rect, 1)
    
    rect.top = rect.bottom
    rect.height = screen.get_height()- rect.top
    pygame.draw.rect(screen,(255,255,255),rect, 1)
    
def draw_matrix(matrix, off_x,off_y,Thickness,outline = (200,200,200),divide = 1):
    global cell_size
    if divide>1:
        x_start_offset = (off_x *cell_size)/divide
    else:
        x_start_offset = 0
        
    for y, row in enumerate(matrix):
        if divide > 1:
            p_x = (off_x) *(cell_size)
        for x, color in enumerate(row):
            if color is not None:
                # if divide > 1:
                #     p_x += cell_size/divide
                # else:
                #     p_x = (off_x+x) *(cell_size)
                p_x = (off_x+x) *(cell_size/divide) + x_start_offset
                p_y = (off_y+y) *(cell_size/divide)
                
                if (str(type(color)) == "<class 'tuple'>"):                    
                    draw_rect(p_x,p_y,color,Thickness,outline,divide)
                else:
                    color -= 1
                    if design_mode==0:
                        color= shape.shape['color'][color]
                        draw_rect(p_x,p_y,color,Thickness,outline,divide)
                    elif design_mode==1:
                        img = shape.shape['char'][color]
                        screen.blit(img, (p_x,p_y,))
                    elif design_mode==2:
                        img = shape.shape['stone'][color]
                        screen.blit(img, (p_x,p_y,))
            else:
                pass
                # pygame.draw.rect(
                #     screen,
                #     (255,255,255),
                #     pygame.Rect((off_x+x) *cell_size,(off_y+y) *cell_size,cell_size,cell_size), 
                #     Thickness)
                    
def init_game():
    global is_pause, pause_cnt
    stone.gameover = False
    is_pause = False
    pause_cnt = 5
    board.new_board()
    stone.new_stone()
    interf.new_stone()
    stone.item_cnt = 2
    pygame.time.set_timer(pygame.USEREVENT+1, 1000)#1초마다 "USEREVENT+1" 이벤트 발생
    pygame.time.set_timer(pygame.USEREVENT+2, 1000)

                
#1.초기화 하기
pygame.init() #pygame 초기화
clock = pygame.time.Clock() #프레임을 처리 하기위해

#2.변수초기화
isActive = True
design_mode = 0
cell_size = 25+10+7
cols = 10
rows = 22+6-5
rlim = cell_size*cols
is_pause = False
pause_cnt = 0
    

#3.스크린 생성하기
SCREEN_WIDTH = cell_size*(cols+3)
SCREEN_HEIGHT = cell_size*rows
screen = pygame.display.set_mode((SCREEN_WIDTH+400, SCREEN_HEIGHT)) #화면생성

img_bg = pygame.image.load('./images/bg.jpg')
img_bg = pygame.transform.scale(img_bg,(screen.get_width(), screen.get_height()))
#4.클래스 생성
client = socketClient()

account = Account(screen)
user_name,isActive = account.run(client)

pygame.display.set_caption(f"codingnow.co.kr 버전02 (접속자 : {user_name})") #타이틀
shape = ShapeLoad(cell_size)
board = Board(rows,cols)
stone = Stone(rows,cols,board,user_name)
interf = Interference(stone,rows,cols,board,user_name)
msg = DrawMsg(screen,stone,user_name,client,rlim,cell_size)

btnDraw = BtnDraw(screen)

stone.set_DrawMsg(msg)
interf.set_DrawMsg(msg)

client.set_interf(interf)
init_game()

# pygame.time.set_timer(pygame.USEREVENT+3, 3000)
while isActive:
    screen.fill((0, 0, 0)) #화면을 흰색으로 채우기
    screen.blit(img_bg,(0,0))
    eventProcess() #이벤트 처리
    btnDraw.draw()
    msg.draw(is_pause,pause_cnt,interf.next_stone)
    
    if stone.gameover == False:
        #게임화면 구분선
        pygame.draw.line(screen,(255, 255, 255),(rlim+1, 0),(rlim+1, SCREEN_HEIGHT-1)) 
            
        #게임화면 바둑판
        draw_matrix(board.bground_grid, 0, 0,0,True)
        #스톤 그리기
        draw_matrix(stone.stone,stone.stone_x, stone.stone_y, 0,True)
        
        for cnt in range(len(stone.next_stone)):
            draw_matrix(stone.next_stone[cnt],cols+1, 2+(3*cnt), 0,True,2)
        
        if len(interf.stone):
            draw_matrix(interf.stone,interf.stone_x, interf.stone_y, 0,True)
            if len(interf.next_stone):
                for cnt in range(len(interf.next_stone)):
                    draw_matrix(interf.next_stone[cnt],cols+6, 2+(3*cnt), 0,True,2)
                    if cnt >=2:
                        break
            
        #보드 그리기
        draw_matrix(board.board, 0, 0, 0,True)
        msg.disp_msg_score()
        draw_guide_line()
        if stone.score != stone.score_pre:
            client.send_score(user_name, stone.score)
            stone.score_pre = stone.score
    msg.drawStatusMsg()
    pygame.display.update() #화면 갱신
    clock.tick(30) #초당 30프레임 
    
# pyinstaller -w -F .\tetris.py
# pyinstaller --onefile --debug=all test.py
# pyinstaller -w -F --debug=all game.py