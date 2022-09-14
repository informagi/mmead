# mmead
MS MARCO entity annotations and disambiguations

### Data using [REL](https://github.com/informagi/REL):

- [Mapping from Entity URL to Entity ID](https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/mmead/entity_id_map.json.gz)
- [Mapping from Entity ID to Entity URL](https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/mmead/id_entity_map.json.gz)
- [300D Wiki2Vec embeddings](https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/mmead/enwiki-20190701-wiki2vec-dim300.tar.bz2)
- [500D Wiki2Vec embeddings](https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/mmead/enwiki-20190701-wiki2vec-dim500.tar.bz2)
- [MSMARCO v1 doc Entity Links](https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/mmead/msmarco_v1_docs_links_v1.0.json.gz)
- [MSMARCO v1 passage Entity Links](https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/mmead/msmarco_v1_passage_links_v1.0.json.gz)
- [MSMARCO v2 doc Entity Links](https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/mmead/msmarco_v2_doc_links_v1.0.tar)
- [MSMARCO v2 passage Entity Links](https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/mmead/msmarco_v2_passage_links_v1.0.tar)

### Specifications:

Format for document links:

```json
{
    "title": [],
    "headings": [],
    "body": [
        {
            "entity_id": 3434750,
            "start_pos": 807,
            "end_pos": 820,
            "entity": "United States", 
            "details": {
                "tag": "LOC",
                "md_score": 0.9995014071464539}
            },
        {
            "entity_id": 3434750,
            "start_pos": 1206,
            "end_pos": 1219,
            "entity": "United States",
            "details": {
                "tag": "LOC",
                "md_score": 0.9995985925197601
            }
        }
    ], 
    "docid": "msmarco_doc_00_0"
}
```
where: 
    - title: Entities found in the title field (In our example there are no entities found) 
    - headings: Entities found in the headings field (In our example there are no entities found) 
    - body: Entities found in the body field (In our example there are two entities found, in the dataset there a more data points for this example) 
    - docid: Document identifier of the collection

- An entity is presented as:
    - entity_id: Unique entity identifier corresponding to internal wikipedia identifier
    - start_pos: Start location of the entity found
    - end_pos: Entities found in the body field
    - label: Entity label
    - details: Linker specific information 

Format for passages links:

```json
{
    "passage": [
        {
            "entity_id": 965751,
            "start_pos": 181,
            "end_pos": 187,
            "entity": "BMW M3",
            "details": {
                "tag": "MISC",
                "md_score": 0.6411977410316467
            }
        },
        {
            "entity_id": 221005,
            "start_pos": 241,
            "end_pos": 253,
            "entity": "Chevrolet Corvette",
            "details": {
                "tag": "MISC",
                "md_score": 0.8472966551780701
            }
        }
    ],
    "pid": "msmarco_passage_00_587"
}
```

where:
- pid: passage identifier corresponding to the passage id in the passage collection
- passage: list of entities found in the passage

The entities are described the same as above. 
