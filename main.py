import time

import pygame
import random

#value
Game_W,Game_H=400,700
bird_move=0
Valocity=0.2
Game_Active=False
Score=0
High_Score=0
i=0
A=False
def show_bg():
    screen.blit(bg,(0,0))

def show_base(x_run):
    screen.blit(bg_base,(x_run,height_base))
    screen.blit(bg_base, (x_run+x_base,   height_base))

def Create_pipe():
    Height= random.randint(350,520)
    Width_Average=random.randint(630,680)
    buttom_pipe=pipe_bg.get_rect(midtop=(450,Height))
    top_pipe = pipe_bg.get_rect(midtop=(450, Height-Width_Average))
    return  buttom_pipe,top_pipe
def pipe_move(pipes):
    for pipe in pipes:
        pipe.centerx -=5
    return  pipes
def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom>=700:
            screen.blit(pipe_bg,pipe)
        else:
            flip =pygame.transform.flip(pipe_bg,False,True)
            screen.blit(flip, pipe)

def Colliderect(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            sound_die.play()
            return False
    if bird_rect.bottom>=height_base or bird_rect.top <= 0:
        sound_die.play()
        return False
    return True
def Game_Over():
    screen.blit(gameover,(Game_W/2-x_go/2,Game_H/2-y_go/2))

def Message_Game():
    screen.blit(message_game, (Game_W / 2 - x_mg / 2, Game_H / 2 - y_mg / 2))
def display_font(status):
    if status=="start":
        score_font=game_font.render("{}".format(int(Score)),True,(255,255,255))
        score_rect=score_font.get_rect(center=(200,int(Game_H/12)))
        screen.blit(score_font,score_rect)
    if status=="over":
        score_font=game_font.render("Score : {}".format(int(Score)),True,(255,255,255))
        score_rect=score_font.get_rect(center=(200,int(Game_H/12)))
        screen.blit(score_font,score_rect)

        Hscore_font = game_font.render("High Score : {}".format(int(High_Score)), True, (255, 255, 255))
        Hscore_rect = score_font.get_rect(center= (165, int(Game_H- Game_H / 6)))
        screen.blit(Hscore_font, Hscore_rect)

def Update_HScore(Score,High_Score):
    if(Score > High_Score):
        High_Score=Score
    return High_Score

def Score_Update(Score,pipes):
    for pipe in pipes:
        if pipe.centerx==90:
            sound_score.play()
            Score+=0.5
    return Score
def rotated_bird(bird):
    bird_new= pygame.transform.rotozoom(bird,-bird_move*3,1)
    return bird_new
def animating():
    New_Bird_Index = bird_Array[index]
    New_Bird_Rect= New_Bird_Index.get_rect(center=(birdX,bird_rect.centery))
    return New_Bird_Index,New_Bird_Rect

pygame.mixer.pre_init(frequency=44100,size=-16,channels=2,buffer=512)
pygame.init()
#font game
game_font = pygame.font.Font("04B_19.TTF",25)
#create the screen
screen = pygame.display.set_mode((Game_W,Game_H))

#title
pygame.display.set_caption("BIRD FLY WITH WEAPONS")
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)

#bird
birdD = pygame.image.load("img/bluebird-downflap.png")
birdM = pygame.image.load("img/bluebird-midflap.png")
birdU = pygame.image.load("img/bluebird-upflap.png")

x=birdD.get_width()
y=birdD.get_height()
bird_Array=[birdD,birdM,birdU]
index=0
bird_Get_Array= bird_Array[index]
birdX=Game_W/6-x/2
birdY=Game_H/2-y/2
bird_rect =bird_Get_Array.get_rect(center=(birdX,birdY))
BIRD_ARRAY = pygame.USEREVENT



x_bird_move =birdD.get_width()

#bg
bg=pygame.image.load("img/background-day.png")
bg=pygame.transform.scale(bg,(Game_W,Game_H)).convert()

#base
x_run=0
bg_base = pygame.image.load("img/base.png")
x_base=bg_base.get_width()
y_base= bg_base.get_height()
bg_base = pygame.transform.scale(bg_base,(Game_W,y*4))
height_base = Game_H - bg_base.get_height()

#pipe
pipe_bg = pygame.image.load("img/pipe-green.png")
pipe_x=pipe_bg.get_width()
pipe_y=pipe_bg.get_height()
pipe_y=int(pipe_y*3/2)
pipe_bg = pygame.transform.scale(pipe_bg,(pipe_x,pipe_y))
pipe_list=[]
pipess=[776]
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,1300)

#gameover
gameover = pygame.image.load("img/gameover.png")
x_go=gameover.get_width()
y_go=gameover.get_height()

#message_game
message_game = pygame.image.load("img/message.png")
x_mg=message_game.get_width()
y_mg=message_game.get_height()
#clock
clock = pygame.time.Clock()

#Sound
sound_fly= pygame.mixer.Sound("sound/sfx_wing.wav")
sound_die= pygame.mixer.Sound("sound/sfx_die.wav")
sound_score=pygame.mixer.Sound("sound/sfx_point.wav")
#game LOOP
run = True

screen.fill((0,0,0))
while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key==pygame.K_SPACE and Game_Active:
                bird_move=0
                bird_move -= 7
            if event.key==pygame.K_SPACE and Game_Active==False:
                Message_Game()
                Game_Active=True
                sound_fly.play()
                pipe_list.clear()
                bird_rect.center=(birdX,birdY)
                bird_move=-2
                Score = 0
        if event.type==pygame.MOUSEBUTTONUP and Game_Active:
            bird_move = 0
            bird_move -= 7
        if event.type==pygame.MOUSEBUTTONUP and Game_Active==False:
            Message_Game()
            Game_Active=True
            sound_fly.play()
            pipe_list.clear()
            bird_rect.center=(birdX,birdY)
            bird_move=-2
            Score=0
        if event.type== SPAWNPIPE and Game_Active:

            pipe_list.extend(Create_pipe())
            x=len(pipe_list)
            del pipe_list[0:x-2]
        if event.type == BIRD_ARRAY and Game_Active:
            if index<2:
                index+=1
            else:
                index=0
            bird_Get_Array,bird_rect=animating()

#begin_game
    #massage_game
    Message_Game()
    #background
    show_bg()


    if Game_Active:
        # bird_move
        bird_move += Valocity
        bird_rotated=rotated_bird(bird_Get_Array)
        bird_rect.centery += bird_move
        screen.blit(bird_rotated, bird_rect)

        Game_Active = Colliderect(pipe_list)
        # pipe
        pipe_list = pipe_move(pipe_list)
        draw_pipe(pipe_list)

        #Score
        Score =Score_Update(Score,pipe_list)
        display_font("start")
    else:

        High_Score = Update_HScore(Score,High_Score)
        display_font("over")
        Message_Game()
        x_run=0

    #base_move
    x_run -=1
    show_base(x_run)
    if x_run <= -x_base:
        x_run=0



    pygame.display.update()
    clock.tick(120)
#end_game
