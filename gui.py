import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon
from Pieces import ChessBoard, Player, InvalidMove, CoordinatesOutOfRange


class ChessMainWindow(QMainWindow):
    """
    The main window for the Chess game application.

    This class represents the graphical user interface (GUI) for a Chess game,
    allowing players to make moves on the chessboard.

    Attributes:
        chess_board (ChessBoard): An instance of the ChessBoard class
        representing the current state of the chessboard.
        current_player (Player): An instance of the Player enum representing
            the current player's turn.
        selected_piece (tuple): A tuple representing the row and column indices
            of the currently selected chess piece.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
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
        """
        Updates the graphical representation of the chessboard in the GUI.
        Iterates over each button on the chessboard and sets the
        appropriate icon.
        """
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
                                "images_pieces/white-pawn.png"))
                        elif str(piece) == 'P':
                            button.setIcon(QIcon(
                                "images_pieces/black-pawn.png"))
                        elif str(piece) == 'r':
                            button.setIcon(QIcon(
                                "images_pieces/white-rook.png"))
                        elif str(piece) == 'R':
                            button.setIcon(QIcon(
                                "images_pieces/black-rook.png"))
                        elif str(piece) == 'n':
                            button.setIcon(QIcon(
                                "images_pieces/white-knight.png"))
                        elif str(piece) == 'N':
                            button.setIcon(QIcon(
                                "images_pieces/black-knight.png"))
                        elif str(piece) == 'b':
                            button.setIcon(QIcon(
                                "images_pieces/white-bishop.png"))
                        elif str(piece) == 'B':
                            button.setIcon(QIcon(
                                "images_pieces/black-bishop.png"))
                        elif str(piece) == 'q':
                            button.setIcon(QIcon(
                                "images_pieces/white-queen.png"))
                        elif str(piece) == 'Q':
                            button.setIcon(QIcon(
                                "images_pieces/black-queen.png"))
                        elif str(piece) == 'k':
                            button.setIcon(QIcon(
                                "images_pieces/white-king.png"))
                        elif str(piece) == 'K':
                            button.setIcon(QIcon(
                                "images_pieces/black-king.png"))
                    else:
                        button.setText("")
                        button.setIcon(QIcon())

    def move_piece(self, row, col):
        """
        Handles the logic for moving a chess piece on the chessboard.

        Args:
            row (int): The row of the target square.
            col (int): The column of the target square.
        """
        try:
            piece = self.chess_board.pieces[row][col]
            if self.selected_piece is None:
                # If no piece is selected, try to select a piece
                if piece is not None and piece.player == self.current_player:
                    self.selected_piece = (row, col)
                    self.highlight_possible_moves(row, col)
            # If player changes a piece to move and piece is not king
            elif (self.selected_piece is not None and piece is not None and
                  self.chess_board.pieces[self.selected_piece[0]][
                    self.selected_piece[1]].player == piece.player and
                    str(self.chess_board.pieces[self.selected_piece[0]][
                    self.selected_piece[1]]) not in ['k', 'K']):
                if piece is not None and piece.player == self.current_player:
                    self.selected_piece = (row, col)
                    self.highlight_possible_moves(row, col)
            # If player changes a piece to move and piece is king and player
            # wants to move it on rook
            elif (self.selected_piece is not None and piece is not None and
                  self.chess_board.pieces[self.selected_piece[0]][
                    self.selected_piece[1]].player == piece.player and
                    str(self.chess_board.pieces[self.selected_piece[0]][
                    self.selected_piece[1]]) in ['k', 'K'] and
                    str(piece) in ['R', 'r']):
                self.chess_board.move_piece(self.selected_piece[0],
                                            self.selected_piece[1], row, col,
                                            self.current_player)
                self.update_board_display()
                self.switch_turn()
                self.selected_piece = None
            # If player changes a piece to move and piece is king
            elif (self.selected_piece is not None and piece is not None and
                  self.chess_board.pieces[self.selected_piece[0]][
                    self.selected_piece[1]].player == piece.player and
                    str(self.chess_board.pieces[self.selected_piece[0]][
                    self.selected_piece[1]]) in ['k', 'K'] and
                    str(piece) not in ['R', 'r']):
                if piece is not None and piece.player == self.current_player:
                    self.selected_piece = (row, col)
                    self.highlight_possible_moves(row, col)
            else:
                # If a piece is selected, move the piece to the clicked square
                if str(piece) in ["k", "K"]:
                    self.show_game_over(
                        f"Checkmate! Player {self.current_player.name} wins.")
                    return
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
        except (InvalidMove, CoordinatesOutOfRange):
            pass

    def show_game_over(self, message):
        """
        Displays the game-over label and disables all buttons when the
        game is over.
        """
        self.game_over_label.setText(message)
        self.PlayerTurn.clear()
        self.PlayerTurn.setStyleSheet("")
        self.game_over_label.show()
        for row in range(8):
            for col in range(8):
                button_name = f"field_{row}_{col}"
                button = getattr(self, button_name, None)
                if button:
                    button.setEnabled(False)

    def highlight_possible_moves(self, row, col):
        """
        Highlights the possible moves for a selected chess piece on
            the chessboard.

        Args:
            row (int): The row of the selected piece.
            col (int): The column of the selected piece.
        """
        board = self.chess_board
        selected_piece = self.chess_board.pieces[row][col]
        possible_moves = selected_piece.possible_moves(row, col, board)

        if (str(selected_piece) in ["k", "K"]):
            possible_moves.update(selected_piece.castling_moves(row, col,
                                                                board))
        if (str(selected_piece) in ["p", "P"]):
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
        """
        Switches the turn to the next player and updates the turn label.
        This method also checks for checkmate and highlights the king if
            in check.
        """
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
        """
        Updates the label to display the current player's turn.
        """
        self.PlayerTurn.setText(f"Turn: {self.current_player.name}")


def main():
    app = QApplication(sys.argv)
    window = ChessMainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
