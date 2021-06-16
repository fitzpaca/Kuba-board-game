# pygame code for Kuba

import pygame

import KubaGame
from KubaGame import KubaGame, GameBoard, Player, InvalidMoveError, Queue

# initialize all the modules required for PyGame
pygame.init()

done = False
screen = pygame.display.set_mode((500, 500))
x = 60
y = 60

while not done:
    # since the game will be a series of events, this syntax will help empty the events'
    #  queue before adding a new one
    for event in pygame.event.get():
        # this syntax is used to exit the program altogether
        if event.type == pygame.QUIT:
            done = True

        # start editing the output window
        pygame.display.set_caption("Kuba Board Game")       # set window title
        # icon = pygame.image.load('game.jpg')              # set title icon
        # pygame.display.set_icon(icon)


        pygame.draw.rect(screen, (0, 128, 255), pygame.Rect(x, y, 90, 90))

        # PyGame is double-buffered so this swaps the buffers.
        #  this call is required for any updates that you make
        #  to the game screen to become visible.
        pygame.display.flip()

