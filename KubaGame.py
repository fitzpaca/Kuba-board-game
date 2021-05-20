# Author: Carl Fitzpatrick
# Date: 05/20/21
# Description: This program lets two players participate in a virtual board game
#       called Kuba.

class KubaGame:
    """represents the Kuba game"""
    def __init__(self, player1, player2):
        """initializes variables for the Board"""
        self._player1 = Player(player1[0], player1[1])
        self._player2 = Player(player2[0], player2[1])
        self._board = GameBoard()

    def display_board(self):
        """displays the """
        print(self._board.get_board())




class GameBoard:
    """represents the playing board"""
    def __init__(self):
        # initialize the board to start positions
        self._game_board = []
        self._game_board.append(['B', 'B', ' ', ' ', ' ', 'W', 'W'])     # initialize row 0...
        self._game_board.append(['B', 'B', ' ', 'R', ' ', 'W', 'W'])
        self._game_board.append([' ', ' ', 'R', 'R', 'R', ' ', ' '])
        self._game_board.append([' ', 'R', 'R', 'R', 'R', 'R', ' '])
        self._game_board.append([' ', ' ', 'R', 'R', 'R', ' ', ' '])
        self._game_board.append(['W', 'W', ' ', 'R', ' ', 'B', 'B'])
        self._game_board.append(['W', 'W', ' ', ' ', ' ', 'B', 'B'])     # ...initialize row 6

    def get_board(self):
        """returns the game board"""
        return self._game_board


class Player:
    """represents a player with a name and marble color"""
    def __init__(self, name, color):
        """initializes members for Player class"""
        self._name = name
        self._color = color


class Marble:
    """represents a marble to play Kuba with"""
    def __init__(self, color):
        """initializes variables for the Marble"""
        self._color = color

    def get_color(self):
        """returns marble color as a string"""
        return self._color


class RedMarble(Marble):
    """represents a red marble with all characteristics of a Marble"""
    def _init__(self):
        """inherits members from Marble and initializes members specific to red marble"""
        super().__init__(color)


game = KubaGame(('PlayerA', 'W'), ('PlayerB', 'B'))
game.display_board()






