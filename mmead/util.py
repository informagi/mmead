from .download_info import EMBEDDING_INFO, LINK_INFO, MAPPING_INFO
from .retrieve import download_and_unpack


def load_embeddings(key):
    if key not in EMBEDDING_INFO:
        raise ValueError(f'{key} is not a valid embedding identifier')
    path_to_data = download_and_unpack(key)
    return path_to_data


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
