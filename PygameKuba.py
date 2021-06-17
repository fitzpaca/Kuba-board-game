# pygame code for Kuba

import pygame

from pygame.locals import(
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT
)

import KubaGame
from KubaGame import KubaGame, GameBoard, Player, InvalidMoveError, Queue

# initialize the board to starting position
game = KubaGame(('PlayerA', 'W'), ('PlayerB', 'B'))
print("Board start (below)")
game.display_board()


# initialize all the modules required for PyGame
pygame.init()

# define constants for the screen width and height
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700

# create the screen object
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# tile color RGB combos
white = (255, 255, 255)
red = (255, 0, 0)

# set tile information (coordinates, color)
tile_x = 0
tile_y = 0
tile_color = white
tile_width = 100
tile_height = 100



# create object for background image
image = pygame.image.load(r'C:\Users\Carl\Desktop\Grease.jpg')

# add this before loop to throttle the frame rate
clock = pygame.time.Clock()



running = True

# Main loop
while running:
    # since the game will be a series of events, this syntax will help empty the events'
    #  queue before adding a new one

    # add this in loop
    clock.tick(600)

    for event in pygame.event.get():
        # did the user hit a key?
        if event.type == KEYDOWN:
            # if the user presses escape, stop the loop
            if event.key == K_ESCAPE:
                running = False

        elif event.type == pygame.QUIT:
            running = False

        # setup the board initially by iterating through rows and columns calling get_marble
        x_counter = 0
        y_counter = 0
        for row in game.get_board()[1:8]:
            for tile in row[1:8]:
                pygame.time.wait(10)
                if x_counter > 600:
                    x_counter = 0

                if tile == 'W':
                    # print("white tile here", x_counter, ', ', y_counter)
                    pygame.draw.rect(screen, white, pygame.Rect(x_counter, y_counter, tile_width, tile_height))

                # move across the board to the right for every tile
                #  until it reaches 600, then reset to 0
                x_counter += 100

            # move down the board row by row until y_counter reaches 600 then stop
            y_counter += 100






        # set the background to loaded image
        # screen.blit(image, (0, 0))

        # change the color of the square by pressing space bar
        # is_red = True
        # if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        #     is_red = not is_red
        #     if is_red:
        #         tile_color = (255, 0, 0)
        #     else:
        #         tile_color = (102, 0, 0)

        # start editing the output window
        pygame.display.set_caption("Kuba Board Game")       # set window title
        # icon = pygame.image.load('game.jpg')              # set title icon
        # pygame.display.set_icon(icon)

        # pressed = pygame.key.get_pressed()
        # if pressed[pygame.K_UP]: tile_y -= 100
        # if pressed[pygame.K_DOWN]: tile_y += 100
        # if pressed[pygame.K_LEFT]: tile_x -= 100
        # if pressed[pygame.K_RIGHT]: tile_x += 100

        pygame.draw.rect(screen, tile_color, pygame.Rect(tile_x, tile_y, tile_width, tile_height))

        # reset screen before drawing next rectangle
        # screen.blit(image, (0, 0))

        # PyGame is double-buffered so this swaps the buffers.
        #  this call is required for any updates that you make
        #  to the game screen to become visible.
        pygame.display.flip()

