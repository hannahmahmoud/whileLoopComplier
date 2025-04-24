
# AST : [{},{},etc ] hwa 3bra 3n list gowha dicts
class SemanticAnalyzer:
    # desc:constructor to initialize a dict for the symbol table and a list errors
    def __init__(self): 
        self.symbol_table = {}
        self.errors = []


   # desc : call visit func and return symbol table  in dict and errors in list  
    def analyze(self, ast): 
        self.visit(ast)
        return self.symbol_table, self.errors

# 
    def visit(self, node):
        if isinstance(node, list): # if my AST is type of list
            for stmt in node:
                self.visit(stmt) # loop in the dicts
        elif isinstance(node, dict):
            node_type = node.get("type")
            if node_type == "decl":
                self.visit_declaration(node) 
            elif node_type == "assign":
                self.visit_assignment(node)
            elif node_type == "binop":
                return self.visit_binop(node)
            elif node_type == "id":
                return self.visit_id(node)
            elif node_type == "number":
                return "int"
            elif node_type == "string":
                return "string"
            elif node_type == "while":
                self.visit_while(node)
            elif node_type == "block":
                self.visit(node["stmts"])

# desc: responisble to make sure that the variable is declared once 
    def visit_declaration(self, node): # node hwa dict el gowa list of AST
        var = node["var"] # bakhod el value of key = var 
        datatype = node["datatype"] # bakhod el value of of key = datatype 
        if var in self.symbol_table: # check if the variable alr exits in symbol table if yes then its declared twice , more
            self.errors.append(f"Semantic Error: Variable '{var}' already declared.")
        else:
            self.symbol_table[var] = datatype

    def visit_assignment(self, node):
        var = node["var"]
        if var not in self.symbol_table: # making sure the variable in declared before assigning it 
            self.errors.append(f"Semantic Error: Variable '{var}' used before declaration.")
            return
        declared_type = self.symbol_table[var] # bgeeb type mn symbol table
        expr_type = self.visit(node["value"]) # recursion calling the vist func 
        if declared_type != expr_type:
            self.errors.append(f"Type Mismatch: Cannot assign '{expr_type}' to variable '{var}' of type '{declared_type}'.")

    def visit_id(self, node):
        var = node["value"]
        if var not in self.symbol_table: # making sure variable is declared 
            self.errors.append(f"Semantic Error: Variable '{var}' used before declaration.")
            return None
        return self.symbol_table[var]

    def visit_binop(self, node):
        left_type = self.visit(node["left"])
        right_type = self.visit(node["right"])
        if left_type != right_type:
            self.errors.append(f"Type Mismatch in binary operation: '{left_type}' vs '{right_type}'")
            return None
        return left_type

    def visit_while(self, node):
        self.visit(node["condition"])
        self.visit(node["block"])
