# mmead
MS MARCO entity annotations and disambiguations

Format for document links:

```json
{
    "title": [
        {"entity_id": n,
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

Format for passages links:

```json
{
    "pid": "msmarco_passage_a_b",
    "entities": [
        {"entity_id": n,
         "start_pos": x,
         "end_pos": y, 
         "label": "entity_label",
         "details": [...]
        }, ...
    ]
}
```
