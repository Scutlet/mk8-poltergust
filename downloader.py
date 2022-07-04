from dataclasses import dataclass, field
from itertools import count

from PIL import Image
import requests

@dataclass
class MK8ModSite:
    id: int = field(default_factory=count().__next__, init=False)
    name: str
    domain: str
    int_api_endpoint: str
    name_api_endpoint: str
    icon: Image.Image|None = None

    def __str__(self):
        return self.name

MOD_SITE_CT_WIKI = MK8ModSite(name="CT Wiki", domain="https://mk8.tockdom.com/wiki/",
    name_api_endpoint=  "https://mk8.tockdom.com/w/api.php?action=query&titles=%(name)s&prop=images&format=json",
    int_api_endpoint=   "https://mk8.tockdom.com/w/api.php?action=query&pageids=%(mod_id)s&prop=images&format=json"
)
MOD_SITE_GAMEBANANA = MK8ModSite(name="GameBanana", domain="https://gamebanana.com/mods/",
    name_api_endpoint=None,
    int_api_endpoint="https://api.gamebanana.com/Core/Item/Data?itemtype=Mod&itemid=%(mod_id)s&return_keys=1&format=json_min&fields=authors,date,description,name,Owner().name,Preview().sSubFeedImageUrl(),screenshots"
)

MOD_SITES = (MOD_SITE_CT_WIKI, MOD_SITE_GAMEBANANA)

@dataclass
class MK8ModVersion:
    major: int
    minor: int
    patch: int = 0

    def __str__(self):
        return f"v{self.major}.{self.minor}.{self.patch}"

@dataclass
class MK8CustomTrack:
    name: str
    mod_site: MK8ModSite
    mod_id: int

    def __str__(self):
        return f"[{self.mod_site}] {self.name}"

class PoltergustDownloader:
    """ TODO """
    def download(self, site_url: str) -> MK8CustomTrack:
        """ TODO """
        api_endpoint = self.get_api_endpoint(site_url)
        if api_endpoint is None:
            # TODO: Invalid query
            print("invalid domain!")
            return
        print(api_endpoint)
        print("start fetching!")

        res = requests.get(api_endpoint)
        if res.status_code != 200:
            # TODO: NO connection
            print("oops! no internet connection or site not reachable!")
            return

        print(res.json())


    def get_api_endpoint(self, site_url: str) -> bool:
        """ TODO """
        for site in MOD_SITES:
            if site_url.startswith(site.domain):
                identifier = site_url[len(site.domain):].replace("#", "/").rsplit("/")[0]
                if identifier.isdigit() and site.int_api_endpoint is not None:
                    return site.int_api_endpoint % {"mod_id": identifier}
                elif site.name_api_endpoint is not None:
                    return site.name_api_endpoint % {"name": identifier}
        return None
