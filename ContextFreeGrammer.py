import json

class ContextFreeGrammer:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current_token(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else (None, None)

    def match(self, expected_type):
        token_type, token_value = self.current_token()
        if token_type == expected_type:
            self.pos += 1
            return token_value
        else:
            raise SyntaxError(f"Expected {expected_type} but found {token_type}")

    def parse(self):
        stmts = self.parse_stmt_list()
        return {"type": "block", "stmts": stmts}

    def parse_stmt_list(self):
        stmts = []
        while self.pos < len(self.tokens):
            token_type, _ = self.current_token()
            if token_type in ('INT', 'ID', 'WHILE'):
                stmt = self.parse_stmt()
                if token_type != 'WHILE':
                    self.match('SEMI')
                stmts.append(stmt)
            else:
                break
        return stmts

    def parse_stmt(self):
        token_type, _ = self.current_token()
        if token_type == 'INT':
            return self.parse_declaration()
        elif token_type == 'ID':
            return self.parse_assignment()
        elif token_type == 'WHILE':
            return self.parse_while_stmt()
        else:
            raise SyntaxError("Invalid statement")

    def parse_declaration(self):
        self.match('INT')
        var_name = self.match('ID')
    
        token_type, _ = self.current_token()
        if token_type == 'ASSIGN':
            self.match('ASSIGN')
            expr = self.parse_expr()
            return {'type': 'decl', 'var': var_name, 'datatype': 'int', 'value': expr}
    
        return {'type': 'decl', 'var': var_name, 'datatype': 'int'}


    def parse_assignment(self):
        var_name = self.match('ID')
        self.match('ASSIGN')
        expr = self.parse_expr()
        return {'type': 'assign', 'var': var_name, 'value': expr}

    def parse_expr(self):
        node = self.parse_term()
        while True:
            token_type, token_value = self.current_token()
            if token_type == 'OP' and token_value in ('+', '-'):
                self.match('OP')
                right = self.parse_term()
                node = {'type': 'binop', 'op': token_value, 'left': node, 'right': right}
            else:
                break
        return node

    def parse_term(self):
        node = self.parse_factor()
        while True:
            token_type, token_value = self.current_token()
            if token_type == 'OP' and token_value in ('*', '/'):
                self.match('OP')
                right = self.parse_factor()
                node = {'type': 'binop', 'op': token_value, 'left': node, 'right': right}
            else:
                break
        return node

    def parse_factor(self):
        token_type, token_value = self.current_token()
        if token_type == 'ID':
            self.match('ID')
            return {'type': 'id', 'value': token_value}
        elif token_type == 'NUMBER':
            self.match('NUMBER')
            return {'type': 'number', 'value': token_value}
        elif token_type == 'LPAREN':
            self.match('LPAREN')
            expr = self.parse_expr()
            self.match('RPAREN')
        elif token_type == 'STRING':
            self.pos += 1
            return {'type': 'string', 'value': token_value}

            return expr
        else:
            raise SyntaxError("Invalid factor")

    def parse_while_stmt(self):
        self.match('WHILE')
        self.match('LPAREN')
        condition = self.parse_condition()  # was: self.parse_expr()
        self.match('RPAREN')
        block = self.parse_block()
        return {'type': 'while', 'condition': condition, 'block': block}

    def parse_block(self):
        self.match('LBRACE')
        stmts = self.parse_stmt_list()
        self.match('RBRACE')
        return {'type': 'block', 'stmts': stmts}

    def parse_condition(self):
        left = self.parse_expr()
        token_type, token_value = self.current_token()
        if token_type == 'REL_OP':
            self.match('REL_OP')
            right = self.parse_expr()
            return {'type': 'relop', 'op': token_value, 'left': left, 'right': right}
        return left


def parse_tokens_to_ast(tokens):
    parser = ContextFreeGrammer(tokens)
    ast = parser.parse()
    return ast


def save_ast_to_file(ast, filename='ast.json'):
    with open(filename, 'w') as f:
        json.dump(ast, f, indent=2)
