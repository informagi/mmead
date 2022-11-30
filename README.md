# MMEAD: MS MARCO Entity Annotations and Disambiguations

## What is MMEAD?
MMEAD, or MS MARCO Entity Annoations and Disambiguations, is a specification for entity links
for the [MSMARCO](https://microsoft.github.io/msmarco/) dataset. MMEAD proposes a JSON specification on how
entity links can be shared for easier usage of entity links. Entity links produced by the
[Radboud Entity Linker (REL)](https://github.com/informargi/rel) are provided. Code to easily work with this data is available.

## How to use
MMEAD provides an API to easily use the data we provide.

### Entity Links
If you load a class that uses the entity links, the data is automatically downloaded the first time you use it.
The following code will load the entity links for the MSMARCO v1 passage collection:
```Python3
>>> from mmead import get_links
>>> links = get_links('v1', 'passage')
```
After downloading and using the data for the first time, the data will be stored in cache. The first time
it might take some time, but afterwards you can access the data quite quickly:
```python3
>>> print(links.load_links_from_docid(123))
[('passage', '7954681', '126', '134', 'Montreal', '123')]
```

### Embeddings
We also provide the [Wikipedia2Vec](https://wikipedia2vec.github.io/wikipedia2vec/) embeddings of the wikipedia dump 
that we linked to. Wikipedia2Vec embeddings contain both word and entity embeddings, we can retrieve both:
```Python3
>>> from mmead import get_embeddings
>>> e = get_embeddings(300, verbose=False)
>>> montreal_word = e.load_word_embedding("Montreal")
>>> montreal_word[:5]
[-0.1258 -0.5049 -0.0563  0.4908  0.3244]
```

The dot-product can be used to measure similarity:
```Python3
>>> montreal_word = e.load_word_embedding("Montreal")
>>> montreal_entity = e.load_entity_embedding("Montreal")
>>> green_word = e.load_word_embedding("green")

>>> montreal_word @ montreal_entity
31.83191792
>>> montreal_word @ green_word
5.55568354
```

### Mappings
There is also a mapping from entity text to its id available, or the other way around:
```Python3
>>> from mmead import get_mappings
>>> m = get_mappings(verbose=False)
>>> m.get_id_from_entity('Montreal')
7954681
>>> m.get_entity_from_id(7954681)
'Montreal'
```


## Available data:
The following data is available through MMEAD: 

### Data using [REL](https://github.com/informagi/REL):
- [Mapping from Entity URL to Entity ID](https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/mmead/entity_id_map.json.gz)
- [Mapping from Entity ID to Entity URL](https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/mmead/id_entity_map.json.gz)
- [300D Wikipedia2Vec embeddings](https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/mmead/enwiki-20190701-wiki2vec-dim300.tar.bz2)
- [500D Wikipedia2Vec embeddings](https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/mmead/enwiki-20190701-wiki2vec-dim500.tar.bz2)
- [MSMARCO v1 doc Entity Links](https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/mmead/msmarco_v1_docs_links_v1.0.json.gz)
- [MSMARCO v1 passage Entity Links](https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/mmead/msmarco_v1_passage_links_v1.0.json.gz)
- [MSMARCO v2 doc Entity Links](https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/mmead/msmarco_v2_doc_links_v1.0.tar)
- [MSMARCO v2 passage Entity Links](https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/mmead/msmarco_v2_passage_links_v1.0.tar)

MMEAD provides code that automatically downloads the data and provides it
through a database, so you do not have to download it manually. 

### Specifications:
Format for document links:

```json
{
    "title": [],
    "headings": [],
    "body": 
    [
        {
            "entity_id": 3434750,
            "start_pos": 807,
            "end_pos": 820,
            "entity": "United States", 
            "details": 
            {
                "tag": "LOC",
                "md_score": 0.9995014071464539
            }
        },       
        {
            "entity_id": 3434750,
            "start_pos": 1206,
            "end_pos": 1219,
            "entity": "United States",
            "details": 
            {
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
    "passage": 
    [
        {
            "entity_id": 965751,
            "start_pos": 181,
            "end_pos": 187,
            "entity": "BMW M3",
            "details": 
            {
                "tag": "MISC",
                "md_score": 0.6411977410316467
            }
        },
        {
            "entity_id": 221005,
            "start_pos": 241,
            "end_pos": 253,
            "entity": "Chevrolet Corvette",
            "details": 
            {
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
