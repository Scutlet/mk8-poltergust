from abc import ABC, abstractmethod
from dataclasses import dataclass
import io
import json
from tkinter import PhotoImage, Tk
from typing import ClassVar

from PIL import Image, ImageOps
import requests

from poltergust.utils import get_resource_path
from poltergust.widgets.widgets import FramableTrack, MK8TrackFrame


class ModDownloadException(Exception):
    """ Raised when something goes wrong when downloading a mod. """

class MK8ModSite(ABC):
    id: int
    name: str
    domain: str
    icon: Image.Image

    mod_id_url = "%(mod_id)s"

    def __str__(self):
        return self.name

    def __eq__(self, other):
        if isinstance(other, MK8ModSite):
            return self.id == other.id
        return False

    def get_url_for_mod_id(self, mod_id: int) -> str:
        """ TODO """
        return self.mod_id_url % {'mod_id': mod_id}

    @abstractmethod
    def get_api_endpoint(self, identifier: str) -> str:
        """
            Gets the API endpoint to fetch mod data for a mod with a given identifier.
            This identifier can, for example, be the mod_id or a mod's (unique) title
        """

    def clean_json(self, json_res: dict) -> dict:
        """
            Cleans up the json response from the request to the site's API endpoint.
            This cleaned version is passed to the `validate` and `get_foo` methods.
        """
        return json_res

    @abstractmethod
    def validate(self, clean_json: dict) -> None:
        """
            Validates the returned json. Can, for example, check whether a mod is
            for the correct game.
        """

    @abstractmethod
    def get_mod_id(self, identifier: str, clean_json: dict) -> int:
        """ Gets the mod id of the response. """

    @abstractmethod
    def get_mod_name(self, clean_json: dict) -> str:
        """ Gets the mod name of the response. """

    @abstractmethod
    def get_mod_author(self, clean_json: dict) -> str:
        """ Gets the mod's author(s) of the response. """

    @abstractmethod
    def get_mod_preview_image(self, clean_json: dict) -> str:
        """ Gets a preview image of the mod of the response. """

class CTWikiSite(MK8ModSite):
    id = 0
    name = "CT Wiki"
    domain = "https://mk8.tockdom.com/wiki/"
    icon = Image.open(get_resource_path("resources/favicons/favicon_ctwiki.png")).resize(size=(16, 16))

    mod_id_url = "https://mk8.tockdom.com/w/index.php?curid=%(mod_id)s"
    shared_api_endpoint = "https://mk8.tockdom.com/w/api.php?action=query&prop=images|templates|categories&clcategories=Category:Track/Retro|Category:Track/Custom|Category:Track/Edit|Category:Track/Import&tldir=descending&format=json&format=json&%s"

    int_api_endpoint = shared_api_endpoint % "pageids=%(mod_id)s"
    name_api_endpoint = shared_api_endpoint % "titles=%(name)s"

    def get_api_endpoint(self, identifier: str) -> str:
        if identifier.isdigit():
            return self.int_api_endpoint % {'mod_id': identifier}
        return self.name_api_endpoint % {'name': identifier}

    def clean_json(self, json_res: dict) -> dict:
        pages: dict = json_res['query']['pages']

        # Unexpected format
        if len(pages) <= 0:
            raise KeyError("page")

        # Fetch dictionary element (there's only one)
        return next(iter(pages.values()))

    def validate(self, clean_json: dict) -> None:
        # Page doesn't exist (invalid URL)
        if clean_json.get('pageid', -1) < 0:
            raise ModDownloadException("Mod not found. Is the URL correct?")

        # Must have params
        for val in ('title', 'pageid'):
            if val not in clean_json:
                raise ModDownloadException(f"Missing {val} in {self.name} API ({self.domain}). The API might have changed!")

        # Incorrect Category
        #   Must be one of: Track/Retro, Track/Custom, Track/Edit, Track/Import
        if clean_json.get('categories', None) is None:
            raise ModDownloadException("Mod is not a custom track. Please verify it has one of the following categories: Track/Retro, Track/Custom, Track/Edit, Track/Import")

    def get_mod_id(self, identifier: str, clean_json: dict) -> int:
        return clean_json['pageid']

    def mod_has_category(self, category_names: list[str], categories_json: list) -> bool:
        """ Checks whether one of the given categories is present in the category list """
        for category in categories_json:
            if category.get("title", None) in category_names:
                return True
        return False

    def get_mod_name(self, clean_json: dict) -> str:
        title: str = clean_json['title']
        if self.mod_has_category(["Category:Track/Retro", "Category:Track/Edit"], clean_json['categories']):
            # Retro tracks have their author name between brackets
            # Track edits have the original track name between brackets
            return title.rsplit(" (")[0]
        return title

    def get_author_from_user_link_template(self, templates_json: list) -> list[str]:
        """ Fetches the User-XXXX-Link template if it exists """
        authors = []
        # Loop over all templates (there might be multiple authors)
        for template in templates_json:
            title: str = template.get('title')
            # Check template name
            if title.startswith("Template:User-") and title.endswith("-Link"):
                # Extract author
                authors.append(title[len("Template:User-"):-len("-Link")])
        return authors

    def get_mod_author(self, clean_json: dict) -> str:
        # Fetch author from 'User-<author>-Link' template
        if 'templates' in clean_json:
            author = self.get_author_from_user_link_template(clean_json['templates'])
            if author:
                return '& '.join(author)

        # Fallback to page title (if available)
        if self.mod_has_category(["Category:Track/Retro"], clean_json.get('categories', [])):
            # Retro tracks have their author name between brackets
            return clean_json['title'].rsplit(" (")[1][:-1]

        # Could not fetch author
        return None

    def get_mod_preview_image(self, clean_json: dict) -> str:
        image_url = None
        for image_data in clean_json.get('images', []):
            title: str = image_data.get('title', '')
            # Simply select the first image that can be found
            image_url = title
            # Check image name
            if any(substr in title.lower() for substr in ("course image", "course icon", "menu image", "menu icon")):
                # Special override found
                image_url = title
                break

        if image_url is not None:
            # Use special URL to find the url of the image
            return f"{self.domain}Special:FilePath/{image_url[len('File:'):]}"

class GameBananaSite(MK8ModSite):
    id = 1
    name = "GameBanana"
    domain = "https://gamebanana.com/mods/"
    icon = Image.open(get_resource_path("resources/favicons/favicon_gb.png")).resize(size=(16, 16))

    mod_id_url = "https://gamebanana.com/mods/%(mod_id)s"
    api_endpoint = "https://api.gamebanana.com/Core/Item/Data?itemtype=Mod&return_keys=1&format=json_min&itemid=%(mod_id)s&fields=authors,name,Owner().name,Preview().sSubFeedImageUrl(),screenshots,Credits().aAuthors(),Category().name,Withhold().bIsWithheld(),RootCategory().name,Game().name,Trash().bIsTrashed()"

    def get_api_endpoint(self, identifier: str) -> str:
        if identifier.isdigit():
            return self.api_endpoint % {'mod_id': identifier}
        return None

    def validate(self, clean_json: dict) -> None:
        if clean_json.get("error", None):
            raise ModDownloadException("Mod not found. Is the URL correct?")

        # Must have params
        for val in ('name', 'Credits().aAuthors()', 'Owner().name', 'Preview().sSubFeedImageUrl()', 'screenshots', 'Withhold().bIsWithheld()', 'Trash().bIsTrashed()', 'Game().name', 'RootCategory().name', 'Category().name'):
            if val not in clean_json:
                raise ModDownloadException(f"Missing {val} in {self.name} API ({self.domain}). The API might have changed!")

        if clean_json["Withhold().bIsWithheld()"]:
            raise ModDownloadException("Mod is withheld. Please fix the issues highlighed by the GameBanana moderators first.")

        if clean_json["Trash().bIsTrashed()"]:
            raise ModDownloadException("Mod is trashed. Please untrash the mod.")

        if clean_json["Game().name"]  == "Mario Kart 8 Deluxe":
            raise ModDownloadException("Mario Kart 8 Deluxe mods are not supported.")

        if clean_json["Game().name"] not in ("Mario Kart 8",):
            raise ModDownloadException("Mod is not a Mario Kart 8 mod.")

        if clean_json["RootCategory().name"] != "Courses":
            raise ModDownloadException("Mod is not a custom track.")

        if clean_json["Category().name"] not in ("Courses", "Custom Tracks"):
            raise ModDownloadException("Mod cannot be a texture hack or battle course.")

    def get_mod_id(self, identifier: str, clean_json: dict) -> int:
        return int(identifier)

    def get_mod_name(self, clean_json: dict) -> str:
        return clean_json['name']

    def get_mod_author(self, clean_json: dict) -> str:
        # Fetch override from credits list (if available)
        authors = []
        for credit in clean_json['Credits().aAuthors()']:
            if credit[1].lower() in ("original author", "original creator", "created the track", "main author", "main creator"):
                # There might be multiple main authors, so don't quit yet
                authors.append(credit[0])

        if authors:
            return '& '.join(authors)

        # Otherwise just return the uploader
        return clean_json['Owner().name']

    def get_mod_preview_image(self, clean_json: dict) -> str:
        # See if a specific image was marked as a preview
        if 'screenshots' in clean_json:
            screenshots = json.loads(clean_json['screenshots'])
            for screenshot in screenshots:
                if any(substr in screenshot.get('_sCaption', '').lower() for substr in ("course image", "course icon", "menu image", "menu icon")):
                    return "https://images.gamebanana.com/img/ss/mods/" + screenshot["_sFile"]
        return clean_json['Preview().sSubFeedImageUrl()']

MOD_SITES: tuple[MK8ModSite] = (CTWikiSite(), GameBananaSite())

@dataclass
class MK8ModVersion:
    major: int
    minor: int
    patch: int = 0

    def __str__(self):
        return f"v{self.major}.{self.minor}.{self.patch}"

@dataclass
class MK8CustomTrack(FramableTrack):
    """ Dataclass for a Mario Kart 8 Custom Track """
    name: str
    mod_site: MK8ModSite
    mod_id: int

    author: str|None = None
    preview_image: str|None = None

    # Preview Image size
    PREVIEW_SIZE: ClassVar[tuple[int, int]] = (288, 162)

    _sort_field_name = "name"

    def __str__(self):
        return f"[{self.mod_site}] {self.name}"

    def __eq__(self, other):
        if isinstance(other, MK8CustomTrack):
            return self.mod_id == other.mod_id and self.mod_site == other.mod_site
        return False

    def frame(self, master: Tk, *args, **kwargs) -> MK8TrackFrame:
        track_name = self.name
        track_author = self.author or "Unknown Author"

        track_preview = None
        if self.preview_image is not None:
            try:
                track_preview = Image.open(self.preview_image).resize(size=self.TRACK_PREVIEW_SIZE)
            except FileNotFoundError as e:
                pass

        if track_preview is None:
            track_preview = self.mod_site.icon.resize(size=(24, 24))

        url_text = str(self.mod_id)
        url_icon = self.mod_site.icon
        url_link = self.mod_site.get_url_for_mod_id(self.mod_id)
        url_tooltip = f"{self.mod_site} - {url_link}"

        return MK8TrackFrame(master, track_name, track_author, track_preview, url_text, url_icon, url_link, url_tooltip, *args, **kwargs)


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
