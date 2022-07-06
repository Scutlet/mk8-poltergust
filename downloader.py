from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import io
from itertools import count
from typing import ClassVar

from PIL import Image, ImageOps
import requests


class ModDownloadException(Exception):
    """ TODO """

class MK8ModSite(ABC):
    id: int
    name: str
    domain: str
    icon: Image.Image|None = None

    def __str__(self):
        return self.name

    @abstractmethod
    def get_api_endpoint(self, identifier: str) -> str:
        """ TODO """

    def clean_json(self, json_res: dict) -> dict:
        """ TODO """
        return json_res

    @abstractmethod
    def validate(self, clean_json: dict) -> None:
        """ TODO """

    @abstractmethod
    def get_mod_id(self, identifier: str, clean_json: dict) -> int:
        """ TODO """

    @abstractmethod
    def get_mod_name(self, clean_json: dict) -> str:
        """ TODO """

    @abstractmethod
    def get_mod_author(self, clean_json: dict) -> str:
        """ TODO """

    @abstractmethod
    def get_mod_preview_image(self, clean_json: dict) -> str:
        """ TODO """

class CTWikiSite(MK8ModSite):
    id = 0
    name = "CT Wiki"
    domain = "https://mk8.tockdom.com/wiki/"

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
        # Must have title
        clean_json['title']

        # Page doesn't exist (invalid URL)
        if clean_json['pageid'] < 0:
            raise ModDownloadException("Mod not found. Is the URL correct?")

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
            if "course image" in title.lower():
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

    api_endpoint = "https://api.gamebanana.com/Core/Item/Data?itemtype=Mod&return_keys=1&format=json_min&itemid=%(mod_id)s&fields=authors,creator,date,description,name,Owner().name,Preview().sSubFeedImageUrl(),screenshots,Credits().ssvAuthorNames(),Credits().aAuthors(),catid,Category().name,Withhold().bIsWithheld(),RootCategory().name,RootCategory().id,is_obsolete,Game().name,Trash().bIsTrashed()"

    def get_api_endpoint(self, identifier: str) -> str:
        if identifier.isdigit():
            return self.api_endpoint % {'mod_id': identifier}
        return None

    def validate(self, clean_json: dict) -> None:
        if clean_json.get("error", None):
            raise ModDownloadException("Mod not found. Is the URL correct?")

        # Must have params
        clean_json['name']
        clean_json['Credits().aAuthors()']
        clean_json['Owner().name']
        clean_json['Preview().sSubFeedImageUrl()']
        clean_json['screenshots']
        clean_json['name']

        if clean_json.get("Withhold().bIsWithheld()", True):
            raise ModDownloadException("Mod is withheld. Please fix the issues highlighed by the GameBanana moderators first.")

        if clean_json.get("Trash().bIsTrashed()", True):
            raise ModDownloadException("Mod is trashed. Please untrash the mod.")

        if clean_json.get("Game().name", None)  == "Mario Kart 8 Deluxe":
            raise ModDownloadException("Mario Kart 8 Deluxe mods are not supported.")

        if clean_json.get("Game().name", None) not in ("Mario Kart 8",):
            raise ModDownloadException("Mod is not a Mario Kart 8 mod.")

        if clean_json.get("RootCategory().name", None) != "Courses":
            raise ModDownloadException("Mod is not a custom track.")

        if clean_json.get("Category().name", None) not in ("Courses", "Custom Tracks"):
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
class MK8CustomTrack:
    """ TODO """
    name: str
    mod_site: MK8ModSite
    mod_id: int

    author: str|None = None
    preview_image: str|None = None

    # Preview Image size
    PREVIEW_SIZE: ClassVar[tuple[int, int]] = (288, 162)

    def __str__(self):
        return f"[{self.mod_site}] {self.name}"



class PoltergustDownloader:
    """ TODO """

    def download(self, site_url: str) -> MK8CustomTrack:
        """ TODO """
        site, identifier, api_endpoint = self.get_api_endpoint(site_url)
        if api_endpoint is None:
            raise ModDownloadException("Invalid Domain! Mods cannot be downloaded from the given website. Please check the URL for typos.")
        print(api_endpoint)
        print("start fetching!")

        res = requests.get(api_endpoint)
        if res.status_code != 200:
            raise ModDownloadException(f"Could not reach {site.name}. The site may be down or you may not have an Internet connection.")

        try:
            clean_json = site.clean_json(res.json())
            site.validate(clean_json)

            print(site.get_mod_id(identifier, clean_json))
            print(site.get_mod_name(clean_json))
            print(site.get_mod_author(clean_json))
            print(site.get_mod_preview_image(clean_json))

            mod = MK8CustomTrack(
                name=site.get_mod_name(clean_json),
                author=site.get_mod_author(clean_json),
                mod_id=site.get_mod_id(identifier, clean_json),
                mod_site=site,
                preview_image=site.get_mod_preview_image(clean_json)
            )
            print(mod.author)
            return mod

        except ModDownloadException as e:
            print(e)
            # TODO: Error handling
            return
        except KeyError as e:
            print(e)
            # TODO: Error handling
            return

    def get_api_endpoint(self, site_url: str) -> tuple[MK8ModSite, str, str]:
        """ TODO """
        for site in MOD_SITES:
            if site_url.startswith(site.domain):
                identifier = site_url[len(site.domain):].replace("#", "/").rsplit("/")[0]
                api_endpoint = site.get_api_endpoint(identifier)
                if api_endpoint is not None:
                    return site, identifier, api_endpoint
        return None, None, None

    def download_preview_image(self, preview_url: str, output_path: str) -> None:
        """ TODO """
        with requests.get(preview_url, stream=True) as res:
            print(res.status_code)
            if res.status_code != 200:
                raise ModDownloadException(f"Could not download {preview_url}: HTTP {res.status_code}. Please check your Internet connection.")

            # Check image size (assumes this is actually correct)
            if int(res.headers['content-length']) > 100000000:
                raise ModDownloadException("Image preview size too large. Max size is 50Mb.")

            with io.BytesIO(res.content) as f:
                with Image.open(f) as img:
                    # Resize and crop image to expected size
                    img = ImageOps.fit(img, MK8CustomTrack.PREVIEW_SIZE)
                    # Discard alpha channel (if present)
                    img = img.convert('RGB')
                    img.save(output_path)
                    return
