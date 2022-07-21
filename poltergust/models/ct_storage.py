from datetime import datetime
import os
import sqlite3
from typing import Iterable
from poltergust.models.mod_sites import MK8ModSite

from poltergust.parsers.downloader import API_MOD_SITES, MK8CustomTrack
from poltergust.utils import Singleton


class MK8CTStorage(metaclass=Singleton):
    """ Stores Custom Track information on disc """
    CACHE_PATH = "cache"
    DB_NAME = "modinfos.db"

    MOD_PREVIEW_FILENAME = "preview_%(mod_site_id)s_%(mod_id)s.jpeg"
    MOD_PREVIEW_PATH = os.path.join(CACHE_PATH, MOD_PREVIEW_FILENAME)

    def __init__(self):
        # Connect with cache
        os.makedirs(self.CACHE_PATH, exist_ok=True)
        path = os.path.join(self.CACHE_PATH, self.DB_NAME)
        self.connection = sqlite3.connect(path)

        # Create tables
        self.connection.execute('''CREATE TABLE IF NOT EXISTS poltergust (key text unique, value text)''')
        self.connection.execute('''INSERT OR REPLACE INTO poltergust VALUES ('version', '2.0.0')''')
        self.connection.commit()
        self.connection.execute('''CREATE TABLE IF NOT EXISTS mods
               (id integer not null, mod_site integer not null, name text, author text, last_updated_at text, primary key (id, mod_site))''')

    def close_connection(self):
        """ Closes the database connection """
        self.connection.close()

    def commit(self):
        """ Saves any changes made by add or delete functions """
        self.connection.commit()

    def get_mods(self) -> Iterable[MK8CustomTrack]:
        """ TODO """
        return map(lambda row: self._get_mod_from_db_infos(row[0], row[1], row[2], row[3]), self.connection.execute('SELECT id, name, author, mod_site FROM mods'))

    def _get_mod_from_db_infos(self, mod_id, name, author, mod_site_id) -> MK8CustomTrack:
        """ TODO """
        preview_image = self.MOD_PREVIEW_PATH % {'mod_id': mod_id, 'mod_site_id': mod_site_id}
        return MK8CustomTrack(name, API_MOD_SITES[mod_site_id], mod_id, author, preview_image)

    def find_mod(self, mod_id: int, mod_site_id: int) -> MK8CustomTrack|None:
        """ Finds a mod from the given mod site with the given mod_id, or None if no such mod exists """
        for mod_id, name, author, mod_site_id in self.connection.execute('SELECT id, name, author, mod_site FROM mods WHERE id = :mod_id AND mod_site = :mod_site_id', {
                    "mod_id": mod_id,
                    "mod_site_id": mod_site_id
                }):
            return self._get_mod_from_db_infos(mod_id, name, author, mod_site_id)
        # Mod not found
        return None

    def add_or_update_mod(self, mod: MK8CustomTrack) -> None:
        """ TODO """
        self.connection.execute('''INSERT OR REPLACE INTO mods (id, mod_site, author, name, last_updated_at) VALUES (:mod_id, :mod_site, :author, :name, :last_updated_at)''', {
            "mod_id": mod.mod_id,
            "mod_site": mod.mod_site.id,
            "author": mod.author,
            "name": mod.name,
            "last_updated_at": datetime.now().isoformat()
        })

if __name__ == "__main__":
    x = MK8CTStorage()
    x.add_or_update_mod(MK8CustomTrack("My cool mod", API_MOD_SITES[0], 100039))
    for mod in x.get_mods():
        print(mod)

