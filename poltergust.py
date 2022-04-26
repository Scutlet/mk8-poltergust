from tkinter import *
from tkinter import ttk, filedialog

class PoltergustUI:
    window_width = 500
    window_height = 400

    BTN_RELOAD_FROM_DISK = "Reload from disk"
    BTN_CLOSE = "Close"

    def __init__(self, root: Tk):
        self.ghostfile: str | None = None

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
        self.character = StringVar()
        character_entry = ttk.Entry(summaryframe, width=7, textvariable=self.character)
        character_entry.grid(column=0, row=0, rowspan=2, sticky=(N,W,E,S))

        # Name
        self.playername = StringVar()
        playername_entry = ttk.Entry(summaryframe, width=7, textvariable=self.playername)
        playername_entry.grid(column=1, row=0, columnspan=4, sticky=(W,E))

        # Flag
        self.flag = StringVar()
        flag_entry = ttk.Entry(summaryframe, width=7, textvariable=self.flag)
        flag_entry.grid(column=1, row=1, sticky=(W,E))

        # Total Time
        self.total_min = IntVar()
        total_min_entry = ttk.Entry(summaryframe, width=7, textvariable=self.total_min)
        total_min_entry.grid(column=2, row=1, sticky=(W,E))

        self.total_sec = IntVar()
        total_sec_entry = ttk.Entry(summaryframe, width=7, textvariable=self.total_sec)
        total_sec_entry.grid(column=3, row=1, sticky=(W,E))

        self.total_ms = IntVar()
        total_ms_entry = ttk.Entry(summaryframe, width=7, textvariable=self.total_ms)
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
        self.kart = self.generate_vehicle_entry(detailframe, StringVar(), 1)
        self.wheels = self.generate_vehicle_entry(detailframe, StringVar(), 2)
        self.glider = self.generate_vehicle_entry(detailframe, StringVar(), 3)



        for child in summaryframe.winfo_children():
            child.grid_configure(padx=5, pady=5)



        playername_entry.focus()
        # root.bind("<Return>", self.calculate)
        self.resize()
        self.update()

    def generate_laptimes_entries(self, frame, amount):
        laptime_entries = []
        for i in range(amount):
            ttk.Label(frame, text=f"{i+1}").grid(column=0, row=i, sticky=(N, W, E, S))

            lap_min = IntVar()
            min_entry = ttk.Entry(frame, width=7, textvariable=lap_min)
            min_entry.grid(column=1, row=i, sticky=(W,E))

            lap_sec = IntVar()
            sec_entry = ttk.Entry(frame, width=7, textvariable=lap_sec)
            sec_entry.grid(column=2, row=i, sticky=(W,E))

            lap_ms = IntVar()
            ms_entry = ttk.Entry(frame, width=7, textvariable=lap_ms)
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

        ttk.Label(vehicleframe, text="Image").grid(column=0, row=0, sticky=(N, W, E, S))

        vehicle_entry = ttk.Entry(vehicleframe, width=7, textvariable=var)
        vehicle_entry.grid(column=1, row=0, sticky=(W,E))

        return var

    def resize(self):
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

            # Show Preview
            self.dataframe.grid()
        else:
            # Disable buttons if no file is open
            self.menu_file.entryconfig(self.BTN_CLOSE, state=DISABLED)
            self.menu_file.entryconfig(self.BTN_RELOAD_FROM_DISK, state=DISABLED)
            self.lb_ghostfile.config(text="No ghost data loaded")

            # Remove Preview
            # self.dataframe.grid_remove()

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
