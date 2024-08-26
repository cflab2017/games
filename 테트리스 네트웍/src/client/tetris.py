import pygame
from pygame.locals import *

from board import *
from stone import *
from client import *
from account import *
from draw_msg import *
from interference import *

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
                if design_mode==0:
                    design_mode = 1
                else:
                    design_mode = 0
                
            if stone.gameover:
                if event.key == pygame.K_RETURN:#재시작
                    init_game()
            else:
                if event.key == pygame.K_p:
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
                    # if event.key == pygame.K_SPACE:#한번에 내리기
                    #     stone.snd_dic['move'].play()
                    #     stone.insta_drop()
                    # if event.key == pygame.K_LEFT:
                    #     stone.snd_dic['move'].play()
                    #     stone.move(-1)
                    # if event.key == pygame.K_RIGHT:
                    #     stone.snd_dic['move'].play()
                    #     stone.move(+1)
                    # if event.key == pygame.K_DOWN:#한칸내리기
                    #     stone.snd_dic['move'].play()
                    #     stone.drop()
                    # if event.key == pygame.K_UP:#회전하기
                    #     stone.snd_dic['move'].play()
                    #     stone.rotate_stone()
                        
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
    if key == pygame.K_LEFT:
        stone.snd_dic['move'].play()
        stone.move(-1)
    if key == pygame.K_RIGHT:
        stone.snd_dic['move'].play()
        stone.move(+1)
    if key == pygame.K_DOWN:#한칸내리기
        stone.snd_dic['move'].play()
        stone.drop()
    if key == pygame.K_UP:#회전하기
        stone.snd_dic['move'].play()
        stone.rotate_stone()
    
def key_process_inter( key):
    if key == pygame.K_x:#한번에 내리기
        interf.snd_dic['move'].play()
        interf.insta_drop()
    if key == pygame.K_a:
        interf.snd_dic['move'].play()
        interf.move(-1)
    if key == pygame.K_d:
        interf.snd_dic['move'].play()
        interf.move(+1)
    if key == pygame.K_s:#한칸내리기
        interf.snd_dic['move'].play()
        interf.drop()
    if key == pygame.K_w:#회전하기
        interf.snd_dic['move'].play()
        interf.rotate_stone()
    if key == pygame.K_1:#삭제
        interf.snd_dic['move'].play()
        interf.del_stone()
        
color_list = [
    (255, 85,  85),
    (100, 200, 115),
    (120, 108, 245),
    (255, 140, 50),
    (50,  120, 52),
    (146, 202, 73),
    (150, 161, 218),
    (100, 0,  100),
    ]        
def draw_matrix(matrix, off_x,off_y,Thickness,outline = False):
    global cell_size
    for y, row in enumerate(matrix):
        for x, color in enumerate(row):
            if color is not None:
                if design_mode == 1 and color in color_list:
                    idex = color_list.index(color)
                    if idex > -1:
                        screen.blit(img_player[idex], ((off_x+x) *cell_size,(off_y+y) *cell_size))
                else:
                    pygame.draw.rect(
                        screen,
                        color,
                        pygame.Rect((off_x+x) *cell_size,(off_y+y) *cell_size,cell_size,cell_size), 
                        Thickness)
                if design_mode==0 and outline:
                    pygame.draw.rect(
                        screen,
                        (200,200,200),
                        pygame.Rect((off_x+x) *cell_size,(off_y+y) *cell_size,cell_size,cell_size), 
                        1)
            else:
                pass
                # pygame.draw.rect(
                #     screen,
                #     (255,255,255),
                #     pygame.Rect((off_x+x) *cell_size,(off_y+y) *cell_size,cell_size,cell_size), 
                #     Thickness)
                    
def load_player_img():
    file_names = [
        "player_army.png",    "player_dinosaur.png",
        "player_ninja.png",   "player_penguin.png",
        "player_Pirate.png",  "player_police.png",
        "player_samurai.png", "player_soldier.png",
        "player_warrior.png",
        ]
    
    img_player = []
    for file in file_names:
        image = pygame.image.load(f"./images/{file}").convert_alpha()
        image = pygame.transform.scale(image, (cell_size, cell_size))
        img_player.append(image)  
        
    return img_player

def init_game():
    global is_pause, pause_cnt
    stone.gameover = False
    is_pause = False
    pause_cnt = 5
    board.new_board()
    stone.new_stone()
    interf.new_stone()
    pygame.time.set_timer(pygame.USEREVENT+1, 1000)#1초마다 "USEREVENT+1" 이벤트 발생
    pygame.time.set_timer(pygame.USEREVENT+2, 1000)

                
#1.초기화 하기
pygame.init() #pygame 초기화
pygame.display.set_caption("codingnow.co.kr 버전02") #타이틀
clock = pygame.time.Clock() #프레임을 처리 하기위해

#2.변수초기화
isActive = True
design_mode = 0
cell_size = 25+10+10
cols = 10
rows = 22+6-5
rlim = cell_size*cols
is_pause = False
pause_cnt = 0
    

#3.스크린 생성하기
SCREEN_WIDTH = cell_size*(cols+3)
SCREEN_HEIGHT = cell_size*rows
screen = pygame.display.set_mode((SCREEN_WIDTH+400, SCREEN_HEIGHT)) #화면생성

img_player = load_player_img()

#4.클래스 생성
client = socketClient()

account = Account(screen)
user_name,isActive = account.run(client)


board = Board(rows,cols)
stone = Stone(rows,cols,board,user_name)
interf = Interference(stone,rows,cols,board,user_name)
msg = DrawMsg(screen,stone,user_name,client,rlim,cell_size)

stone.set_DrawMsg(msg)
interf.set_DrawMsg(msg)

client.set_interf(interf)
init_game()

# pygame.time.set_timer(pygame.USEREVENT+3, 3000)
while isActive:
    screen.fill((0, 0, 0)) #화면을 흰색으로 채우기
    eventProcess() #이벤트 처리
    
    msg.draw(is_pause,pause_cnt,interf.next_stone)
    
    if stone.gameover == False:
        #게임화면 구분선
        pygame.draw.line(screen,(255, 255, 255),(rlim+1, 0),(rlim+1, SCREEN_HEIGHT-1)) 
            
        #게임화면 바둑판
        draw_matrix(board.bground_grid, 0, 0,0,True)
        #스톤 그리기
        draw_matrix(stone.stone,stone.stone_x, stone.stone_y, 0,True)
        draw_matrix(stone.next_stone,cols+1, 2, 0,True)
        
        if len(interf.stone):
            draw_matrix(interf.stone,interf.stone_x, interf.stone_y, 0,True)
            if len(interf.next_stone):
                draw_matrix(interf.next_stone[0],cols+6, 2, 0,True)
            
        #보드 그리기
        draw_matrix(board.board, 0, 0, 0,True)
                    
        if stone.score != stone.score_pre:
            client.send_score(user_name, stone.score)
            stone.score_pre = stone.score
    msg.drawStatusMsg()
    pygame.display.update() #화면 갱신
    clock.tick(30) #초당 30프레임 
    
# pyinstaller -w -F .\tetris.py
# pyinstaller --onefile --debug=all test.py
# pyinstaller -w -F --debug=all game.py