"""Main logic"""
from typing import List
from SubQuery import SubQuery
from regex_exp import RE_SUBQUERY, RE_WITH, RE_FINAL_SELECT, RE_LIST_TB_REF
from table_deps import TDependencies


def update_query(
        queries: List[SubQuery],
        current_query: str,
        deps: TDependencies,
        current_name: str):
    """Update query using sub_tables"""
    for query in queries:
        for regex in RE_LIST_TB_REF:
            exists = regex(query.name).search(current_query)
            while exists:
                deps.add(current_name, query.name)
                current_query = regex(query.name).sub(
                    f'\\1{query.new_name}\\3',
                    current_query
                )
                exists = regex(query.name).search(current_query)

    return current_query


def get_subquery(query: str) -> str:
    """Extract the subquery from given partial query"""
    limited = query[query.index('('):].strip()
    # find closing location
    index = -1
    stack = []
    open_char = ["("]
    close_char = {")": "("}

    for char in limited:
        index += 1
        if char in open_char:
            stack.append(char)
            continue

        if char in close_char and stack[-1] == close_char[char]:
            stack.pop()

        if not stack:
            return limited[1:index]

    assert False, 'Error, closing parenthesis not found for partial query'
    return query


def split_quey(
        content: str,
        tmp_db: str,
        tmp_schema: str) -> TDependencies:
    """ Divedes the query."""
    splits = list(RE_WITH.finditer(content))
    sub_tables = list()
    deps = TDependencies()

    print('\n')
    for i, split in enumerate(splits):
        start = split.start()
        end = (
                len(content) - 1 if i == len(splits) - 1
                else splits[i + 1].start())

        print(split, f'from {start} to {end}')
        query = RE_SUBQUERY.findall(content[start:end])

        assert query and len(query[0]) == 3,\
               f'\n\nUnsuported subquery: {content[start:end]}\n' + \
               f'using {RE_SUBQUERY}'

        table_name = query[0][0]
        # subquery = query[0][1]
        subquery = get_subquery(content[start:end])

        # Generate temporary table and replace table references
        sub_tables.append(SubQuery(
            table_name,
            update_query(sub_tables, subquery, deps, table_name),
            tmp_db,
            tmp_schema))

        deps.link(table_name, sub_tables[-1])

    print('\n')

    select = RE_FINAL_SELECT.findall(content[start:])
    assert isinstance(select, list) and len(select) == 1, \
           f'Unsuported final query: {content[start:]}'

    select = update_query(sub_tables, select[-1], deps, 'select')
    deps.link('select', select)

    return deps
