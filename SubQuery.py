"""Subquery Logic."""
from uuid import uuid4


class SubQuery:
    """SubQuery class"""

    def __init__(self, name: str, query: str, database=None, schema=None):
        self.name = name
        prefix = '' if not database else database.strip().upper() + '.'
        prefix += '' if not schema else schema.strip().upper() + '.'
        self.new_name = f'{prefix}_TMP_{name}_{uuid4().hex.upper()}'
        self.query = query

    def __str__(self):
        return 'CREATE OR REPLACE TEMPORARY TABLE ' + \
                f'{self.new_name} AS (\t{self.query});'

    def __repr__(self) -> str:
        return f'SubQuery({self.name} -> {self.new_name})'
