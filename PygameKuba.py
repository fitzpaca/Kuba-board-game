# pygame code for Kuba

import pygame

import KubaGame
from KubaGame import KubaGame, GameBoard, Player, InvalidMoveError, Queue

# initialize all the modules required for PyGame
pygame.init()

# define constants for the screen width and height
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

# create the screen object
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# set tile information (coordinates, color)
tile_x = 0
tile_y = 0
tile_color = (255, 255, 255)    # white

# create object for background image
image = pygame.image.load(r'C:\Users\Carl\Desktop\Grease.jpg')

# add this before loop to throttle the frame rate
clock = pygame.time.Clock()

running = True
while running:
    # since the game will be a series of events, this syntax will help empty the events'
    #  queue before adding a new one
    for event in pygame.event.get():
        # did the user click the window close button?
        if event.type == pygame.QUIT:
            running = False

        # set the background to loaded image
        screen.blit(image, (0, 0))

        # change the color of the square by pressing space bar
        is_red = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            is_red = not is_red
            if is_red:
                tile_color = (255, 0, 0)
            else:
                tile_color = (102, 0, 0)

        # start editing the output window
        pygame.display.set_caption("Kuba Board Game")       # set window title
        # icon = pygame.image.load('game.jpg')              # set title icon
        # pygame.display.set_icon(icon)

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]: tile_y -= 100
        if pressed[pygame.K_DOWN]: tile_y += 100
        if pressed[pygame.K_LEFT]: tile_x -= 100
        if pressed[pygame.K_RIGHT]: tile_x += 100

        # add this in loop
        clock.tick(60)

        pygame.draw.rect(screen, tile_color, pygame.Rect(tile_x, tile_y, 100, 100))

        # reset screen before drawing next rectangle
        # screen.blit(image, (0, 0))

        # PyGame is double-buffered so this swaps the buffers.
        #  this call is required for any updates that you make
        #  to the game screen to become visible.
        pygame.display.flip()

