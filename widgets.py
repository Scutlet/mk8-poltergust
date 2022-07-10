from abc import ABC, abstractmethod
from idlelib.tooltip import Hovertip
from tkinter import *
from tkinter import ttk
from tkinter.font import Font, ITALIC
import webbrowser

from PIL import Image, ImageTk

from utils import WrappingLabel, get_resource_path

class MK8TrackFrame(LabelFrame):
    """ TODO """
    BASE_FONT = "TkDefaultFont"

    def __init__(self, master: Tk, track_name: str, track_author: str, track_preview: Image.Image, url_text: str, url_icon: Image.Image, url_link: str, url_tooltip: str, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.ITALICS_FONT = Font(font=self.BASE_FONT)
        self.ITALICS_FONT.config(slant=ITALIC)

        # Create and clear canvas
        canvas = Canvas(self, width=96, height=54, borderwidth=0, highlightthickness=0)
        canvas.create_rectangle(0, 0, 96, 54, fill="#e8e8e3", outline="#e8e8e3")

        # Cache image so it's not garbage collected
        self._track_preview = ImageTk.PhotoImage(track_preview)

        # Write to canvas
        canvas.create_image(96/2, 54/2, image=self._track_preview, anchor=CENTER)
        canvas.pack(side=LEFT, padx=(0, 4), pady=(0, 1))

        # Track Name
        title_lb = WrappingLabel(self, text=track_name)
        title_lb.pack(side=TOP, fill=X, padx=(0, 2))
        ttk.Separator(self, orient=HORIZONTAL).pack(fill=X, padx=4, pady=(2, 0))

        # Track author
        author_text = track_author
        author_lb = Label(self, wraplength=135, text=author_text, font=self.ITALICS_FONT)
        author_lb.pack(side=LEFT)

        # URL
        self._url_icon = ImageTk.PhotoImage(url_icon)
        mod_id_lb = Label(self, wraplength=135, text=f" {url_text}", image=self._url_icon, compound=LEFT, cursor="hand2", fg="blue")
        mod_id_lb.place(relx=0.5, rely=0.5, anchor=CENTER)
        mod_id_lb.pack(side=RIGHT)

        # Tooltip and URL
        site_url = url_link
        mod_id_lb.bind("<Button-1>",
            lambda e, site_url=site_url: webbrowser.open(site_url)
        )
        Hovertip(mod_id_lb, url_tooltip, hover_delay=1000)

class FramableTrack(ABC):
    """ TODO """
    TRACK_PREVIEW_SIZE: tuple[int, int] = (96, 54)

    _sort_field_name: str = None

    @property
    def sort_field(self) -> str:
        """ TODO """
        return getattr(self, self._sort_field_name)

    @abstractmethod
    def frame(self, master: Tk, *args, **kwargs) -> MK8TrackFrame:
        """ TODO """


class IntEntry(ttk.Entry):
    """ Tkinter entry that only accepts numbers as its input """
    def __init__(self, master: Tk, *args, **kwargs):
        super().__init__(master, *args, validate="key", validatecommand=(master.register(self.validate_input), "%P", '%d'), **kwargs)

    def validate_input(self, input: str, acttype: int):
        return acttype != '1' or input.isdigit()


class IconButton(Button):
    """ Button with both text and an icon """
    def __init__(self, master: Tk, *args, image_path: str="", compound:str=LEFT, text:str|float="", **kwargs):
        self._img = None
        if image_path:
            self._img = PhotoImage(file=get_resource_path(image_path))
        super().__init__(master, *args, image=self._img, compound=compound, text=f" {text}", **kwargs)
