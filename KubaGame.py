# Author: Carl Fitzpatrick
# Date: 05/20/21
# Description: This program lets two players participate in a virtual board game
#       called Kuba.

class KubaGame:
    """represents the Kuba board game"""
    def __init__(self, player1, player2):
        """initializes variables for the Board"""
        self._player1 = Player(player1[0], player1[1])
        self._player2 = Player(player2[0], player2[1])
        self._board = GameBoard()
        self._turn = None
        self._winner = None
        self._marble_count = ()     # (W, B, R)

    def display_board(self):
        """displays the game board"""

        # display board by printing each row as a string w tiles separated by spaces
        for row in self._board.get_board():
            print("  ".join(x for x in row))

        # display board by printing each row as a list
        # for row in self._board.get_board():
        #     print(row)

    def get_current_turn(self):
        """Returns the players name whose turn it is.
         Returns none if nobody has played yet."""
        return self._turn

    def set_current_turn(self, name):
        """updates current turn"""
        self._turn = name

    def get_marble_count(self):
        """returns the marble count as a tuple (White, Black, Red)"""
        return self._board.get_marble_count()

    def get_captured(self, name):
        """returns the number of captured red marbles by the given player name"""
        return self.get_player(name).get_captured()

    def get_winner(self):
        """returns the winner of the game. returns None if game is not over."""
        return self._winner

    def set_winner(self, name):
        """sets the winner of the game to a player's name"""
        self._winner = name

    def get_marble(self, position):
        """returns the color of marble at a given position. returns 'X' if tile is empty."""
        return self._board.get_tile(position)

    def make_move(self, name, position, direction):
        """makes a move on the game board"""
        # if the parameters are validated
        if self.valid_make_move(name, position, direction):
            # make the move for the current player
            current_player = self.get_player(name)
            self._board.push_marble(position, current_player.get_color(), direction)
            # self._board.set_marble(position[0], position[1], current_player.get_color())

            # update the current turn to the other player
            other_player = self.get_other_player(name)
            self.set_current_turn(other_player.get_name())

        # check for game winner after every valid turn


    def get_player(self, name):
        """returns a Player from a given name"""
        if name == self._player1.get_name():
            return self._player1
        if name == self._player2.get_name():
            return self._player2

    def get_other_player(self, name):
        """returns the opposing Player from a given name"""
        if name == self._player1.get_name():
            return self._player2
        if name == self._player2.get_name():
            return self._player1

    # ------ start error handling for KubaGame --------------------------
    def marble_color_check(self, name, position):
        """data validation for tile color player is attempting to move"""
        marble_on_tile = self.get_marble(position)
        player_attempting = self.get_player(name).get_color()
        if player_attempting == marble_on_tile:
            pass
        else:
            raise InvalidMoveError

    def direction_check(self, direction):
        """data validation for make_move direction input"""
        if direction == 'F' or direction == 'B' or direction == 'L' or direction == 'R':
            pass
        else:
            raise InvalidMoveError

    def position_check(self, position):
        """data validation for make_move position input"""
        if position[0] in range(7) and position[1] in range(7):
            pass
        else:
            raise InvalidMoveError

    def turn_check(self, name):
        """data validation to make sure that it is the player's turn who is attempting the move"""
        if name == self.get_current_turn() or self.get_current_turn() is None:
            pass
        else:
            raise InvalidMoveError

    def winner_check(self):
        """data validation that the game has not been won already"""
        if self._winner is None:
            pass
        else:
            raise InvalidMoveError

    def valid_make_move(self, name, position, direction):
        """handles data validation for make_move function"""
        # data validation for game already won
        try:
            self.winner_check()
        except InvalidMoveError:
            print("The game has already been won!")
            return False

        # data validation for position
        try:
            self.position_check(position)
        except InvalidMoveError:
            print("Invalid position input!")
            return False

        # data validation for direction
        try:
            self.direction_check(direction)
        except InvalidMoveError:
            print("Invalid direction! Must be 'F', 'B', 'L', or 'R'")
            return False

        # data validation for current turn
        try:
            self.turn_check(name)
        except InvalidMoveError:
            print("It is not your turn!")
            return False

        # data validation for marble color
        try:
            self.marble_color_check(name, position)
        except InvalidMoveError:
            print("You can only push your own marbles!")
            return False





        # otherwise, input is validated
        return True

    # ------ end error handling for KubaGame --------------------------


class GameBoard:
    """represents the playing board"""
    def __init__(self):
        # initialize the board to start positions
        self._board = []
        self._board.append(['B', 'B', ' ', ' ', ' ', 'W', 'W', '|'])     # initialize row 0...
        self._board.append(['B', 'B', ' ', 'R', ' ', 'W', 'W', '|'])
        self._board.append([' ', ' ', 'R', 'R', 'R', ' ', ' ', '|'])
        self._board.append([' ', 'R', 'R', 'R', 'R', 'R', ' ', '|'])
        self._board.append([' ', ' ', 'R', 'R', 'R', ' ', ' ', '|'])
        self._board.append(['W', 'W', ' ', 'R', ' ', 'B', 'B', '|'])
        self._board.append(['W', 'W', ' ', ' ', ' ', 'B', 'B', '|'])     # ...initialize row 6
        self._board.append(['-', '-', '-', '-', '-', '-', '-', '-'])

    def get_board(self):
        """returns the game board"""
        return self._board

    def set_marble(self, row, col, color):
        """places a marble on a tile and updates game board"""
        self._board[row][col] = color

    def push_marble(self, position, color, direction):
        # push the marble in the given direction
        # (if we want to push a marble left, then the tile to the right must be empty (empty or right edge)
        if direction == 'L':
            self._board[position[0]][position[1] - 1] = color

        # make the given tile empty
        self._board[position[0]][position[1]] = ' '



    def get_tile(self, position):
        """returns the status of a tile"""
        return self._board[position[0]][position[1]]

    def get_marble_count(self):
        """tallies the count of marbles on the board by color"""
        red_count = 0
        black_count = 0
        white_count = 0
        for row in self._board:
            for tile in row:
                if tile == 'R':
                    red_count += 1
                elif tile == 'B':
                    black_count += 1
                elif tile == 'W':
                    white_count += 1
        return (white_count, black_count, red_count)



class Player:
    """represents a player with a name and marble color"""
    def __init__(self, name, color):
        """initializes members for Player class"""
        self._name = name
        self._color = color
        self._captured = 0      # initialize a player's captured count to 0

    def get_name(self):
        """returns player's name"""
        return self._name

    def get_color(self):
        """returns a player's marble color"""
        return self._color

    def get_captured(self):
        """returns a player's number of captured red marbles"""
        return self._captured

    def add_captured(self):
        """adds a captured red marble to the player's count of captures"""
        self._captured += 1


class InvalidMoveError(Exception):
    """exception for invalid direction input"""
    pass




game = KubaGame(('PlayerA', 'W'), ('PlayerB', 'B'))
# game.make_move('PlayerB', (0,0), 'B')
# game.make_move('PlayerA', (2,6), 'x')
# game.make_move('PlayerA', (0,6), 'F')
# game.make_move('PlayerB', (0,6), 'B')
# game.make_move('PlayerB', (2,6), 'L')
game.set_winner("Carl")
game.make_move('PlayerA', (0, 5), 'L')
game.make_move('PlayerB', (6, 5), 'L')
game.display_board()








