# Author: Carl Fitzpatrick
# Date: 05/20/21
# Description: This program lets two players participate in a virtual board game
#       called Kuba.

class KubaGame:
    """represents the playing board"""
    def __init__(self, player1, player2):
        """initializes variables for the Board"""
        self._player1 = Player(player1)
        self._player2 = Player(player2)

        # initialize the board to have 7 rows of X's
        self._board = []
        for row in range(7):
            self._board.append(['X', 'X', 'X', 'X', 'X', 'X', 'X'])

    def display_board(self):
        """displays the Board row by row"""
        for row in self._board:
            print(row)

    def make_move(self, player_name, coordinates):
        self._board[coordinates[0]][coordinates[1]] =

class Player:
    """represents a player in the KubaGame"""
    def __init__(self, name, color):
        self._name = name
        self._color = color

    def get_color(self):
        return self._color

    def get_name(self):
        return self._name




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
# game.make_move('PlayerA', (6,5))
# game.display_board()







