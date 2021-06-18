# pygame code for Kuba

################################################################################
# Imports ######################################################################
################################################################################
import pygame, sys, math

from pygame.locals import *

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

# set tile information (coordinates, color)
tile_radius = 40
tile_spacing = 5

# define constants for the screen width and height
SCREEN_WIDTH = (8 * tile_spacing) + (7 * 2 * tile_radius)
SCREEN_HEIGHT = (8 * tile_spacing) + (7 * 2 * tile_radius)

# tile color RGB combos
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
grey = (192, 192, 192)

# create the screen object
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


################################################################################
# Game Loop ####################################################################
################################################################################
running = True
while running:
    # since the game will be a series of events, this syntax will help empty the events'
    #  queue before adding a new one
    for event in pygame.event.get():

        # fill the background with a color
        screen.fill(grey)

        # start editing the output window
        pygame.display.set_caption("Kuba Board Game")  # set window title

        # display all marbles on the board
        x_counter = tile_radius + tile_spacing
        y_counter = tile_radius + tile_spacing
        for row in game.get_board()[1:8]:
            for tile in row[1:8]:
                if x_counter > (7 * tile_spacing) + ((6 * 2 + 1) * tile_radius):
                    x_counter = tile_radius + tile_spacing

                if tile == 'W':
                    pygame.draw.circle(screen, white, (x_counter, y_counter), tile_radius)

                if tile == 'R':
                    pygame.draw.circle(screen, red, (x_counter, y_counter), tile_radius)

                if tile == 'B':
                    pygame.draw.circle(screen, black, (x_counter, y_counter), tile_radius)

                # move across the board to the right for every tile
                #  until it reaches 660, then reset to 0
                x_counter += 2 * tile_radius + tile_spacing

            # move down the board row by row until y_counter reaches 600 then stop
            y_counter += 2 * tile_radius + tile_spacing

        # did the user hit a key?
        if event.type == KEYDOWN:
            # if the user presses escape, stop the loop
            if event.key == K_ESCAPE:
                running = False

        # currently allows left click, right click, scroll
        elif event.type == MOUSEBUTTONDOWN:
            # store mouse click coordinates
            mx, my = pygame.mouse.get_pos()

            for row in range(tile_radius + tile_spacing,
                             (8 * tile_spacing) + (7 * 2 * tile_radius),
                             2 * tile_radius + tile_spacing):
                for col in range(tile_radius + tile_spacing,
                             (8 * tile_spacing) + (7 * 2 * tile_radius),
                             2 * tile_radius + tile_spacing):
                    x_pos = row
                    y_pos = col

                    mx_sq = (mx - x_pos) ** 2
                    my_sq = (my - y_pos) ** 2

                    if math.sqrt(mx_sq + my_sq) <= tile_radius:
                        marble_index = (int((y_pos - (tile_radius + tile_spacing)) / (2 * tile_radius + tile_spacing)),
                                        int((x_pos - (tile_radius + tile_spacing)) / (2 * tile_radius + tile_spacing)))
                        print(marble_index)
                        # output color of marble:
                        if screen.get_at((mx, my)) == white:
                            print('W')
                        elif screen.get_at((mx, my)) == black:
                            print('B')
                        elif screen.get_at((mx, my)) == red:
                            print('R')

        elif event.type == pygame.QUIT:
            running = False

        # call to update output screen
        pygame.display.flip()
