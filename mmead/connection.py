import duckdb
import os

from .retrieve import get_cache_home

_db_connection = None


def get_connection(database=os.path.join(get_cache_home(), 'mmead.db')):
    global _db_connection
    if not _db_connection:
        _db_connection = DBConnection(database)
    return _db_connection


def close_connection():
    global _db_connection
    if _db_connection:
        _db_connection.connection.close()
    _db_connection = None


class DBConnection(object):

    def __init__(self, database: str, mem: int = 0) -> None:
        if mem:
            self.mem = mem
        else:
            # If mem is not provided we set the max mem to half of RAM
            mem_bytes = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES')
            mem_gib = mem_bytes/(1024.**3)
            self.mem = mem_gib//2
        self.connection = duckdb.connect(database)
        self.connection.install_extension("json")
        self.connection.load_extension("json")
        self.connection.execute(f"SET memory_limit='{self.mem}GB'")
        self.connection.execute("SET experimental_parallel_csv=true;")
        self.cursor = self.connection.cursor()
