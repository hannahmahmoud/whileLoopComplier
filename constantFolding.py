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

def read_tac_from_file_1(file_path: str) -> List[Union[str, TACInstruction]]:
    """Strictly read only valid TAC instructions; preserve all others as raw lines."""
    tac = []
    try:
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                # Skip or preserve non-standard lines (labels, jumps, print)
                if (line.endswith(':') or
                    line.startswith('goto') or
                    line.startswith('if') or
                    line.startswith('ifFalse') or
                    line.startswith('print')):
                    tac.append(line)
                    continue

                # Match pattern: x = y or x = y op z
                match_binary = re.match(r"^(\w+)\s*=\s*(\w+)\s*([\+\-\*/])\s*(\w+)$", line)
                match_assign = re.match(r"^(\w+)\s*=\s*(\w+)$", line)

                if match_binary:
                    result, op1, operator, op2 = match_binary.groups()
                    tac.append(TACInstruction(result=result, op1=op1, operator=operator, op2=op2))
                elif match_assign:
                    result, op1 = match_assign.groups()
                    tac.append(TACInstruction(result=result, op1=op1))
                else:
                    # Fallback: preserve unexpected formats as-is
                    tac.append(line)

        return tac
    except FileNotFoundError:
        raise FileNotFoundError(f"TAC file not found: {file_path}")
    except Exception as e:
        raise ValueError(f"Error parsing TAC file: {str(e)}")

def constant_folding(tac: List[Union[str, TACInstruction]]) -> List[Union[str, TACInstruction]]:
    """Perform constant folding on TAC instructions only."""
    def is_constant(val: str) -> bool:
        try:
            float(val)
            return True
        except:
            return False

    def evaluate(op1: str, operator: str, op2: str) -> float:
        x, y = float(op1), float(op2)
        if operator == '+': return x + y
        if operator == '-': return x - y
        if operator == '*': return x * y
        if operator == '/':
            if y == 0:
                raise ValueError("Division by zero")
            return x / y
        raise ValueError(f"Unknown operator: {operator}")

    constants = {}
    folded = []

    for instr in tac:
        # DIFFERENCE: Preserve non-TACInstruction lines without processing
        if not isinstance(instr, TACInstruction):  # DIFFERENCE
            folded.append(instr)
            continue  # DIFFERENCE

        if instr.operator is None and is_constant(instr.op1):
            constants[instr.result] = instr.op1
            folded.append(instr)

        elif instr.operator in {'+', '-', '*', '/'}:
            op1_val = constants.get(instr.op1, instr.op1)
            op2_val = constants.get(instr.op2, instr.op2)

            if is_constant(op1_val) and is_constant(op2_val):
                result = evaluate(op1_val, instr.operator, op2_val)
                constants[instr.result] = str(result)
                folded.append(TACInstruction(result=instr.result, op1=str(result)))
            else:
                folded.append(TACInstruction(
                    result=instr.result,
                    op1=op1_val,
                    operator=instr.operator,
                    op2=op2_val
                ))
        else:
            folded.append(instr)

    return folded

def save_tac_to_file_1(tac: List[Union[str, TACInstruction]], file_path: str):
    """Save TAC instructions to a file."""
    with open(file_path, 'w') as f:
        for instr in tac:
            # DIFFERENCE: Write non-TACInstruction lines directly
            if isinstance(instr, str):  # DIFFERENCE
                f.write(instr + '\n')  # DIFFERENCE
            elif instr.operator is None:
                f.write(f"{instr.result} = {instr.op1}\n")
            else:
                f.write(f"{instr.result} = {instr.op1} {instr.operator} {instr.op2}\n")
