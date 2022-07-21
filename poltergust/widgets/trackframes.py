from abc import ABC, abstractmethod
from idlelib.tooltip import Hovertip
from tkinter import *
from tkinter import ttk
from tkinter.font import Font, ITALIC
import webbrowser

from PIL import Image, ImageTk

from poltergust.utils import WrappingLabel

class MK8TrackFrameBase(LabelFrame):
    """ A frame containing information of a FramableTrack """
    BASE_FONT = "TkDefaultFont"
    TRACK_PREVIEW_SIZE: tuple[int, int] = (64, 64)

    def __init__(self, master: Toplevel, track_name: str, track_preview: Image.Image, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.ITALICS_FONT = Font(font=self.BASE_FONT)
        self.ITALICS_FONT.config(slant=ITALIC)

        # Create and clear canvas
        self.canvas = Canvas(self, width=self.TRACK_PREVIEW_SIZE[0], height=self.TRACK_PREVIEW_SIZE[1], borderwidth=0, highlightthickness=0)
        self.canvas.create_rectangle(0, 0, self.TRACK_PREVIEW_SIZE[0], self.TRACK_PREVIEW_SIZE[1], fill="#e8e8e3", outline="#e8e8e3")

        # Cache image so it's not garbage collected
        self._track_preview = ImageTk.PhotoImage(track_preview)

        # Write to canvas
        self.canvas.create_image(self.TRACK_PREVIEW_SIZE[0]/2, self.TRACK_PREVIEW_SIZE[1]/2, image=self._track_preview, anchor=CENTER)
        self.canvas.pack(side=LEFT, padx=(0, 4), pady=(0, 1))

        # Track Name
        self._title_lb = WrappingLabel(self, text=track_name)
        self._title_lb.pack(side=TOP, fill=X, padx=(0, 2), pady=0)


class MK8TrackFrameSmall(MK8TrackFrameBase):
    """ A small variant of a framed track """
    TRACK_PREVIEW_SIZE = (48, 27)

    def __init__(self, master: Toplevel, track_name: str, track_preview: Image.Image, *args, **kwargs):
        super().__init__(master, track_name, track_preview, *args, **kwargs)

        # Center the label
        self._title_lb.pack_forget()
        self._title_lb.pack(side=LEFT, fill=X, padx=(0, 2))


class MK8TrackFrameBig(MK8TrackFrameBase):
    """ A larger variant of a framed track. Is able to include more information. """

    TRACK_PREVIEW_SIZE = (96, 54)

    def __init__(self, master: Toplevel, track_name: str, track_preview: Image.Image, track_author: str, url_text: str, url_icon: Image.Image, url_link: str, url_tooltip: str, *args, **kwargs):
        super().__init__(master, track_name, track_preview, *args, **kwargs)

        self._sep = ttk.Separator(self, orient=HORIZONTAL)
        self._sep.pack(fill=X, padx=4, pady=(2, 0))

        # Track author
        author_text = track_author
        author_lb = Label(self, text=author_text, font=self.ITALICS_FONT)
        author_lb.pack(side=LEFT)

        # URL
        self._url_icon = ImageTk.PhotoImage(url_icon)
        mod_id_lb = Label(self, text=f" {url_text}", image=self._url_icon, compound=LEFT, cursor="hand2", fg="blue")
        mod_id_lb.place(relx=0.5, rely=0.5, anchor=CENTER)
        mod_id_lb.pack(side=RIGHT)

        # Tooltip and URL
        site_url = url_link
        mod_id_lb.bind("<Button-1>",
            lambda e, site_url=site_url: webbrowser.open(site_url)
        )
        Hovertip(mod_id_lb, url_tooltip, hover_delay=1000)

        self._widgets: list[Widget] = [self, self._title_lb, author_lb, mod_id_lb]
        self._default_color = author_lb.cget("background") # System background (SystemButtonFace on Windows/MacOS)

    def set_color(self, background: str|None):
        """ Sets the background colour of the frame. """
        style = ttk.Style()
        self._sep.configure(style="TSeparator")
        background = background or self._default_color

        # Color separator
        style.configure(f"{background}.TSeparator", background=background)
        self._sep.configure(style=f"{background}.TSeparator")

        # Color widgets
        for widget in self._widgets:
            widget.configure(background=background)



class FramableTrack(ABC):
    """ Abstract class to make a track a FramableTrack """
    TRACK_PREVIEW_SIZE: tuple[int, int] = (96, 54)

    _sort_field_name: str = None

    @property
    def sort_field(self) -> str:
        """ The name of the class's field that should be used for sorting and searching purposes """
        return getattr(self, self._sort_field_name)

    @abstractmethod
    def frame(self, master: Toplevel, *args, **kwargs) -> MK8TrackFrameBig:
        """ Creates a big frame with information about this track. """

class MiniFramableTrack(FramableTrack, ABC):
    """ Abstract class to make a track a FramableTrack that also supports a small variant. """
    @abstractmethod
    def miniframe(self, master: Toplevel, *args, **kwargs) -> MK8TrackFrameSmall:
        """ Creates a small frame with information about this track. """

