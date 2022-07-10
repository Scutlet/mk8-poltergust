from idlelib.tooltip import Hovertip
from tkinter import *
from tkinter import ttk, filedialog
from tkinter.font import NORMAL as FONT_NORMAL
import webbrowser

from PIL import ImageTk

from gamedata import MK8GhostType, COURSE_IDS, CHARACTERS, FLAGS, GLIDERS, KARTS, MII_WEIGHT_CLASSES, WHEELS
from imagemapper import MK8CharacterImageMapper, MK8FlagImageMapper, MK8ImageAtlasMapper, MK8VehiclePartImageMapper, MK8TrackImageMapper
from utils import get_resource_path
from view_about import PoltergustAboutView


class PoltergustMainView:
    """
        Defines and builds the Poltergust UI using Tkinter.
    """
    WINDOW_WIDTH = 550
    WINDOW_HEIGHT = 400

    # Buttons
    BTN_OPEN = "Open..."
    BTN_CLOSE = "Close"
    BTN_RELOAD_FROM_DISK = "Reload from disk"
    BTN_EXPORT_AS_STAFF_GHOST = "Convert to Staff Ghost"
    BTN_EXPORT_AS_DOWNLOADED_GHOST = "Convert to Downloaded Ghost"
    BTN_DOWNLOADED_GHOST_SLOT_PREFIX = "Slot "
    BTN_EXTRACT_MII = "Extract Mii"
    BTN_REPLACE_MII = "Replace Mii"
    BTN_CHANGE_TRACK = "Change Track"
    BTN_CT_MANAGER = "Custom Track Manager"

    # FONT = ("Agency FB", 14, FONT_NORMAL)
    FONT = ("Courier", 14, FONT_NORMAL)

    # Editing is not yet supported
    EDIT_STATE = "readonly"

    # Window Icon
    WINDOW_ICON = get_resource_path("resources/scutlet_static_cropped.png")

    # Icon Atlas mappers
    CHARACTER_MAPPER = MK8CharacterImageMapper()
    FLAG_MAPPER = MK8FlagImageMapper()
    VEHICLE_PART_MAPPER = MK8VehiclePartImageMapper()
    TRACK_MAPPER = MK8TrackImageMapper()

    # Icon sizes
    FLAG_SIZE = (33, 22)
    CHARACTER_SIZE = (64, 64)
    VEHICLE_PART_SIZE = (75, 48)
    TRACK_SIZE = (80, 45)

    def __init__(self, root: Tk):
        """ Initializes the UI """
        self.data = None
        self.ghostfile = None

        self.root = root
        root.option_add('*tearOff', FALSE)
        root.title("Poltergust - Mario Kart 8 Ghost Data Tool")
        root.iconphoto(True, PhotoImage(file=self.WINDOW_ICON))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        # Create main frame (needed to have a consistent background across platforms and themes)
        mainframe = ttk.Frame(root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

        # Create a menubar
        self.menubar = Menu(root)
        root['menu'] = self.menubar

        self.menu_file = Menu(self.menubar)
        self.menu_export = Menu(self.menubar)
        self.menu_edit = Menu(self.menubar)
        self.menu_help = Menu(self.menubar)
        self.menubar.add_cascade(menu=self.menu_file, label='File')
        self.menubar.add_cascade(menu=self.menu_edit, label='Edit')
        self.menubar.add_cascade(menu=self.menu_export, label='Export')
        self.menubar.add_command(label=self.BTN_CT_MANAGER)
        self.menubar.add_cascade(menu=self.menu_help, label='Help')

        # File options
        self.menu_file.add_command(label=self.BTN_OPEN)
        self.menu_file.add_command(label=self.BTN_RELOAD_FROM_DISK)
        self.menu_file.add_command(label=self.BTN_CLOSE)

        # Export options
        self.menu_export.add_command(label=self.BTN_EXTRACT_MII)
        self.menu_export.add_command(label=self.BTN_EXPORT_AS_STAFF_GHOST)
        self.menu_export_download = Menu(self.menu_export)
        for slot in range(16):
            self.menu_export_download.add_command(label=self.BTN_DOWNLOADED_GHOST_SLOT_PREFIX+str(slot))
        self.menu_export.add_cascade(menu=self.menu_export_download, label=self.BTN_EXPORT_AS_DOWNLOADED_GHOST)

        # Edit Options
        # self.menu_edit.add_command(label=self.BTN_REPLACE_MII)
        self.menu_edit.add_command(label=self.BTN_CHANGE_TRACK)

        # About options
        self.menu_help.add_command(label="About", command=self.popup_about)
        self.menu_help.add_command(label="Report a Bug",
            command=lambda: webbrowser.open("https://github.com/Scutlet/mk8-poltergust/issues")
        )
        self.menu_help.add_command(label='Mii Viewer',
            command=lambda: webbrowser.open('https://kazuki-4ys.github.io/web_apps/MiiInfoEditorCTR/')
        )

        # Loaded file
        self.lb_ghostfile = ttk.Label(mainframe, text="")
        self.lb_ghostfile.grid(column=0, row=0, sticky=(N, W, E, S))

        # Configure data frame
        self.dataframe = ttk.Frame(mainframe)
        self.dataframe.grid(column=0, row=1, sticky=(N, W, E, S))

        # Ghostinfo frame (contains character, name, flag, total time)
        ghostinfosframe = ttk.Frame(self.dataframe)
        ghostinfosframe.grid(column=0, row=0, columnspan=2, sticky=(N, W, E, S))

        # Game Version
        self.game_version = ttk.Label(ghostinfosframe, text="GAME VERSION PLACEHOLDER")
        self.game_version.grid(column=0, row=0, padx=3, sticky=(N, W, E, S))
        self.ghost_type = ttk.Label(ghostinfosframe, text="GHOST TYPE PLACEHOLDER")
        self.ghost_type.grid(column=0, row=1, padx=3, sticky=(W, E))

        # Summary frame (contains character, name, flag, total time)
        summaryframe = ttk.LabelFrame(self.dataframe)
        summaryframe.grid(column=0, row=1, sticky=(N, W, E, S), padx=(0, 3))

        # Character
        self.character_canvas = Canvas(summaryframe, width=self.CHARACTER_SIZE[0], height=self.CHARACTER_SIZE[1], borderwidth=0, highlightthickness=0)
        self.character_canvas.grid(column=0, row=0, rowspan=2, sticky=(N,W,E,S))
        self.character_tip = Hovertip(self.character_canvas, 'PLACEHOLDER', hover_delay=1000)

        # Name
        self.playername = StringVar()
        playername_entry = ttk.Entry(summaryframe, width=16, textvariable=self.playername, font=self.FONT, state=self.EDIT_STATE)
        playername_entry.grid(column=1, row=0, columnspan=4, sticky=(W,E), padx=(0, 3))

        # Flag
        self.flag_canvas = Canvas(summaryframe, width=self.FLAG_SIZE[0], height=self.FLAG_SIZE[1], borderwidth=0, highlightthickness=0)
        self.flag_canvas.grid(column=1, row=1)
        self.flag_tip = Hovertip(self.flag_canvas, 'PLACEHOLDER', hover_delay=1000)

        # Total Time (Stringvar to allow leading zeroes)
        self.total_min = StringVar()
        total_min_entry = ttk.Entry(summaryframe, width=1, textvariable=self.total_min, font=self.FONT, justify=CENTER, state=self.EDIT_STATE)
        total_min_entry.grid(column=2, row=1, sticky=(W,E), padx=(20, 0))

        self.total_sec = StringVar()
        total_sec_entry = ttk.Entry(summaryframe, width=2, textvariable=self.total_sec, font=self.FONT, justify=CENTER, state=self.EDIT_STATE)
        total_sec_entry.grid(column=3, row=1, sticky=(W,E))

        self.total_ms = StringVar()
        total_ms_entry = ttk.Entry(summaryframe, width=3, textvariable=self.total_ms, font=self.FONT, justify=CENTER, state=self.EDIT_STATE)
        total_ms_entry.grid(column=4, row=1, sticky=(W,E), padx=(0, 3))

        # Trackinfo frame
        trackframe = ttk.LabelFrame(self.dataframe)
        trackframe.grid(column=1, row=1, sticky=(N, W, E, S))
        self.track_canvas = Canvas(trackframe, width=self.TRACK_SIZE[0], height=self.TRACK_SIZE[1], borderwidth=0, highlightthickness=0)
        self.track_canvas.grid(column=0, row=0, sticky=(N,W,E,S), pady=(7, 10), padx=(4, 4))
        self.track_tip = Hovertip(self.track_canvas, 'PLACEHOLDER', hover_delay=1000)

        self.track = StringVar()
        track_entry = ttk.Entry(trackframe, width=25, textvariable=self.track, font=(self.FONT[0], 9, self.FONT[2]), state=self.EDIT_STATE)
        track_entry.grid(column=1, row=0, sticky=(W,E), padx=(0, 3))

        # Lap Times frame (contains all lap times)
        laptimesframe = ttk.LabelFrame(self.dataframe)
        laptimesframe.grid(column=0, row=2, sticky=(N, W, E, S), padx=(0, 3))

        # Lap Times
        self.lap_splits = self.generate_laptimes_entries(laptimesframe, 7)

        # Vehicle frame
        vehicleframe = ttk.LabelFrame(self.dataframe)
        vehicleframe.grid(column=1, row=2, sticky=(N, W, E, S))

        # Vehicle Combination
        self.kart, self.kart_canvas, self.kart_tip = self.generate_vehicle_entry(vehicleframe, StringVar(), 1)
        self.wheels, self.wheels_canvas, self.wheels_tip = self.generate_vehicle_entry(vehicleframe, StringVar(), 2)
        self.glider, self.glider_canvas, self.glider_tip = self.generate_vehicle_entry(vehicleframe, StringVar(), 3)

        playername_entry.focus()

        self.resize_window()

    def popup_about(self) -> None:
        """ Displays 'about' information """
        PoltergustAboutView(self.root)

    def select_ghost_file(self) -> str:
        """ UI Popup for selecting a ghost file """
        return filedialog.askopenfilename(
            parent=self.root,
            title="Open MK8 Ghost Data",
            filetypes=(("MK8 Ghost Data (*.dat)", ".dat"), ('All files', '*.*'))
        )

    def select_mii_output_folder(self, filename: str) -> str:
        """ UI Popup for selecting a Mii extraction output location """
        return filedialog.asksaveasfilename(
            parent=self.root,
            title=self.BTN_EXTRACT_MII,
            defaultextension=".3dsmii",
            filetypes=(("Wii U/3DS Mii (.3dsmii)", ".3dsmii"), ('All files', '*.*')),
            initialfile=filename,
        )

    def select_mii_file(self) -> str:
        """ UI Popup for selecting a Mii file """
        return filedialog.askopenfilename(
            parent=self.root,
            title="Select new Mii",
            defaultextension=".3dsmii",
            filetypes=(("Wii U/3DS Mii (.3dsmii)", ".3dsmii"), ('All files', '*.*')),
        )

    def select_conversion_staff_output_folder(self) -> str:
        """ UI Popup for selecting a Staff Ghost conversion output location """
        return filedialog.askdirectory(
            parent=self.root,
            title="Output directory for MK8 Staff Ghost",
        )

    def select_conversion_download_output_folder(self) -> str:
        """ UI Popup for selecting a Downloaded Ghost conversion output location """
        return filedialog.askdirectory(
            parent=self.root,
            title="Output directory for MK8 Downloaded Ghost",
        )




    def set_ghost_type(self, ghost_type: MK8GhostType, ghost_number: int, ghost_has_header: bool) -> None:
        """ Sets ghost type text """
        if ghost_type == MK8GhostType.STAFF_GHOST:
            self.ghost_type.config(text="Staff Ghost")
            # No need to export a staff ghost as itself
            self.menu_export.entryconfig(self.BTN_EXPORT_AS_STAFF_GHOST, state=DISABLED)
        elif ghost_type == MK8GhostType.PLAYER_GHOST:
            self.ghost_type.config(text="Player Ghost")
        elif ghost_type == MK8GhostType.DOWNLOADED_GHOST:
            text = f"Downloaded Ghost - Slot {ghost_number}"
            if not ghost_has_header:
                text += " (Poltergust Conversion/Nintendo Clients Package Download)"
            else:
                text += " (In-Game Download)"
            self.ghost_type.config(text=text)
            # No need to export a downloaded ghost in the same ghost slot
            self.menu_export_download.entryconfig(self.BTN_DOWNLOADED_GHOST_SLOT_PREFIX + str(ghost_number), state=DISABLED)
        else:
            self.ghost_type.config(text="MKTV Replay")

    def set_flag(self, flag_id: int) -> None:
        """ Sets the player flag """
        flag = ("Unknown Flag", None)
        if 0 <= flag_id < len(FLAGS):
            flag = FLAGS[flag_id]
            if flag[0] is None:
                # A zero-flag means no flag was set
                flag = ("No Flag", None)

        # Update flag image
        self.set_mapped_image(self.flag_canvas, self.FLAG_MAPPER, flag[1], resize_to=self.FLAG_SIZE)
        self.flag_tip.text = flag[0] + f" ({flag_id})"

    def set_character(self, character_id: int, character_variant_id: int, mii_weight_class_id: int) -> None:
        """ Sets the character icon """

        char = CHARACTERS.get(character_id, (f"Unknown Character", None))
        if type(char[1]) != int and char[1] is not None:
            # We have subcharacters (E.g. Blue Yoshi, BoTW Link, Mii)
            indx = character_variant_id
            variant = char[1][indx] if 0 <= indx and indx < len(char[1]) else ("Unknown Variant", None)
            if char[0] == "Mii":
                # Miis also have a weight class
                indx = mii_weight_class_id
                variant[0] += F" - {MII_WEIGHT_CLASSES[indx] if 0 <= indx and indx < len(MII_WEIGHT_CLASSES) else 'Unknown Weight Class'}"
            char = (f"{char[0]} ({variant[0]})", variant[1])

        self.set_mapped_image(self.character_canvas, self.CHARACTER_MAPPER, char[1], resize_to=self.CHARACTER_SIZE)
        self.character_tip.text = f"{char[0]} ({character_id})"

    def set_track(self, track_id: int, ghost_number: int) -> None:
        """ Sets the track preview """
        track = COURSE_IDS.get(track_id, None)
        track_name = "Unknown Track"
        track_icon_index = None
        if track is not None:
            track_name = track.name
            track_icon_index = track.icon_index
        self.set_mapped_image(self.track_canvas, self.TRACK_MAPPER, track_icon_index, resize_to=self.TRACK_SIZE)
        self.track.set(track_name)
        self.track_tip.text = f"{ghost_number} - {track_id}"

    def set_vehicle_parts(self, kart_id: int, wheels_id: int, glider_id: int) -> None:
        """ Sets vehicle part previews """
        # Kart
        kart = KARTS.get(kart_id, ("Unknown Kart", None))
        self.set_mapped_image(self.kart_canvas, self.VEHICLE_PART_MAPPER, kart[1], resize_to=self.VEHICLE_PART_SIZE)
        self.kart.set(kart[0])
        self.kart_tip.text = str(kart_id)

        # Wheels
        wheels = WHEELS.get(wheels_id, ("Unknown Wheels", None))
        self.set_mapped_image(self.wheels_canvas, self.VEHICLE_PART_MAPPER, wheels[1], resize_to=self.VEHICLE_PART_SIZE)
        self.wheels.set(wheels[0])
        self.wheels_tip.text = str(wheels_id)

        # Glider
        glider = GLIDERS.get(glider_id, ("Unknown Glider", None))
        self.set_mapped_image(self.glider_canvas, self.VEHICLE_PART_MAPPER, glider[1], resize_to=self.VEHICLE_PART_SIZE)
        self.glider.set(glider[0])
        self.glider_tip.text = str(glider_id)

    def set_mapped_image(self, canvas: Canvas, mapper: MK8ImageAtlasMapper, index: int | None, resize_to: tuple[int, int] | None = None) -> None:
        """ Extracts the icon at a specific index in an icon atlas, resizes it, and places it in a canvas element """
        img = mapper.index_to_image(index, resize_to=resize_to)
        self_img_name = str(canvas)
        setattr(self, self_img_name, ImageTk.PhotoImage(img))
        canvas.delete("all")
        canvas.create_image(0, 0, image=getattr(self, self_img_name), anchor=NW)

    def generate_laptimes_entries(self, frame, amount):
        """ Builds the UI for individual lap times """
        laptime_entries = []
        for i in range(amount):
            ttk.Label(frame, text=f"{i+1}").grid(column=0, row=i, padx=(70, 5))

            lap_min = StringVar()
            min_entry = ttk.Entry(frame, width=1, textvariable=lap_min, font=self.FONT, state=self.EDIT_STATE)
            min_entry.grid(column=1, row=i, pady=2)

            lap_sec = StringVar()
            sec_entry = ttk.Entry(frame, width=2, textvariable=lap_sec, font=self.FONT, state=self.EDIT_STATE)
            sec_entry.grid(column=2, row=i)

            lap_ms = StringVar()
            ms_entry = ttk.Entry(frame, width=3, textvariable=lap_ms, font=self.FONT, state=self.EDIT_STATE)
            ms_entry.grid(column=3, row=i)

            laptime_entries.append({
                'min': (lap_min, min_entry),
                'sec': (lap_sec, sec_entry),
                'ms': (lap_ms, ms_entry),
            })
        return laptime_entries

    def generate_vehicle_entry(self, frame, var, i):
        """ Generates the UI for the three vehicle parts """
        vehicleframe = ttk.LabelFrame(frame)
        vehicleframe.grid(column=5, row=i, sticky=(N, W, E, S), padx=10, pady=1)

        canvas = Canvas(vehicleframe, width=self.VEHICLE_PART_SIZE[0], height=self.VEHICLE_PART_SIZE[1], borderwidth=0, highlightthickness=0)
        canvas.grid(column=0, row=0, sticky=(N,W,E,S), padx=(4, 4))

        tip = Hovertip(canvas, 'PLACEHOLDER', hover_delay=1000)

        vehicle_entry = ttk.Entry(vehicleframe, width=15, textvariable=var, font=self.FONT, state=self.EDIT_STATE)
        vehicle_entry.grid(column=1, row=0, sticky=(W,E), padx=(0, 3))

        return var, canvas, tip

    def resize_window(self):
        """ Resizes the window and moves it to the middle of the screen """
        ws = self.root.winfo_screenwidth() # width of the screen
        hs = self.root.winfo_screenheight() # height of the screen

        # calculate x and y coordinates for the Tk root window
        x = int((ws/2) - (self.WINDOW_WIDTH/2))
        y = int(hs/8)

        self.root.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}+{x}+{y}")
