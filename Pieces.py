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

    def display_board(self):
        for row_number, row in enumerate(self._board, 1):
            print(str(row_number) + ' '+ ' '.join(row))
        
        print('  ', end ='')
        for column_number in range(1, 9):
            print(str(column_number) + ' ', end = '')

# Example usage:
board = ChessBoard()

# Display the board
board.display_board()
