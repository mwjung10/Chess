class ChessPiece:
    def __init__(self, player):
        self._player = player

    @property
    def player(self):
        return self._player
    
    @property
    def symbol(self):
        return self._symbol
    
    def __str__(self):
        return self._symbol

class Pawn(ChessPiece):
    def __init__(self, player):
        super().__init__(player)
        self._symbol = 'p' if player == 1 else 'P'
    
    def possible_moves(self, current_row, current_col, board):
        moves = []

        forward_row = current_row + (-1 if self.player == 1 else 1)
        if 0 <= forward_row <= 7 and board.pieces[forward_row][current_col] is None:
            moves.append((forward_row, current_col))
            # If pawn is on the first row it can move 2 swquares forward
            if ((self.player == 1 and current_row == 6) or (self.player == 2 and current_row == 1)) and board.pieces[forward_row - 1* (1 if self.player == 1 else -1)][current_col] is None:
                moves.append((forward_row - 1 * (1 if self.player == 1 else -1), current_col))

        # Checking for diagonal captures
        left_col = current_col - 1
        right_col = current_col + 1

        if 0 <= forward_row < 8:
            if 0 <= left_col < 8 and board._pieces[forward_row][left_col] is not None and board.pieces[forward_row][left_col].player != self.player:
                moves.append((forward_row, left_col))

            if 0 <= right_col < 8 and board._pieces[forward_row][right_col] is not None and board.pieces[forward_row][right_col].player != self.player:
                moves.append((forward_row, right_col))

        return moves

class Rook(ChessPiece):
    def __init__(self, player):
        super().__init__(player)
        self._symbol = 'r' if player == 1 else 'R'

class Knight(ChessPiece):
    def __init__(self, player):
        super().__init__(player)
        self._symbol = 'n' if player == 1 else 'N'

class Bishop(ChessPiece):
    def __init__(self, player):
        super().__init__(player)
        self._symbol = 'b' if player == 1 else 'B'

class Queen(ChessPiece):
    def __init__(self, player):
        super().__init__(player)
        self._symbol = 'q' if player == 1 else 'Q'

class King(ChessPiece):
    def __init__(self, player):
        super().__init__(player)
        self._symbol = 'k' if player == 1 else 'K'

class ChessBoard:
    def __init__(self):
        self._board = [['O' if (i + j) % 2 == 0 else 'X' for j in range(8)] for i in range(8)]
        self._pieces = [[None for j in range(8)] for i in range(8)]
        # Place pieces for Player 1
        self.place_piece(Rook(1), 0, 0)
        self.place_piece(Knight(1), 0, 1)
        self.place_piece(Bishop(1), 0, 2)
        self.place_piece(Queen(1), 0, 3)
        self.place_piece(King(1), 0, 4)
        self.place_piece(Bishop(1), 0, 5)
        self.place_piece(Knight(1), 0, 6)
        self.place_piece(Rook(1), 0, 7)

        for i in range(8):
            self.place_piece(Pawn(1), 1, i)

        # Place pieces for Player 2
        self.place_piece(Rook(2), 7, 0)
        self.place_piece(Knight(2), 7, 1)
        self.place_piece(Bishop(2), 7, 2)
        self.place_piece(Queen(2), 7, 3)
        self.place_piece(King(2), 7, 4)
        self.place_piece(Bishop(2), 7, 5)
        self.place_piece(Knight(2), 7, 6)
        self.place_piece(Rook(2), 7, 7)

        for i in range(8):
            self.place_piece(Pawn(2), 6, i)

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
            print(str(row_number) + ' '+ ' '.join(row))
        
        print('  ', end ='')
        for column_number in range(1, 9):
            print(str(column_number) + ' ', end = '')


board = ChessBoard()
board.display_board()
