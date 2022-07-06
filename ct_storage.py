from datetime import datetime
import os
import sqlite3
from typing import Iterable
from downloader import MOD_SITES

from view_ct_manager import MK8CustomTrack

class MK8CTStorage:
    """ Stores Custom Track information on disc """
    CACHE_PATH = "cache"
    DB_NAME = "modinfos.db"

    MOD_PREVIEW_FILENAME = "preview_%(mod_site_id)s_%(mod_id)s.jpeg"
    MOD_PREVIEW_PATH = os.path.join(CACHE_PATH, MOD_PREVIEW_FILENAME)

    def __init__(self):
        self._setup()

    def _setup(self):
        """ Initial setup """
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

    def save_changes(self):
        """ Saves any changes made by add or delete functions """
        self.connection.commit()

    def get_mods(self) -> Iterable[MK8CustomTrack]:
        """ TODO """
        return map(lambda row: MK8CustomTrack(row[1], MOD_SITES[row[3]], row[0]), self.connection.execute('SELECT id, name, author, mod_site FROM mods'))

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
    x.add_or_update_mod(MK8CustomTrack("My cool mod", MOD_SITES[0], 100039))
    for mod in x.get_mods():
        print(mod)

