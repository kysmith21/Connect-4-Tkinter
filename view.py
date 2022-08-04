from tkinter import *
from model import *
from controller import *
import time
# ----------------------------------------------------------------------
# View - a frame in the root window and the GUI widgets
# ----------------------------------------------------------------------
class View(Frame):
    p1Color = "#EB523E"
    p2Color = "#E6DD3B"
    container = None
    boardGrid = None
    winnerName = None
    tempPiece = None
    curColor = p1Color

    def __init__(self, container):
        super().__init__(container)
        self.topCanvas = None
        self.container = container
        self.controller = None
        self.model = None
        self.unbind = 0

        # Main Menu / Start Menu
        # Title
        self.title = Label(container, text="Connect 4", bg="#FFEEDB", fg="#ED9B40", font="Cooper 60 bold underline")
        self.title.config(highlightbackground = "#000000", highlightthickness=2)
        self.title.place(relx=.5, rely=.28, anchor=CENTER)


        # Start Game button
        self.startGame = Button(container, text ="Start Game", height = 3,
          width = 20, font="Cooper 16 ", command =self.startGame)
        self.startGame.place(relx=.5, rely=.4, anchor=CENTER)

        # Scoreboard button
        self.scoreboard = Button(container, height = 3,
          width = 20, text="Scoreboard", font="Cooper 16", command= self.viewScoreBoard)
        self.scoreboard.place(relx=.5, rely=.5, anchor=CENTER)


    # Function to start our first inital game
    def startGame(self):
        # Clear old screen items
        self.clearScreen()

        # Add Menu bar
        menuBar = Menu(self.container)
        self.container.config(menu=menuBar)
        gameMenu = Menu(menuBar)

        gameMenu.add_command(
            label='Main Menu',
            command=self.mainMenu
        )

        gameMenu.add_command(
            label='Exit',
            command=self.container.destroy
        )

        menuBar.add_cascade(
            label="File",
            menu=gameMenu
        )

        # Round labels to show who's turn it is
        self.roundLabel1 = Label(self.container, text="Player 1", bg="#FFEEDB", fg="#BA3B46", font="Cooper 32 bold" )
        self.roundLabel2 = Label(self.container, text="Player 2", bg="#FFEEDB", fg="#BA3B46", font="Cooper 24" )
        self.roundLabel1.place(relx=0.85, rely=0.4)
        self.roundLabel2.place(relx=0.85, rely=0.5)

        self.timer = Label(self.container, text="", font=('Cooper', 40))
        self.timer.place(relx=0.1, rely=0.5)


        # Canvas for C4 grid
        self.canvas = Canvas(self.container, height=700, width=860, bg='#7FCBB3')
        self.canvas.place(relx=0.5, rely=0.5, anchor=CENTER)
        cPos = 55
        rPos = 50


        # Make c4 grid w piece objects
        for r in range(6):
            for c in range(7):
                piece = self.canvas.create_oval(cPos, rPos, cPos+90, rPos+90, fill="#FFEEDB")
                self.canvas.tag_bind(piece, '<Button-1>', self.pieceClickEvent)
                cPos += 110
            rPos += 100
            cPos = 55

        self.topCanvas = Canvas(self.container, height=100, width=860, bg='#FFEEDB', highlightbackground = '#FFEEDB')
        self.topCanvas.place(relx=0.5, rely=0.14, anchor=CENTER)
        self.canvas.bind('<Motion>', self.pieceTemp)

    # Function for hover piece
    def pieceTemp(self, event):
        x, y = event.x, event.y
        print("X: "+ str(x) + " Y: " + str(y))
        item = self.canvas.find_closest(event.x, event.y)
        if self.tempPiece != None:
            self.topCanvas.delete(self.tempPiece)

        boardCol = int((x- 155) / 110)
        if x < 156:
            self.tempPiece = self.topCanvas.create_oval( + 55, 10, (90) + 55, 100,
                                                      fill=self.curColor)
        elif x > 805:
            self.tempPiece = self.topCanvas.create_oval(715, 10, 805, 100,
                                                        fill=self.curColor)
        else:
            self.tempPiece = self.topCanvas.create_oval((boardCol * 110) + 165, 10, ((boardCol) * 110)+255, 100, fill=self.curColor)

    # Function to start a new game after our first inital game, new things need to be set for tkinter to be happy
    def restartGame(self):
        self.unbind = 0
        # reset model
        self.model.newGame()

        # Clear old screen items
        self.clearScreen()

        # Add Menu bar
        menuBar = Menu(self.container)
        self.container.config(menu=menuBar)
        gameMenu = Menu(menuBar)

        gameMenu.add_command(
            label='Main Menu',
            command=self.mainMenu
        )

        gameMenu.add_command(
            label='Exit',
            command=self.container.destroy
        )

        menuBar.add_cascade(
            label="File",
            menu=gameMenu
        )

        # Round labels to show who's turn it is
        self.roundLabel1 = Label(self.container, text="Player 1", bg="#FFEEDB", fg="#BA3B46", font="Cooper 32 bold")
        self.roundLabel2 = Label(self.container, text="Player 2", bg="#FFEEDB", fg="#BA3B46", font="Cooper 24")
        self.roundLabel1.place(relx=0.85, rely=0.4)
        self.roundLabel2.place(relx=0.85, rely=0.5)

        self.timer = Label(self.container, text="", font=('Cooper', 40))
        self.timer.place(relx=0.1, rely=0.5)

        # Canvas for C4 grid
        self.canvas = Canvas(self.container, height=700, width=860, bg='#7FCBB3')
        self.canvas.place(relx=0.5, rely=0.5, anchor=CENTER)
        cPos = 55
        rPos = 50

        # Make c4 grid w piece objects
        for r in range(6):
            for c in range(7):
                piece = self.canvas.create_oval(cPos, rPos, cPos + 90, rPos + 90, fill="#FFEEDB")
                self.canvas.tag_bind(piece, '<Button-1>', self.pieceClickEvent)
                cPos += 110
            rPos += 100
            cPos = 55

        self.topCanvas = Canvas(self.container, height=100, width=860, bg='#FFEEDB', highlightbackground='#FFEEDB')
        self.topCanvas.place(relx=0.5, rely=0.12, anchor=CENTER)
        self.canvas.bind('<Motion>', self.pieceTemp)

    # Function to allow us to move to next turn and change board
    def pieceClickEvent(self, event):
        if self.unbind == 1:
            return
        item = self.canvas.find_closest(event.x, event.y)
        # Calculate where in terms of the model board layout
        (x1, y1, x2, y2) = self.canvas.coords(item)
        boardCol = int((x1-55)/95)
        boardRow = int((y1-50)/84)


        if self.controller.curPlayer == 1:
            if self.controller.playRound(1, boardCol, boardRow):

                #self.updateTimer()
                # Check win or Tie for player
                if self.controller.checkWin(1):
                    self.unbind = 1
                    print("Player 1 Wins!")
                    top = Toplevel(self.container)
                    top.geometry("500x250")
                    top.title("Winner!")
                    Label(top, text="Player 1 Won! Insert Name: ", font=('Cooper 12 bold')).place(x=150, y=80)
                    self.name = Entry(top)
                    self.name.place(x=190, y=120)
                    Button(top, text="Add To Scoreboard", command=self.endGame).place(x=195, y=150)
                    #self.canvas.unbind('<Button-1>', self.pieceClickEvent)
                    self.canvas.itemconfigure(item, fill=self.p1Color)
                    unbind = 1

                if self.controller.checkTie():
                    print("A Tie")
                    top.geometry("500x250")
                    top.title("Tie")
                    Label(top, text="The game ended in a Tie", font=('Cooper 12 bold')).place(x=150, y=80)
                    Button(top, text="Back to Main Menu", command=self.mainMenu).place(x=195, y=150)
                    self.unbind = 1

                # Valid info sent to controller, update other parts of view
                self.canvas.itemconfigure(item, fill=self.p1Color)
                self.controller.curPlayer = 2
                self.curColor = self.p2Color
                self.topCanvas.itemconfig(self.tempPiece, fill=self.curColor)
                self.roundLabel2.config(font="Cooper 32 bold")
                self.roundLabel1.config(font="Cooper 24")

        else:
            if self.controller.playRound(2, boardCol, boardRow):

                #self.updateTimer()
                # Check win or Tie for player
                if self.controller.checkWin(2):

                    print("Player 2 Wins!")
                    top = Toplevel(self.container)
                    top.geometry("500x250")
                    top.title("Winner!")
                    Label(top, text="Player 2 Won! Insert Name: ", font=('Cooper 12 bold')).place(x=150, y=80)
                    self.name = Entry(top)
                    self.name.place(x=190, y=120)
                    Button(top, text="Add To Scoreboard", command=self.endGame).place(x=195, y=150)
                    self.canvas.itemconfigure(item, fill=self.p2Color)
                    #self.canvas.unbind('<Button-1>', self.pieceClickEvent)
                    self.unbind = 1

                if self.controller.checkTie():
                    print("A Tie")
                    top = Toplevel(self.container)
                    top.geometry("500x250")
                    top.title("Tie")
                    Label(top, text="The game ended in a Tie", font=('Cooper 12 bold')).place(x=150, y=80)
                    Button(top, text="Back to Main Menu", command=self.mainMenu).place(x=195, y=150)
                    self.unbind = 1

                # Valid info sent to controller, update other parts of view
                self.canvas.itemconfigure(item, fill=self.p2Color)
                self.controller.curPlayer = 1
                self.curColor = self.p1Color
                self.topCanvas.itemconfig(self.tempPiece, fill=self.curColor)
                self.roundLabel1.config(font="Cooper 32 bold")
                self.roundLabel2.config(font="Cooper 24")

        print('Clicked object at: ', boardRow, boardCol)

    # Function to take us to our scorboard module
    def viewScoreBoard(self):
        self.clearScreen()
        print(self.model.winners)
        x = 0.5
        y = 0.37
        self.labFrame = LabelFrame(self.container, bg='#FDE8CD', fg='#FFCC92', width=500,height=500).place(relx=0.50, rely=0.45, anchor=CENTER)
        Label(self.labFrame, text="Scoreboard", bg="#FDE8CD", fg="#ED9B40", font="Cooper 60 bold underline").place(relx=0.50, rely=0.28, anchor=CENTER)
        if len(self.model.winners) == 0:
            Label(self.labFrame, text="No Winners", bg="#FDE8CD", fg="#BA3B46", font="Cooper 32 bold").place(relx=x, rely=y,
                                                                                   anchor=CENTER)
            y += .1
        else:
            for name in self.model.winners:
                if self.model.winners[name] == 1:
                    line = name + " : " + str(self.model.winners[name]) + " win "
                else:
                    line = name + " : " + str(self.model.winners[name]) + " wins "
                Label(self.labFrame, text=line, bg="#FDE8CD", fg="#BA3B46", font="Cooper 32 bold").place(relx=x, rely=y, anchor=CENTER)
                y += .05

        Button(self.labFrame, text="Return",font="Cooper 14 ", command=self.mainMenu).place(relx=x-.003, rely=0.65, anchor=CENTER)



    # Function to take us back to Main menu
    def mainMenu(self):
        self.clearScreen()

        # Main Menu / Start Menu
        # Title
        self.title = Label(self.container, text="Connect 4", bg="#FFEEDB", fg="#ED9B40", font="Cooper 60 bold underline")
        self.title.config(highlightbackground="#000000", highlightthickness=2)
        self.title.place(relx=.5, rely=.28, anchor=CENTER)
        # self.title.place(x=500, y=500)

        # Start Game button
        self.startGame = Button(self.container, text="Start Game", height=3,
                                width=20, font="Cooper 16",command=self.restartGame)
        self.startGame.place(relx=.5, rely=.4, anchor=CENTER)

        # Scoreboard button
        self.scoreboard = Button(self.container, height=3,
                                 width=20, font="Cooper 16", text="Scoreboard", command=self.viewScoreBoard)
        self.scoreboard.place(relx=.5, rely=.5, anchor=CENTER)

    # Function to end current game and move back to main menu
    def endGame(self):
        self.winnerName = self.name.get()
        print(self.winnerName)

        self.model.addtoscoreBoard(self.winnerName)

        self.mainMenu()


    def set_controller(self, controller):
        self.controller = controller

    def set_model(self, model):
        self.model = model

    def clearScreen(self):
        for item in self.container.winfo_children():
                item.destroy()