import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QSizePolicy
from PyQt5.uic import loadUi
from Pieces import ChessBoard, Player, InvalidMove, CoordinatesOutOfRange


class ChessMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("chess.ui", self)

        self.chess_board = ChessBoard()
        self.current_player = Player.WHITE
        self.update_board_display()

        # Connect buttons to the move_piece function
        for row in range(8):
            for col in range(8):
                button_name = f"field_{row}_{col}"
                button = getattr(self, button_name, None)
                if button:
                    button.clicked.connect(lambda _, r=row, c=col: self.move_piece(r, c))

        # Display the current player's turn
        self.update_turn_label()


    def update_board_display(self):
        # GUI update, so it will reflect the current state of the chessboard
        for row in range(8):
            for col in range(8):
                piece = self.chess_board.pieces[row][col]
                button_name = f"field_{row}_{col}"
                button = getattr(self, button_name, None)

                if button is not None:
                    if piece is not None:
                        button.setText(str(piece))
                    else:
                        button.setText("")

    def move_piece(self, row, col):
        try:
            self.chess_board.move_piece(0, 0, row, col, self.current_player)
            self.update_board_display()
            self.switch_turn()
        except (InvalidMove, CoordinatesOutOfRange) as e:
            print(f"Error: {e}")  #WILL BE CHANGED - PRINT IS ONLY TEMPORARY (to show problems in my code)

    def switch_turn(self):
        self.current_player = Player.BLACK if self.current_player == Player.WHITE else Player.WHITE
        self.update_turn_label()

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
