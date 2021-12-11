from uuid import uuid4

class SubQuery:
    """SubQuery class"""

    def __init__(self, name: str, query: str):
        self.name = name
        self.new_name = f'_TMP_{name}_{uuid4().hex.upper()}'
        self.query = query

    def __str__(self):
        return f'CREATE OR REPLACE TEMPORARY TABLE {self.new_name} AS (\t{self.query});'

    def __repr__(self) -> str:
        return f'SubQuery({self.name} -> {self.new_name})'
