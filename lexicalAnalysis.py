import re # python bulid in regular expression module 
# provide tool like match , maniplulate ...etc

# 3mleen list of tuples ashan ykon immutable type zy const kda myfn3sh dataa tkon ttghyar
token_specification = [
    ('INT',        r'int'),
    ('Float',        r'float'),
    ('CHAR',        r'char'),
    ('LONG',        r'long'),
    ('Short',        r'short'),
    ('Double',        r'double'),
    ('WHILE',      r'\bwhile\b'), 
    ('AND',        r'\band\b'),
    ('OR',         r'\bor\b'),
    ('REL_OP',     r'==|!=|<=|>=|<|>'),
    ('ASSIGN',     r'='),
    ('OP',         r'\+|-|\*|/'),
    ('NUMBER',     r'\b\d+(\.\d+)?\b'),
    ('ID',         r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'),
    ('LPAREN',     r'\('),
    ('RPAREN',     r'\)'),
    ('LBRACE',     r'\{'),
    ('RBRACE',     r'\}'),
    ('SEMI',       r';'),
    ('SKIP',       r'[ \t]+'),     # Skip whitespace
    ('NEWLINE',    r'\n'),         # Newlines
    ('COMMENT',    r'#.*'),  
    
       
    # Line comments
]

#\bexpression\b: This pattern will match the word expression only when it is a complete word, 
# not part of another word. The \b ensures that expression is surrounded by word boundaries 
# (i.e., spaces, punctuation, or the start/end of the string).

# Master regex
token_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_specification) 
# create a one  regular expression  beh eny b3ml eh ba bahot kol haga m3 type bt3ha yaeny 
#(?P<WHILE>\bwhile\b)|?P<AND>\band\b)|(?P<OR>\bor\b)|(?P<REL_OP>==|!=|<=|>=|<|>)| KDA BA LAGHET MAH AKHLSS
#f'(...)' syntax you are referring to is an example of f-string formatting (also called formatted string

get_token = re.compile(token_regex).match
#This compiles the token_regex into a regex object, which allows it to be used for matching operations efficiently.
#.match: The match method is then extracted from the compiled regex, which is used to match the token patterns against the input code.
# hena hwa match baa el hagat bzbt el mowgoda fe input code leh token specification lakn fe kolo yaeny masln low 
# while (x>5)
#{i++;} ana hena msh mstghdma ba \t aw hagat dehh fah deh ba mowgoda bs empty fe token regex , bs msh mowgoda fe get_token 
def lexer_from_file(file_path):
    with open(file_path, 'r') as file:
        code = file.read()

    tokens = [] # empty list to save in it the token 
    position = 0
    line = 1
    match_object = get_token(code, position) # it holds the result of matching your big regex at position position in the code.
    while match_object: # loop untill its match_object is null ba loop gowa el object yaeny 
        kind = match_object.lastgroup #  # which token type matched (e.g., WHILE, ID, REL_OP, .)
        value = match_object.group() #  # what actual text matched (e.g., "while", "x", etc.)
        if kind == 'NEWLINE':
            line += 1
        elif kind == 'SKIP' or kind == 'COMMENT':
            pass
        else:
            tokens.append((kind, value))
        position = match_object.end()  # move to the next part of the code
        match_object = get_token(code, position)  #


    if position != len(code):
        raise RuntimeError(f"Illegal character at line {line}")

    return tokens