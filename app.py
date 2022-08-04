from tkinter import *
from model import *
from view import *
from controller import *
# ----------------------------------------------------------------------
# App - the root window and the MVC objects
# ----------------------------------------------------------------------
class App(Tk):
    def __init__(self):
        super().__init__()
        self.title('Connect 4 ')
        self.geometry('1920x1080')
        self.config(bg='#FFEEDB')

        # ---- create a model
        model = Model()

        # ---- create a view (tkinter frame) and place it in the root window
        view = View(self)
        view.grid(row=0, column=0, padx=10, pady=10)
        # set the view for the model
        model.set_view(view)
        # set the model for the view
        view.set_model(model)

        # ---- create a controller
        controller = Controller()
        # set the model for the controller
        controller.set_model(model)
        # set the controller for the view
        view.set_controller(controller)

    # =========================================================================


app = App()
app.mainloop()