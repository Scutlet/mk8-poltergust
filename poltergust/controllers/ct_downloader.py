import logging
from tkinter import Event, messagebox
from poltergust.models.ct_storage import MK8CTStorage
from poltergust.models.mod_models import MK8CustomTrack
from poltergust.models.mod_sites import ModDownloadException
from poltergust.parsers.downloader import PoltergustDownloader
from poltergust.utils import Observable

from poltergust.views.ct_add_view import PoltergustAddCTView


class CTDownloaderController(Observable[MK8CustomTrack]):
    """ Controller responsible for handling the CT info downloader view """

    def __init__(self, view: PoltergustAddCTView) -> None:
        super().__init__()

        self._view = view
        self._view.fetch_button.config(command=self.on_download_button_click)

        self._db = MK8CTStorage()
        self._downloader = PoltergustDownloader()

    def on_download_button_click(self, e: Event|None=None) -> None:
        """ Fetches the info from the url input by the user """
        try:
            mod = self.download_ct_infos(self._view.ct_url.get())
            self.notify_listeners(mod)
            messagebox.showinfo("Download Complete!", f"Mod information was downloaded successfully!\nName: {mod.name}\nAuthor(s): {mod.author}\nSite: {mod.mod_site}", parent=self._view)
        except ModDownloadException as e:
            logging.error(e)
            messagebox.showerror("Download Error!", str(e), parent=self._view)

    def download_ct_infos(self, url: str) -> MK8CustomTrack:
        """
            Downloads info for a mod located at a given URL.
            :raise: ModDownloadException if the download could not be completed
        """
        mod = self._downloader.download_from_url(url)
        if mod.preview_image is not None:
            # Download image
            preview_path = self._db.MOD_PREVIEW_PATH % {'mod_id': mod.mod_id, 'mod_site_id': mod.mod_site.id}
            self._downloader.download_preview_image(mod.preview_image, preview_path)
            mod.preview_image = preview_path

        # Add downloaded info to the db
        self._db.add_or_update_mod(mod)
        self._db.commit()
        return mod
