from Pieces import ChessPiece, ChessBoard
from Pieces import Pawn, Rook, Bishop, Knight, King, Queen
from Pieces import CoordinatesOutOfRange, InvalidMove
import pytest

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


def test_Pawn_possible_moves_player_1():
    board = ChessBoard()
    assert board.pieces[1][0].possible_moves(1, 0, board) == {(2,0), (3,0)}
    
def test_Pawn_possible_moves_player_2():
    board = ChessBoard()
    assert board.pieces[6][1].possible_moves(6, 1, board) == {(5,1), (4,1)}

def test_Pawn_possible_moves_diagonal_capture():
    board = ChessBoard()
    board.create_empty_board()
    pawn = Pawn(1)
    board.place_piece(pawn, 1, 0)
    board.place_piece(Pawn(2), 2, 1)
    assert board.pieces[1][0].possible_moves(1, 0, board) == {(2,0), (3,0), (2, 1)}


def test_rook_possible_moves_only_rook_on_the_board():
    board = ChessBoard()
    board.create_empty_board()
    rook = Rook(1)
    board.place_piece(rook, 4, 4)
    assert rook.possible_moves(4, 4, board) == {
        (3, 4), (2, 4), (1, 4), (0, 4),  
        (5, 4), (6, 4), (7, 4),       
        (4, 3), (4, 2), (4, 1), (4, 0),  
        (4, 5), (4, 6), (4, 7),       
    }
    
def test_Rock_possible_moves_other_pieces_on_the_board():
    board = ChessBoard()
    board.create_empty_board()
    rook = Rook(1)
    board.place_piece(rook, 4, 4)
    board.place_piece(Pawn(2), 4, 2)
    board.place_piece(Knight(1), 1, 4)
    assert rook.possible_moves(4, 4, board) == {
        (3, 4), (2, 4),  
        (5, 4), (6, 4), (7, 4),       
        (4, 3), (4, 2),
        (4, 5), (4, 6), (4, 7),       
    }


def test_knight_possible_moves_only_knight_on_the_board():
    board = ChessBoard()
    board.create_empty_board()
    knight = Knight(1)
    board.place_piece(knight, 4, 4)
    assert knight.possible_moves(4, 4, board) == {
        (2, 3), (2, 5),
        (3, 2), (3, 6),
        (5, 2), (5, 6),
        (6, 3), (6, 5),
    }

def test_knight_possible_moves_other_pieces_on_the_board():
    board = ChessBoard()
    board.create_empty_board()
    knight = Knight(1)
    board.place_piece(knight, 4, 4)
    board.place_piece(Pawn(2), 2, 3)
    board.place_piece(Knight(1), 3, 2)
    assert knight.possible_moves(4, 4, board) == {
        (2, 3), (2, 5),
        (3, 6),
        (5, 2), (5, 6),
        (6, 3), (6, 5),
    }

def test_bishop_possible_moves_only_bishop_on_the_board():
    board = ChessBoard()
    board.create_empty_board()
    bishop = Bishop(1)
    board.place_piece(bishop, 3, 3)
    assert bishop.possible_moves(3, 3, board) == {
        (2, 2), (1, 1), (0, 0),
        (2, 4), (1, 5), (0, 6),
        (4, 2), (5, 1), (6, 0),
        (4, 4), (5, 5), (6, 6), (7, 7),
    }

def test_bishop_possible_moves_other_pieces_on_the_board():
    board = ChessBoard()
    board.create_empty_board()
    bishop = Bishop(1)
    board.place_piece(bishop, 3, 3)
    board.place_piece(Pawn(2), 2, 2)
    board.place_piece(Knight(1), 1, 1)
    assert bishop.possible_moves(3, 3, board) == {
        (2, 2),
        (2, 4), (1, 5), (0, 6),
        (4, 2), (5, 1), (6, 0),
        (4, 4), (5, 5), (6, 6), (7, 7)
    }

def test_bishop_possible_moves_blocked_by_pieces():
    board = ChessBoard()
    board.create_empty_board()
    bishop = Bishop(1)
    board.place_piece(bishop, 3, 3)
    board.place_piece(Pawn(1), 2, 2)
    board.place_piece(Pawn(2), 2, 4)
    assert bishop.possible_moves(3, 3, board) == {
        (2, 4),
        (4, 2), (5, 1), (6, 0),
        (4, 4), (5, 5), (6, 6), (7, 7)
    }


def test_queen_possible_moves_only_queen_on_the_board():
    board = ChessBoard()
    board.create_empty_board()
    queen = Queen(1)
    board.place_piece(queen, 3, 3)
    assert queen.possible_moves(3, 3, board) == {
        (2, 3), (1, 3), (0, 3), 
        (4, 3), (5, 3), (6, 3), (7, 3),
        (3, 2), (3, 1), (3, 0),  
        (3, 4), (3, 5), (3, 6), (3, 7),
        (2, 2), (1, 1), (0, 0),  
        (2, 4), (1, 5), (0, 6),
        (4, 2), (5, 1), (6, 0),
        (4, 4), (5, 5), (6, 6), (7, 7)
    }

def test_queen_possible_moves_other_pieces_on_the_board():
    board = ChessBoard()
    board.create_empty_board()
    queen = Queen(1)
    board.place_piece(queen, 3, 3)
    board.place_piece(Pawn(2), 2, 3)
    board.place_piece(Knight(1), 1, 3)
    assert queen.possible_moves(3, 3, board) == {
        (2, 3), 
        (4, 3), (5, 3), (6, 3), (7, 3),
        (3, 2), (3, 1), (3, 0),  
        (3, 4), (3, 5), (3, 6), (3, 7),
        (2, 2), (1, 1), (0, 0),  
        (2, 4), (1, 5), (0, 6),
        (4, 2), (5, 1), (6, 0),
        (4, 4), (5, 5), (6, 6), (7, 7)
    }

def test_queen_possible_moves_blocked_by_pieces():
    board = ChessBoard()
    board.create_empty_board()
    queen = Queen(1)
    board.place_piece(queen, 3, 3)
    board.place_piece(Pawn(1), 2, 3)  
    board.place_piece(Pawn(2), 2, 2)  
    assert queen.possible_moves(3, 3, board) == {
        (4, 3), (5, 3), (6, 3), (7, 3),
        (3, 2), (3, 1), (3, 0), 
        (3, 4), (3, 5), (3, 6), (3, 7), 
        (2, 2),
        (2, 4), (1, 5), (0, 6),
        (4, 2), (5, 1), (6, 0),
        (4, 4), (5, 5), (6, 6), (7, 7)
    }

def test_king_possible_moves_only_king_on_the_board():
    board = ChessBoard()
    board.create_empty_board()
    king = King(1)
    board.place_piece(king, 3, 3)
    assert king.possible_moves(3, 3, board) == {
        (2, 3), (2, 2), (2, 4), 
        (3, 2), (3, 4), 
        (4, 3), (4, 2), (4, 4),  
    }

def test_king_possible_moves_other_pieces_on_the_board():
    board = ChessBoard()
    board.create_empty_board()
    king = King(1)
    board.place_piece(king, 3, 3)
    board.place_piece(Pawn(2), 2, 3)
    board.place_piece(Knight(1), 4, 2)
    assert king.possible_moves(3, 3, board) == {
       (2, 3), (2, 2), (2, 4), 
        (3, 2), (3, 4), 
        (4, 3), (4, 4), 
    }


def test_king_possible_moves_blocked_by_pieces():
    board = ChessBoard()
    board.create_empty_board()
    king = King(1)
    board.place_piece(king, 3, 3)
    board.place_piece(Pawn(1), 2, 3)  
    board.place_piece(Pawn(2), 2, 2)  
    assert king.possible_moves(3, 3, board) == {
        (2, 2), (2, 4), 
        (3, 2), (3, 4), 
        (4, 3), (4, 2), (4, 4), 
    }


def test_move_piece_successful():
    board = ChessBoard()
    board.create_empty_board()
    board.place_piece(Rook(1), 1, 1) 

    assert board.pieces[1][1].player == 1  # Check the initial position of the piece
    assert board.pieces[2][1] is None  

    board.move_piece(1, 1, 2, 1, 1)

    assert board.pieces[1][1] is None 
    assert board.pieces[2][1].player == 1  

def test_move_piece_invalid_coordinates():
    board = ChessBoard()
    board.create_empty_board()
    board.place_piece(Rook(1), 1, 1) 

    with pytest.raises(CoordinatesOutOfRange):
        board.move_piece(1, 1, 8, 8, 1)

def test_move_piece_invalid_player():
    board = ChessBoard()
    board.create_empty_board()
    board.place_piece(Rook(1), 1, 1)  

    with pytest.raises(InvalidMove):
        board.move_piece(1, 1, 2, 1, 2)

def test_move_piece_invalid_move():
    board = ChessBoard()
    board.create_empty_board()
    board.place_piece(Rook(1), 1, 1) 

    with pytest.raises(InvalidMove):
        board.move_piece(1, 1, 4, 4, 1)

