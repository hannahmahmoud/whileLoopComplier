import re

class commonSubElmination:
    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path

    def read_tac(self):
        with open(self.input_path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f.readlines()]

    def write_tac(self, optimized_tac):
        with open(self.output_path, "w", encoding="utf-8") as f:
            for line in optimized_tac:
                f.write(line + "\n")

    def extract_expr(self, line):
        """Extract an expression like 'a + b' from 't3 = a + b'"""
        match = re.match(r"^(t\d+)\s*=\s*(\w+)\s*([\+\-\*/<>=!]+)\s*(\w+)$", line)
        if match:
            temp, op1, operator, op2 = match.groups()
            return f"{op1} {operator} {op2}", temp
        return None, None

    def get_assigned_var(self, line):
        match = re.match(r"^(\w+)\s*=", line)
        return match.group(1) if match else None

    def get_rhs(self, line):
        match = re.match(r"^\w+\s*=\s*(.+)", line)
        return match.group(1).strip() if match else None

    def optimize_tac(self):
        tac_lines = self.read_tac()
        expr_map = {}  # {expression_str: temp_var}
        temp_replacements = {}  # {old_temp: new_temp}
        optimized = []

        for line in tac_lines:
            if not line or line.endswith(":") or line.startswith("if") or line.startswith("goto") or line.startswith("print"):
                optimized.append(line)
                continue

            expr, current_temp = self.extract_expr(line)

            if expr:
                if expr in expr_map:
                    temp_replacements[current_temp] = expr_map[expr]
                    # Skip this line, as it's redundant
                    continue
                else:
                    expr_map[expr] = current_temp
                    optimized.append(line)
            else:
                # Check for assignments and apply temp replacements
                lhs = self.get_assigned_var(line)
                rhs = self.get_rhs(line)

                for old_temp, new_temp in temp_replacements.items():
                    if rhs and old_temp in rhs:
                        rhs = rhs.replace(old_temp, new_temp)
                optimized.append(f"{lhs} = {rhs}" if rhs else line)

        self.write_tac(optimized)