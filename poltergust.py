from tkinter.font import NORMAL, BOLD
from idlelib.tooltip import Hovertip
from tkinter import *
from tkinter import ttk, filedialog

from PIL import Image, ImageTk

from imagemapper import MK8CharacterImageMapper, MK8FlagImageMapper, MK8ImageAtlasMapper, MK8VehiclePartImageMapper
from gamedata import COURSE_NUMBERS, COURSE_IDS, CHARACTERS, KARTS, WHEELS, GLIDERS, FLAGS
from parser import MK8GhostFilenameParser, MK8GhostData



class PoltergustUI:
    window_width = 500
    window_height = 400

    BTN_RELOAD_FROM_DISK = "Reload from disk"
    BTN_CLOSE = "Close"

    # FONT = ("Agency FB", 14, NORMAL)
    FONT = ("Courier", 14, NORMAL)

    FLAG_SIZE = (33, 22)
    CHARACTER_SIZE = (64, 64)
    VEHICLE_PART_SIZE = (100, 64)

    # Editing is not yet supported
    EDIT_STATE = "readonly"

    def __init__(self, root: Tk):
        self.ghostfile: str | None = None
        self.data: MK8GhostData | None = None

        self.root = root
        root.option_add('*tearOff', FALSE)
        root.title("Poltergust - Mario Kart 8 Ghost Data Tool")
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        # Create main frame (needed to have a consistent background across platforms and themes)
        mainframe = ttk.Frame(root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

        # Create a menubar
        self.menubar = Menu(root)
        root['menu'] = self.menubar

        self.menu_file = Menu(self.menubar)
        self.menu_edit = Menu(self.menubar)
        self.menubar.add_cascade(menu=self.menu_file, label='File')
        self.menubar.add_cascade(menu=self.menu_edit, label='Edit')

        self.menu_file.add_command(label='Open...', command=self.open_ghost_file)
        self.menu_file.add_command(label=self.BTN_RELOAD_FROM_DISK, command=self.update)
        self.menu_file.add_command(label=self.BTN_CLOSE, command=self.close_current_file)

        # Loaded file
        self.lb_ghostfile = ttk.Label(mainframe, text="")
        self.lb_ghostfile.grid(column=0, row=0, sticky=(N, W, E, S))

        # Configure data frame
        self.dataframe = ttk.Frame(mainframe)
        self.dataframe.grid(column=0, row=1, sticky=(N, W, E, S))

        # Summary frame (contains character, name, flag, total time)
        summaryframe = ttk.LabelFrame(self.dataframe)
        summaryframe.grid(column=0, row=0, sticky=(N, W, E, S))

        # Character
        self.character_canvas = Canvas(summaryframe, width=self.CHARACTER_SIZE[0], height=self.CHARACTER_SIZE[1])
        self.character_canvas.grid(column=0, row=0, rowspan=2, sticky=(N,W,E,S))
        self.character_tip = Hovertip(self.character_canvas, 'PLACEHOLDER', hover_delay=1000)

        # Name
        self.playername = StringVar()
        playername_entry = ttk.Entry(summaryframe, width=16, textvariable=self.playername, font=self.FONT, state=self.EDIT_STATE)
        playername_entry.grid(column=1, row=0, columnspan=4, sticky=(W,E))

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
        total_ms_entry.grid(column=4, row=1, sticky=(W,E))

        # Detailframe (contains vehicle selections and lap times)
        detailframe = ttk.LabelFrame(self.dataframe)
        detailframe.grid(column=0, row=1, sticky=(N, W, E, S))

        # Lap Times frame (contains all lap times)
        laptimesframe = ttk.LabelFrame(detailframe)
        laptimesframe.grid(column=0, row=0, sticky=(N, W, E, S))

        # Lap Times
        self.lap_times = self.generate_laptimes_entries(laptimesframe, 7)

        # Vehicle Combination
        self.kart, self.kart_canvas = self.generate_vehicle_entry(detailframe, StringVar(), 1)
        self.wheels, self.wheels_canvas = self.generate_vehicle_entry(detailframe, StringVar(), 2)
        self.glider, self.glider_canvas = self.generate_vehicle_entry(detailframe, StringVar(), 3)

        # for child in summaryframe.winfo_children():
        #     child.grid_configure(padx=5, pady=5)

        playername_entry.focus()
        # root.bind("<Return>", self.calculate)
        self.resize_window()
        self.update()

    def generate_laptimes_entries(self, frame, amount):
        laptime_entries = []
        for i in range(amount):
            ttk.Label(frame, text=f"{i+1}").grid(column=0, row=i, sticky=(N, W, E, S))

            lap_min = StringVar()
            min_entry = ttk.Entry(frame, width=1, textvariable=lap_min, font=self.FONT, state=self.EDIT_STATE)
            min_entry.grid(column=1, row=i, sticky=(W,E))

            lap_sec = StringVar()
            sec_entry = ttk.Entry(frame, width=2, textvariable=lap_sec, font=self.FONT, state=self.EDIT_STATE)
            sec_entry.grid(column=2, row=i, sticky=(W,E))

            lap_ms = StringVar()
            ms_entry = ttk.Entry(frame, width=3, textvariable=lap_ms, font=self.FONT, state=self.EDIT_STATE)
            ms_entry.grid(column=3, row=i, sticky=(W,E))

            laptime_entries.append({
                'min': (lap_min, min_entry),
                'sec': (lap_sec, sec_entry),
                'ms': (lap_ms, ms_entry),
            })
        return laptime_entries

    def generate_vehicle_entry(self, frame, var, i):
        vehicleframe = ttk.LabelFrame(frame)
        vehicleframe.grid(column=0, row=i, sticky=(N, W, E, S))

        canvas = Canvas(vehicleframe, width=self.VEHICLE_PART_SIZE[0], height=self.VEHICLE_PART_SIZE[1])
        canvas.grid(column=0, row=0, sticky=(N,W,E,S))

        vehicle_entry = ttk.Entry(vehicleframe, width=7, textvariable=var, font=self.FONT, state=self.EDIT_STATE)
        vehicle_entry.grid(column=1, row=0, sticky=(W,E))

        return var, canvas

    def resize_window(self):
        """ Resizes the window and moves it to the middle of the screen """
        ws = self.root.winfo_screenwidth() # width of the screen
        hs = self.root.winfo_screenheight() # height of the screen

        # calculate x and y coordinates for the Tk root window
        x = int((ws/2) - (self.window_width/2))
        y = int(hs/8)

        self.root.geometry(f"{self.window_width}x{self.window_height}+{x}+{y}")

    def update(self):
        if self.ghostfile:
            # Enable buttons if a file is open
            self.menu_file.entryconfig(self.BTN_CLOSE, state=NORMAL)
            self.menu_file.entryconfig(self.BTN_RELOAD_FROM_DISK, state=NORMAL)

            # Name of opened file
            file_str = "Loaded File: " + self.ghostfile.rpartition("/")[2][:40]
            if len(self.ghostfile) > 40:
                file_str += "..."

            self.lb_ghostfile.config(text=file_str)

            # Parse file
            self.parse_file(self.ghostfile)

            # Update Images
            self.update_flag()
            self.update_character()
            self.update_vehicle_parts()

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
                    lap['min'][0].set("1")
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
            self.lb_ghostfile.config(text="No ghost data loaded")

            # Remove Preview
            self.dataframe.grid_remove()

    def parse_file(self, filepath: str):
        filename = filepath.rpartition("/")[2].rpartition(".")[0]
        self.data = MK8GhostFilenameParser(filename).parse()

    def update_flag(self):
        assert self.data is not None

        flag = ("Unknown Flag", None)
        if 0 <= self.data.flag_id < len(FLAGS):
            flag = FLAGS[self.data.flag_id]

        self.set_mapped_image(self.flag_canvas, MK8FlagImageMapper, flag[1], resize_to=self.FLAG_SIZE)
        self.flag_tip.text = flag[0]

    def update_character(self) -> None:
        assert self.data is not None

        char = CHARACTERS.get(self.data.character_id, ("Unknown Character", None))
        self.set_mapped_image(self.character_canvas, MK8CharacterImageMapper, char[1], resize_to=self.CHARACTER_SIZE)
        self.character_tip.text = char[0]

    def update_vehicle_parts(self) -> None:
        assert self.data is not None

        # Kart
        kart = KARTS.get(self.data.kart_id, ("Unknown Kart", None))
        self.set_mapped_image(self.kart_canvas, MK8VehiclePartImageMapper, kart[1], resize_to=self.VEHICLE_PART_SIZE)
        self.kart.set(kart[0])

        # Wheels
        wheels = WHEELS.get(self.data.wheels_id, ("Unknown Wheels", None))
        self.set_mapped_image(self.wheels_canvas, MK8VehiclePartImageMapper, wheels[1], resize_to=self.VEHICLE_PART_SIZE)
        self.wheels.set(wheels[0])

        # Glider
        glider = GLIDERS.get(self.data.glider_id, ("Unknown Glider", None))
        self.set_mapped_image(self.glider_canvas, MK8VehiclePartImageMapper, glider[1], resize_to=self.VEHICLE_PART_SIZE)
        self.glider.set(glider[0])

    def set_mapped_image(self, canvas: Canvas, mapper: MK8ImageAtlasMapper, index: int | None, resize_to: tuple[int, int] | None = None) -> None:
        img = mapper.index_to_image(index, resize_to=resize_to)
        self_img_name = str(canvas)
        setattr(self, self_img_name, ImageTk.PhotoImage(img))
        canvas.create_image(0, 0, image=getattr(self, self_img_name), anchor=NW)

    def open_ghost_file(self):
        filename = filedialog.askopenfilename(
            title="Open MK8 Ghost Data",
            filetypes=(("MK8 Ghost Data (*.dat)", ".dat"), ('All files', '*.*'))
        )
        if not filename:
            # Selection aborted; nothing to do
            return

        self.ghostfile = filename
        self.update()

    def close_current_file(self):
        self.ghostfile = None
        self.update()

if __name__ == '__main__':
    # Create and display the UI
    root = Tk()
    PoltergustUI(root)
    root.mainloop()
