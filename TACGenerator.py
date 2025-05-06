class TACGenerator:
    def __init__(self):
        self.tac = []  # List to store TAC instructions
        self.temp_count = 1  # Counter for temporary variables (t1, t2, ...)
        self.label_count = 1  # Counter for labels (L1, L2, ...)

    def new_temp(self):
        """Generate a new temporary variable name."""
        temp = f"t{self.temp_count}"
        self.temp_count += 1
        return temp

    def new_label(self):
        """Generate a new label name."""
        label = f"L{self.label_count}"
        self.label_count += 1
        return label

    def emit(self, instruction):
        """Add a TAC instruction to the output."""
        self.tac.append(instruction)

    def generate_expression(self, node):
        """Generate TAC for an expression (e.g., number, id, binop, relop, logop)."""
        if node["type"] == "number":
            temp = self.new_temp()
            self.emit(f"{temp} = {node['value']}")
            return temp
        elif node["type"] == "boolean":
            temp = self.new_temp()
            self.emit(f"{temp} = {node['value']}")
            return temp
        elif node["type"] == "string":
            temp = self.new_temp()
            self.emit(f"{temp} = {node['value']}")
            return temp
        elif node["type"] == "character":
            temp = self.new_temp()
            self.emit(f"{temp} = {node['value']}")
            return temp
        elif node["type"] == "id":
            return node["value"]
        elif node["type"] == "binop":
            left = self.generate_expression(node["left"])
            right = self.generate_expression(node["right"])
            temp = self.new_temp()
            if node["op"] in ["+", "-", "*", "/"]:
                self.emit(f"{temp} = {left} {node['op']} {right}")
            else:
                raise ValueError(f"Unsupported binary operator: {node['op']}")
            return temp
        elif node["type"] == "relop":
            left = self.generate_expression(node["left"])
            right = self.generate_expression(node["right"])
            temp = self.new_temp()
            if node["op"] in ["==", "!=", "<", ">", "<=", ">="]:
                self.emit(f"{temp} = {left} {node['op']} {right}")
            else:
                raise ValueError(f"Unsupported relational operator: {node['op']}")
            return temp
        elif node["type"] == "logop":
            left = self.generate_expression(node["left"])
            right = self.generate_expression(node["right"])
            temp = self.new_temp()
            op = "and" if node["op"] == "&&" else "or" if node["op"] == "||" else None
            if not op:
                raise ValueError(f"Unsupported logical operator: {node['op']}")
            self.emit(f"{temp} = {left} {op} {right}")
            return temp
        else:
            raise ValueError(f"Unsupported expression type: {node['type']}")

    def generate_statement(self, node):
        """Generate TAC for a statement (e.g., decl, assign, unary_op, while, block)."""
        if node["type"] == "decl":
            # Handle variable declaration (e.g., bool x = true)
            target = node["var"]
            value = self.generate_expression(node["value"])
            self.emit(f"{target} = {value}")
        elif node["type"] == "assign":
            # Handle assignment (e.g., str = "marar")
            target = node["var"]
            value = self.generate_expression(node["value"])
            self.emit(f"{target} = {value}")
        elif node["type"] == "unary_op":
            # Handle increment/decrement (e.g., x++, x--)
            target = node["var"]
            op = "+" if node["op"] in ["INCREMENT", "++"] else "-" if node["op"] in ["DECREMENT", "--"] else None
            if not op:
                raise ValueError(f"Unsupported unary operator: {node['op']}")
            temp = self.new_temp()
            self.emit(f"{temp} = {target} {op} 1")
            self.emit(f"{target} = {temp}")
        elif node["type"] == "while":
            # Handle while loop
            loop_start = self.new_label()
            loop_end = self.new_label()

            # Emit loop start label
            self.emit(f"{loop_start}:")

            # Generate TAC for the condition
            condition = self.generate_expression(node["condition"])
            self.emit(f"ifFalse {condition} goto {loop_end}")

            # Generate TAC for the loop body (always a block)
            if node["block"]["type"] == "block":
                for stmt in node["block"]["stmts"]:
                    self.generate_statement(stmt)
            else:
                raise ValueError(f"Expected block in while loop, got {node['block']['type']}")

            # Jump back to loop start
            self.emit(f"goto {loop_start}")

            # Emit loop end label
            self.emit(f"{loop_end}:")
        elif node["type"] == "print":
            self.generate_print(node)
        elif node["type"] == "block":# Handle block node by processing each statement in stmts

            for stmt in node["stmts"]:
                self.generate_statement(stmt)
        else:
            raise ValueError(f"Unsupported statement type: {node['type']}")

    def generate_print(self, node):
        """Generate TAC for cout << statements."""
        for expr in node["values"]:
            value = self.generate_expression(expr)
            self.emit(f"print {value}")  # ✅ Emits TAC for printing the value

    def generate_tac(self, ast):
        """Generate TAC for the entire AST."""
        self.tac = []  # Reset TAC list
        self.temp_count = 1  # Reset temporary variable counter
        self.label_count = 1  # Reset label counter

        # Process the AST root (block node)
        if ast["type"] == "block":
            for stmt in ast["stmts"]:
                self.generate_statement(stmt)
        else:
            self.generate_statement(ast)

        return self.tac