from tkinter import *

from controller import PoltergustController
from view_main import PoltergustMainView


if __name__ == '__main__':
    # Create and display the UI
    root = Tk()
    view = PoltergustMainView(root)
    controller = PoltergustController(view)

    root.mainloop()
