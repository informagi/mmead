from abc import ABC

from ..util import load_links


def get_links(version, passage_or_doc, verbose=True):
    if version == 'v1' and passage_or_doc == 'passage':
        return V1PassageLinks(verbose)
    elif version == 'v1' and passage_or_doc == 'doc':
        return V1DocLinks(verbose)
    elif version == 'v2' and passage_or_doc == 'passage':
        return V2PassageLinks(verbose)
    elif version == 'v2' and passage_or_doc == 'doc':
        return V2DocLinks(verbose)
    else:
        raise IOError("version should be v1 or v2, passage_or_doc should be passage or doc..")


class Links:

    def __init__(self, key, verbose=True):
        self.identifier = key
        self.cursor = load_links(self.identifier, verbose=verbose)
        self.fetch = self.cursor.fetchall

    def load_links_from_docid(self, docid):
        raise NotImplementedError()

    def load_docs_from_entity_id(self):
        raise NotImplementedError()


class V1PassageLinks(Links):
    def __init__(self, verbose):
        super().__init__(key="msmarco_v1_passage_links", verbose=verbose)

    def load_links_from_docid(self, docid):
        self.cursor.execute(f"""
            SELECT field, entity_id, start_pos, end_pos, entity, pid 
            FROM {self.identifier}
            WHERE pid = '{docid}'
        """)
        return self.fetch()

    def load_docs_from_entity_id(self):
        raise NotImplementedError()


class V1DocLinks(Links):
    def __init__(self, verbose):
        super().__init__(key="msmarco_v1_doc_links", verbose=verbose)

    def load_links_from_docid(self, docid):
        self.cursor.execute(f"""
            SELECT field, entity_id, start_pos, end_pos, entity, id 
            FROM {self.identifier}
            WHERE id = '{docid}'
        """)
        return self.fetch()

    def load_docs_from_entity_id(self):
        raise NotImplementedError()


class V2PassageLinks(Links):
    def __init__(self, verbose):
        super().__init__(key="msmarco_v2_passage_links", verbose=verbose)

    def load_links_from_docid(self, docid):
        self.cursor.execute(f"""
            SELECT field, entity_id, start_pos, end_pos, entity, id 
            FROM {self.identifier}
            WHERE id = '{docid}'
        """)
        return self.fetch()

    def load_docs_from_entity_id(self):
        raise NotImplementedError()


class V2DocLinks(Links):
    def __init__(self, verbose):
        super().__init__(key="msmarco_v2_doc_links", verbose=verbose)

    def load_links_from_docid(self, docid):
        _, __, segment, offset = docid.split('_')
        return self.load_links_from_segment_and_offset(segment, offset)

    def load_links_from_segment_and_offset(self, segment, offset):
        self.cursor.execute(f"""
            SELECT field, entity_id, start_pos, end_pos, entity, id 
            FROM {self.identifier}
            WHERE segment = '{segment}'
            AND doc_offset = '{offset}'
        """)
        return self.fetch()

    def load_docs_from_entity_id(self):
        raise NotImplementedError()

