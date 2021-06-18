# pygame code for Kuba

################################################################################
# Imports ######################################################################
################################################################################
import pygame, sys, math

from pygame.locals import *

import KubaGame
from KubaGame import KubaGame

################################################################################
# Kuba Game Setup ##############################################################
################################################################################

# initialize the board to starting position
game = KubaGame(('PlayerA', 'W'), ('PlayerB', 'B'))
print("Board start (below)")
game.display_board()

# game.make_move('PlayerA', (0,0), 'R')

################################################################################
# Screen Setup #################################################################
################################################################################

# initialize all the modules required for PyGame
pygame.init()

# define constants for the screen width and height
SCREEN_WIDTH = 720
SCREEN_HEIGHT = 720

# tile color RGB combos
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
grey = (192, 192, 192)

# set tile information (coordinates, color)
tile_x = 0
tile_y = 0
tile_color = white
tile_width = 80
tile_height = 80
tile_radius = 40

# create the screen object
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

running = True
################################################################################
# Game Loop ####################################################################
################################################################################
while running:
    # since the game will be a series of events, this syntax will help empty the events'
    #  queue before adding a new one
    for event in pygame.event.get():

        # fill the background with a color
        screen.fill(grey)

        # start editing the output window
        pygame.display.set_caption("Kuba Board Game")  # set window title

        # did the user hit a key?
        if event.type == KEYDOWN:
            # if the user presses escape, stop the loop
            if event.key == K_ESCAPE:
                running = False

        # currently allows left click, right click, scroll
        elif event.type == MOUSEBUTTONDOWN:
            # store mouse click coordinates
            mx, my = pygame.mouse.get_pos()

            for row in range(60, 720, 100):
                for col in range(60, 720, 100):
                    x_pos = row
                    y_pos = col

                    mx_sq = (mx - x_pos)**2
                    my_sq = (my - y_pos)**2

                    if math.sqrt(mx_sq + my_sq) <= 40:
                        marble_index = (int((y_pos - 60) / 100), int((x_pos - 60) / 100))
                        print(marble_index)


        elif event.type == pygame.QUIT:
            running = False

        # display all marbles on the board
        x_counter = 60
        y_counter = 60
        for row in game.get_board()[1:8]:
            for tile in row[1:8]:
                if x_counter > 660:
                    x_counter = 60

                if tile == 'W':
                    pygame.draw.circle(screen, white, (x_counter, y_counter), tile_radius)

                if tile == 'R':
                    pygame.draw.circle(screen, red, (x_counter, y_counter), tile_radius)

                if tile == 'B':
                    pygame.draw.circle(screen, black, (x_counter, y_counter), tile_radius)

                # move across the board to the right for every tile
                #  until it reaches 660, then reset to 0
                x_counter += 100

            # move down the board row by row until y_counter reaches 600 then stop
            y_counter += 100

        # call to update output screen
        pygame.display.flip()
