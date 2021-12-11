from re import compile, DOTALL, IGNORECASE

SP = r'[ \n]+'
RE_WITH = compile(r'(WITH|,)[ \n]+(\w+)[ \n]+AS[ \n]+\(', IGNORECASE)
RE_SUBQUERY = compile(r'[ \n]+(\w+)[ \n]+AS[ \n]+\([ \n]*(.*)\)(SELECT){0,1}', IGNORECASE|DOTALL)
RE_FINAL_SELECT = compile(r'[ \n]+\w+[ \n]+AS[ \n]+\([ \n]*.*\)[ \n]+(SELECT.*);{0,1}', IGNORECASE|DOTALL)