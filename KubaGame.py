# Author: Carl Fitzpatrick
# Date: 05/20/21
# Description: This program lets two players participate in a virtual board game
#               called Kuba.
import copy


class KubaGame:
    """
    This class represents the Kuba board game and playing functionalities.
    This class communicates with the following classes:
     - GameBoard: KubaGame uses GameBoard to initialize and change the physical
            board with marbles on it. It also returns important information
            about the status of the board to KubaGame.
     - Player: KubaGame uses Player object to initialize and return information about
            players 1 and 2.
     - InvalidMoveError: KubaGame uses InvalidMoveError to pass an error when a player
            inputs an invalid move.
     """
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
        """
        Purpose: initializes variables for the game
        Parameters: Player object (player1), Player object (player2)
        Returns: N/A
        """
        # display board by printing each row as a string w tiles separated by spaces
        for row in self._board.get_board():
            print("  ".join(x for x in row))

    def display_prev(self):
        """ *********  delete before turning in  ********* """
        for row in self._board_prev:
            print("  ".join(x for x in row))

    def set_board_prev(self, board):
        """
        Purpose: stores a deep copy of the previous valid playing board
            object for use in previous board position checks
        Parameters: GameBoard object
        Returns: N/A
        """
        self._board_prev = copy.deepcopy(board)

    def get_player(self, name):
        """
        Purpose: returns the player object for a given player name
        Parameters: name (string)
        Returns: Player object
        """
        if name == self._player1.get_name():
            return self._player1
        if name == self._player2.get_name():
            return self._player2

    def get_other_player(self, name):
        """
        Purpose: returns the opposing player object for a given player name
        Parameters: name (string)
        Returns: Player object
        """
        if name == self._player1.get_name():
            return self._player2
        if name == self._player2.get_name():
            return self._player1

    def get_current_turn(self):
        """
        Purpose: Returns the current Player whose turn it is.
            Returns None if the game has not been started.
        Parameters: N/A
        Returns: a Player or None
        """
        return self._turn

    def set_current_turn(self, name):
        """
        Purpose: Updates the current turn
        Parameters: player name (string)
        Returns: N/A
        """
        self._turn = name

    def get_marble_count(self):
        """
        Purpose: Returns the marble count on the board as a tuple (# white marbles, # black, # red)
        Parameters: N/A
        Returns: marble count as a tuple
        """
        return self._board.get_marble_count()

    def get_captured(self, name):
        """
        Purpose: returns the number of captured red marbles by the given player
        Parameters: player name (string)
        Returns: a Player's number of captured red marbles
        """
        return self.get_player(name).get_captured()

    def update_captured(self, name, reds_before):
        """
        Purpose: checks if a player captured a red marble on their turn.
            If so, adds the red to the Player's capture tally
        Parameters: player name (string), red marbles captured before this turn (number)
        Returns: None if there were no reds captured.
        """
        reds_after = self.get_marble_count()[2]
        if reds_before == reds_after:
            return
        # otherwise, a red has been captured -- give credit to player
        self.get_player(name).add_captured()

    def get_winner(self):
        """
        Purpose: returns the winner of the game. returns None if game is not over
        Parameters: N/A
        Returns: winning Player or None
        """
        return self._winner

    def check_for_winner(self):
        """
        Purpose: checks if the game has been won by a player capturing 7 reds or 7 opposing marbles.
            Returns True if a player has won the game. False otherwise.
        Parameters: N/A
        Returns: True or False
        """
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
        """
        Purpose: sets the winner of the game to a player's name
        Parameters: Player name (string)
        Returns: N/A
        """
        self._winner = name

    def get_marble(self, board_pos):
        """
        Purpose: returns the color of marble at a given position. returns 'X' if tile is empty.
        Parameters: board tile coordinates as a tuple
        Returns: tile status as a string ('X', 'W', 'B', 'R')
        """
        return self._board.get_tile(board_pos)

    def make_hyp_move(self, coordinates, direction):
        """
        Purpose: makes a hypothetical move and then compares it with the previous board
            to check for invalid board repeat moves
        Parameters: position (tuple) and direction ('F', 'B', 'L', or 'R') of hypothetical marble push
        Returns: GameBoard object with hyp. move completed
        """
        # make a deep copy of the board object
        board_copy = copy.deepcopy(self._board)

        # make the hypothetical move on the deep copy
        board_copy.push_marble_q(coordinates, direction)

        return board_copy

    def make_move(self, player_name, coordinates, direction):
        """
        Purpose: handles a player attempting to make a move on the game board with data validation.
            Data validation handled and described in valid_make_move() method.
        Parameters: the Player's name attempting the move (string), position (tuple) of marble to push,
            and the direction of the push ('F', 'B', 'L', or 'R')
        Returns: True if the move was validated and successful. False otherwise.
        """
        # convert input position to actual game board object position
        board_pos = (coordinates[0] + 1, coordinates[1] + 1)

        # if the parameters are validated
        if self.valid_make_move(player_name, board_pos, direction):

            # store a deep copy of the previous board and then make the validated move
            self.set_board_prev(self._board.get_board())

            # count the reds before the move is made
            reds_before = self.get_marble_count()[2]

            # make the move for the current player
            self._board.push_marble_q(board_pos, direction)

            # update any reds captured on this turn for the player
            self.update_captured(player_name, reds_before)

            # update the current turn to the other player
            other_player = self.get_other_player(player_name)
            self.set_current_turn(other_player.get_name())

            # clear the board tray after every valid move
            self._board.clear_tray()

            # check for game winner after every valid turn
            # (** only here to print out win statement can delete bc its called prior to turn)
            self.check_for_winner()     # updates self._winner and prints win announcement
            return True
        return False

    # ------ start error handling for make_move --------------------------
    def marble_color_check(self, name, position):
        """
        Purpose: data validation for tile color player is attempting to move.
            Raises InvalidMoveError if data is not valid.
        Parameters: Player name (string) and tile position (tuple)
        Returns: N/A
        """
        marble_on_tile = self.get_marble(position)
        player_attempting = self.get_player(name).get_color()
        if player_attempting == marble_on_tile:
            pass
        else:
            raise InvalidMoveError

    @staticmethod
    def direction_check(direction):
        """
        Purpose: data validation for the direction string the player inputs
            Raises InvalidMoveError if data is not valid.
        Parameters: Direction (string)
        Returns: N/A
        """
        if direction == 'F' or direction == 'B' or direction == 'L' or direction == 'R':
            pass
        else:
            raise InvalidMoveError

    @staticmethod
    def position_check(board_pos):
        """
        Purpose: data validation for the position tuple the player inputs
            Raises InvalidMoveError if data is not valid.
        Parameters: tile position (tuple)
        Returns: N/A
        """
        if board_pos[0] in range(1, 8) and board_pos[1] in range(1, 8):
            pass
        else:
            raise InvalidMoveError

    def turn_check(self, name):
        """
        Purpose: data validation to make sure that it is the player's turn to make the move
            Raises InvalidMoveError if data is not valid.
        Parameters: Player's name (string)
        Returns: N/A
        """
        if name == self.get_current_turn() or self.get_current_turn() is None:
            pass
        else:
            raise InvalidMoveError

    def winner_check(self):
        """
        Purpose: data validation to make sure the game has not already been won
            Raises InvalidMoveError if data is not valid.
        Parameters: N/A
        Returns: N/A
        """
        self.check_for_winner()
        if self._winner is None:
            pass
        else:
            raise InvalidMoveError

    def push_check(self, position, direction):
        """
        Purpose: handles data validation that the player is legally allowed
                  to push the given marble in the direction given.
            Raises InvalidMoveError if data is not valid.
        Parameters: tile position (tuple) and direction (string)
        Returns: N/A
        """
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
        """
        Purpose: handles data validation that this move will not result in an identical board setup to
                  the board setup at the beginning of last turn.
            Raises InvalidMoveError if data is not valid.
        Parameters: tile position (tuple) and direction (string)
        Returns: N/A
        """
        hyp_board_object = self.make_hyp_move(board_pos, direction)
        hyp_board = hyp_board_object.get_board()

        # if the hypothetical board matches the prev_board, raise InvalidMoveError
        if hyp_board == self._board_prev:
            raise InvalidMoveError
        pass

    def self_capture_check(self, name, board_pos, direction):
        """
        Purpose: handles data validation that this move will not result in a player
                  pushing one of his own marbles off the edge.
            Raises InvalidMoveError if data is not valid.
        Parameters: Player name (string), tile position (tuple), direction (string)
        Returns: N/A
        """
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
        """
        Purpose: handles all data validation for the make_move method.
            Returns False if the move is not allowed according to the game rules
             if or any parameter for make_move is invalid.
            Returns True if valid move.
            Practically, this function calls each specific data validation method and if
             any of them raise the InvalidMoveError, it returns False. Otherwise, if the data
             passes all data validation, it returns True.
        Parameters: Player name (string), tile position (tuple), direction (string)
        Returns: True or False
        """
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
    """
    This class represents the physical playing board and handles the processing
        and passing of information relevant to the board positions and marbles.
    This class communicates with the following classes:
     - Queue: GameBoard uses the Queue class to enqueue and dequeue values in the
            push_marble_q method
    """
    def __init__(self):
        """
        Purpose: initialize the board to starting marble positions
                  with a perimeter tray.
            Initialize the row checker as a Queue.
        Parameters: N/A
        Returns: N/A
        """
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
        """
        Purpose: clears the game board tray
        Parameters: N/A
        Returns: N/A
        """
        self._board[0] = ['-', '-', '-', '-', '-', '-', '-', '-', '-']
        self._board[8] = ['-', '-', '-', '-', '-', '-', '-', '-', '-']
        index = 0
        for row in self._board:
            if index != 0 and index != 8:
                row[0] = '|'
                row[8] = '|'
            index += 1

    def get_board(self):
        """
        Purpose: getter method for the game board data member
        Parameters: N/A
        Returns: game board (list)
        """
        return self._board

    def push_marble_q(self, position, direction):
        """
        Purpose: pushes a the marble in the given position in the given direction,
                  pushing all marbles in front of it too
            Practically, this method uses the marble_row Queue to "push" each marble forward by
             storing the next marble then replacing it with the previous marble using the Queue.
        Parameters: tile position (tuple) and direction (string)
        Returns: None
        """
        # initialize the queue with an empty space and then first tile
        self._marble_row.clear()
        self._marble_row.enqueue(' ')
        self._marble_row.enqueue(self._board[position[0]][position[1]])
        counter = 0         # counter points at the first current tile

        if direction == 'R':
            while self._board[position[0]][position[1] + counter] in ['B', 'W', 'R']:
                # dequeue the val into current
                self._board[position[0]][position[1] + counter] = self._marble_row.dequeue()
                # enqueue the next val
                self._marble_row.enqueue(self._board[position[0]][position[1] + counter + 1])
                counter += 1
            self._board[position[0]][position[1] + counter] = self._marble_row.dequeue()

        if direction == 'L':
            while self._board[position[0]][position[1] - counter] in ['B', 'W', 'R']:
                self._board[position[0]][position[1] - counter] = self._marble_row.dequeue()
                self._marble_row.enqueue(self._board[position[0]][position[1] - (counter + 1)])
                counter += 1
            self._board[position[0]][position[1] - counter] = self._marble_row.dequeue()

        if direction == 'B':
            while self._board[position[0] + counter][position[1]] in ['B', 'W', 'R']:
                self._board[position[0] + counter][position[1]] = self._marble_row.dequeue()
                self._marble_row.enqueue(self._board[position[0] + counter + 1][position[1]])
                counter += 1
            self._board[position[0] + counter][position[1]] = self._marble_row.dequeue()

        if direction == 'F':
            while self._board[position[0] - counter][position[1]] in ['B', 'W', 'R']:
                self._board[position[0] - counter][position[1]] = self._marble_row.dequeue()
                self._marble_row.enqueue(self._board[position[0] - (counter + 1)][position[1]])
                counter += 1
            self._board[position[0] - counter][position[1]] = self._marble_row.dequeue()

        return

    def get_tile(self, position):
        """
        Purpose: getter method for a given tile's status
        Parameters: tile position (tuple)
        Returns: status of given tile (string)
        """
        return self._board[position[0]][position[1]]

    def get_marble_count(self):
        """
        Purpose: getter method for the number of each marble on the board
        Parameters: N/A
        Returns: count of each marble on the board (tuple) (# white marbles, # black, # red)
        """
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
    """
    This class represents a Player in the KubaGame with a name, color, and # of reds captured.
        It also handles returning and updating this information when necessary.
    This class does not communicate with other classes. It produces a sovereign player
        object. It is used by the KubaGame class though.
    """
    def __init__(self, name, color):
        """
        Purpose: init method for Player class data members
        Parameters: Player name (string) and Player's marble color (string)
        Returns: N/A
        """
        self._name = name
        self._color = color
        self._captured = 0      # initialize a player's captured count to 0

    def get_name(self):
        """
        Purpose: getter method for Player's name
        Parameters: N/A
        Returns: Player's name (string)
        """
        return self._name

    def get_color(self):
        """
        Purpose: getter method for Player's marble color
        Parameters: N/A
        Returns: Player's marble color (string)
        """
        return self._color

    def get_captured(self):
        """
        Purpose: getter method for Player's number of captured red marbles
        Parameters: N/A
        Returns: Player's number of captured red marbles
        """
        return self._captured

    def add_captured(self):
        """
        Purpose: adds a captured red marble to the player's count of captured reds
        Parameters: N/A
        Returns: N/A
        """
        self._captured += 1


class InvalidMoveError(Exception):
    """
    This class is an exception error for invalid player inputs.
    This class is used by the KubaGame class, but it does not communicate with
        any other classes itself.
    """
    pass


class Queue:
    """
    This class is used to pass methods for data structure (list) manipulations.
    It does not communicate with other classes, but it is used by the GameBoard class.
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
print("Board start (below)")
game.display_board()
print("1 (below)", game.make_move('PlayerB', (0, 5), 'B'))
game.display_board()
print("2 (below)", game.make_move('PlayerA', (0, 1), 'B'))
game.display_board()
print("3 (below)", game.make_move('PlayerB', (1, 5), 'B'))
game.display_board()
print("4 (below)", game.make_move('PlayerA', (2, 1), 'R'))
game.display_board()
# print(game.get_current_turn())
print("5 (below)", game.make_move('PlayerB', (3, 5), 'L'))
game.display_board()
print(game.get_marble_count())
print(game.get_current_turn())
print("6 (below)", game.make_move('PlayerA', (2, 2), 'R'))
game.display_board()
print("7 (below)", game.make_move('PlayerB', (3, 4), 'L'))
game.display_board()
print("9 (below)", game.make_move('PlayerA', (2, 3), 'R'))
game.display_board()
print("10 (below)", game.make_move('PlayerB', (3, 3), 'L'))
game.display_board()
print("11 (below)", game.make_move('PlayerA', (2, 4), 'R'))
game.display_board()
print("12 (below)", game.make_move('PlayerB', (3, 2), 'L'))
game.display_board()
print("13 (below)", game.make_move('PlayerA', (2, 5), 'R'))
game.display_board()
print("14 (below)", game.make_move('PlayerB', (3, 1), 'L'))
game.display_board()
print("15 (below)", game.make_move('PlayerA', (2, 6), 'F'))
game.display_board()
print("16 (below)", game.make_move('PlayerB', (6, 1), 'F'))
game.display_board()
print("17 (below)", game.make_move('PlayerA', (1, 6), 'F'))
game.display_board()
print("18 (below)", game.make_move('PlayerB', (4, 1), 'R'))
game.display_board()
print("19 (below)", game.make_move('PlayerA', (0, 6), 'B'))
game.display_board()
print("20 (below)", game.make_move('PlayerB', (4, 2), 'R'))
game.display_board()
print("21 (below)", game.make_move('PlayerA', (1, 0), 'R'))
game.display_board()
print("22 (below)", game.make_move('PlayerB', (4, 3), 'R'))
game.display_board()
print("23 (below)", game.make_move('PlayerA', (5, 6), 'L'))
game.display_board()
print("24 (below)", game.make_move('PlayerB', (4, 4), 'R'))
game.display_board()
print("23 (below)", game.make_move('PlayerA', (5, 6), 'L'))
game.display_board()

# Display status of game:
print('Current turn: ', game.get_current_turn())
print('Marble count (W, B, R):', game.get_marble_count())
print('PlayerA captured reds:', game.get_player('PlayerA').get_captured())
print('PlayerB captured reds:', game.get_player('PlayerB').get_captured())
print('Winner: ', game.get_winner())


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
