import os
import duckdb
import json

from .download_info import EMBEDDING_INFO, LINK_INFO, MAPPING_INFO
from .retrieve import download_and_unpack, get_cache_home
from .connection import get_connection


def load_embeddings(key, db_path=os.path.join(get_cache_home(), 'mmead.db'), force=False, verbose=True):
    if key not in EMBEDDING_INFO:
        raise ValueError(f'{key} is not a valid embedding identifier')
    path_to_data = ''
    cursor = get_connection(db_path).cursor
    path_to_data = download_and_unpack(key)
    try:
        cursor.execute(f"SELECT * FROM {key} LIMIT 1")
        if force:
            if verbose:
                print(f"Table {key} already exists but force=True, so we drop the table and reload...")
        else:
            if verbose:
                print(f"Table {key} already exists, skipping the loading...")
            return cursor
    except duckdb.CatalogException:
        pass
    with open(path_to_data, 'rt') as embedding_file:
        entries, dims = [int(e) for e in embedding_file.readline().strip().split()]
        cursor.execute("START TRANSACTION")
        cursor.execute(
            f"CREATE OR REPLACE TABLE {key} (id INTEGER PRIMARY KEY, key VARCHAR, embedding REAL[])"
        )
        cursor.execute("CREATE TEMP SEQUENCE identifiers;")
        for n in range(entries):
            try:
                embedding = embedding_file.readline().strip().split()
                identifier, values = embedding[0], [float(e) for e in embedding[1:]]
                cursor.execute(f"INSERT INTO {key} VALUES (nextval('identifiers'), ?, {json.dumps(values)})", [identifier])
            except EOFError:
                cursor.execute("ROLLBACK")
                cursor.execute("DROP SEQUENCE identifiers")
                raise ValueError("There is less data than the header suggests.")
        try:
            assert embedding_file.read() == ''
        except AssertionError:
            cursor.execute("ROLLBACK")
            cursor.execute("DROP SEQUENCE identifiers")
            raise ValueError("There is more data than the header suggests")
        cursor.execute("COMMIT")
        cursor.execute("DROP SEQUENCE identifiers")
    if os.path.exists(path_to_data):
        os.remove(path_to_data)
    if os.path.isdir(os.path.dirname(path_to_data)):
        try:
            os.rmdir(os.path.dirname(path_to_data))
        except OSError:
            pass
    if verbose:
        print(f"Table {key} is available...")
    return cursor


def load_mappings(key):
    if key not in MAPPING_INFO:
        raise ValueError(f'{key} is not a valid mapping identifier')
    path_to_data = download_and_unpack(key)
    return path_to_data


def load_links(key):
    if key not in LINK_INFO:
        raise ValueError(f'{key} is not a valid link identifier')
    path_to_data = download_and_unpack(key)
    return path_to_data
