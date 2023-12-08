from Pieces import ChessPiece, ChessBoard
from Pieces import Pawn, Rook, Bishop, Knight, King, Queen

def test_piece_creation():
    pawn = Pawn(1)
    assert pawn.player == 1
    assert str(pawn) == 'p'

    rook = Rook(2)
    assert rook.player == 2
    assert str(rook) == 'R'


def test_CheessPiece_creation():
    piece = ChessPiece(2)
    assert piece.player == 2


def test_board_creation():
    board = ChessBoard()
    assert str(board.pieces[0][0]) == 'r'
    assert str(board.pieces[1][1]) == 'p'
    assert str(board.pieces[7][1]) == 'N'
    assert str(board.pieces[6][5]) == 'P'

def test_place_piece():
    board = ChessBoard()
    piece = Rook(1)
    board.place_piece(piece, 2, 3)
    assert str(board.pieces[2][3]) == 'r'
    assert board.board[2][3] == 'r'


