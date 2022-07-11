import io
import requests

from PIL import Image, ImageOps

from poltergust.models.mod_models import MK8CustomTrack
from poltergust.models.mod_sites import MOD_SITES, MK8ModSite, ModDownloadException


class PoltergustDownloader:
    """ Connects to the API endpoint of `MOD_SITES` and fetches a mod's information from them. """
    TIMEOUT = 6.05

    def download(self, site_url: str) -> MK8CustomTrack:
        """
            Fetches mod data from a given site_url, raising a ModDownloadException if
            that is not possible.
        """
        site, identifier, api_endpoint = self.get_mod_site_for_url(site_url)
        if api_endpoint is None:
            raise ModDownloadException("Invalid Domain! Mods cannot be downloaded from the given URL. Please check the URL for typos.")

        try:
            print(f"Making request to: {api_endpoint}")
            res = requests.get(api_endpoint, timeout=self.TIMEOUT)
            print("Request done!")
        except requests.ConnectTimeout as e:
            raise ModDownloadException(f"Could not reach {site.name}. The site may be down or you may not have an Internet connection.") from e

        if res.status_code != 200:
            raise ModDownloadException(f"Something went wrong when fetching the mod data from {site.name}: HTTP {res.status_code}. Please try again later.")

        clean_json = site.clean_json(res.json())
        site.validate(clean_json)

        mod = MK8CustomTrack(
            name=site.get_mod_name(clean_json),
            author=site.get_mod_author(clean_json),
            mod_id=site.get_mod_id(identifier, clean_json),
            mod_site=site,
            preview_image=site.get_mod_preview_image(clean_json)
        )
        return mod

    def get_mod_site_for_url(self, site_url: str) -> tuple[MK8ModSite, str, str]:
        """
            Gets a (mod_site, identifier, api_endpoint) triple for a given URL.
            The triple represents a site with a corresponding API endpoint that
            can be used to fetch data from the mod located at the site URL.
            The identifier represents what is injected in the api_endpoint, and is
            extracted from the site URL.
        """
        for site in MOD_SITES:
            if site_url.startswith(site.domain):
                identifier = site_url[len(site.domain):].replace("#", "/").rsplit("/")[0]
                api_endpoint = site.get_api_endpoint(identifier)
                if api_endpoint is not None:
                    return site, identifier, api_endpoint
        return None, None, None

    def download_preview_image(self, preview_url: str, output_path: str) -> None:
        """ Downloads a preview image from a given URL to a given path on the system """
        with requests.get(preview_url, stream=True, timeout=self.TIMEOUT) as res:
            if res.status_code != 200:
                raise ModDownloadException(f"Could not download {preview_url}: HTTP {res.status_code}. Please check your Internet connection.")

            # Check image size (assumes this is actually correct)
            if int(res.headers['content-length']) > 5*1000*1000:
                raise ModDownloadException(f"Image preview size too large: {res.headers['content-length']}. Max size is 50Mb.")

            with io.BytesIO(res.content) as f:
                with Image.open(f) as img:
                    # Resize and crop image to expected size
                    img = ImageOps.fit(img, MK8CustomTrack.PREVIEW_SIZE)
                    # Discard alpha channel (if present)
                    img = img.convert('RGB')
                    img.save(output_path)
