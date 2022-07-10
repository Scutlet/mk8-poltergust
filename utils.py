from abc import ABCMeta
import os
import sys
from tkinter import *
from tkinter import ttk

class Singleton(type):
    """ Singleton Metaclass """
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class SingletonABCMeta(ABCMeta, Singleton):
    """ Singleton Metaclass to use if also using an abstract base class """

def get_resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class WrappingLabel(ttk.Label):
    ''' A type of Label that automatically adjusts the wrap to the size '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bind('<Configure>', lambda e: self.config(wraplength=self.winfo_width()))

class PoltergustPopup(Toplevel):
    """ General Popup class that places the window in the middle of the screen on creation """

class PoltergustBlockingPopup(PoltergustPopup):
    """ General Popup class that takes control from the main window """
    window_title = None
    window_width = None
    window_height = None

    def __init__(self, master: Tk, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.wm_title(self.window_title)

        ws = master.winfo_screenwidth() # width of the screen
        hs = master.winfo_screenheight() # height of the screen

        # calculate x and y coordinates for the Tk root window
        x = int((ws/2) - (275/2))
        y = int(hs/7)

        self.geometry(f"{self.window_width}x{self.window_height}+{x}+{y}")

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



# Inject 8 bytes just before Mii data.
# With Header:
# 27C-284

# Without 0x48 Header:
# 234-23c
