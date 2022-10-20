EMBEDDING_INFO = {
    "wiki2vec_300d": {  # todo: loading
        "description": "300 Dimensional Wiki2Vec embedddings, includes entity embeddings and word embeddings.",
        "filename": "enwiki-20190701-wiki2vec-dim300.tar.bz2",
        "extension": ".tar.bz2",
        # "url": "https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/mmead/enwiki-20190701-wiki2vec-dim300.tar.bz2",
        "url": "http://gem.cs.ru.nl/enwiki-20190701-wiki2vec-dim300.tar.bz2",
        # "md5": "fdb377a91cfc2d37c52bd7831f0a0ff4",
        "md5": "2a9e75b903245a5928eea98f3bc5267a",
        "to_file": "enwiki-20190701-model-w2v-dim300",
        "version": "wikipedia-20190701",
    },
    "wiki2vec_500d": {  # todo: loading
        "description": "500 Dimensional Wiki2Vec embedddings, includes entity embeddings and word embeddings.",
        "filename": "enwiki-20190701-wiki2vec-dim500.tar.bz2",
        "extension": ".tar.bz2",
        "url": "https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/mmead/enwiki-20190701-wiki2vec-dim500.tar.bz2",
        "md5": "14c3d3634124c5622a0ac9e28ec6ad9e",
        "to_file": "enwiki-20190701-model-w2v-dim500",
        "version": "wikipedia-20190701",
    },
    '_folder': 'embeddings',
}

LINK_INFO = {
    "msmarco_v1_doc_links": {  # todo loading
        "description": "Entity Links for MS MARCO v1 Documents",
        "filename": "msmarco_v1_docs_links_v1.0.json.gz",
        "extension": ".gz",
        #"url": "https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/mmead/msmarco_v1_docs_links_v1.0.json.gz",
        "url": "http://gem.cs.ru.nl/msmarco_v1_docs_links_v1.0.json.gz",
        #"md5": "b5c4e57db92047713b4ebef41afd3bef",
        "md5": "bbd3158ea1788545288e2053b1e73f6b",
        "version": "wikipedia-20190701",
        "to_file": "msmarco_v1_doc_links",
    },
    "msmarco_v1_passage_links": {  # todo loading
        "description": "Entity Links for MS MARCO v1 Passages",
        "filename": "msmarco_v1_passage_links_v1.0.json.gz",
        "extension": ".gz",
        "url": "https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/mmead/msmarco_v1_passage_links_v1.0.json.gz",
        "md5": "05cca3cb7172d3e7dd7f6baf1d5f5fdc",
        "version": "wikipedia-20190701",
        "to_file": "msmarco_v1_passage_links",
    },
    "msmarco_v2_doc_links": {  # todo loading
        "description": "Entity Links for MS MARCO v2 Documents",
        "filename": "msmarco_v2_doc_links_v1.0.tar",
        "extension": ".tar",
        #  "url": "https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/mmead/msmarco_v2_doc_links_v1.0.tar",
        "url": "http://gem.cs.ru.nl/msmarco_v2_doc_links_v1.0.tar",
        #  "md5": "16aa44d80063dfb3a89aeb774ee3a77f",
        "md5": "094af22515ab81193db648ce7e1078bf",
        "version": "wikipedia-20190701",
        "to_file": "msmarco_v2_doc_links",
    },
    "msmarco_v2_passage_links": {  # todo loading
        "description": "Entity Links for MS MARCO v2 Passages",
        "filename": "msmarco_v2_passage_links_v1.0.tar",
        "extension": ".tar",
        "url": "https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/mmead/msmarco_v2_passage_links_v1.0.tar",
        "md5": "40779507b30d358e66fd1e6e2295876d",
        "version": "wikipedia-20190701",
        "to_file": "msmarco_v2_passage_links",
    },
    '_folder': 'links',
}

MAPPING_INFO = {
    "entity_id_mapping": {  # todo loading
        "description": "Mapping from textual entity identifier to numerical entity identifier",
        "filename": "entity_id_map.json.gz",
        "extension": ".gz",
        #"url": "https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/mmead/entity_id_map.json.gz",
        "url": "http://gem.cs.ru.nl/entity_id_map.json.gz",
        #"md5": "8cf41b73b6678bd215df3ac3f6b27763",
        "md5": "2a397b9aa4b19c84087c679eb33a6da8",
        "version": "",
        "to_file": "entity_id_mapping.json",
    },
    "id_entity_mapping": {  # todo loading
        "description": "Mapping from numerical entity identifier to textual entity identifier",
        "filename": "id_entity_map.json.gz",
        "extension": ".gz",
        "url": "https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/mmead/id_entity_map.json.gz",
        "md5": "c1ccaf9db115b0120230846bfb541a3f",
        "version": "",
        "to_file": "id_entity_mapping.json",
    },
    '_folder': 'mappings',
}