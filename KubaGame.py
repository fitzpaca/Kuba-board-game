# Author: Carl Fitzpatrick
# Date: 05/20/21
# Description: This program lets two players participate in a virtual board game
#               called Kuba.
import copy

class KubaGame:
    """represents the Kuba board game"""
    def __init__(self, player1, player2):
        """initializes variables for the Board"""
        self._player1 = Player(player1[0], player1[1])
        self._player2 = Player(player2[0], player2[1])
        self._board = GameBoard()
        self._turn = None
        self._winner = None
        self._marble_count = (8, 8, 13)     # (W, B, R)
        self._board_prev = copy.deepcopy(self._board.get_board())

    def display_board(self):
        """displays the game board"""
        # display board by printing each row as a string w tiles separated by spaces
        for row in self._board.get_board():
            print("  ".join(x for x in row))

    def display_prev(self):
        for row in self._board_prev:
            print("  ".join(x for x in row))

    def set_board_prev(self, board):
        """sets the board history to store the previous valid board"""
        self._board_prev = copy.deepcopy(board)

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

    def update_captured(self, name, reds_before):
        """checks if a player captured a red marble on their turn. Calls add_captured if so."""
        reds_after = self.get_marble_count()[2]
        if reds_before == reds_after:
            return
        # otherwise, a red has been captured -- give credit to player
        self.get_player(name).add_captured()

    def get_winner(self):
        """returns the winner of the game. returns None if game is not over."""
        return self._winner

    def check_for_winner(self):
        """checks if the game has been won by a player capturing 7 reds or 7 opposing marbles.
        Returns True if a player has won the game. False otherwise."""
        if self._player1.get_captured() == 7:
            self.set_winner(self._player1.get_name())
            print(self._player1.get_name(), "captured 7 reds and won the game!")

        if self._player2.get_captured() == 7:
            self.set_winner(self._player2.get_name())
            print(self._player2.get_name(), "captured 7 reds and won the game!")

        # if player 1 has no marbles on the board, player 2 wins
        if self.get_marble_count()[0] == 0:
            self.set_winner(self._player2.get_name())
            print(self._player1.get_name(), "has no remaining marbles. Other player wins!")

        # if player 2 has no marbles on the board, player 1 wins
        if self.get_marble_count()[1] == 0:
            self.set_winner(self._player1.get_name())
            print(self._player2.get_name(), "has no remaining marbles. Other player wins!")

    def set_winner(self,  name):
        """sets the winner of the game to a player's name"""
        self._winner = name

    def get_marble(self, board_pos):
        """returns the color of marble at a given position. returns 'X' if tile is empty."""
        return self._board.get_tile(board_pos)

    def make_hyp_move(self, coordinates, direction):
        """makes a hypothetical move and then compares it with the previous board to check for invalid board repeat moves"""
        # make a deep copy of the board object
        board_copy = copy.deepcopy(self._board)

        # make the hypothetical move on the deep copy
        board_copy.push_marble_q(coordinates, direction)

        return board_copy

    def make_move(self, playername, coordinates, direction):
        """makes a move on the game board"""

        # convert input position to actual game board object position
        board_pos = (coordinates[0] + 1, coordinates[1] + 1)

        # if the parameters are validated
        if self.valid_make_move(playername, board_pos, direction):

            # store a deep copy of the previous board and then make the validated move
            self.set_board_prev(self._board.get_board())

            # count the reds before the move is made
            reds_before = self.get_marble_count()[2]

            # make the move for the current player
            self._board.push_marble_q(board_pos, direction)

            # update any reds captured on this turn for the player
            self.update_captured(playername, reds_before)

            # update the current turn to the other player
            other_player = self.get_other_player(playername)
            self.set_current_turn(other_player.get_name())

            # clear the board tray after every valid move
            self._board.clear_tray()

            # check for game winner after every valid turn (** only here to print out win statement can delete bc its called prior to turn)
            self.check_for_winner()     # updates self._winner and prints win announcement
            return True
        return False

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

    # ------ start error handling for make_move --------------------------
    def marble_color_check(self, name, position):
        """data validation for tile color player is attempting to move"""
        marble_on_tile = self.get_marble(position)
        player_attempting = self.get_player(name).get_color()
        if player_attempting == marble_on_tile:
            pass
        else:
            raise InvalidMoveError

    @staticmethod
    def direction_check(direction):
        """data validation for make_move direction input"""
        if direction == 'F' or direction == 'B' or direction == 'L' or direction == 'R':
            pass
        else:
            raise InvalidMoveError

    @staticmethod
    def position_check(board_pos):
        """data validation for make_move position input"""
        if board_pos[0] in range(1, 8) and board_pos[1] in range(1, 8):
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
        self.check_for_winner()
        if self._winner is None:
            pass
        else:
            raise InvalidMoveError

    def push_check(self, position, direction):
        """data validation that the player is legally allowed to push the given marble in the direction given"""
        # if the direction the player wants to push is Left, check one tile to the right for empty or tray
        if direction == "L" \
                and (self._board.get_tile((position[0], position[1] + 1)) == ' '
                     or self._board.get_tile((position[0], position[1] + 1)) == '-'
                     or self._board.get_tile((position[0], position[1] + 1)) == '|'):
            pass
        elif direction == "R" \
                and (self._board.get_tile((position[0], position[1] - 1)) == ' '
                     or self._board.get_tile((position[0], position[1] - 1)) == '-'
                     or self._board.get_tile((position[0], position[1] - 1)) == '|'):
            pass
        elif direction == "B" \
                and (self._board.get_tile((position[0] - 1, position[1])) == ' '
                     or self._board.get_tile((position[0] - 1, position[1])) == '-'
                     or self._board.get_tile((position[0] - 1, position[1])) == '|'):
            pass
        elif direction == "F" \
                and (self._board.get_tile((position[0] + 1, position[1])) == ' '
                     or self._board.get_tile((position[0] + 1, position[1])) == '-'
                     or self._board.get_tile((position[0] + 1, position[1])) == '|'):
            pass
        else:
            raise InvalidMoveError

    def history_check(self, board_pos, direction):
        """check that this move will not result in the identical board setup to the beginning of last turn"""
        hyp_board_object = self.make_hyp_move(board_pos, direction)
        hyp_board = hyp_board_object.get_board()

        # if the hypothetical board matches the prev_board, raise InvalidMoveError
        if hyp_board == self._board_prev:
            raise InvalidMoveError
        pass

    def self_capture_check(self, name, board_pos, direction):
        """check that this move will not result in a player pushing one of his own marbles of the edge"""
        if name == self._player1.get_name():
            # store the number of player1's marbles before the turn
            marbles_before = self._board.get_marble_count()[0]

            # make the hypothetical move (changing only a deep copy)
            hyp_board_obj = self.make_hyp_move(board_pos, direction)
            marbles_after = hyp_board_obj.get_marble_count()[0]

            if marbles_before != marbles_after:
                raise InvalidMoveError

        if name == self._player2.get_name():
            # store the number of player1's marbles before the turn
            marbles_before = self._board.get_marble_count()[1]

            # make the hypothetical move (changing only a deep copy)
            hyp_board_obj = self.make_hyp_move(board_pos, direction)
            marbles_after = hyp_board_obj.get_marble_count()[1]

            if marbles_before != marbles_after:
                raise InvalidMoveError
        pass

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

        # data validation for push validity
        try:
            self.push_check(position, direction)
        except InvalidMoveError:
            print("There must be an adjacent edge or empty tile to push the marble in that direction!")
            return False

        # data validation for a player pushing their own marble off the board
        try:
            self.self_capture_check(name, position, direction)
        except InvalidMoveError:
            print("You cannot make a move that pushes your own marble off the board")
            return False

        # data validation for board history
        try:
            self.history_check(position, direction)
        except InvalidMoveError:
            print("You cannot revert the last player's move to identical board!")
            return False

        # otherwise, input is validated
        return True

    # ------ end error handling for make_move --------------------------


class GameBoard:
    """represents the playing board"""
    def __init__(self):
        """initialize the board to start positions"""
        self._board = []
        self._board.append(['-', '-', '-', '-', '-', '-', '-', '-', '-'])
        self._board.append(['|', 'W', 'W', ' ', ' ', ' ', 'B', 'B', '|'])     # initialize row 0...
        self._board.append(['|', 'W', 'W', ' ', 'R', ' ', 'B', 'B', '|'])
        self._board.append(['|', ' ', ' ', 'R', 'R', 'R', ' ', ' ', '|'])
        self._board.append(['|', ' ', 'R', 'R', 'R', 'R', 'R', ' ', '|'])
        self._board.append(['|', ' ', ' ', 'R', 'R', 'R', ' ', ' ', '|'])
        self._board.append(['|', 'B', 'B', ' ', 'R', ' ', 'W', 'W', '|'])
        self._board.append(['|', 'B', 'B', ' ', ' ', ' ', 'W', 'W', '|'])     # ...initialize row 6
        self._board.append(['-', '-', '-', '-', '-', '-', '-', '-', '-'])
        self._marble_row = Queue()

    def clear_tray(self):
        """clears the game board tray"""
        self._board[0] = ['-', '-', '-', '-', '-', '-', '-', '-', '-']
        self._board[8] = ['-', '-', '-', '-', '-', '-', '-', '-', '-']
        index = 0
        for row in self._board:
            if index != 0 and index != 8:
                row[0] = '|'
                row[8] = '|'
            index += 1

    def get_board(self):
        """returns the game board"""
        return self._board

    def push_marble_q(self, position, direction):
        """pushes a the marble in the given position in the given direction, pushing all marbles in front of it too"""
        # initialize the queue with an empty space and then first tile
        self._marble_row.clear()
        self._marble_row.enqueue(' ')
        self._marble_row.enqueue(self._board[position[0]][position[1]])
        counter = 0         # counter points at the first current tile

        if direction == 'R':
            while self._board[position[0]][position[1] + counter] in ['B', 'W', 'R']:
                self._board[position[0]][position[1] + counter] = self._marble_row.dequeue()       # dequeue the val into current
                self._marble_row.enqueue(self._board[position[0]][position[1] + counter + 1])       # queue the next val
                counter += 1
            self._board[position[0]][position[1] + counter] = self._marble_row.dequeue()

        if direction == 'L':
            while self._board[position[0]][position[1] - counter] in ['B', 'W', 'R']:
                self._board[position[0]][position[1] - counter] = self._marble_row.dequeue()       # dequeue the val into current
                self._marble_row.enqueue(self._board[position[0]][position[1] - (counter + 1)])
                counter += 1
            self._board[position[0]][position[1] - counter] = self._marble_row.dequeue()

        if direction == 'B':
            while self._board[position[0] + counter][position[1]] in ['B', 'W', 'R']:
                self._board[position[0] + counter][position[1]] = self._marble_row.dequeue()       # dequeue the val into current
                self._marble_row.enqueue(self._board[position[0] + counter + 1][position[1]])       # queue the next val
                counter += 1
            self._board[position[0] + counter][position[1]] = self._marble_row.dequeue()

        if direction == 'F':
            while self._board[position[0] - counter][position[1]] in ['B', 'W', 'R']:
                self._board[position[0] - counter][position[1]] = self._marble_row.dequeue()       # dequeue the val into current
                self._marble_row.enqueue(self._board[position[0] - (counter + 1)][position[1]])
                counter += 1
            self._board[position[0] - counter][position[1]] = self._marble_row.dequeue()

        return

    def get_tile(self, position):
        """returns the status of a tile"""
        return self._board[position[0]][position[1]]

    def get_marble_count(self):
        """tallies the count of marbles on the board by color"""
        red_count = 0
        black_count = 0
        white_count = 0
        for row in self._board[1:8]:                    # only count marbles on the playing board
            for tile in row[1:8]:
                if tile == 'R':
                    red_count += 1
                elif tile == 'B':
                    black_count += 1
                elif tile == 'W':
                    white_count += 1
        return white_count, black_count, red_count      # returns a tuple of these values


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


class Queue:
    """
    An implementation of the Queue ADT that uses Python's built-in lists
        ** referenced from Module 7 **
    """
    def __init__(self):
        self.list = []

    def enqueue(self, data):
        self.list.append(data)

    def dequeue(self):
        val = self.list[0]
        del self.list[0]
        return val

    def clear(self):
        self.list = []







game = KubaGame(('PlayerA', 'W'), ('PlayerB', 'B'))
game.display_board()
print("1", game.make_move('PlayerB', (0, 5), 'B'))
game.display_board()
print("2", game.make_move('PlayerA', (6, 5), 'F'))
game.display_board()
print("3", game.make_move('PlayerB', (1, 5), 'B'))
game.display_board()
print("4", game.make_move('PlayerA', (6, 5), 'F'))
game.display_board()
print(game.get_current_turn())
print("4", game.make_move('PlayerA', (6, 5), 'R'))
game.display_board()
print(game.get_current_turn())








# print("2", game.make_move('PlayerA', (2, 6), 'x'))
# print("3", game.make_move('PlayerA', (0, 6), 'F'))
# print("4", game.make_move('PlayerB', (0, 6), 'B'))
# print("5", game.make_move('PlayerB', (2, 6), 'L'))
# print("6", game.make_move('PlayerA', (0, 5), 'L'))
#
# game.display_board()
# print(game.get_marble_count())
# print("7", game.make_move('PlayerA', (6, 0), 'L'))
# print("8", game.make_move('PlayerB', (6, 6), 'R'))
# print("9", game.make_move('PlayerA', (6, 1), 'B'))
#
# game.display_board()
# print(game.get_marble_count())














