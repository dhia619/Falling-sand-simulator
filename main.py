import pygame
import numpy as np
from random import choice
from tool import *

pygame.init()

clock = pygame.time.Clock()

screen_width,screen_height = 1000,700
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Falling sand simulation")

#COLORS
BLACK = (0,0,0)
WHITE = (255,255,255)
ORANGE = (252, 205, 42)
BLUE = (67, 121, 242)
GRAY = (142, 172, 205)
SAND = [(252, 205, 42),(210, 180, 140),(222, 184, 135),(238, 232, 170)]

#drawing variables
cell_size = 4
simulation_display_width,simulation_display_height = screen_width-100,screen_height

#intialize the environnement matrix
world_matrix = np.zeros((simulation_display_height//cell_size,simulation_display_width//cell_size))

#tools
tool_start_y = 20
water = Tool("assets/water.png",screen_width-75,tool_start_y)
fire = Tool("assets/fire.png",screen_width-75,tool_start_y+70)
sand = Tool("assets/sand.png",screen_width-75,tool_start_y+150)
stone = Tool("assets/stone.png",screen_width-75,tool_start_y+230)
tools = [water,fire,sand,stone]

def render_world(surface,world_matrix):
    block_color = ORANGE
    for i in range(len(world_matrix)):
        for j in range(len(world_matrix[i])):
            if world_matrix[i,j] != 0:
                # Sand
                if world_matrix[i,j] < len(SAND):block_color = SAND[int(world_matrix[i,j])]
                # Water
                elif world_matrix[i,j] == 10:block_color = BLUE
                # Stone
                elif world_matrix[i,j] == 11:block_color = GRAY
                #draw the block
                pygame.draw.rect(surface,(block_color),(j*cell_size,i*cell_size,cell_size,cell_size))


brush_size = 2

def place_block(world_matrix, block_index, mouse_pos):
    if mouse_pos[0] < simulation_display_width:  # Ensure cursor is in the simulation area
        mapped_x, mapped_y = mouse_pos[0] // cell_size, mouse_pos[1] // cell_size
        mapped_x = min(mapped_x, simulation_display_width // cell_size - 1)  # Prevent cursor out of the window
        mapped_y = min(mapped_y, simulation_display_height // cell_size - 1)

        # Draw a block area based on the brush size
        for i in range(-brush_size // 2, brush_size // 2 + 1):
            for j in range(-brush_size // 2, brush_size // 2 + 1):
                new_x = mapped_x + j
                new_y = mapped_y + i
                if 0 <= new_x < simulation_display_width // cell_size and 0 <= new_y < simulation_display_height // cell_size:
                    world_matrix[new_y, new_x] = block_index

def move_block(world_matrix,i,j,new_i,new_j,block):
    if world_matrix[new_i,new_j] == 0:
        world_matrix[new_i,new_j] = block
        world_matrix[i,j] = 0
        return True
    
    elif i < simulation_display_height//cell_size - 1 and world_matrix[i+1,j] == 10 and block != 10:
        world_matrix[i+1,j] = block
        world_matrix[i,j] = 10
        return True

    return False

def block_behaviour(world_matrix,visited,block,i,j):

    """ i : y coordinate 
        j : x coordinate
    """

    if block < 9:  # Sand block
        if i < len(world_matrix) - 1:  # Ensure there's space below to move down

            # Right border: block can only move down or down-left
            if j == simulation_display_width // cell_size - 1:
                if move_block(world_matrix, i, j, i + 1, j, block):  # Move down
                    return
                elif move_block(world_matrix, i, j, i + 1, j - 1, block):  # Move down-left
                    return

            # Left border: block can only move down or down-right
            elif j == 0:
                if move_block(world_matrix, i, j, i + 1, j, block):  # Move down
                    return
                elif move_block(world_matrix, i, j, i + 1, j + 1, block):  # Move down-right
                    return

            # General case: block can move down, down-right, or down-left
            else:
                if move_block(world_matrix, i, j, i + 1, j, block):  # Move down
                    return
                elif move_block(world_matrix, i, j, i + 1, j + 1, block) and np.random.rand() > 0.5:  # Down-right
                    return
                elif move_block(world_matrix, i, j, i + 1, j - 1, block):  # Down-left
                    return

                     
    if block == 10 and not visited[i, j]:  # Water block and hasn't moved yet
        # Check if the block can move down 
        if i < len(world_matrix) - 1 and move_block(world_matrix,i,j,i+1,j,block):
            visited[i + 1, j] = 1
        else:
            # Randomize left/right movement to avoid oscillation
            direction = choice(['left', 'right'])
            
            if direction == 'left' and j > 0:
                # Move horizontally left
                if move_block(world_matrix,i,j,i,j-1,block):
                    visited[i, j - 1] = 1
            elif direction == 'right' and j < len(world_matrix[i]) - 1:
                # Move horizontally right
                if move_block(world_matrix,i,j,i,j+1,block):
                    visited[i, j + 1] = 1

def update_world(world_matrix):

    # Create a "visited" matrix to track blocks that have moved in the current update
    visited = np.zeros_like(world_matrix)

    for i in range(len(world_matrix)-1,-1,-1):
        for j in range(len(world_matrix[i])-1,-1,-1):
            block = world_matrix[i,j]
            if block != 0:
                block_behaviour(world_matrix,visited,block,i,j)
                continue

selected_block = 1

on = True

#game loop
while on:
    
    mouse_pos = pygame.mouse.get_pos()
    
    #fill background with black
    screen.fill(BLACK)

    #draw vertical line to seperate the simulation canvas from the tool menu
    pygame.draw.line(screen,WHITE,(screen_width-100,0),(screen_width-100,screen_height),1)

    #draw the tools
    for t in tools:
        t.draw(screen,mouse_pos)

    #check for mouse click
    mouse = pygame.mouse.get_pressed()
    # left click : draw
    if mouse[0]:
        if selected_block < 10:
            selected_block = np.random.randint(0,len(SAND)-1)
        place_block(world_matrix,selected_block,mouse_pos)
        
        for t in tools:
            if t.rect.collidepoint(mouse_pos):
                if t == water:
                    selected_block = 10
                elif t == sand:
                    selected_block = np.random.randint(0,len(SAND)-1)
                elif t == stone:
                    selected_block = 11
    # right click : erase
    if mouse[2]:
        place_block(world_matrix,0,mouse_pos)

    #check for keyboard press
    keys = pygame.key.get_pressed()
    if keys[pygame.K_1]:
        selected_block = np.random.randint(0,len(SAND)-1) # Sand
    if keys[pygame.K_2]:
        selected_block = 10 # Water
    if keys[pygame.K_3]:
        selected_block = 11 # Stone
    #draw the canvas
    render_world(screen,world_matrix)

    update_world(world_matrix)

    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            on = False
        


    clock.tick(60)
    pygame.display.flip()


pygame.quit()