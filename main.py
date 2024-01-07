# NOT ALL LOGIC IS IMPLEMENTED HERE.
# This was just used for testing, before implementing gui
from Pieces import ChessBoard


def main_logic(current_player, board):
    while True:
        board.display_board()
        print(f"\nPlayer {current_player}'s turn.")

        move_from = input("Enter the piece you want to move (row, col): ")
        move_from = move_from.split(',')
        move_from = [int(m) for m in move_from]

        piece_row, piece_col = move_from[0] - 1, move_from[1] - 1
        current_piece = board.pieces[piece_row][piece_col]

        possible_moves = current_piece.possible_moves(piece_row, piece_col,
                                                      board)

        print(f'''Possible moves for the selected piece at
               ({move_from[0]}, {move_from[1]}): ''', end="")
        for move in possible_moves:
            print(f"({move[0] + 1}, {move[1] + 1}), ", end="")

        print()
        move_to = input("Enter the destination (row, col): ")
        move_to = move_to.split(',')
        move_to = [int(m) for m in move_to]
        dest_row, dest_col = move_to[0] - 1, move_to[1] - 1

        board.move_piece(piece_row, piece_col, dest_row, dest_col,
                         current_player)

        if board.is_checkmate(current_player):
            board.display_board()
            print(f"\nCheckmate! Player {current_player} wins!")
            break

        current_player = 3 - current_player


def main():
    board = ChessBoard()
    current_player = 1
    main_logic(current_player, board)


if __name__ == '__main__':
    main()
