from dataclasses import dataclass
from typing import List, Union
import os
import re

# TAC instruction representation
@dataclass
class TACInstruction:
    result: str
    op1: str
    operator: str = None
    op2: str = None

TACLine = Union[TACInstruction, str]

def read_tac_from_file_3(file_path: str) -> List[TACLine]:
    """Reads TAC from file, preserving control flow and parsing valid instructions."""
    tac = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            # Control or label lines
            if (line.endswith(":") or
                line.startswith("goto") or
                line.startswith("if") or
                line.startswith("ifFalse") or
                line.startswith("print")):
                tac.append(line)
                continue

            # Match binary op: x = y op z
            match_bin = re.match(r"^(\w+)\s*=\s*(\w+)\s*([\+\-\*/])\s*(\w+)$", line)
            match_assign = re.match(r"^(\w+)\s*=\s*(\w+)$", line)

            if match_bin:
                result, op1, operator, op2 = match_bin.groups()
                tac.append(TACInstruction(result=result, op1=op1, operator=operator, op2=op2))
            elif match_assign:
                result, op1 = match_assign.groups()
                tac.append(TACInstruction(result=result, op1=op1))
            else:
                tac.append(line)  # Preserve any unknown line

    return tac

def find_used_variables(tac: List[TACLine]) -> set:
    """Scan TAC to find all variables that are used after being defined."""
    used = set()

    for instr in tac:
        if isinstance(instr, str):
            matches = re.findall(r'\b\w+\b', instr)
            for token in matches:
                if token not in {'goto', 'if', 'ifFalse', 'print'} and not token.endswith(':'):
                    used.add(token)
        else:
            if instr.op1 and not instr.op1.replace('.', '', 1).isdigit():
                used.add(instr.op1)
            if instr.op2 and not instr.op2.replace('.', '', 1).isdigit():
                used.add(instr.op2)

    return used

def dead_code_elimination(tac: List[TACLine]) -> List[TACLine]:
    used_vars = find_used_variables(tac)
    optimized = []

    for instr in tac:
        if isinstance(instr, TACInstruction):
            if instr.result in used_vars:
                optimized.append(instr)
        else:
            optimized.append(instr)

    return optimized

def save_tac_to_file_3(tac: List[TACLine], file_path: str):
    with open(file_path, "w", encoding="utf-8") as f:
        for instr in tac:
            if isinstance(instr, str):
                f.write(instr + "\n")
            elif instr.operator is None:
                f.write(f"{instr.result} = {instr.op1}\n")
            else:
                f.write(f"{instr.result} = {instr.op1} {instr.operator} {instr.op2}\n")


