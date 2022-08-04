from tkinter import *
from model import *
from view import *
#----------------------------------------------------------------------
# Controller
#----------------------------------------------------------------------
class Controller:
    model = None
    curPlayer = 1

    def __init__(self):
        self.model = None

    def set_model(self, model):
        self.model = model

    def playRound(self, player, col, row):
        return self.model.setPeice(col, row, player)

    def checkWin(self, player):
        return self.model.checkWin(player)

    def checkTie(self):
        return self.model.checkTie()
