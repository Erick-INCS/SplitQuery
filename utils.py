from re import compile, IGNORECASE
from typing import List, Tuple
from SubQuery import SubQuery
from regex import SP, RE_SUBQUERY, RE_WITH, RE_FINAL_SELECT


def update_query(queries: List[SubQuery], current_query: str):
    """Update query using sub_tables"""
    for query in queries:
        ref_regex = compile(f'({SP}){query.name}({SP})', IGNORECASE)
        current_query = ref_regex.sub(f'\\1{query.new_name}\\2', current_query)

    return current_query

def split_quey(content: str) -> Tuple[List[str], str]:
    splits = list(RE_WITH.finditer(content))
    sub_tables = list()

    print('\n')
    for i, split in enumerate(splits):
        start = split.start()
        end = len(content) - 1 if i == len(splits) - 1 else splits[i + 1].start()

        print(split, f'from {start} to {end}')
        query = RE_SUBQUERY.findall(content[start:end])

        assert query and len(query[0]) == 3, f'Unsuported subquery: {content[start:end]}'
        table_name = query[0][0]
        subquery = query[0][1]

        # Generate temporary table and replace table references
        sub_tables.append(SubQuery(table_name, update_query(sub_tables, subquery)))
    print('\n')

    select = RE_FINAL_SELECT.findall(content[start:])
    assert isinstance(select, list) and len(select) == 1, f'Unsuported final query: {content[start:]}'
    select = update_query(sub_tables, select[-1])
    
    return sub_tables, select
