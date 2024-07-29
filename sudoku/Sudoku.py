import sys
import pygame
import time
import tkinter as tk
from tkinter import messagebox
from pygame.color import THECOLORS as COLORS
from build import print_matrix, give_me_a_game, check


def draw_background():
    screen.fill(COLORS['white'])
    #畫出背景網格
    #surface: 需要繪製到的表面（在程式中是 screen）。
    #color: 矩形的顏色（在程式中是 COLORS['black']）。
    #rect: 一個表示矩形位置和大小的元组 (x, y, width, height)。
    #width: 矩形邊框的寬度。如果為 0 或省略，則填充整个矩形。
    pygame.draw.rect(screen,COLORS['black'],(0,0,300,900),5)
    pygame.draw.rect(screen,COLORS['black'],(300,0,300,900),5)
    pygame.draw.rect(screen,COLORS['black'],(600,0,300,900),5)

    pygame.draw.rect(screen,COLORS['black'],(0,0,900,300),5)
    pygame.draw.rect(screen,COLORS['black'],(0,300,900,300),5)
    pygame.draw.rect(screen,COLORS['black'],(0,600,900,300),5)

def draw_choose():
    #在當前選中的格子上繪製一个藍色的矩形，用於顯示用户當前選擇的格子位置。
    pygame.draw.rect(screen,COLORS['green'],(cur_j*100+5,cur_i*100+5,100-10,100-10),0)

def check_win(matrix_all,matrix):
    if matrix_all == matrix:
        return True
    return False

def check_color(matrix,i,j):
    _matrix = [[col for col in row]for row in matrix]
    _matrix[i][j] = 0
    if check(_matrix,i,j,matrix[i][j]):
        return COLORS['blue']
    return COLORS['red']

def draw_number():
    for i in range(len(MATRIX)):
        for j in range(len(MATRIX[0])):
            _color = check_color(MATRIX,i,j) if (i,j) in BLANK_IJ else COLORS['gray']
            txt = font80.render(str(MATRIX[i][j] if MATRIX[i][j] not in [0,'0'] else ''),True,_color)
            x,y = j*100+30,i*100+10
            screen.blit(txt,(x,y))

def draw_context():
    txt = font40.render('Blank:'+str(cur_blank_size)+'   Change:'+str(cur_change_size),True,COLORS['black'])
    x,y = 10,900
    screen.blit(txt,(x,y))

def draw_countdown(remaining_time):
    txt = font40.render(f'Time: {remaining_time}', True, COLORS['black'])
    x, y = 700, 900
    screen.blit(txt, (x, y))

def show_message_box(title, message):
    root = tk.Tk()
    root.withdraw()  # 隱藏主視窗
    messagebox.showinfo(title, message)
    root.destroy()

# init pygame
pygame.init()

# contant
SIZE = [900,1000]
font80 = pygame.font.SysFont('Times', 80)
font100 = pygame.font.SysFont('Times', 90)
font40 = pygame.font.SysFont('Times', 40)

# create screen 500*500
screen = pygame.display.set_mode(SIZE)

# variable parameter
cur_i, cur_j = 0,0
cur_blank_size = int(sys.argv[1]) if len(sys.argv) > 1 else 10
cur_change_size = 0

# matrix abount
MATRIX_ANSWER,MATRIX,BLANK_IJ = give_me_a_game(blank_size=cur_blank_size)
print(BLANK_IJ)
print_matrix(MATRIX)

# countdown timer
countdown = 60  # 60 seconds countdown
start_time = time.time()

# main loop
running = True
while running:
    current_time = time.time()
    elapsed_time = current_time - start_time
    remaining_time = int(countdown - elapsed_time)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        elif event.type == pygame.MOUSEBUTTONDOWN:
            cur_j,cur_i = int(event.pos[0]/100),int(event.pos[1]/100)
        elif event.type == pygame.KEYUP:
            if chr(event.key) in ['1','2','3','4','5','6','7','8','9'] and (cur_i,cur_j) in BLANK_IJ:
                MATRIX[cur_i][cur_j] = int(chr(event.key))
                cur_blank_size = sum([1 if col==0 or col=='0' else 0 for row in MATRIX for col in row])
                cur_change_size +=1
    # background
    draw_background()
    # choose item
    draw_choose()
    # numbers
    draw_number()
    # point
    draw_context()
    # countdown timer
    draw_countdown(remaining_time)
    # flip
    pygame.display.update()

    # check win or not
    if check_win(MATRIX_ANSWER,MATRIX):
        show_message_box('Congratulations!', 'You win, very good!!!')
        break

    # check if time is up
    if remaining_time <= 0:
        show_message_box('Game Over', 'Time is up! You lose.')
        running = False
pygame.quit()
