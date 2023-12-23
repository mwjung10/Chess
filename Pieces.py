from enum import Enum

class Player(Enum):
    WHITE = 1
    BLACK = 2


class ChessPiece:
    def __init__(self, player):
        self._player = Player(player)

    @property
    def player(self):
        return self._player

    @property
    def symbol(self):
        return self._symbol

    def __str__(self):
        return self._symbol


class CoordinatesOutOfRange(Exception):
    def __init__(self):
        super().__init__("Coordinates out of range. Board has 8x8 squares")


class InvalidMove(Exception):
    def __init__(self):
        super().__init__("Invalid move. Select different move")


class Pawn(ChessPiece):
    def __init__(self, player):
        super().__init__(player)
        self._symbol = 'p' if player == Player.WHITE.value else 'P'

    def possible_moves(self, current_row, current_col, board):
        moves = []

        forward_row = current_row + (-1 if self.player == Player.BLACK else 1)
        if (0 <= forward_row <= 7 and
                board.pieces[forward_row][current_col] is None):
            moves.append((forward_row, current_col))
            # If pawn is on the first row it can move 2 swquares forward
            if (((self.player == Player.BLACK and current_row == 6) or
                    (self.player == Player.WHITE and current_row == 1)) and
                    board.pieces[forward_row - 1 * (1 if self.player == Player.BLACK else - 1)][current_col] is None):
                moves.append((forward_row - 1 * (1 if self.player == Player.BLACK else -1), current_col))

        # Checking for diagonal captures
        left_col = current_col - 1
        right_col = current_col + 1

        if 0 <= forward_row < 8:
            if 0 <= left_col < 8 and board.pieces[forward_row][left_col] is not None and board.pieces[forward_row][left_col].player != self.player:
                moves.append((forward_row, left_col))

            if 0 <= right_col < 8 and board.pieces[forward_row][right_col] is not None and board.pieces[forward_row][right_col].player != self.player:
                moves.append((forward_row, right_col))

        return set(moves)


class Rook(ChessPiece):
    def __init__(self, player):
        super().__init__(player)
        self._symbol = 'r' if player == Player.WHITE.value else 'R'

    def possible_moves(self, current_row, current_col, board):
        moves = []

        # Checking upward moves
        for row in range(current_row - 1, -1, -1):
            if board.pieces[row][current_col] is None:
                moves.append((row, current_col))
            else:
                if board.pieces[row][current_col].player != self.player:
                    moves.append((row, current_col))
                break

        # Checking downward moves
        for row in range(current_row + 1, 8):
            if board.pieces[row][current_col] is None:
                moves.append((row, current_col))
            else:
                if board.pieces[row][current_col].player != self.player:
                    moves.append((row, current_col))
                break

        # Checking leftward moves
        for col in range(current_col - 1, -1, -1):
            if board.pieces[current_row][col] is None:
                moves.append((current_row, col))
            else:
                if board.pieces[current_row][col].player != self.player:
                    moves.append((current_row, col))
                break

        # Checking rightward moves
        for col in range(current_col + 1, 8):
            if board.pieces[current_row][col] is None:
                moves.append((current_row, col))
            else:
                if board.pieces[current_row][col].player != self.player:
                    moves.append((current_row, col))
                break

        return set(moves)


class Knight(ChessPiece):
    def __init__(self, player):
        super().__init__(player)
        self._symbol = 'n' if player == Player.WHITE.value else 'N'

    def possible_moves(self, current_row, current_col, board):
        moves = []
        possible_directions = [(-2, -1), (-2, 1),
                               (-1, -2), (-1, 2),
                               (1, -2), (1, 2),
                               (2, -1), (2, 1)]

        for direction in possible_directions:
            new_row = current_row + direction[0]
            new_col = current_col + direction[1]
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                destination = board.pieces[new_row][new_col]
                if destination is None or destination.player != self.player:
                    moves.append((new_row, new_col))

        return set(moves)


class Bishop(ChessPiece):
    def __init__(self, player):
        super().__init__(player)
        self._symbol = 'b' if player == Player.WHITE.value else 'B'

    def possible_moves(self, current_row, current_col, board):
        moves = []
        possible_directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        for direction in possible_directions:
            new_row = current_row + direction[0]
            new_col = current_col + direction[1]
            while 0 <= new_row < 8 and 0 <= new_col < 8:
                destination_piece = board.pieces[new_row][new_col]

                if destination_piece is None:
                    moves.append((new_row, new_col))
                elif destination_piece.player != self.player:
                    moves.append((new_row, new_col))
                    break
                else:
                    break

                new_row += direction[0]
                new_col += direction[1]

        return set(moves)


class Queen(ChessPiece):
    def __init__(self, player):
        super().__init__(player)
        self._symbol = 'q' if player == Player.WHITE.value else 'Q'

    def possible_moves(self, current_row, current_col, board):
        moves = []
        possible_directions = [
            (-1, 0), (1, 0), (0, -1), (0, 1),  # upward, downward, left, right
            (-1, -1), (-1, 1), (1, -1), (1, 1)  # diagonal
        ]

        for direction in possible_directions:
            new_row, new_col = current_row + direction[0], current_col + direction[1]

            while 0 <= new_row < 8 and 0 <= new_col < 8:
                destination_piece = board.pieces[new_row][new_col]

                if destination_piece is None:
                    moves.append((new_row, new_col))
                elif destination_piece.player != self.player:
                    moves.append((new_row, new_col))
                    break
                else:
                    break

                new_row += direction[0]
                new_col += direction[1]

        return set(moves)


class King(ChessPiece):
    def __init__(self, player):
        super().__init__(player)
        self._symbol = 'k' if player == Player.WHITE.value else 'K'

    def possible_moves(self, current_row, current_col, board):
        moves = []
        directions = [
            (-1, 0), (1, 0), (0, -1), (0, 1),
            (-1, -1), (-1, 1), (1, -1), (1, 1)
        ]

        for direction in directions:
            new_row, new_col = current_row + direction[0], current_col + direction[1]

            if 0 <= new_row < 8 and 0 <= new_col < 8:
                destination_piece = board.pieces[new_row][new_col]
                if destination_piece is None or destination_piece.player != self.player:
                    moves.append((new_row, new_col))

        return set(moves)


def create_empty_board():
    return ChessBoard(False)


class ChessBoard:
    def __init__(self, empty=True):
        self._board = [['O' if (i + j) % 2 == 0 else 'X' for j in range(8)] for i in range(8)]
        self._pieces = [[None for j in range(8)] for i in range(8)]
        # Place pieces for Player 1
        if empty:
            self.place_piece(Rook(Player.WHITE.value), 0, 0)
            self.place_piece(Knight(Player.WHITE.value), 0, 1)
            self.place_piece(Bishop(Player.WHITE.value), 0, 2)
            self.place_piece(Queen(Player.WHITE.value), 0, 3)
            self.place_piece(King(Player.WHITE.value), 0, 4)
            self.place_piece(Bishop(Player.WHITE.value), 0, 5)
            self.place_piece(Knight(Player.WHITE.value), 0, 6)
            self.place_piece(Rook(Player.WHITE.value), 0, 7)

            for i in range(8):
                self.place_piece(Pawn(Player.WHITE.value), 1, i)

            # Place pieces for Player 2
            self.place_piece(Rook(Player.BLACK.value), 7, 0)
            self.place_piece(Knight(Player.BLACK.value), 7, 1)
            self.place_piece(Bishop(Player.BLACK.value), 7, 2)
            self.place_piece(Queen(Player.BLACK.value), 7, 3)
            self.place_piece(King(Player.BLACK.value), 7, 4)
            self.place_piece(Bishop(Player.BLACK.value), 7, 5)
            self.place_piece(Knight(Player.BLACK.value), 7, 6)
            self.place_piece(Rook(Player.BLACK.value), 7, 7)

            for i in range(8):
                self.place_piece(Pawn(Player.BLACK.value), 6, i)

    def place_piece(self, piece, row, col):
        self._board[row][col] = str(piece)
        self._pieces[row][col] = piece

    @property
    def board(self):
        return self._board

    @property
    def pieces(self):
        return self._pieces

    def display_board(self):
        for row_number, row in enumerate(self._board, 1):
            print(str(row_number) + ' ' + ' '.join(row))

        print('  ', end='')
        for column_number in range(1, 9):
            print(str(column_number) + ' ', end='')

    def move_piece(self, piece_row, piece_column, row_to_move, column_to_move, player):
        # Function has to get already corrected coordinates. Coordinates have to be corrected (row -1, column - 1) outside the function.
        if not (0 <= piece_row < 8 and 0 <= piece_column < 8 and 0 <= row_to_move < 8 and 0 <= column_to_move < 8):
            raise CoordinatesOutOfRange()

        current_piece = self._pieces[piece_row][piece_column]

        if current_piece is None or current_piece.player != player:
            raise InvalidMove()

        if (row_to_move, column_to_move) not in current_piece.possible_moves(piece_row, piece_column, self):
            raise InvalidMove()

        self._pieces[piece_row][piece_column] = None
        self._pieces[row_to_move][column_to_move] = current_piece

        self.update_board_display()

    def remove_piece(self, piece_row, piece_column):
        if not (0 <= piece_row < 8 and 0 <= piece_column < 8):
            raise CoordinatesOutOfRange()

        current_piece = self._pieces[piece_row][piece_column]

        if current_piece is None:
            raise InvalidMove()

        self._pieces[piece_row][piece_column] = None

    def update_board_display(self):
        self._board = [['O' if (i + j) % 2 == 0 else 'X' for j in range(8)]
                       for i in range(8)]

        for row in range(8):
            for col in range(8):
                piece = self._pieces[row][col]
                if piece is not None:
                    self._board[row][col] = str(piece)


    def is_in_check(self, row, col, player):
        # Check if the piece is under threat
        for i in range(8):
            for j in range(8):
                piece = self._pieces[i][j]
                if piece is not None and piece.player != player:
                    moves = piece.possible_moves(i, j, self)
                    if (row, col) in moves:
                        return True
        return False

    def is_checkmate(self, player):
        # True if in checkmate, Flase if not
        # Find the king's position for the player
        king_position = None
        for row in range(8):
            for col in range(8):
                piece = self._pieces[row][col]
                if piece and piece.symbol.upper() == 'K' and piece.player == player:
                    king_position = (row, col)
                    break
            if king_position:
                break

        # Check if the king is in check
        if self.is_in_check(king_position[0], king_position[1], player):
            # Check if there are any legal moves to escape the check
            for row in range(8):
                for col in range(8):
                    piece = self._pieces[row][col]
                    if piece is not None and piece.player == player:
                        moves = piece.possible_moves(row, col, self)
                        for move in moves:
                            temp_board = self.copy_board()
                            temp_board.move_piece(row, col, move[0], move[1], player)
                            if not temp_board.is_in_check(king_position[0], king_position[1], player):
                                return False

            return True

        return False

    def copy_board(self):
        # Create a copy of the current board and pieces
        copy_board = ChessBoard()
        copy_board._board = [row.copy() for row in self._board]
        copy_board._pieces = [row.copy() for row in self._pieces]
        return copy_board


