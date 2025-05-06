class SemanticAnalyzer:
    def _init_(self):
        self.symbol_table = {}
        self.errors = []

    def analyze(self, ast):
        """Traverses the AST and performs semantic analysis."""
        self.errors = []  # Reset errors
        self.symbol_table = {}  # Reset symbol table

        for stmt in ast["stmts"]:
            self.handle_statement(stmt)

        return self.symbol_table, self.errors

    def handle_statement(self, stmt):
        stmt_type = stmt["type"]

        if stmt_type == "decl":
            self.handle_declaration(stmt)
        elif stmt_type == "assign":
            self.handle_assignment(stmt)
        elif stmt_type == "while":
            self.handle_while_loop(stmt)
        elif stmt_type == "logop":  # Handles logical operations (&&, ||)
            self.handle_logical_op(stmt)
        elif stmt_type == "unary_op":  # Handles unary operations (++ / --)
            self.handle_unary_op(stmt)
        elif stmt_type == "print":
            self.handle_print(stmt)
        else:
            self.errors.append(f"Unsupported statement type: {stmt_type}")

    def handle_print(self, stmt):
        """Ensures cout << prints only valid types."""
        for expr in stmt["values"]:
            expr_type = self.get_expression_type(expr)
            if expr_type in ["int", "float", "bool", "char", "string"]:
                continue  # ✅ Allowed types
            else:
                self.errors.append(f"Semantic Error: cout cannot print a value of type '{expr_type}'.")

    def handle_declaration(self, stmt):
        """Handles variable declarations, ensuring proper type handling."""
        var_name = stmt["var"]
        var_type = stmt["datatype"]

        if var_name in self.symbol_table:
            self.errors.append(f"Semantic Error: Variable '{var_name}' is already declared.")
            return  # ✅ Stop further processing to prevent type mismatch errors

        self.symbol_table[var_name] = var_type

        if "value" in stmt:
            value_type = self.get_expression_type(stmt["value"])
            if var_type != value_type:
                self.errors.append(
                    f"Type Mismatch: Cannot initialize '{var_name}' of type '{var_type}' "
                    f"with a value of type '{value_type}'."
                )

    def handle_assignment(self, stmt):
        """Ensures assignments use declared variables with correct types."""
        var_name = stmt["var"]
        if var_name not in self.symbol_table:
            self.errors.append(f"Semantic Error: Variable '{var_name}' is used without being declared.")
            return

        expected_type = self.symbol_table[var_name]
        value_type = self.get_expression_type(stmt["value"])

        if expected_type != value_type:
            self.errors.append(
                f"Type Mismatch: Cannot assign a value of type '{value_type}' "
                f"to variable '{var_name}' of type '{expected_type}'."
            )

    def handle_logical_op(self, stmt):
        """Handles logical operations (&&, ||)."""
        left_type = self.get_expression_type(stmt["left"])
        right_type = self.get_expression_type(stmt["right"])

        if left_type == "undefined" or right_type == "undefined":
            return "undefined"

        if left_type == "bool" and right_type == "bool":
            return "bool"
        else:
            self.errors.append(
                f"Type Mismatch: Logical operators require boolean operands, got '{left_type}' and '{right_type}'."
            )
            return "undefined"

    def handle_while_loop(self, stmt):
        """Ensures while-loop conditions evaluate to boolean."""
        condition = stmt["condition"]
        condition_type = self.get_expression_type(condition)

        if condition_type != "bool":
            self.errors.append(f"Semantic Error: While loop condition must evaluate to a boolean, got '{condition_type}'.")

        for inner_stmt in stmt["block"]["stmts"]:
            self.handle_statement(inner_stmt)

    def handle_unary_op(self, stmt):
        """Handles unary operations like increment and decrement."""
        var_name = stmt["var"]

        if var_name not in self.symbol_table:
            self.errors.append(f"Semantic Error: Variable '{var_name}' is used without being declared.")
            return

        var_type = self.symbol_table[var_name]
        if var_type != "int":
            self.errors.append(f"Semantic Error: Unary operation '{stmt['op']}' cannot be applied to type '{var_type}'.")

    def get_expression_type(self, expr):
        """Determines the type of an expression."""
        expr_type = expr["type"]

        if expr_type == "number":
            return "float" if "." in str(expr["value"]) else "int"
        elif expr_type == "boolean":
            return "bool"
        elif expr_type == "string":
            return "string"
        elif expr_type == "character":
            return "char"
        elif expr_type == "id":
            var_name = expr["value"]
            if var_name not in self.symbol_table:
                self.errors.append(f"Semantic Error: Variable '{var_name}' is used without being declared.")
                return "undefined"
            return self.symbol_table[var_name]
        elif expr_type == "relop":  # Handling relational operators (==, !=, <, >)
            left_type = self.get_expression_type(expr["left"])
            right_type = self.get_expression_type(expr["right"])

            if left_type == "undefined" or right_type == "undefined":
                return "undefined"

            if left_type == right_type:
                return "bool"
            else:
                self.errors.append(f"Type Mismatch: Cannot compare '{left_type}' with '{right_type}'.")
                return "undefined"
        elif expr_type == "logop":  # Handling logical operations (&&, ||)
            return self.handle_logical_op(expr)
        elif expr_type == "binop":  # Handling binary operations (+, -, *, /)
            left_type = self.get_expression_type(expr["left"])
            right_type = self.get_expression_type(expr["right"])

            if left_type == "undefined" or right_type == "undefined":
                return "undefined"

            if left_type == right_type and left_type in ["int", "float"]:
                return left_type
            else:
                self.errors.append(f"Type Mismatch: Cannot perform operation on '{left_type}' and '{right_type}'.")
                return "undefined"
        else:
            self.errors.append(f"Unsupported expression type: {expr_type}")
            return "undefined"