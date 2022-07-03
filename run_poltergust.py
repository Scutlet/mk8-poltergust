from tkinter import *

from poltergust import PoltergustUI
from controller import PoltergustController


if __name__ == '__main__':
    # Create and display the UI
    root = Tk()
    view = PoltergustUI(root)
    controller = PoltergustController(view)

    root.mainloop()
