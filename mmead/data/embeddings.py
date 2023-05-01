from ..util import load_embeddings

import numpy as np


def get_embeddings(dims=300, verbose=True):
    if dims == 300:
        return Embeddings('wiki2vec_300d', verbose)
    elif dims == 500:
        return Embeddings('wiki2vec_500d', verbose)
    else:
        raise IOError("dims should be either 300 or 500 ...")


class Embeddings:

    def __init__(self, key, verbose):
        self.identifier = key
        self.cursor = load_embeddings(self.identifier, verbose=verbose)
        self.fetch = self.cursor.fetchone

    def load_word_embedding(self, word):
        self.cursor.execute(f"""
            SELECT embedding 
            FROM wiki2vec_300d
            WHERE key = lower('{word}')
            LIMIT 1
        """)
        if (res := self.fetch()) is not None:
            return np.array(res[0])
        else:
            raise ValueError(f"No result available for word {word} ...")

    def load_entity_embedding(self, entity):
        self.cursor.execute(f"""
            SELECT embedding 
            FROM wiki2vec_300d
            WHERE key = 'ENTITY/{entity.replace(' ', '_')}'
            LIMIT 1
        """)
        if (res := self.fetch()) is not None:
            return np.array(res[0])
        else:
            raise ValueError(f"No result available for entity {entity} ...")
