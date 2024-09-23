import pygame
from pygame import *
import random
from drawImg import *
from exam import *

class CreateEng:    
    isMousePressed = False
    isGameOver = False
    gameover_delay_on = False
    msg_result = ''
    score = 0
    quiz = {
        'answer1' :  {'rect':pygame.Rect(0,150,150,150),'word':'',},
        'answer2' :  {'rect':pygame.Rect(0,150,150,150),'word':'',},
        'answer3' :  {'rect':pygame.Rect(0,150,150,150),'word':'',},
        'question' : {'rect':pygame.Rect(0,0,200,60),'word':'','correct':'',}
        }
    
    
    def __init__(self,screen:Surface) -> None:
        self.screen = screen
                
        self.snd_click = pygame.mixer.Sound(f'./sound/click.wav')
        self.snd_gameover = pygame.mixer.Sound(f'./sound/game_over.wav')
        
        self.quiz['answer2']['rect'].centerx = self.screen.get_width()/2
        self.quiz['answer1']['rect'].right = self.quiz['answer2']['rect'].left-20
        self.quiz['answer3']['rect'].left = self.quiz['answer2']['rect'].right+20
        self.quiz['question']['rect'].centerx = self.screen.get_width()/2
        self.quiz['question']['rect'].bottom = self.screen.get_height()-20
        
        self.image_squirrel = pygame.image.load('./images/squirrel.png').convert_alpha()
        self.image_squirrel = pygame.transform.scale(self.image_squirrel, (200, 200))
        self.rect_squirrel = self.image_squirrel.get_rect()
        
        self.image_score = pygame.image.load('./images/score.png').convert_alpha()
        self.image_score = pygame.transform.scale(self.image_score, (200, 100))
        self.rect_score = self.image_score.get_rect()
        self.rect_score.centerx = self.screen.get_width()/2
        self.rect_score.centery = self.screen.get_height()/2+160
        
        self.image_basket = pygame.image.load('./images/basket.png').convert_alpha()
        self.image_basket = pygame.transform.scale(self.image_basket, (200, 60))
        self.rect_basket = self.image_basket.get_rect()
        self.rect_basket.centerx = self.screen.get_width()/2
        self.rect_basket.bottom = self.screen.get_height()-30
        
        self.restart_btn_tick = 0
        
        self.result_group = pygame.sprite.Group()
        self.reset_game()

    def reset_game(self):
        self.result_group.empty()
        self.words_quiz = list(ExamDic.words.keys())
        self.create_next_quiz()
        self.msg_result = ''
        self.score = 0
        
    def create_next_quiz(self):
        if len(self.words_quiz) > 0:
            selct_quiz = random.choice(self.words_quiz) #랜덤으로 하나 선택
            self.words_quiz.remove(selct_quiz) #선택된것은 리스트에서 삭제
            word_correct = ExamDic.words[selct_quiz] #선택된 것으로 정답을 가져온다.
            self.quiz['question']['word'] = selct_quiz
            self.quiz['question']['correct'] = word_correct

            words_eng = list(ExamDic.words.values()) #예제 단어를 모두 가져온다.
            words_eng.remove(word_correct) #정답 단어는 삭제한다.
            words_eng = random.sample(words_eng,3) #3개를 선택한다.
            words_eng[0] = word_correct #첫번째에 정답을 넣는다.
            random.shuffle(words_eng) #보기를 섞는다.
            
            self.quiz['answer1']['word'] = words_eng[0]
            self.quiz['answer2']['word'] = words_eng[1]
            self.quiz['answer3']['word'] = words_eng[2]        
            return True
        else:
            return False
        
    def display_text(self,msg, centerx, centery,color):    
        if len(msg):
            font = pygame.font.SysFont("malgungothic", 30)    
            img = font.render(msg , 1, color)
            rect = img.get_rect()
            rect.centerx = centerx
            rect.centery = centery
            self.screen.blit(img,(rect.x, rect.y))
        
    def display_box(self,quiz,correct=None):
        color = (255,255,255)
        offset_y = 0
        if correct is not None and self.isGameOver==False:
            offset_y = 60
            self.rect_squirrel.center = quiz['rect'].center
            self.screen.blit(self.image_squirrel, self.rect_squirrel)
            mouse_pos = pygame.mouse.get_pos()
            if quiz['rect'].collidepoint(mouse_pos):
                color = (200,0,0)
                if pygame.mouse.get_pressed()[0]:
                    if self.isMousePressed==False:
                        if quiz['word'] == correct:
                            self.msg_result = '정답'
                            self.score += 10
                        else:
                            self.msg_result = '오답'
                        self.isMousePressed = True
                        self.snd_click.play()
                        
                        img = DrawImg(self.screen, 
                                      quiz['rect'].centerx, 
                                      quiz['rect'].centery, 
                                      self.quiz['question']['rect'].centerx, 
                                      self.quiz['question']['rect'].top, 
                                      )
                        self.result_group.add(img)
                else:
                    if self.isMousePressed:
                        if self.create_next_quiz() == False:
                            self.isGameOver = True
                            self.gameover_delay_on = True
                            self.snd_gameover.play()
                    self.isMousePressed = False
                
        # pygame.draw.rect(self.screen, color,quiz['rect'],1)    
        self.display_text(quiz['word'],quiz['rect'].centerx,quiz['rect'].centery+offset_y,color)  
                      
    def restart_btn(self):
        font = pygame.font.SysFont("malgungothic", 30)    
        img = font.render("재시작(클릭)" , 1, (255,0,0),(255,255,255))
        
        elapse = pygame.time.get_ticks()-self.restart_btn_tick
        if elapse < 200:
            img.set_alpha(100)
        elif elapse < 400:
            img.set_alpha(200)
        else:
            self.restart_btn_tick = pygame.time.get_ticks()
            img.set_alpha(100)
            
        rect = img.get_rect()
        rect.centerx = self.screen.get_width()/2
        rect.centery = self.screen.get_height()/2+50
        
        mouse_pos = pygame.mouse.get_pos()
        if rect.collidepoint(mouse_pos):
            img.set_alpha(200)
            if pygame.mouse.get_pressed()[0]:
                return True
        self.screen.blit(img,(rect.x, rect.y))
        return False
    
    def draw_score(self):
        self.screen.blit(self.image_score, self.rect_score)        
        self.display_text(f'점수:{self.score}', self.rect_score.centerx,self.rect_score.centery+10,(255,255,255))
        
    def draw(self):
        
        if self.gameover_delay_on:
            for res in self.result_group:
                if res.is_finish==False:
                    break
            else:
                self.gameover_delay_on = False
            
        self.draw_score()
        
        if self.isGameOver and self.gameover_delay_on==0:
            if self.restart_btn():
                self.isGameOver = False
                self.reset_game()
        else:           
            
            correct = self.quiz['question']['correct']
            self.display_box(self.quiz['answer1'],correct)
            self.display_box(self.quiz['answer2'],correct)
            self.display_box(self.quiz['answer3'],correct)
            
            self.screen.blit(self.image_basket, self.rect_basket)            
            self.display_box(self.quiz['question'])
            
            self.result_group.update()
            self.result_group.draw(self.screen)
            
            self.display_text(self.msg_result, self.screen.get_width()/2,self.screen.get_height()/2+80,(255,255,0))
            