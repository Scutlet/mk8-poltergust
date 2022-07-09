from idlelib.tooltip import Hovertip
from tkinter import *
from tkinter import ttk
from tkinter.font import Font, ITALIC
import webbrowser

from PIL import Image, ImageTk

from downloader import MK8CustomTrack, MOD_SITES
from utils import PoltergustPopup, WrappingLabel, get_resource_path


class PoltergustCTManagerView(PoltergustPopup):
    """
        Displays a window of all cached CTs.
    """
    window_title = "Poltergust - Custom Track Database"
    window_width = 310
    window_height = 400

    BASE_FONT = "TkDefaultFont"

    # Add mod sites
    mod_site_choices = {site.name: site for site in MOD_SITES}

    def __init__(self, master: Tk, track_list: list[MK8CustomTrack], *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.ITALICS_FONT = Font(font=self.BASE_FONT)
        self.ITALICS_FONT.config(slant=ITALIC)

        # Cache mod site icons so they're not garbage collected
        self._mod_site_image_cache = [ImageTk.PhotoImage(site.icon) for site in MOD_SITES]

        # Top frame
        top = Frame(self)
        top.pack(padx=5, pady=6, fill=X)

        # Add CT Box
        self._plus_img = PhotoImage(file=get_resource_path('resources/icons/plus-solid.png'))
        self.add_button = Button(top, text="Add a Mod", image=self._plus_img, compound=LEFT)
        self.add_button.pack(side=LEFT)

        # Search Box
        self.search_value = StringVar()
        self.search_value.trace_add("write", lambda var, index, mode: self.reload_list())
        ttk.Entry(top, width=25, textvariable=self.search_value).pack(side=RIGHT)

        # Search Icon
        self._search_img = PhotoImage(file=get_resource_path('resources/icons/magnifying-glass-solid.png'))
        canvas = Canvas(top, width=10, height=10, borderwidth=0, highlightthickness=0)
        canvas.create_image(0, 0, image=self._search_img, anchor=NW)
        canvas.pack(side=RIGHT, padx=(0, 4))

        # Only canvas elements are scrollable
        self.canvas = Canvas(self, bd=0, borderwidth=0, highlightthickness=0)
        vsb = Scrollbar(self, command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=vsb.set)

        # Scrollbar
        vsb.pack(side=RIGHT, fill=Y)
        self.vsb = vsb
        self.canvas.pack(side=RIGHT, fill=BOTH, expand=True)

        # Track List
        self.track_frame = ttk.Frame(self.canvas)
        self.track_frame.pack()
        self.track_widgets = self._build_track_list(track_list)
        self.reload_list()

        # Make sure Tkinter knows what's scrollable
        self.canvas.create_window(0, 0, anchor="nw", window=self.track_frame, tags=("inner",))

        # Recalculate bounding box if the frame or window changes size
        self.canvas.bind("<Configure>", self._resize_inner_frame)
        self.track_frame.bind("<Configure>", self._reset_scrollregion)

        # Make the mouse wheel move the scrollbar
        self.canvas.bind_all("<MouseWheel>", self._set_scroll) # for Windows/MacOS
        self.canvas.bind_all("<Button-4>", self._set_scroll) # for Linux
        self.canvas.bind_all("<Button-5>", self._set_scroll) # for Linux

    def _set_scroll(self, event):
        """ Moves the scrollbar when the user scrolls the mouse wheel """
        start, end = self.vsb.get()
        if start <= 0 and end >= 1:
            # There's nothing to scroll; Scrollbar is disabled
            return

        amount = -1
        if event.num == 5 or event.delta < 0:
            # Scrolling down instead
            amount = 1
        self.canvas.yview_scroll(amount, "units")

    def _reset_scrollregion(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _resize_inner_frame(self, event):
        self.canvas.itemconfig("inner", width=event.width)

    def _build_track_list(self, track_list: list[MK8CustomTrack]) -> list[tuple[MK8CustomTrack, Widget]]:
        """ TODO """
        track_widgets = []
        imgs = []

        for track in sorted(track_list, key=lambda item: item.name):
            frame = ttk.LabelFrame(self.track_frame)

            # Track Preview Image
            canvas = Canvas(frame, width=96, height=54, borderwidth=0, highlightthickness=0)
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

            img = ImageTk.PhotoImage(img)
            imgs.append(img)

            canvas.create_image(96/2, 54/2, image=img, anchor=CENTER)
            canvas.pack(side=LEFT, padx=(0, 4))

            # Track Name
            title_lb = WrappingLabel(frame, text=track.name)
            title_lb.pack(side=TOP, fill=X, padx=(0, 2))
            ttk.Separator(frame, orient=HORIZONTAL).pack(fill=X, padx=4, pady=(2, 0))

            # Track author
            author_text = track.author or "Unknown Author"
            author_lb = Label(frame, wraplength=135, text=author_text, font=self.ITALICS_FONT)
            author_lb.pack(side=LEFT, anchor=N)

            # ModId
            mod_id_lb = Label(frame, wraplength=135, text=f" {track.mod_id}", image=self._mod_site_image_cache[track.mod_site.id], compound=LEFT, cursor="hand2", fg="blue")
            mod_id_lb.place(relx=0.5, rely=0.5, anchor=CENTER)
            mod_id_lb.pack(side=RIGHT, anchor=N)

            # Tooltip and URL
            site_url = track.mod_site.get_url_for_mod_id(track.mod_id)
            mod_id_lb.bind("<Button-1>",
                lambda e, site_url=site_url: webbrowser.open(site_url)
            )
            Hovertip(mod_id_lb, f"{track.mod_site} - {site_url}", hover_delay=1000)

            track_widgets.append((track, frame))
        self._previews = imgs
        return track_widgets

    def reload_list(self):
        """ TODO """
        search_value = self.search_value.get().lower()
        for track, widget in self.track_widgets:
            widget.pack_forget()
            if not search_value or search_value in track.name.lower():
                widget.pack(fill='both', padx=(2, 5))
