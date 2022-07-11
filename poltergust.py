import logging, os, sys
from tkinter import *
from tkinter import messagebox

from dotenv import load_dotenv

from poltergust.controllers.controller import PoltergustController
from poltergust.models.ct_storage import MK8CTStorage
from poltergust.views.main import PoltergustMainView


if __name__ == '__main__':
    # Load environment variables
    load_dotenv(".env")

    # Logging config
    logging_config = {}

    # Log to file
    logfile = os.getenv("LOGFILE", "error.log")
    if logfile:
        logging_config['filename'] = logfile

    # Set other config
    logging.basicConfig(
        encoding='utf-8',
        level=os.getenv("LOGLEVEL", "WARNING"),
        format="[%(levelname)s] <%(asctime)s> %(name)s: %(message)s",
        datefmt='%Y-%m-%d %H:%M:%S',
        **logging_config
    )

    # Pass unhandled exceptions to logger
    def on_unhandled_exception_base(exctype, exc, tb):
        logging.error("An unhandled exception occurred.", exc_info=(exctype, exc, tb))

    # Show messagebox on unhandled exception
    def on_unhandled_exception_messagebox(exctype, exc, tb):
        on_unhandled_exception_base(exctype, exc, tb)
        messagebox.showerror(
            "ERROR: Unhandled Exception occurred!",
            f"Oh no, something went terribly wrong! Please report the issue, and include error.log and (if applicable) the current ghost file.\n\n{exctype.__name__}: {exc}"
        )

    # Show messagebox on error?
    unhandled_exc_hook = on_unhandled_exception_base
    if os.getenv("MESSAGEBOX_ON_ERROR", 1) == 1:
        unhandled_exc_hook = on_unhandled_exception_messagebox

    # Override default stderr
    sys.excepthook = unhandled_exc_hook

    # Override Tkinter stderr
    root = Tk()
    root.report_callback_exception = unhandled_exc_hook

    # Create and display the UI
    view = PoltergustMainView(root)
    db = MK8CTStorage()
    controller = PoltergustController(view, db)

    # Immediately open file if passed in
    if len(sys.argv) == 2:
        # Replace \ by / path separators (for Windows)
        controller.open_ghostfile(sys.argv[1].replace("\\", "/"))

    logging.info("Starting Poltergust")
    root.mainloop()
