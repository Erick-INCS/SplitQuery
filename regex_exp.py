"""Regular expressions."""
from re import compile as c, DOTALL, IGNORECASE

SP = r'[ \n]+'
SPO = r'[ \n]*'
RE_WITH = c(r'(WITH[ \n]+|,[ \n]*)([\w\."]+)[ \n]+AS[ \n]+\(', IGNORECASE)
RE_SUBQUERY = c(
    r'[ \n]*([\w\."]+)[ \n]+AS[ \n]+\([ \n]*(.*)[ \n]*\)(SELECT){0,1}',
    IGNORECASE | DOTALL
)
RE_FINAL_SELECT = c(
    r'[ \n]+[\w\."]+[ \n]+AS[ \n]+\([ \n]*.*\)[ \n]+(SELECT.*);{0,1}',
    IGNORECASE | DOTALL
)


def sre_tbl_name(table: str) -> str:
    """Return the regex equivalence to a table name."""
    def add_quotes(text: str) -> str:
        return f'"{text}"'

    alt_name = '.'.join(map(add_quotes, table.split('.')))

    return f'{table.strip()}|{alt_name}'


def re_table_ref_field(table: str):
    """Return Regex to find a table reference in select."""
    table = sre_tbl_name(table)
    return c(
        # f'({SP}){table}(\\.\\w+.+{SP}FROM{SP})',
        f'({SP})({table})(\\."?\\w+"?.+{SP})',
        IGNORECASE | DOTALL
    )


def re_table_ref_comb(table: str):
    """Return Regex to find a table reference by compination query."""
    def wsp(name: str) -> str:
        return f'{SP}{name}{SP}'

    keys_words = ['FROM', f'UNION{SP}ALL', 'UNION', f'MERGE{SP}INTO', 'JOIN']
    expr = f'({"|".join(map(wsp, keys_words))})({table})({SP})'

    return c(
        expr,
        IGNORECASE | DOTALL
    )


RE_LIST_TB_REF = [
    re_table_ref_comb,
    re_table_ref_field,
]
