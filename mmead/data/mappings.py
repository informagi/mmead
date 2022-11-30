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
        if (res := self.fetch()) is not None:
            return res[0]
        else:
            raise ValueError(f"No result available for id {identifier} ...")

    def get_id_from_entity(self, entity):
        self.cursor.execute(f"""
            SELECT id
            FROM entity_id_mapping
            WHERE entity = '{entity}'
        """)
        if (res := self.fetch()) is not None:
            return res[0]
        else:
            raise ValueError(f"No result available for entity {entity} ...")
