"""Logic for sub-table dependency."""

from SubQuery import SubQuery


class TDependencies:
    """Contain all the dependencies for the query."""

    def __init__(self):
        self.deps = dict()
        self.queries = dict()

    def add(self, table: str, depends_of: str):
        """Add a new dependency."""
        self.deps[table] = self.deps.get(table, set())
        self.deps[table].add(depends_of)

    def link(self, table: str, query: SubQuery):
        """Store the processed subquery."""
        self.queries[table] = self.queries.get(table, list()) + [query]
