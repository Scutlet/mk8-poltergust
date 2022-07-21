from tkinter import LEFT, Button, PhotoImage, Toplevel, ttk

from poltergust.utils import get_resource_path


class IntEntry(ttk.Entry):
    """ Tkinter entry that only accepts numbers as its input """
    def __init__(self, master: Toplevel, *args, **kwargs):
        super().__init__(master, *args, validate="key", validatecommand=(master.register(self.validate_input), "%P", '%d'), **kwargs)

    def validate_input(self, input: str, acttype: int):
        return acttype != '1' or input.isdigit()


class IconButton(Button):
    """ Button with both text and an icon """
    def __init__(self, master: Toplevel, *args, image_path: str="", compound:str=LEFT, text:str|float="", **kwargs):
        self._img = None
        if image_path:
            self._img = PhotoImage(file=get_resource_path(image_path))
        super().__init__(master, *args, image=self._img, compound=compound, text=f" {text}", **kwargs)

    def set_icon(self, image_path: str) -> None:
        """ Sets the icon of the button """
        self._img = PhotoImage(file=get_resource_path(image_path))
        self.config(image=self._img)
