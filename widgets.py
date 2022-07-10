from idlelib.tooltip import Hovertip
from tkinter import *
from tkinter import ttk
from tkinter.font import Font, ITALIC
import webbrowser

from PIL import Image, ImageTk

from downloader import MK8CustomTrack
from utils import WrappingLabel


class MK8CustomTrackFrame(LabelFrame):
    BASE_FONT = "TkDefaultFont"

    def __init__(self, master: Tk, track: MK8CustomTrack, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.ITALICS_FONT = Font(font=self.BASE_FONT)
        self.ITALICS_FONT.config(slant=ITALIC)

        # Track Preview Image
        canvas = Canvas(self, width=96, height=54, borderwidth=0, highlightthickness=0)
        img = None
        if track.preview_image is not None:
            try:
                img = Image.open(track.preview_image)
                img = img.resize(size=(96, 54))
            except FileNotFoundError as e:
                pass

        if img is None:
            # Select fallback image
            img = track.mod_site.icon
            img = img.resize(size=(24, 24))
            canvas.create_rectangle(0, 0, 96, 54, fill="#e8e8e3", outline="#e8e8e3")

        # Cache image so it's not garbage collected
        img = ImageTk.PhotoImage(img)
        self._track_preview_img = img

        canvas.create_image(96/2, 54/2, image=img, anchor=CENTER)
        canvas.pack(side=LEFT, padx=(0, 4), pady=(0, 1))

        # Track Name
        title_lb = WrappingLabel(self, text=track.name)
        title_lb.pack(side=TOP, fill=X, padx=(0, 2))
        ttk.Separator(self, orient=HORIZONTAL).pack(fill=X, padx=4, pady=(2, 0))

        # Track author
        author_text = track.author or "Unknown Author"
        author_lb = Label(self, wraplength=135, text=author_text, font=self.ITALICS_FONT)
        author_lb.pack(side=LEFT)

        # ModId
        self._mod_site_img = ImageTk.PhotoImage(track.mod_site.icon)
        mod_id_lb = Label(self, wraplength=135, text=f" {track.mod_id}", image=self._mod_site_img, compound=LEFT, cursor="hand2", fg="blue")
        mod_id_lb.place(relx=0.5, rely=0.5, anchor=CENTER)
        mod_id_lb.pack(side=RIGHT)

        # Tooltip and URL
        site_url = track.mod_site.get_url_for_mod_id(track.mod_id)
        mod_id_lb.bind("<Button-1>",
            lambda e, site_url=site_url: webbrowser.open(site_url)
        )
        Hovertip(mod_id_lb, f"{track.mod_site} - {site_url}", hover_delay=1000)
