import pygame
import numpy as np

pygame.init()

clock = pygame.time.Clock()

screen_width,screen_height = 700,500
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Falling sand simulation")

#COLORS
BLACK = (0,0,0)
ORANGE = (252, 205, 42)
BLUE = (67, 121, 242)

#drawing variables
cell_size = 10

#intialize the environnement matrix
world_matrix = np.zeros((screen_height//cell_size,screen_width//cell_size))


def render_world(surface,world_matrix):
    for i in range(len(world_matrix)):
        for j in range(len(world_matrix[i])):
            #draw sand block
            if world_matrix[i,j] == 1:
                pygame.draw.rect(surface,(ORANGE),(j*cell_size,i*cell_size,cell_size,cell_size))
            elif world_matrix[i,j] == 2:
                pygame.draw.rect(surface,(BLUE),(j*cell_size,i*cell_size,cell_size,cell_size))


def place_block(world_matrix,block_index):
    mouse_pos = pygame.mouse.get_pos()
    mapped_x,mapped_y = mouse_pos[0]//cell_size,mouse_pos[1]//cell_size
    world_matrix[mapped_y,mapped_x] = block_index


def update_world(world_matrix):

    for i in range(len(world_matrix)-1,0,-1):
        for j in range(len(world_matrix[i])-1,0,-1):
            block = world_matrix[i,j]
            if block == 1: # Sand block
                if i < len(world_matrix)-1 and j < len(world_matrix[i])-1 and j > 0:
                    if world_matrix[i+1,j] == 0:
                        world_matrix[i+1,j] = 1
                        world_matrix[i,j] = 0
                    elif world_matrix[i+1,j+1] == 0 and np.random.rand() > 0.5:
                        world_matrix[i+1,j+1] = 1
                        world_matrix[i,j] = 0
                    elif world_matrix[i+1,j-1] == 0:
                        world_matrix[i+1,j-1] = 1
                        world_matrix[i,j] = 0
            if block == 2:  # Water block
                # Check if the block can move down
                if i < len(world_matrix) - 1:
                    if world_matrix[i + 1, j] == 0:  # Empty below
                        world_matrix[i + 1, j] = 2
                        world_matrix[i, j] = 0
                    # If blocked below, try to move left or right
                    elif j > 0 and world_matrix[i + 1, j - 1] == 0:  # Down-left
                        world_matrix[i + 1, j - 1] = 2
                        world_matrix[i, j] = 0
                    elif j < len(world_matrix[i]) - 1 and world_matrix[i + 1, j + 1] == 0:  # Down-right
                        world_matrix[i + 1, j + 1] = 2
                        world_matrix[i, j] = 0
                    # If blocked below and diagonals, check left and right for horizontal flow
                    elif j > 0 and world_matrix[i, j - 1] == 0:  # Left
                        world_matrix[i, j - 1] = 2
                        world_matrix[i, j] = 0
                    elif j < len(world_matrix[i]) - 1 and world_matrix[i, j + 1] == 0:  # Right
                        world_matrix[i, j + 1] = 2
                        world_matrix[i, j] = 0

on = True

#game loop
while on:

    #fill background with black
    screen.fill(BLACK)

    #check for mouse click
    mouse = pygame.mouse.get_pressed()
    #check for left click
    if mouse[0]:
        place_block(world_matrix,1)
    if mouse[2]:
        place_block(world_matrix,2)

    #draw the canvas
    render_world(screen,world_matrix)

    update_world(world_matrix)


    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            on = False
        


    clock.tick(120)
    pygame.display.flip()


pygame.quit()