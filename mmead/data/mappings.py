from ..util import load_mappings


def get_mappings(verbose=True):
    return Mapping(verbose)


class Mapping:

    def __init__(self, verbose):
        self.cursor = load_mappings("entity_id_mapping", verbose=verbose)
        self.fetch = self.cursor.fetchone

    def get_entity_from_id(self, identifier):
        self.cursor.execute(f"""
            SELECT entity
            FROM entity_id_mapping
            WHERE id = {identifier}
        """)
        try:
            return self.fetch()[0]
        except TypeError:
            raise ValueError(f"There is not entry for id {identifier} ...")

    def get_id_from_entity(self, entity):
        self.cursor.execute(f"""
            SELECT id
            FROM entity_id_mapping
            WHERE entity = '{entity}'
        """)
        try:
            return self.cursor.fetchone()[0]
        except TypeError:
            raise ValueError(f"There is not entry for entity {entity} ...")
