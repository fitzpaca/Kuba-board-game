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

################################################################################
# Board Setup #################################################################
################################################################################

# initialize all the modules required for PyGame
pygame.init()

# set tile information (coordinates, color)
tile_radius = 50
tile_spacing = 5

# define constants for the board width and height
BOARD_WIDTH = (8 * tile_spacing) + (7 * 2 * tile_radius)
BOARD_HEIGHT = (8 * tile_spacing) + (7 * 2 * tile_radius)

# tile color RGB combos
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
grey = (192, 192, 192)
yellow = (255, 255, 51)
blue = (0, 0, 255)

# create the board object
board = pygame.display.set_mode((BOARD_WIDTH, BOARD_HEIGHT))

# create marble selector
marble_select = False
select_color = None
marble_color = None
select_pos = (0, 0)

marble_index = None
direction = None


################################################################################
# Game Loop ####################################################################
################################################################################
running = True
while running:
    # since the game will be a series of events, this syntax will help empty the events'
    #  queue before adding a new one
    for event in pygame.event.get():

        # fill the background with a color
        board.fill(grey)

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
                    pygame.draw.circle(board, white, (x_counter, y_counter), tile_radius)

                if tile == 'R':
                    pygame.draw.circle(board, red, (x_counter, y_counter), tile_radius)

                if tile == 'B':
                    pygame.draw.circle(board, black, (x_counter, y_counter), tile_radius)

                # move across the board to the right for every tile
                #  until it reaches 660, then reset to 0
                x_counter += 2 * tile_radius + tile_spacing

            # move down the board row by row until y_counter reaches 600 then stop
            y_counter += 2 * tile_radius + tile_spacing

        # display the marble selector highlight:
        if marble_select:
            if marble_color == black:
                select_color = yellow
            if marble_color == white:
                select_color = blue
            pygame.draw.circle(board, select_color, select_pos, tile_radius, 5)

        # let the user select a marble (currently allows left click, right click, scroll)
        if event.type == MOUSEBUTTONDOWN:
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

                    # if the user clicks on a valid marble position and there is a white marble in it
                    if math.sqrt(mx_sq + my_sq) <= tile_radius and board.get_at((mx, my)) == white:
                        # update the marble index
                        marble_index = (int((y_pos - (tile_radius + tile_spacing)) / (2 * tile_radius + tile_spacing)),
                                        int((x_pos - (tile_radius + tile_spacing)) / (2 * tile_radius + tile_spacing)))
                        print(marble_index)
                        marble_select = True
                        marble_color = white
                        select_pos = (x_pos, y_pos)
                        print('W')


                    # if the user clicks on a valid marble position and there is a black marble in it
                    elif math.sqrt(mx_sq + my_sq) <= tile_radius and board.get_at((mx, my)) == black:
                        # update the marble index
                        marble_index = (int((y_pos - (tile_radius + tile_spacing)) / (2 * tile_radius + tile_spacing)),
                                        int((x_pos - (tile_radius + tile_spacing)) / (2 * tile_radius + tile_spacing)))
                        print(marble_index)
                        marble_select = True
                        marble_color = black
                        select_pos = (x_pos, y_pos)
                        print('B')

        # did the user hit a key?
        elif event.type == KEYDOWN:
            # if the user presses escape, stop the loop
            if event.key == K_ESCAPE:
                running = False
            # accept keyboard input for marble direction (arrow keys only)
            elif event.key == K_UP:
                direction = 'F'
            elif event.key == K_DOWN:
                direction = 'B'
            elif event.key == K_LEFT:
                direction = 'L'
            elif event.key == K_RIGHT:
                direction = 'R'

            # attempt to make a move
            if game.make_move('PlayerB', marble_index, direction):
                marble_select = False
            if game.make_move('PlayerA', marble_index, direction):
                marble_select = False





        # if an arrow key was pressed after a valid selection was made, make a move

        # reset the make move indicator so that it does not repeat


        elif event.type == pygame.QUIT:
            running = False

        # call to update output board
        pygame.display.flip()
