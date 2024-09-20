import pygame
from pygame import *
from shapeLoad import *

from board import *
from stone import *
from interference import *

class Draw_line():
    def __init__(self,screen:Surface,cell_size,rlim,cols) -> None:
        self.screen = screen
        self.cell_size = cell_size
        self.rlim = rlim
        self.cols = cols
        self.design_mode = 0
        self.shape = ShapeLoad(self.cell_size)
    
                
    def draw_rect(self,p_x,p_y,color,Thickness,outline,divide = 1,alpha=None):
        rect = pygame.Rect(p_x,p_y,self.cell_size/divide,self.cell_size/divide)
        if alpha is None:
            pygame.draw.rect(self.screen,color,rect,Thickness)
        else:
            temp_surface = pygame.Surface((rect.width,rect.height))
            pygame.draw.rect(temp_surface,color,(0,0,rect.width,rect.height),Thickness)
            temp_surface.set_alpha(alpha)
            self.screen.blit(temp_surface, rect)
            # pygame.draw.rect(self.screen,color,rect,Thickness)
        
        if outline:
            # pygame.draw.rect(self.screen,(200,200,200),rect,1)
            temp_surface = pygame.Surface((rect.width,rect.height))
            pygame.draw.rect(temp_surface,(90,90,90),(0,0,rect.width,rect.height),1)
            temp_surface.set_alpha(alpha)
            self.screen.blit(temp_surface, rect)
        
    def draw_guide_line(self):
        rect = pygame.Rect(self.rlim,0,self.screen.get_width()-self.rlim,220)
        pygame.draw.rect(self.screen,(255,255,255),rect, 1)
        
        rect.top = rect.bottom
        rect.height = 360
        pygame.draw.rect(self.screen,(255,255,255),rect, 1)
        
        rect.top = rect.bottom
        rect.height = 200
        pygame.draw.rect(self.screen,(255,255,255),rect, 1)
        
        rect.top = rect.bottom
        rect.height = self.screen.get_height()- rect.top
        pygame.draw.rect(self.screen,(255,255,255),rect, 1)
    
    def draw_matrix(self,matrix, off_x,off_y,Thickness,outline = (200,200,200),divide = 1, alpha = None,freeze=False):
        if divide>1:
            x_start_offset = (off_x *self.cell_size)/divide
        else:
            x_start_offset = 0
            
        for y, row in enumerate(matrix):
            if divide > 1:
                p_x = (off_x) *(self.cell_size)
            for x, color in enumerate(row):
                if color is not None:
                    # if divide > 1:
                    #     p_x += cell_size/divide
                    # else:
                    #     p_x = (off_x+x) *(cell_size)
                    p_x = (off_x+x) *(self.cell_size/divide) + x_start_offset
                    p_y = (off_y+y) *(self.cell_size/divide)
                    
                    if (str(type(color)) == "<class 'tuple'>"):                    
                        self.draw_rect(p_x,p_y,color,Thickness,outline,divide,alpha)
                    else:
                        color -= 1
                        if freeze:
                            img = self.shape.shape['stone'][1]
                            if divide > 1:
                                img = pygame.transform.scale(img,(int(self.cell_size/divide),int(self.cell_size/divide)))
                            self.screen.blit(img, (p_x,p_y,))
                        elif self.design_mode==0:
                            # color= shape.shape['color'][color]
                            # draw_rect(p_x,p_y,color,Thickness,outline,divide)
                            img = self.shape.shape['color'][color]
                            if divide > 1:
                                img = pygame.transform.scale(img,(int(self.cell_size/divide),int(self.cell_size/divide)))
                            self.screen.blit(img, (p_x,p_y,))
                        elif self.design_mode==1:
                            img = self.shape.shape['char'][color]
                            if divide > 1:
                                img = pygame.transform.scale(img,(int(self.cell_size/divide),int(self.cell_size/divide)))
                            self.screen.blit(img, (p_x,p_y,))
                        elif self.design_mode==2:
                            img = self.shape.shape['stone'][color]
                            if divide > 1:
                                img = pygame.transform.scale(img,(int(self.cell_size/divide),int(self.cell_size/divide)))
                            self.screen.blit(img, (p_x,p_y,))
                            
    def draw(self,board:Board,stone:Stone,interf:Interference, freeze):        
        #게임화면 구분선
        pygame.draw.line(self.screen,(255, 255, 255),(self.rlim+1, 0),(self.rlim+1, self.screen.get_height())) 
            
        #게임화면 바둑판
        self.draw_matrix(board.bground_grid, 0, 0,0,True,alpha=150)
        
        if len(stone.stone) > 0:
            board.set_trace_grid_width_stone(stone.stone_x,stone.stone_y,len(stone.stone[0]))
            self.draw_matrix(board.trace_grid, 0, 0,0,True,alpha=20)
            
        #스톤 그리기
        self.draw_matrix(stone.stone,stone.stone_x, stone.stone_y, 0,True,freeze=freeze)
        
        for cnt in range(len(stone.next_stone)):
            self.draw_matrix(stone.next_stone[cnt],self.cols+1, 2+(3*cnt), 0,True,2,freeze=freeze)
        
        if len(interf.stone):
            self.draw_matrix(interf.stone,interf.stone_x, interf.stone_y, 0,True,freeze=freeze)
            if len(interf.next_stone):
                for cnt in range(len(interf.next_stone)):
                    self.draw_matrix(interf.next_stone[cnt],self.cols+6, 2+(3*cnt), 0,True,2,freeze=freeze)
                    if cnt >=2:
                        break
            
        #보드 그리기
        self.draw_matrix(board.board, 0, 0, 0,True)
        self.draw_guide_line()