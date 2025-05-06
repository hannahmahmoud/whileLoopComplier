import re  # python bulid in regular expression module

# provide tool like match , maniplulate ...etc

# 3mleen list of tuples ashan ykon immutable type zy const kda myfn3sh dataa tkon ttghyar
token_specification = [
    ('COUT', r'\bcout\b'),  # Recognize cout
    ('OUTPUT', r'<<'), 
    ('WHILE', r'\bwhile\b'),  # Recognize "while"
    ('TYPE', r'\b(int|float|char|long|short|double|string|bool)\b'),# Recognize types
    ('BOOLEAN', r'\b(true|false)\b'),  # Recognize boolean literals
    ('CHARACTER', r"'[^']'"),  # Match any single character
    ('AND', r'&&'),  # Logical AND
    ('OR', r'\|\|'),  # Logical OR
    ('REL_OP', r'==|!=|<=|>=|<|>'),  # Relational operators
    ('ASSIGN', r'='),  # Assignment operator
    ('INCREMENT', r'\+\+'),  # Increment operator
    ('DECREMENT', r'--'),  # Decrement operator
    ('NUMBER', r'\b\d+(\.\d+)?\b'),  # Integer and floating-point numbers
    ('ID', r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'),  # Identifiers
    ('STRING', r'"[^"]*"'),  # String literals
    ('OP', r'[+\-*/]'),  # Arithmetic operators
     # Recognize output operator (<<)
    ('LPAREN', r'\('),  # Left parenthesis
    ('RPAREN', r'\)'),  # Right parenthesis
    ('LBRACE', r'\{'),  # Left brace
    ('RBRACE', r'\}'),  # Right brace
    ('SEMI', r';'),  # Semicolon
    ('SKIP', r'[ \t]+'),  # Skip whitespace
    ('NEWLINE', r'\n'),  # Newlines
    ('COMMENT', r'#.*'),  # Comments
]



# \bexpression\b: This pattern will match the word expression only when it is a complete word,
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
        elif kind == 'SKIP' or kind == 'COMMENT' :
            pass

        else:
            tokens.append((kind, value))
        position = match_object.end()  # move to the next part of the code
        match_object = get_token(code, position)  #


    if position != len(code):
        raise RuntimeError(f"Illegal character at line {line}")
    return tokens

from lexicalAnalysis import get_token  # Ensure token matching is imported



def lexer_without_declarations(file_path):
    """Extracts and prints tokens while skipping declaration lines."""
    with open(file_path, 'r') as file:
        code_lines = file.readlines()

    tokens = []  # Store non-declaration tokens
    for line in code_lines:
        if re.search(r'\b(int|float|char|long|short|double|string|bool)\b', line):  # Skip declaration lines
            continue  # ✅ Ignore entire declaration line

        position = 0
        match_object = get_token(line, position)

        while match_object:
            kind = match_object.lastgroup  # Token type
            value = match_object.group()  # Matched value

            if kind not in ['SKIP', 'COMMENT']:  # Ignore spaces & comments
                tokens.append(value)  # ✅ Store only the token values

            position = match_object.end()
            match_object = get_token(line, position)

    # ✅ Remove any newline characters from tokens
    tokens = [token for token in tokens if token != '\n']

    # ✅ Print the cleaned token list
    print("📌 Token Values (Without Declarations & Newlines):")
    print(tokens)  # ✅ Prints as a list

    return tokens  # ✅ Returns token values as a list