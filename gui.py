import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon
from Pieces import ChessBoard, Player, InvalidMove, CoordinatesOutOfRange
from Pieces import King, Pawn


class ChessMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("chess.ui", self)

        self.chess_board = ChessBoard()
        self.current_player = Player.WHITE
        self.selected_piece = None
        self.update_board_display()

        # Connect buttons to the move_piece function
        for row in range(8):
            for col in range(8):
                button_name = f"field_{row}_{col}"
                button = getattr(self, button_name, None)
                if button:
                    button.clicked.connect(lambda _, r=row, c=col:
                                           self.move_piece(r, c))

        # Display the current player's turn
        self.update_turn_label()

    def update_board_display(self):
        # GUI update, so it will reflect the current state of the chessboard
        for row in range(8):
            for col in range(8):
                piece = self.chess_board.pieces[row][col]
                button_name = f"field_{row}_{col}"
                button = getattr(self, button_name, None)
                button.setProperty("highlighted", False)

                if button is not None:
                    if piece is not None:
                        if str(piece) == 'p':
                            button.setIcon(QIcon(
                                "images_pieces\\white-pawn.png"))
                        elif str(piece) == 'P':
                            button.setIcon(QIcon(
                                "images_pieces\\black-pawn.png"))
                        elif str(piece) == 'r':
                            button.setIcon(QIcon(
                                "images_pieces\\white-rook.png"))
                        elif str(piece) == 'R':
                            button.setIcon(QIcon(
                                "images_pieces\\black-rook.png"))
                        elif str(piece) == 'n':
                            button.setIcon(QIcon(
                                "images_pieces\\white-knight.png"))
                        elif str(piece) == 'N':
                            button.setIcon(QIcon(
                                "images_pieces\\black-knight.png"))
                        elif str(piece) == 'b':
                            button.setIcon(QIcon(
                                "images_pieces\\white-bishop.png"))
                        elif str(piece) == 'B':
                            button.setIcon(QIcon(
                                "images_pieces\\black-bishop.png"))
                        elif str(piece) == 'q':
                            button.setIcon(QIcon(
                                "images_pieces\\white-queen.png"))
                        elif str(piece) == 'Q':
                            button.setIcon(QIcon(
                                "images_pieces\\black-queen.png"))
                        elif str(piece) == 'k':
                            button.setIcon(QIcon(
                                "images_pieces\\white-king.png"))
                        elif str(piece) == 'K':
                            button.setIcon(QIcon(
                                "images_pieces\\black-king.png"))
                    else:
                        button.setText("")
                        button.setIcon(QIcon())

    def move_piece(self, row, col):
        try:
            if self.selected_piece is None:
                # If no piece is selected, try to select a piece
                piece = self.chess_board.pieces[row][col]
                if piece is not None and piece.player == self.current_player:
                    self.selected_piece = (row, col)
                    self.highlight_possible_moves(row, col)
            else:
                # If a piece is selected, move the piece to the clicked square
                piece = self.chess_board.pieces[row][col]
                if str(piece) in ["k", "K"]:
                    print("GAME OVER")
                self.chess_board.move_piece(self.selected_piece[0],
                                            self.selected_piece[1], row, col,
                                            self.current_player)

                self.update_board_display()
                if self.chess_board.is_checkmate(self.current_player):
                    self.switch_turn()
                    self.show_game_over(f"Checkmate! Player\
                                         {self.current_player.name} wins.")
                self.switch_turn()
                self.selected_piece = None
        except (InvalidMove, CoordinatesOutOfRange) as e:
            print(f"Error: {e}")  # TO BE CHANGED

    def show_game_over(self, message):
        print(message)

    def highlight_possible_moves(self, row, col):
        board = self.chess_board
        selected_piece = self.chess_board.pieces[row][col]
        possible_moves = selected_piece.possible_moves(row, col, board)

        if (isinstance(selected_piece, King)):
            possible_moves.update(selected_piece.castling_moves(row, col,
                                                                board))
        if (isinstance(selected_piece, Pawn)):
            possible_moves.update(
                selected_piece.en_passant_possible_moves(row, col, board))

        for r in range(8):
            for c in range(8):
                button_name = f"field_{r}_{c}"
                button = getattr(self, button_name, None)

                if button is not None:
                    if (r, c) in possible_moves:
                        button.setStyleSheet("background-color: #c5e371;")
                    else:
                        if (r+c) % 2:
                            button.setStyleSheet("background-color: #1eb053;")
                        else:
                            button.setStyleSheet("background-color: #d6d0a9;")
        self.repaint()

    def switch_turn(self):
        self.current_player = (Player.BLACK if
                               self.current_player == Player.WHITE else
                               Player.WHITE)
        self.update_turn_label()
        # If there is a threat of checkamate, the king will highlight red
        king_pos = self.chess_board.king_pos(self.current_player)
        if self.chess_board.is_in_check(king_pos[0], king_pos[1],
                                        self.current_player):
            button_name = f"field_{king_pos[0]}_{king_pos[1]}"
            button = getattr(self, button_name, None)
            button.setStyleSheet("background-color: #F53636;")

    def update_turn_label(self):
        # Update the label to show the current player's turn
        self.PlayerTurn.setText(f"Turn: {self.current_player.name}")


def main():
    app = QApplication(sys.argv)
    window = ChessMainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
