import json

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current_token(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else (None, None)

    def match(self, expected_type):
        token_type, token_value = self.current_token()
        if token_type == expected_type:
            print(f"Match: {expected_type} → '{token_value}'")
            self.pos += 1
            return token_value
        else:
            raise SyntaxError(f"Expected {expected_type} but found {token_type}")

    def parse(self):
        print("Expanding: PROGRAM → BLOCK")
        stmts = self.parse_stmt_list()
        return {"type": "block", "stmts": stmts}

    def parse_declaration(self):
        print("Expanding: decl → TYPE ID (ASSIGN expr)? SEMI")
        datatype = self.match('TYPE')
        var_name = self.match('ID')

        default_values = {
            "int": 0,
            "float": 0.0,
            "bool": False,
            "string": '""',
            "char": "'\\0'"
        }

        token_type, _ = self.current_token()
        if token_type == 'ASSIGN':
            self.match('ASSIGN')
            expr = self.parse_expr()
            return {'type': 'decl', 'var': var_name, 'datatype': datatype, 'value': expr}

        return {'type': 'decl', 'var': var_name, 'datatype': datatype,
                'value': {'type': datatype, 'value': default_values.get(datatype, "undefined")}}

    def parse_assignment(self):
        print("Expanding: assign → ID ASSIGN expr SEMI")
        var_name = self.match('ID')
        self.match('ASSIGN')
        expr = self.parse_expr()
        return {'type': 'assign', 'var': var_name, 'value': expr}

    def parse_stmt_list(self):
        print("Expanding: BLOCK → stmt_list")
        stmts = []
        while self.pos < len(self.tokens):
            token_type, _ = self.current_token()

            # Handle comments: Skip tokens starting with // until SEMI or RBRACE
            if token_type == 'OP' and self.pos + 1 < len(self.tokens) and self.tokens[self.pos + 1] == ('OP', '/'):
                print("Skipping comment: //")
                self.pos += 2  # Skip the two '/' tokens
                while self.pos < len(self.tokens):
                    token_type, _ = self.current_token()
                    if token_type in ('SEMI', 'RBRACE'):
                        if token_type == 'SEMI':
                            self.pos += 1  # Consume the SEMI after a comment
                        break
                    self.pos += 1
                continue

            if token_type == 'WHILE':
                print("Expanding: stmt_list → while_stmt stmt_list")
                stmt = self.parse_while_stmt()
                stmts.append(stmt)
            elif token_type in ('TYPE', 'ID', 'COUT'):
                print("Expanding: stmt_list → stmt stmt_list")
                stmt = self.parse_stmt()
                # Match SEMI after the statement, unless it's followed by RBRACE
                token_type, _ = self.current_token()
                if token_type == 'SEMI':
                    self.match('SEMI')
                stmts.append(stmt)
            elif token_type == 'RBRACE':
                print("Expanding: stmt_list → ε (end of block)")
                break
            else:
                print("Expanding: stmt_list → ε (end of statements)")
                break
        return stmts

    def parse_stmt(self):
        token_type, _ = self.current_token()

        if token_type == 'TYPE':
            print("Expanding: stmt → decl")
            return self.parse_declaration()
        elif token_type == 'ID':
            next_token_type, _ = self.tokens[self.pos + 1] if self.pos + 1 < len(self.tokens) else (None, None)
            if next_token_type == 'ASSIGN':
                return self.parse_assignment()
            elif next_token_type in ('INCREMENT', 'DECREMENT'):
                return self.parse_increment_decrement()
            elif next_token_type == 'REL_OP':
                return self.parse_expr()
            else:
                raise SyntaxError(f"Unexpected token {next_token_type} after '{token_type}'")
        elif token_type == 'COUT':
            print("Expanding: stmt → print_stmt")
            return self.parse_print_stmt()
        elif token_type == 'WHILE':
            print("Expanding: stmt → while_stmt")
            return self.parse_while_stmt()
        else:
            raise SyntaxError(f"Invalid statement starting with {token_type}")

    def parse_while_stmt(self):
        print("Expanding: while_stmt → WHILE LPAREN expr RPAREN block")
        self.match('WHILE')
        self.match('LPAREN')
        condition = self.parse_expr()
        self.match('RPAREN')
        block = self.parse_block()
        return {'type': 'while', 'condition': condition, 'block': block}

    def parse_print_stmt(self):
        print("Expanding: print_stmt → COUT print_args SEMI")
        self.match('COUT')
        values = []
        while self.current_token()[0] == 'OUTPUT':
            self.match('OUTPUT')
            values.append(self.parse_expr())
        self.match('SEMI')
        return {'type': 'print', 'values': values}

    def parse_block(self):
        print("Expanding: block → LBRACE stmt_list RBRACE")
        self.match('LBRACE')
        stmts = self.parse_stmt_list()
        self.match('RBRACE')
        return {'type': 'block', 'stmts': stmts}

    def parse_increment_decrement(self):
        print("Expanding: unary_op → ID (INCREMENT | DECREMENT)")
        var_name = self.match('ID')
        op_type = self.match(self.current_token()[0])
        return {'type': 'unary_op', 'op': op_type, 'var': var_name}

    def parse_expr(self):
        print("Expanding: expr → term ((OP term)*) | term REL_OP term | expr AND expr | expr OR expr")
        node = self.parse_term()
        while True:
            token_type, token_value = self.current_token()
            if token_type == 'REL_OP':
                print(f"Expanding: expr → term REL_OP term ('{token_value}')")
                self.match('REL_OP')
                right = self.parse_term()
                node = {'type': 'relop', 'op': token_value, 'left': node, 'right': right}
            elif token_type == 'AND':
                print(f"Expanding: expr → expr AND expr ('{token_value}')")
                self.match('AND')
                right = self.parse_expr()
                node = {'type': 'logop', 'op': '&&', 'left': node, 'right': right}
            elif token_type == 'OR':
                print(f"Expanding: expr → expr OR expr ('{token_value}')")
                self.match('OR')
                right = self.parse_expr()
                node = {'type': 'logop', 'op': '||', 'left': node, 'right': right}
            elif token_type == 'OP' and token_value in ('+', '-'):
                print(f"Expanding: expr → term OP term ('{token_value}')")
                self.match('OP')
                right = self.parse_term()
                node = {'type': 'binop', 'op': token_value, 'left': node, 'right': right}
            else:
                break
        return node

    def parse_term(self):
        print("Expanding: term → factor ((OP factor)*)")
        node = self.parse_factor()
        while True:
            token_type, token_value = self.current_token()
            if token_type == 'OP' and token_value in ('*', '/'):
                print(f"Expanding: term → factor OP factor ('{token_value}')")
                self.match('OP')
                right = self.parse_factor()
                node = {'type': 'binop', 'op': token_value, 'left': node, 'right': right}
            else:
                break
        return node

    def parse_factor(self):
        token_type, token_value = self.current_token()
        if token_type in ('ID', 'NUMBER', 'BOOLEAN', 'STRING', 'CHARACTER'):
            print(f"Expanding: factor → {token_type} ('{token_value}')")
            self.match(token_type)
            return {'type': token_type.lower(), 'value': token_value}
        elif token_type == 'LPAREN':
            print("Expanding: factor → LPAREN expr RPAREN")
            self.match('LPAREN')
            expr = self.parse_expr()
            self.match('RPAREN')
            return expr
        else:
            raise SyntaxError(f"Invalid factor: {token_type}")

def parse_tokens_to_ast(tokens):
    parser = Parser(tokens)
    try:
        ast = parser.parse()
        return ast
    except SyntaxError as e:
        print(f"Syntax Error: {e}")
        return None

def save_ast_to_file(ast, filename='ast.json'):
    with open(filename, 'w') as f:
        json.dump(ast, f, indent=2)

# Test the parser with the provided tokens
tokens = [
    ('TYPE', 'int'), ('ID', 'i'), ('ASSIGN', '='), ('NUMBER', '0'), ('SEMI', ';'),
    ('TYPE', 'int'), ('ID', 'limit'), ('ASSIGN', '='), ('NUMBER', '10'), ('SEMI', ';'),
    ('TYPE', 'int'), ('ID', 'sum'), ('ASSIGN', '='), ('NUMBER', '0'), ('SEMI', ';'),
    ('WHILE', 'while'), ('LPAREN', '('), ('ID', 'i'), ('REL_OP', '<'), ('ID', 'limit'), ('RPAREN', ')'),
    ('LBRACE', '{'),
    ('ID', 'i'), ('INCREMENT', '++'), ('SEMI', ';'),
    ('OP', '/'), ('OP', '/'), ('ID', 'hi'),
    ('ID', 'sum'), ('ASSIGN', '='), ('ID', 'sum'), ('OP', '+'), ('ID', 'i'), ('SEMI', ';'),
    ('OP', '/'), ('OP', '/'), ('ID', 'bye'),
    ('RBRACE', '}')
]

ast = parse_tokens_to_ast(tokens)
if ast:
    save_ast_to_file(ast)