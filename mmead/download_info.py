EMBEDDING_INFO = {
    "wiki2vec_300d": {
        "description": "300 Dimensional Wiki2Vec embedddings, includes entity embeddings and word embeddings.",
        "filename": "enwiki-20190701-wiki2vec-dim300.tar.bz2",
        "extension": ".tar.bz2",
        "url": "https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/mmead/enwiki-20190701-wiki2vec-dim300.tar.bz2",
        "md5": "fdb377a91cfc2d37c52bd7831f0a0ff4",
        "to_file": "enwiki-20190701-model-w2v-dim300",
        "version": "wikipedia-20190701",
    },
    "wiki2vec_500d": {
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
    "msmarco_v1_doc_links": {
        'rel': {
            "description": "Entity Links for MS MARCO v1 Documents tagged by REL",
            "filename": "msmarco_v1_docs_links_v1.0.json.gz",
            "extension": ".gz",
            "url": "https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/mmead/msmarco_v1_docs_links_v1.0.json.gz",
            "md5": "b5c4e57db92047713b4ebef41afd3bef",
            "version": "wikipedia-20190701",
            "to_file": "msmarco_v1_doc_links_rel",
        }
    },
    "msmarco_v1_passage_links": {
        'rel': {
            "description": "Entity Links for MS MARCO v1 Passages tagged by REL",
            "filename": "msmarco_v1_passage_links_v1.0.json.gz",
            "extension": ".gz",
            "url": "https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/mmead/msmarco_v1_passage_links_v1.0.json.gz",
            "md5": "05cca3cb7172d3e7dd7f6baf1d5f5fdc",
            "version": "wikipedia-20190701",
            "to_file": "msmarco_v1_passage_links_rel",
        },
        'blink': {
            "description": "Entity Links for MS MARCO v1 Passages tagged by BLINK",
            "filename": "blink_mmead.tar.gz",
            "extension": ".tar.gz",
            "url": "http://gem.cs.ru.nl/blink_mmead.tar.gz",
            "md5": "c32f954769a75b02034a2f0ab87a9595",
            "version": "wikipedia-20190801",
            "to_file": "blink_mmead",
         }
    },
    "msmarco_v2_doc_links": {
        'rel': {
            "description": "Entity Links for MS MARCO v2 Documents tagged by REL",
            "filename": "msmarco_v2_doc_links_v1.0.tar",
            "extension": ".tar",
            "url": "https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/mmead/msmarco_v2_doc_links_v1.0.tar",
            "md5": "16aa44d80063dfb3a89aeb774ee3a77f",
            "version": "wikipedia-20190701",
            "to_file": "msmarco_v2_doc_links_rel",
        }
    },
    "msmarco_v2_passage_links": {
        'rel': {
            "description": "Entity Links for MS MARCO v2 Passages tagged by REL",
            "filename": "msmarco_v2_passage_links_v1.0.tar",
            "extension": ".tar",
            "url": "https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/mmead/msmarco_v2_passage_links_v1.0.tar",
            "md5": "40779507b30d358e66fd1e6e2295876d",
            "version": "wikipedia-20190701",
            "to_file": "msmarco_v2_passage_links_rel",
        }
    },
    '_folder': 'links',
}

MAPPING_INFO = {
    "entity_id_mapping": {
        "description": "Mapping from textual entity identifier to numerical entity identifier",
        "filename": "entity_id_map.json.gz",
        "extension": ".gz",
        "url": "https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/mmead/entity_id_map.json.gz",
        "md5": "8cf41b73b6678bd215df3ac3f6b27763",
        "version": "",
        "to_file": "entity_id_mapping.json",
    },
    "id_entity_mapping": {
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
