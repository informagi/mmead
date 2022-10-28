import os
import duckdb

from .download_info import EMBEDDING_INFO, LINK_INFO, MAPPING_INFO
from .retrieve import download_and_unpack
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


def _remove_raw_data(path_to_data, verbose):
    if verbose:
        print("Data is loaded in the tables, removing raw data files...")
    if os.path.exists(path_to_data):
        os.remove(path_to_data)
    if os.path.isdir(os.path.dirname(path_to_data)):
        try:
            os.rmdir(os.path.dirname(path_to_data))
        except OSError:
            pass


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
        SELECT nextval('identifiers') AS id, 
               column000 AS key, 
               {str(['column{:0>{}}'.format(i, str(len(str(dims)))) for i in range(1, dims + 1)]).replace("'", "")} 
               AS embedding 
        FROM read_csv_auto('{path_to_data}', skip=1, delim=' ')
    """)
    cursor.execute("DROP SEQUENCE identifiers")
    _remove_raw_data(path_to_data, verbose)
    if verbose:
        print(f"Table {key} is available...")
    return cursor


def load_mappings(key, force=False, verbose=True):
    if key not in MAPPING_INFO:
        raise ValueError(f'{key} is not a valid mapping identifier')
    cursor = _get_cursor()
    if _check_force(key, cursor, verbose, force):
        return cursor
    path_to_data = download_and_unpack(key, force=force)
    if key == 'entity_id_mapping':  # Sorry for this ...
        cursor.execute(f"""
            CREATE TABLE {key} AS 
            SELECT trim(trim(reverse(substring(reverse(text),strpos(reverse(text), ' :'), length(text))), '{{: ' ), '"')
                   AS entity, 
                   CAST(trim(reverse(substring(reverse(text), 0, strpos(reverse(text), ' :'))), '}}') AS INTEGER)
                   AS id 
            FROM read_csv_auto('{path_to_data}', delim='', columns={{'text': 'VARCHAR'}})
        """)
    else:  # and this...
        cursor.execute(f"""
            CREATE TABLE {key} AS 
            SELECT trim(trim(substring(text, strpos(text, ': '), length(text)), ': }}'), '"') AS entity,
                   CAST(trim(substring(text, 0, strpos(text, ': ')), '{{"') AS INT) AS id
            FROM read_csv_auto('{path_to_data}', delim='', columns={{'text': 'VARCHAR'}})
        """)
    _remove_raw_data(path_to_data, verbose)
    if verbose:
        print(f"Table {key} is available..., with columns id and entity")
    return cursor


def load_links(key, force=False, verbose=True):
    if key not in LINK_INFO:
        raise ValueError(f'{key} is not a valid link identifier')
    cursor = _get_cursor()
    if _check_force(key, cursor, verbose, force):
        return cursor
    path_to_data = download_and_unpack(key, force=force)
    if key == 'msmarco_v1_doc_links':
        return _load_msmarco_v1_doc_links(key, path_to_data, cursor, verbose)
    elif key == 'msmarco_v1_passage_links':
        return _load_msmarco_v1_passage_links(key, path_to_data, cursor, verbose)
    elif key == 'msmarco_v2_doc_links':
        return _load_msmarco_v2_doc_links(key, path_to_data, cursor, verbose)
    elif key == 'msmarco_v2_passage_links':
        return _load_msmarco_v2_passage_links(key, path_to_data, cursor, verbose)
    else:
        raise ValueError("This key is not recognized")


def _load_msmarco_v1_doc_links(key, path_to_data, cursor, verbose):
    if verbose:
        print("Loading the MS MARCO v1 document entity links, this might take a while...")
    cursor.begin()
    cursor.execute("CREATE TEMP TABLE t1 (j JSON)")
    cursor.execute(f"""
        INSERT INTO t1 SELECT * FROM read_csv_auto('{path_to_data}', delim='', maximum_line_size='8000000')
    """)
    cursor.execute(f"""
        CREATE OR REPLACE TABLE {key} AS
            SELECT 
            'body' AS field,
            q1.body->>'entity_id' AS entity_id,
            q1.body->>'start_pos' AS start_pos,
            q1.body->>'end_pos' AS end_pos,
            q1.body->>'entity' AS entity,
            q1.id 
        FROM 
        (
            SELECT json(UNNEST(json_transform(j->>'body', '["JSON"]'))) as body, 
                   j->>'docid' as id 
            FROM t1
        ) as q1
    """)
    cursor.execute(f"""
        INSERT INTO {key}
        SELECT
            'title' as field,
            q1.title->>'entity_id' AS entity_id,
            q1.title->>'start_pos' AS start_pos,
            q1.title->>'end_pos' AS end_pos,
            q1.title->>'entity' AS entity,
            q1.id 
        FROM 
        (
            SELECT json(UNNEST(json_transform(j->>'title', '["JSON"]'))) as title, 
                   j->>'docid' as id 
            FROM t1
        ) as q1
    """)
    cursor.execute("DROP TABLE t1")
    cursor.commit()
    if verbose:
        print(f"Table {key} is available...")
    return cursor


def _load_msmarco_v1_passage_links(key, path_to_data, cursor, verbose):
    cursor.execute(f"CREATE OR REPLACE TABLE {key} (j JSON)")
    cursor.execute(f"INSERT INTO {key} SELECT * FROM read_json_objects('{path_to_data}')")
    if verbose:
        print(f"Table {key} is available...")
    return cursor


def _load_msmarco_v2_doc_links(key, path_to_data, cursor, verbose):
    cursor.execute(f"CREATE OR REPLACE TABLE {key} (j JSON)")
    for file in os.listdir(path_to_data):
        filename = os.path.join(path_to_data, file)
        cursor.execute(f"INSERT INTO {key} SELECT * FROM read_json_objects('{filename}')")
    if verbose:
        print(f"Table {key} is available..., with JSON column j...")
    return cursor


def _load_msmarco_v2_passage_links(key, path_to_data, cursor, verbose):
    cursor.execute(f"CREATE OR REPLACE TABLE {key} (j JSON)")
    for file in os.listdir(path_to_data):
        filename = os.path.join(path_to_data, file)
        cursor.execute(f"INSERT INTO {key} SELECT * FROM read_json_objects('{filename}')")
    if verbose:
        print(f"Table {key} is available..., with JSON column j...")
    return cursor
