# mmead
MS MARCO entity annotations and disambiguations

Format for document links:

```json
{
    "title": [
        {
         "entity_id": n,
         "start_pos": x,
         "end_pos": y, 
         "label": "entity_label",
         "details": [...]
        }, ...
    ],
    "headings": [...],
    "body": [...],
    "docid": "msmarco_doc_a_b" 
}
```
where: 
- title: Entities found in the title field
- headings: Entities found in the headings field
- body: Entities found in the body field
- docid: Document identifier of the collection

- An entity is presented as the following:
```
{
    "entity_id": n, 
    "start_pos": x,
    "end_pos": y, 
    "label": "entity_label",
    "details": {...}
}
```

where:
- entity_id: Unique entity identifier corresponding to internal wikipedia identifier
- start_pos: Start location of the entity found
- end_pos: Entities found in the body field
- label: Entity label
- details: Linker specific information 

Format for passages links:

```json
{
    "pid": "msmarco_passage_a_b",
    "docid": "msmarco_doc_c_d",
    "spans": [(e, f), ...]
    "passage": [
        {
         "entity_id": n,
         "start_pos": x,
         "end_pos": y, 
         "label": "entity_label",
         "details": {...}
        }, ...
    ]
}
```

where:
- pid: passage identifier corresponding to the passage id in the passage collection
- docid: document identifier of the document where the passage was constructed from
- spans: spans of the passage in document with identifier $docid
- passage: list of entities found in the passage

The entities are described the same as above. 
