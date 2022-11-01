from ..util import load_links


class MsmarcoV1Docs:

    def __init__(self, links='msmarco_v1_doc_links', verbose=False):
        self.identifier = links
        self.cursor = load_links(self.identifier, verbose=verbose)

    def load_links_from_docid(self, docid):
        self.cursor.execute(f"""
            SELECT field, entity_id, start_pos, end_pos, entity, id 
            FROM '{self.identifier}'
            WHERE id = '{docid}'
        """)
        return self.cursor.fetchall()
