import os
from tkinter import messagebox
from tkinter.font import NORMAL, BOLD
from idlelib.tooltip import Hovertip
from tkinter import *
from tkinter import ttk, filedialog
import webbrowser

from PIL import Image, ImageTk

from imagemapper import MK8CharacterImageMapper, MK8FlagImageMapper, MK8ImageAtlasMapper, MK8VehiclePartImageMapper, MK8TrackImageMapper
from gamedata import COURSE_IDS, CHARACTERS, KARTS, WHEELS, GLIDERS, FLAGS
from mii_handler import MK8GhostDataMiiHandler
from parser import MK8_GHOST_TYPES, MK8GhostFilenameParser, MK8GhostData
from staff_ghost_converter import MK8StaffGhostConverter



class PoltergustUI:
    """
        Defines and builds the Poltergust UI using Tkinter.
    """
    WINDOW_WIDTH = 550
    WINDOW_HEIGHT = 400

    BTN_RELOAD_FROM_DISK = "Reload from disk"
    BTN_CLOSE = "Close"
    BTN_EXPORT_AS_STAFF_GHOST = "Convert to Staff Ghost"
    BTN_EXTRACT_MII = "Extract Mii"
    BTN_REPLACE_MII = "Replace Mii"

    # FONT = ("Agency FB", 14, NORMAL)
    FONT = ("Courier", 14, NORMAL)

    FLAG_SIZE = (33, 22)
    CHARACTER_SIZE = (64, 64)
    VEHICLE_PART_SIZE = (75, 48)
    TRACK_SIZE = (80, 45)

    # Editing is not yet supported
    EDIT_STATE = "readonly"

    # Window Icon
    WINDOW_ICON = "resources/scutlet_static_cropped.png"

    def __init__(self, root: Tk):
        """ Initializes the UI """
        self.ghostfile: str | None = None
        self.data: MK8GhostData | None = None

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
        self.menubar.add_cascade(menu=self.menu_help, label='Help')

        # File options
        self.menu_file.add_command(label='Open...', command=self.open_ghost_file)
        self.menu_file.add_command(label=self.BTN_RELOAD_FROM_DISK, command=self.update)
        self.menu_file.add_command(label=self.BTN_CLOSE, command=self.close_current_file)

        # Export options
        self.menu_export.add_command(label=self.BTN_EXPORT_AS_STAFF_GHOST, command=self.export_as_staff)
        self.menu_export.add_command(label=self.BTN_EXTRACT_MII, command=self.extract_mii)

        # Edit options
        self.menu_edit.add_command(label=self.BTN_REPLACE_MII, command=self.replace_mii)

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
        self.character_canvas = Canvas(summaryframe, width=self.CHARACTER_SIZE[0], height=self.CHARACTER_SIZE[1])
        self.character_canvas.grid(column=0, row=0, rowspan=2, sticky=(N,W,E,S))
        self.character_tip = Hovertip(self.character_canvas, 'PLACEHOLDER', hover_delay=1000)

        # Name
        self.playername = StringVar()
        playername_entry = ttk.Entry(summaryframe, width=16, textvariable=self.playername, font=self.FONT, state=self.EDIT_STATE)
        playername_entry.grid(column=1, row=0, columnspan=4, sticky=(W,E), padx=(0, 3))

        # Flag
        self.flag_canvas = Canvas(summaryframe, width=self.FLAG_SIZE[0], height=self.FLAG_SIZE[1])
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
        self.track_canvas = Canvas(trackframe, width=self.TRACK_SIZE[0], height=self.TRACK_SIZE[1])
        self.track_canvas.grid(column=0, row=0, sticky=(N,W,E,S), pady=(7, 10))
        self.track_tip = Hovertip(self.track_canvas, 'PLACEHOLDER', hover_delay=1000)

        self.track = StringVar()
        track_entry = ttk.Entry(trackframe, width=25, textvariable=self.track, font=(self.FONT[0], 9, self.FONT[2]), state=self.EDIT_STATE)
        track_entry.grid(column=1, row=0, sticky=(W,E), padx=(0, 3))

        # Lap Times frame (contains all lap times)
        laptimesframe = ttk.LabelFrame(self.dataframe)
        laptimesframe.grid(column=0, row=2, sticky=(N, W, E, S), padx=(0, 3))

        # Lap Times
        self.lap_times = self.generate_laptimes_entries(laptimesframe, 7)

        # Vehicle frame
        vehicleframe = ttk.LabelFrame(self.dataframe)
        vehicleframe.grid(column=1, row=2, sticky=(N, W, E, S))

        # Vehicle Combination
        self.kart, self.kart_canvas, self.kart_tip = self.generate_vehicle_entry(vehicleframe, StringVar(), 1)
        self.wheels, self.wheels_canvas, self.wheels_tip = self.generate_vehicle_entry(vehicleframe, StringVar(), 2)
        self.glider, self.glider_canvas, self.glider_tip = self.generate_vehicle_entry(vehicleframe, StringVar(), 3)

        # for child in summaryframe.winfo_children():
        #     child.grid_configure(padx=5, pady=5)

        playername_entry.focus()
        # root.bind("<Return>", self.calculate)
        self.resize_window()
        self.update()

    def popup_about(self):
        """ Displays 'about' information """
        win = Toplevel(self.root)
        win.wm_title("Poltergust - About")

        with Image.open("resources/scutlet.png") as img:
            scutlet_canvas = Canvas(win, width=128, height=128)
            scutlet_canvas.grid(column=0, row=0, sticky=(N,W,E,S))
            self.scutlet_img = ImageTk.PhotoImage(img.resize((128, 128)))
            scutlet_canvas.create_image(0, 0, image=self.scutlet_img, anchor=NW)

        ttk.Label(win, text="Developed by Scutlet").grid(column=1, row=0)
        ttk.Label(win, text="This software is available under GPL v3").grid(column=0, row=1, columnspan=2)

        ws = self.root.winfo_screenwidth() # width of the screen
        hs = self.root.winfo_screenheight() # height of the screen

        # calculate x and y coordinates for the Tk root window
        x = int((ws/2) - (275/2))
        y = int(hs/7)

        win.geometry(f"275x150+{x}+{y}")

        win.wait_visibility()
        win.grab_set()

    def popup_success(self, title: str, message: str) -> None:
        """ Displays 'export success' message """
        win = Toplevel(self.root)
        win.wm_title(title)

        ttk.Label(win, text=message, wraplength=275).grid(row=0, column=0)

        ttk.Button(win, text="Ok", command=win.destroy).grid(row=1, column=0, pady=(20, 0))

        ws = self.root.winfo_screenwidth() # width of the screen
        hs = self.root.winfo_screenheight() # height of the screen

        # calculate x and y coordinates for the Tk root window
        x = int((ws/2) - (275/2))
        y = int(hs/7)

        win.geometry(f"275x150+{x}+{y}")

    def extract_mii(self):
        """ Invokes the Mii handler and extracts the Mii from the currently loaded ghost file """
        filename = filedialog.asksaveasfilename(
            parent=self.root,
            title=self.BTN_EXTRACT_MII,
            defaultextension=".3dsmii",
            filetypes=(("Wii U/3DS Mii (.3dsmii)", ".3dsmii"), ('All files', '*.*')),
            initialfile=f"mii-{self.data.playername}",
        )

        handler = MK8GhostDataMiiHandler(self.ghostfile, self.data.ghost_type == MK8_GHOST_TYPES.STAFF_GHOST)

        try:
            handler.extract(filename)
        except Exception as e:
            print(e)
            messagebox.showerror("Invalid Mii Data", "This ghost file contained invalid Mii data; it could not be extracted.")
            return

        messagebox.showinfo("Mii extracted!", f"The Mii for this ghost file was extracted successfully to {filename}")

    def replace_mii(self):
        """ Invokes the Mii handler and replaces the Mii from the currently loaded ghost file """
        assert self.ghostfile is not None

        new_mii = filedialog.askopenfilename(
            parent=self.root,
            title="Select new Mii",
            defaultextension=".3dsmii",
            filetypes=(("Wii U/3DS Mii (.3dsmii)", ".3dsmii"), ('All files', '*.*')),
        )

        handler = MK8GhostDataMiiHandler(self.ghostfile, self.data.ghost_type == MK8_GHOST_TYPES.STAFF_GHOST)

        try:
            handler.replace(new_mii)
        except Exception as e:
            print(e)
            messagebox.showerror("Invalid Mii Data", "This Mii file contained invalid Mii data; it could not be injected.")
            return

        # Generate new filename
        mii_name = handler.extract_mii_name()
        self.data.playername = mii_name
        new_name = MK8GhostFilenameParser.serialize_filename(self.data)

        # Rename file
        current_folder = self.ghostfile.rpartition("/")[0]
        new_file = current_folder + "/" + new_name
        os.rename(self.ghostfile, new_file)

        self.ghostfile = new_file
        self.playername.set(self.data.playername)

        messagebox.showinfo("Mii replaced!", f"The Mii for this ghost file was successfully replaced!")

    def export_as_staff(self):
        """ Exports the currently loaded ghostfile as a staff ghost """
        assert self.ghostfile is not None
        converter = MK8StaffGhostConverter(self.ghostfile)
        foldername = filedialog.askdirectory(
            parent=self.root,
            title="Output directory for MK8 Staff Ghost",
        )
        output_file = os.path.join(foldername, MK8_GHOST_TYPES.STAFF_GHOST.value + self.ghostfile.rpartition("/")[2][2:])
        res = converter.convert(output_file)
        if res:
            messagebox.showinfo("Staff Ghost Exported", f"Staff Ghost data was exported successfully! It can be found under {output_file}")

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

        canvas = Canvas(vehicleframe, width=self.VEHICLE_PART_SIZE[0], height=self.VEHICLE_PART_SIZE[1])
        canvas.grid(column=0, row=0, sticky=(N,W,E,S))

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

    def update(self):
        """ Updates the UI contents based on the loaded ghostfile """
        if self.ghostfile:
            # Enable buttons if a file is open
            self.menu_file.entryconfig(self.BTN_CLOSE, state=NORMAL)
            self.menu_file.entryconfig(self.BTN_RELOAD_FROM_DISK, state=NORMAL)
            self.menu_export.entryconfig(self.BTN_EXPORT_AS_STAFF_GHOST, state=NORMAL)
            self.menu_export.entryconfig(self.BTN_EXTRACT_MII, state=NORMAL)
            self.menu_edit.entryconfig(self.BTN_REPLACE_MII, state=NORMAL)

            # Name of opened file
            file_str = "Loaded File: " + self.ghostfile.rpartition("/")[2][:40]
            if len(self.ghostfile) > 40:
                file_str += "..."

            self.lb_ghostfile.config(text=file_str)

            # Parse file
            self.parse_file(self.ghostfile)

            # Update ghostinfos
            self.game_version.config(text=f"Game version {self.data.game_version}")
            if self.data.ghost_type == MK8_GHOST_TYPES.STAFF_GHOST:
                self.ghost_type.config(text="Staff Ghost")
                # No need to export a staff ghost
                self.menu_export.entryconfig(self.BTN_EXPORT_AS_STAFF_GHOST, state=DISABLED)
            elif self.data.ghost_type == MK8_GHOST_TYPES.PLAYER_GHOST:
                self.ghost_type.config(text="Player Ghost")
            elif self.data.ghost_type == MK8_GHOST_TYPES.DOWNLOADED_GHOST:
                self.ghost_type.config(text=f"Downloaded Ghost (Slot {self.data.ghost_number})")
            else:
                self.ghost_type.config(text="MKTV Replay")

            # Update Images
            self.update_flag()
            self.update_character()
            self.update_vehicle_parts()
            self.update_track()

            # Update text
            self.playername.set(self.data.playername)
            self.total_min.set(self.data.total_minutes)
            self.total_sec.set(f"{self.data.total_seconds:02d}")
            self.total_ms.set(f"{self.data.total_ms:03d}")

            for i, lap in enumerate(self.lap_times):
                lap_mins = getattr(self.data, f'lap{i+1}_minutes')
                if lap_mins is not None:
                    lap['min'][0].set(lap_mins)
                    lap['sec'][0].set(f"{getattr(self.data, f'lap{i+1}_seconds'):02d}")
                    lap['ms'][0].set(f"{getattr(self.data, f'lap{i+1}_ms'):03d}")
                else:
                    lap['min'][0].set("9")
                    lap['sec'][0].set("59")
                    lap['ms'][0].set("999")

            # Show Preview
            self.dataframe.grid()
        else:
            # Discard data
            self.data = None

            # Disable buttons if no file is open
            self.menu_file.entryconfig(self.BTN_CLOSE, state=DISABLED)
            self.menu_file.entryconfig(self.BTN_RELOAD_FROM_DISK, state=DISABLED)
            self.menu_export.entryconfig(self.BTN_EXPORT_AS_STAFF_GHOST, state=DISABLED)
            self.menu_export.entryconfig(self.BTN_EXTRACT_MII, state=DISABLED)
            self.menu_edit.entryconfig(self.BTN_REPLACE_MII, state=DISABLED)
            self.lb_ghostfile.config(text="No ghost data loaded")

            # Remove Preview
            self.dataframe.grid_remove()

    def parse_file(self, filepath: str):
        """ Invokes a parser to read ghost data from a ghost's filename """
        filename = filepath.rpartition("/")[2].rpartition(".")[0]
        self.data = MK8GhostFilenameParser(filename).parse()

    def update_flag(self):
        """ Updates the player flag in the UI based on the loaded ghostfile """
        assert self.data is not None

        flag = ("Unknown Flag", None)
        if 0 <= self.data.flag_id < len(FLAGS):
            flag = FLAGS[self.data.flag_id]
            if flag[0] is None:
                flag = ("No Flag", None)

        self.set_mapped_image(self.flag_canvas, MK8FlagImageMapper, flag[1], resize_to=self.FLAG_SIZE)
        self.flag_tip.text = flag[0] + f" ({self.data.flag_id})"

    def update_character(self) -> None:
        """ Updates the character in the UI based on the loaded ghostfile """
        assert self.data is not None

        char = CHARACTERS.get(self.data.character_id, (f"Unknown Character", None))
        if type(char[1]) != int and char[1] is not None:
            # We have subcharacters (E.g. Blue Yoshi, BoTW Link, Mii)
            indx = self.data.character_variant_id
            variant = char[1][indx] if 0 <= indx and indx < len(char[1]) else ("Unknown Variant", None)
            if char[0] == "Mii":
                # We also have a weight class
                indx = self.data.mii_weight_class_id
                variant[0] += F" - {MII_WEIGHT_CLASSES[indx] if 0 <= indx and indx < len(MII_WEIGHT_CLASSES) else 'Unknown Weight Class'}"
            char = (f"{char[0]} ({variant[0]})", variant[1])

        self.set_mapped_image(self.character_canvas, MK8CharacterImageMapper, char[1], resize_to=self.CHARACTER_SIZE)
        self.character_tip.text = f"{char[0]} ({self.data.character_id})"

    def update_track(self) -> None:
        """ Updates the track in the UI based on the loaded ghostfile """
        assert self.data is not None

        track = COURSE_IDS.get(self.data.track_id, ("Unknown Track", None))

        if self.data.ghost_type != MK8_GHOST_TYPES.DOWNLOADED_GHOST and self.data.track_id - 16 != self.data.ghost_number:
            # Track ID - 16 matches ghost number, but only for non-download ghosts
            track = ("Unknown Track", None)

        self.set_mapped_image(self.track_canvas, MK8TrackImageMapper, track[1], resize_to=self.TRACK_SIZE)
        self.track.set(track[0])
        self.track_tip.text = f"{self.data.ghost_number} - {self.data.track_id}"

    def update_vehicle_parts(self) -> None:
        """ Updates the vehicle parts in the UI based on the loaded ghostfile """
        assert self.data is not None

        # Kart
        kart = KARTS.get(self.data.kart_id, ("Unknown Kart", None))
        self.set_mapped_image(self.kart_canvas, MK8VehiclePartImageMapper, kart[1], resize_to=self.VEHICLE_PART_SIZE)
        self.kart.set(kart[0])
        self.kart_tip.text = str(self.data.kart_id)

        # Wheels
        wheels = WHEELS.get(self.data.wheels_id, ("Unknown Wheels", None))
        self.set_mapped_image(self.wheels_canvas, MK8VehiclePartImageMapper, wheels[1], resize_to=self.VEHICLE_PART_SIZE)
        self.wheels.set(wheels[0])
        self.wheels_tip.text = str(self.data.wheels_id)

        # Glider
        glider = GLIDERS.get(self.data.glider_id, ("Unknown Glider", None))
        self.set_mapped_image(self.glider_canvas, MK8VehiclePartImageMapper, glider[1], resize_to=self.VEHICLE_PART_SIZE)
        self.glider.set(glider[0])
        self.glider_tip.text = str(self.data.glider_id)

    def set_mapped_image(self, canvas: Canvas, mapper: MK8ImageAtlasMapper, index: int | None, resize_to: tuple[int, int] | None = None) -> None:
        """ Extracts the icon at a specific index in an icon atlas, resizes it, and places it in a canvas element """
        img = mapper.index_to_image(index, resize_to=resize_to)
        self_img_name = str(canvas)
        setattr(self, self_img_name, ImageTk.PhotoImage(img))
        canvas.create_image(0, 0, image=getattr(self, self_img_name), anchor=NW)

    def open_ghost_file(self):
        """ UI Popup for opening a ghost file """
        filename = filedialog.askopenfilename(
            parent=self.root,
            title="Open MK8 Ghost Data",
            filetypes=(("MK8 Ghost Data (*.dat)", ".dat"), ('All files', '*.*'))
        )
        if not filename:
            # Selection aborted; nothing to do
            return

        self.ghostfile = filename
        self.update()

    def close_current_file(self):
        """ Closes the currently opened ghostfile and cleans up left-behind data """
        self.ghostfile = None
        self.data = None
        self.update()


if __name__ == '__main__':
    # Create and display the UI
    root = Tk()
    PoltergustUI(root)
    root.mainloop()
