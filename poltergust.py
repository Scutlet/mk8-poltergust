from tkinter import *

from controller import PoltergustController
from ct_storage import MK8CTStorage
from view_main import PoltergustMainView


if __name__ == '__main__':
    # Create and display the UI
    root = Tk()
    view = PoltergustMainView(root)
    db = MK8CTStorage()
    controller = PoltergustController(view, db)

    root.mainloop()
