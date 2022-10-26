import os
import duckdb

from .download_info import EMBEDDING_INFO, LINK_INFO, MAPPING_INFO
from .retrieve import download_and_unpack, get_cache_home
from .connection import get_connection


def _get_cursor():
    return get_connection().cursor


def _check_force(key, cursor, verbose, force):
    try:
        cursor.execute(f"SELECT * FROM {key} LIMIT 1")
        if force:
            if verbose:
                print(f"Table {key} already exists but force=True, so we drop the table and reload...")
        else:
            if verbose:
                print(f"Table {key} already exists, skipping the loading...")
            return True
    except duckdb.CatalogException:
        pass
    return False


def load_embeddings(key, force=False, verbose=True):
    if key not in EMBEDDING_INFO:
        raise ValueError(f'{key} is not a valid embedding identifier')
    cursor = _get_cursor()
    if _check_force(key, cursor, verbose, force):
        return cursor
    path_to_data = download_and_unpack(key, force=force)
    with open(path_to_data, 'rt') as embedding_file:
        entries, dims = [int(e) for e in embedding_file.readline().strip().split()]
    cursor.execute("CREATE TEMP SEQUENCE identifiers;")
    cursor.execute(f"""
        CREATE OR REPLACE TABLE {key} AS 
        SELECT 
            nextval('identifiers') AS id, 
            column000 AS key, 
            {str(['column{:0>{}}'.format(i, str(len(str(dims))))
                  for i in range(1, dims + 1)]).replace("'", "")} AS embedding 
        FROM read_csv_auto('{path_to_data}', skip=1, delim=' ')"""
                   )
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


def load_mappings(key, force=True, verbose=True):
    if key not in MAPPING_INFO:
        raise ValueError(f'{key} is not a valid mapping identifier')
    cursor = _get_cursor()
    if _check_force(key, cursor, verbose, force):
        return cursor
    path_to_data = download_and_unpack(key)
    if key == 'entity_id_mapping':  # Sorry for this ...
        cursor.execute(f"""
            CREATE TABLE {key} AS 
            SELECT trim(trim(reverse(substring(reverse(text), strpos(reverse(text), ' :'),length(text))), '{{: ' ),
                        '"') AS entity, 
                   CAST(trim(reverse(substring(reverse(text), 0, strpos(reverse(text), ' :'))), '}}') AS INTEGER) AS id 
            FROM read_csv_auto('{path_to_data}',
                               delim='',
                               columns={{'text': 'VARCHAR'}})
        """)
    else:  # and this...
        cursor.execute(f"""
            CREATE TABLE {key} AS 
            SELECT 
                CAST(trim(substring(text, 0, strpos(text, ': ')), '{{"') AS INT) AS id,
                trim(trim(substring(text, strpos(text, ': '), length(text)), ': }}'), '"') AS entity
            FROM read_csv_auto('{path_to_data}', delim='', columns={{'text': 'VARCHAR'}})
        """)
    if verbose:
        print(f"Table {key} is available..., with columns id and entity")
    return cursor


def load_links(key, force=True, verbose=True):
    if key not in LINK_INFO:
        raise ValueError(f'{key} is not a valid link identifier')
    path_to_data = download_and_unpack(key)
    cursor = _get_cursor()
    if _check_force(key, cursor, verbose, force):
        return cursor
    if key == 'msmarco_v1_doc_links':
        return _load_msmarco_v1_links(key, path_to_data, cursor, verbose)
    elif key == 'msmarco_v1_passage_links':
        return _load_msmarco_v1_links(key, path_to_data, cursor, verbose)
    elif key == 'msmarco_v2_doc_links':
        return _load_msmarco_v2_links(key, path_to_data, cursor, verbose)
    elif key == 'msmarco_v2_passage_links':
        return _load_msmarco_v2_links(key, path_to_data, cursor, verbose)
    else:
        raise ValueError("This key is not recognized")


def _load_msmarco_v1_links(key, path_to_data, cursor, verbose):
    cursor.execute(f"CREATE OR REPLACE TABLE {key} (j JSON)")
    cursor.execute(f"INSERT INTO {key} SELECT * FROM read_json_objects('{path_to_data}')")
    if verbose:
        print(f"Table {key} is available..., with JSON column j...")
    return cursor


def _load_msmarco_v2_links(key, path_to_data, cursor, verbose):
    cursor.execute(f"CREATE OR REPLACE TABLE {key} (j JSON)")
    for file in os.listdir(path_to_data):
        filename = os.path.join(path_to_data, file)
        cursor.execute(f"INSERT INTO {key} SELECT * FROM read_json_objects('{filename}')")
    if verbose:
        print(f"Table {key} is available..., with JSON column j...")
    return cursor
