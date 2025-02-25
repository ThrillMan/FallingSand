import pygame
import numpy as np
from copy import copy, deepcopy
import random
import colorsys
def draw():
    for i in range(sand_matrix_height):
        for j in range(sand_matrix_width):
            if sand_matrix[i][j]>=1:
                x_coord = i * SAND_PARTICLE_SIZE
                y_coord = j * SAND_PARTICLE_SIZE
                sand = pygame.Rect(x_coord,y_coord,
                                   SAND_PARTICLE_SIZE,
                                   SAND_PARTICLE_SIZE)

                sand_matrix_color = sand_matrix[i][j]
                hue = sand_matrix_color/250
                col = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
                rgb = tuple(int(c * 255) for c in col)
                color = pygame.Color(rgb)

                pygame.draw.rect(screen, color, sand)

def update_sand_state():
    new_state = deepcopy(sand_matrix)
    for i in range(sand_matrix_height):
        for j in range(sand_matrix_width-1):
            if sand_matrix[i][j]>=1:
                color = sand_matrix[i][j]
                if sand_matrix[i][j+1]==0:
                    # Empty space below -> fall straight down
                    new_state[i][j]=0
                    new_state[i][j + 1]=color
                if sand_matrix[i][j+1]>=1:
                    # Make sand fall to the left or to the right if
                    # there is an empty spot next to it
                    if random.randint(0,1)==0:
                        # Left
                        if i>0:
                            if sand_matrix[i-1][j+1]==0:
                                new_state[i][j] = 0
                                new_state[i-1][j+1]=color
                    else:
                        # Right
                        if i < sand_matrix_width-1:
                            if sand_matrix[i + 1][j + 1] == 0:
                                new_state[i][j] = 0
                                new_state[i + 1][j + 1] = color


    return new_state

def brush(x,y):
    global sand_color
    if sand_color>250:
        sand_color=1

    sand_matrix[x_coord][y_coord] = sand_color
    sand_color+=1
    matrix = 5
    extent = matrix // 2
    for i in range(-extent,extent):
        for j in range(-extent,extent):
            col = x_coord + i
            row = y_coord + j
            if(col>=0 and col<sand_matrix_width-1 and row>=0 and row<sand_matrix_height):
                sand_matrix[col][row] = sand_color
                sand_color+=1

WIDTH = 1000
HEIGHT = 1000
SAND_PARTICLE_SIZE = 5
sand_matrix = np.zeros((WIDTH//SAND_PARTICLE_SIZE
                        , HEIGHT//SAND_PARTICLE_SIZE))
sand_matrix_width = len(sand_matrix[0])
sand_matrix_height = len(sand_matrix)

sand_color = 1

pygame.init()
pygame.display.set_caption('FallingSand')
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen_rect = screen.get_rect()

mouse_pressed = False


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pressed = True
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_pressed = False


    if mouse_pressed:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if mouse_x>=WIDTH or mouse_y>=HEIGHT:
            continue
        if mouse_x<0 or mouse_y<0:
            continue
        x_coord = mouse_x // SAND_PARTICLE_SIZE
        y_coord = mouse_y // SAND_PARTICLE_SIZE

        brush(x_coord,y_coord)
    sand_matrix = update_sand_state()
    screen.fill((0, 0, 0))
    draw()
    pygame.display.update()
    clock.tick(60)