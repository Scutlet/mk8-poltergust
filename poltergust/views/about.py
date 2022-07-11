from tkinter import *
from tkinter import ttk

from PIL import Image, ImageTk

from poltergust.utils import PoltergustBlockingPopup, get_resource_path


class PoltergustAboutView(PoltergustBlockingPopup):
    """ Displays "About" information of the application. """
    window_title = "Poltergust - About"
    window_width = 275
    window_height = 160

    def __init__(self, master: Tk, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        with Image.open(get_resource_path("resources/scutlet.png")) as img:
            scutlet_canvas = Canvas(self, width=64, height=64, borderwidth=0, highlightthickness=0)
            scutlet_canvas.grid(column=1, row=1, sticky=(N,W,E,S))
            self.scutlet_img = ImageTk.PhotoImage(img.resize((64, 64)))
            scutlet_canvas.create_image(0, 0, image=self.scutlet_img, anchor=NW)

        ttk.Label(self, wraplength=275, text="Poltergust visualises Mario Kart 8 ghost data based on their filenames. It's possible to manually tinker with those, but doing so may break assumptions made by this tool. Do so at your own risk.").grid(column=0, row=0, columnspan=2, padx=2, pady=2)
        ttk.Label(self, wraplength=135, text="Created by Scutlet").grid(column=0, row=1)
        ttk.Label(self, text="This software is available under GPL v3").grid(column=0, row=2, columnspan=2)
