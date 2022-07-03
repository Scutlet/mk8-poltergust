from tkinter import *
from tkinter import ttk

from PIL import Image, ImageTk

from utils import get_resource_path

class PoltergustAboutView(Toplevel):
    """ Displays "About" information of the application. """

    def __init__(self, master: Tk, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.wm_title("Poltergust - About")

        with Image.open(get_resource_path("resources/scutlet.png")) as img:
            scutlet_canvas = Canvas(self, width=64, height=64)
            scutlet_canvas.grid(column=1, row=1, sticky=(N,W,E,S))
            self.scutlet_img = ImageTk.PhotoImage(img.resize((64, 64)))
            scutlet_canvas.create_image(0, 0, image=self.scutlet_img, anchor=NW)

        ttk.Label(self, wraplength=275, text="Poltergust visualises Mario Kart 8 ghost data based on their filenames. It's possible to manually tinker with those, but doing so may break assumptions made by this tool. Do so at your own risk.").grid(column=0, row=0, columnspan=2, padx=2, pady=2)
        ttk.Label(self, wraplength=135, text="Created by Scutlet").grid(column=0, row=1)
        ttk.Label(self, text="This software is available under GPL v3").grid(column=0, row=2, columnspan=2)

        ws = master.winfo_screenwidth() # width of the screen
        hs = master.winfo_screenheight() # height of the screen

        # calculate x and y coordinates for the Tk root window
        x = int((ws/2) - (275/2))
        y = int(hs/7)

        self.geometry(f"275x160+{x}+{y}")

        # Disable bottom window
        master.attributes('-disabled', 1)
        self.transient(master)
        self.focus_set()
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        """ On closing the about window """
        # Give back control to the bottom window
        self.master.attributes('-disabled', 0)
        self.destroy()
