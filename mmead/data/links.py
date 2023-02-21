from ..util import load_links
import json


def get_links(version, passage_or_doc, linker='rel', verbose=True):
    if version == 'v1' and passage_or_doc == 'passage' and linker == 'rel':
        return V1PassageLinksREL(verbose)
    elif version == 'v1' and passage_or_doc == 'passage' and linker == 'blink':
        return V1PassageLinksBlink(verbose)
    elif version == 'v1' and passage_or_doc == 'doc':
        return V1DocLinks(verbose)
    elif version == 'v2' and passage_or_doc == 'passage':
        return V2PassageLinks(verbose)
    elif version == 'v2' and passage_or_doc == 'doc':
        return V2DocLinks(verbose)
    else:
        raise IOError("version should be v1 or v2, passage_or_doc should be passage or doc ...")


class Links:

    def __init__(self, key, verbose=True, linker='rel'):
        self.identifier = key
        self.cursor = load_links(self.identifier, verbose=verbose, linker=linker)

    def load_links_from_docid(self, docid):
        raise NotImplementedError()

    def load_links_from_docids(self, docid):
        raise NotImplementedError()


class V1PassageLinksREL(Links):
    def __init__(self, verbose):
        super().__init__(key="msmarco_v1_passage_links", verbose=verbose)

    def load_links_from_docid(self, docid):
        self.cursor.execute(f"""
            SELECT to_json(
                {{
                    'passage': json_group_array(x),
                    'pid': '{docid}'
                }}
            )
            FROM (
                SELECT to_json(
                    {{
                        'entity_id': entity_id,
                        'start_pos': start_pos,
                        'end_pos': end_pos,
                        'entity': entity,
                    }}
                ) AS x
                FROM {self.identifier}
                WHERE pid = {docid}
            )
        """)
        return self.cursor.fetchone()[0]

    def load_links_from_docids(self, docid):
        raise NotImplementedError()


class V1PassageLinksBlink(Links):
    def __init__(self, verbose):
        super().__init__(key="msmarco_v1_passage_links", verbose=verbose, linker='blink')

    def load_links_from_docid(self, docid):
        self.cursor.execute(f"""
            SELECT to_json(
                {{
                    'passage': json_group_array(x),
                    'pid': '{docid}'
                }}
            )
            FROM (
                SELECT to_json(
                    {{
                        'entity_id': entity_id,
                        'start_pos': start_pos,
                        'end_pos': end_pos,
                        'entity': entity,
                    }}
                ) AS x
                FROM {self.identifier}
                WHERE pid = {docid}
            )
        """)
        return self.cursor.fetchone()[0]

    def load_links_from_docids(self, docid):
        raise NotImplementedError()


class V1DocLinks(Links):
    def __init__(self, verbose):
        super().__init__(key="msmarco_v1_doc_links", verbose=verbose)

    def load_links_from_docid(self, docid):
        self.cursor.execute(f"""
            SELECT to_json(
                {{
                    'body': json_group_array(x),
                    'docid': '{docid}'
                }}
            )
            FROM (
                SELECT to_json(
                    {{
                        'entity_id': entity_id,
                        'start_pos': start_pos,
                        'end_pos': end_pos,
                        'entity': entity 
                    }}
                ) as x
                FROM {self.identifier}
                WHERE id = '{docid}'
            )
        """)
        return self.cursor.fetchone()[0]

    def load_links_from_docids(self, docid):
        raise NotImplementedError()


class V2PassageLinks(Links):
    def __init__(self, verbose):
        super().__init__(key="msmarco_v2_passage_links", verbose=verbose)

    def load_links_from_docid(self, docid):
        _, __, segment, offset = docid.split('_')
        return self.load_links_from_segment_and_offset(segment, offset)

    def load_links_from_segment_and_offset(self, segment, offset):
        docid = f"msmarco_passage_{segment}_{offset}"
        self.cursor.execute(f"""
            SELECT to_json(
                {{
                    'passage': json_group_array(x),
                    'docid': '{docid}'
                }}
            )
            FROM (
                SELECT to_json(
                    {{
                        'entity_id': entity_id,
                        'start_pos': start_pos,
                        'end_pos': end_pos,
                        'entity': entity 
                    }}
                ) as x
                FROM {self.identifier}
                WHERE segment = '{segment}'
                AND passage_offset = '{offset}'
            )
        """)
        return self.cursor.fetchone()[0]

    def load_links_from_docids(self, docid):
        raise NotImplementedError()


class V2DocLinks(Links):
    def __init__(self, verbose):
        super().__init__(key="msmarco_v2_doc_links", verbose=verbose)

    def load_links_from_docid(self, docid):
        _, __, segment, offset = docid.split('_')
        return self.load_links_from_segment_and_offset(segment, offset)

    def load_links_from_segment_and_offset(self, segment, offset):
        docid = f"msmarco_doc_{segment}_{offset}"
        self.cursor.execute(f"""
                SELECT to_json(
                    {{
                        'docid': '{docid}'
                    }}
                )
                UNION
                SELECT to_json(
                    {{
                        'title': list_concat([], CAST(json_group_array(x) AS JSON[])),
                    }}
                )
                FROM (
                    SELECT to_json(
                        {{
                            'entity_id': entity_id,
                            'start_pos': start_pos,
                            'end_pos': end_pos,
                            'entity': entity 
                        }}
                    ) as x
                    FROM {self.identifier}
                    WHERE segment = '{segment}'
                    AND doc_offset = '{offset}'
                    AND field = 'title'
                )
                UNION
                SELECT to_json(
                    {{
                        'header': list_concat([], CAST(json_group_array(x) AS JSON[])),
                    }}
                )
                FROM (
                    SELECT to_json(
                        {{
                            'entity_id': entity_id,
                            'start_pos': start_pos,
                            'end_pos': end_pos,
                            'entity': entity 
                        }}
                    ) as x
                    FROM {self.identifier}
                    WHERE segment = '{segment}'
                    AND doc_offset = '{offset}'
                    AND field = 'header'
                )
                UNION
                SELECT to_json(
                    {{
                        'body': list_concat([], CAST(json_group_array(x) AS JSON[])),
                    }}
                )
                FROM (
                    SELECT to_json(
                        {{
                            'entity_id': entity_id,
                            'start_pos': start_pos,
                            'end_pos': end_pos,
                            'entity': entity 
                        }}
                    ) as x
                    FROM {self.identifier}
                    WHERE segment = '{segment}'
                    AND doc_offset = '{offset}'
                    AND field = 'body'
                )
        """)
        output = dict()
        for out in self.cursor.fetchall():
            output |= json.loads(out[0])
        return json.dumps(output)

    def load_links_from_docids(self, docid):
        raise NotImplementedError()
