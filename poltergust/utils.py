from abc import ABCMeta
import os
import sys
from tkinter import *
from tkinter import ttk
from typing import Callable, Generic, TypeVar

def get_resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def bind_tree(widget: Widget, event, callback, add: str='', force_rebind=False):
    """
        Binds an event to a widget and all its descendants.
        Skips widgets already bound, unless `force_rebind=True`.
        See: https://stackoverflow.com/a/11457766
    """
    if not widget.bind(event) or force_rebind:
        widget.bind(event, callback, add)

    for child in widget.children.values():
        bind_tree(child, event, callback)

class WrappingLabel(ttk.Label):
    ''' A type of Label that automatically adjusts the wrap to the size '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bind('<Configure>', lambda e: self.config(wraplength=self.winfo_width()))

class PoltergustPopup(Toplevel):
    """ General Popup class that places the window in the middle of the screen on creation """
    window_title = None
    window_width = None
    window_height = None

    def __init__(self, master: Toplevel, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.wm_title(self.window_title)

        ws = master.winfo_screenwidth() # width of the screen
        hs = master.winfo_screenheight() # height of the screen

        # calculate x and y coordinates for the Tk root window
        x = int((ws/2) - (275/2))
        y = int(hs/7)

        self.geometry(f"{self.window_width}x{self.window_height}+{x}+{y}")

        # Close with <esc>
        self.bind("<Escape>", lambda e: self.on_close())

    def on_close(self):
        """ On closing the popup """
        self.destroy()

class PoltergustBlockingPopup(PoltergustPopup):
    """ General Popup class that takes control from the main window """
    window_title = None
    window_width = None
    window_height = None

    def __init__(self, master: Toplevel, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        # Disable bottom window
        master.attributes('-disabled', 1)
        self.transient(master)
        self.focus_set()
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        # Give back control to the bottom window
        self.master.attributes('-disabled', 0)

        super().on_close()

class Singleton(type):
    """ Singleton pattern Metaclass """
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class SingletonABCMeta(ABCMeta, Singleton):
    """ Singleton Metaclass to use if also using an abstract base class """

T = TypeVar('T')

class Observable(Generic[T]):
    """
        Observer pattern. Signifies that the class accepts 'listeners' that are notified
        when a value of type T changes. What this value is left up to the class implementing
        this pattern.
    """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._listeners: list[Callable[[T], None]] = []

    def add_listener(self, listener: Callable[[T], None]) -> None:
        """ Adds a listener. """
        self._listeners.append(listener)

    def notify_listeners(self, val: T) -> None:
        """ Notifies all listeners. """
        for listener in self._listeners:
            listener(val)
