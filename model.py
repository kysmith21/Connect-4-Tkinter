from tkinter import *
from view import *
from controller import *
import numpy as np


# ----------------------------------------------------------------------
# Model - the data we want to view and control
# ----------------------------------------------------------------------
class Model:
    pieceCounter = 0
    ROWS = 6
    COLS = 7
    winners = {
               }

    def __init__(self):
        self.view = None
        self.board = None
        self.View = None
        self.newGame()

    def getBoard(self):
        return self.board

    def setBoard(self, board):
        self.board = board

    def getPeice(self, col, row):
        return self.board[col][row]

    def setPeice(self, col, row, player):
        # Check if coordinates are valid for placement
        if self.board[row][col] == 0:
            if self.board[row][col] or (row + 1) > 5 or self.board[row+1][col] != 0:
                # If valid, change the board
                self.board[row][col] = player
                self.view.update()
                self.pieceCounter += 1
                return True
        return False

    # After piece has been placed, we must check to see if the user had a winning move
    def checkWin(self, player):
        if (self.horizontalC4(player) or self.verticalC4(player)
                or self.diagonalLowerRightC4(player) or self.diagonalLowerLeftC4(player)):
            return True
        return False

    # Check and announce Tie
    def checkTie(self):
        if self.pieceCounter >= 42:
            # Notify there has been a tie
            return True
        return False

    def horizontalC4(self, player):
        for col in range(self.COLS - 3):
            for row in range(self.ROWS):
                if (self.board[row][col] == player and
                        self.board[row][col + 1] == player and
                        self.board[row][col + 2] == player and
                        self.board[row][col + 3] == player):
                    return True
        return False

    def verticalC4(self, player):
        for col in range(self.COLS):
            for row in range(self.ROWS - 3):
                if (self.board[row][col] == player and
                        self.board[row + 1][col] == player and
                        self.board[row + 2][col] == player and
                        self.board[row + 3][col] == player):
                    return True

        return False

    def diagonalLowerRightC4(self, player):
        for col in range(self.COLS - 3):
            for row in range(self.ROWS - 3):
                if (self.board[row][col] == player and
                        self.board[row + 1][col + 1] == player and
                        self.board[row + 2][col + 2] == player and
                        self.board[row + 3][col + 3] == player):
                    return True
        return False

    def diagonalLowerLeftC4(self, player):
        for col in range(self.COLS - 3):
            for row in range(3, self.ROWS):
                if (self.board[row][col] == player and
                        self.board[row - 1][col + 1] == player and
                        self.board[row - 2][col + 2] == player and
                        self.board[row - 3][col + 3] == player):
                    return True
        return False

    # Reset Board for new game
    def newGame(self):
        self.pieceCounter = 0
        self.board = [[0 for x in range(self.COLS)] for y in range(self.ROWS)]

    def set_view(self, view):
        self.view = view

    def addtoscoreBoard(self, name):
        if name in self.winners:
            count = self.winners[name]
            count += count
            self.winners[name] = count
        else:
            self.winners[name] = 1

    def printArray(self):
        print(np.matrix(self.board))