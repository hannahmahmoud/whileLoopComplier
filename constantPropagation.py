from dataclasses import dataclass
from typing import List, Optional
import os

# TAC instruction representation
@dataclass
class TACInstruction:
    type: str  # 'assign', 'binop', 'cmp', 'label', 'ifFalse', 'goto', 'print'
    result: Optional[str] = None  # For assign, binop, cmp
    op1: Optional[str] = None  # For assign, binop, cmp, ifFalse
    operator: Optional[str] = None  # For binop, cmp
    op2: Optional[str] = None  # For binop, cmp
    target: Optional[str] = None  # For label, ifFalse, goto
    value: Optional[str] = None  # For print

def read_tac_from_file_2(file_path: str) -> List[TACInstruction]:
    """Read TAC instructions from a text file."""
    tac = []
    try:
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                parts = line.split()
                if not parts:
                    raise ValueError(f"Empty instruction: {line}")
                
                # Label (e.g., L1:)
                if parts[0].endswith(':'):
                    label = parts[0][:-1]
                    tac.append(TACInstruction(type='label', target=label))
                    continue
                
                # Goto (e.g., goto L2)
                if parts[0] == 'goto':
                    if len(parts) != 2:
                        raise ValueError(f"Invalid goto: {line}")
                    tac.append(TACInstruction(type='goto', target=parts[1]))
                    continue
                
                # IfFalse (e.g., ifFalse t5 goto L2)
                if parts[0] == 'ifFalse':
                    if len(parts) != 4 or parts[2] != 'goto':
                        raise ValueError(f"Invalid ifFalse: {line}")
                    tac.append(TACInstruction(type='ifFalse', op1=parts[1], target=parts[3]))
                    continue
                
                # Print (e.g., print i)
                if parts[0] == 'print':
                    if len(parts) != 2:
                        raise ValueError(f"Invalid print: {line}")
                    tac.append(TACInstruction(type='print', value=parts[1]))
                    continue
                
                # Assignment or binary/comparison operation
                if len(parts) < 3 or parts[1] != '=':
                    raise ValueError(f"Invalid instruction: {line}")
                
                result, rest = parts[0], parts[2:]
                if len(rest) == 1:
                    # Assignment: result = op1
                    tac.append(TACInstruction(type='assign', result=result, op1=rest[0]))
                elif len(rest) == 3:
                    # Binary operation or comparison: result = op1 operator op2
                    op1, operator, op2 = rest
                    if operator in {'+', '-', '*', '/'}:
                        tac.append(TACInstruction(type='binop', result=result, op1=op1, operator=operator, op2=op2))
                    elif operator in {'<', '>', '<=', '>=', '==', '!='}:
                        tac.append(TACInstruction(type='cmp', result=result, op1=op1, operator=operator, op2=op2))
                    else:
                        raise ValueError(f"Invalid operator {operator} in: {line}")
                else:
                    raise ValueError(f"Malformed instruction: {line}")
        
        return tac
    except FileNotFoundError:
        raise FileNotFoundError(f"TAC file not found: {file_path}")
    except Exception as e:
        raise ValueError(f"Error parsing TAC file: {str(e)}")

def constant_propagation(tac: List[TACInstruction]) -> List[TACInstruction]:
    """Perform constant propagation on TAC instructions, avoiding loop-modified variables."""
    # Helper to check if a string is a numeric constant
    def is_constant(val: str) -> bool:
        try:
            float(val)  # Works for integers and floats
            return True
        except (ValueError, TypeError):
            return False

    # Helper to check if a string is an integer constant
    def is_integer(val: str) -> bool:
        try:
            int_val = int(val)
            return str(int_val) == val  # Ensure no decimal or scientific notation
        except (ValueError, TypeError):
            return False

    # Helper to evaluate a binary or comparison operation
    def evaluate(op1: str, operator: str, op2: str) -> str:
        x, y = float(op1), float(op2)
        if operator == '+':
            result = x + y
        elif operator == '-':
            result = x - y
        elif operator == '*':
            result = x * y
        elif operator == '/':
            if y == 0:
                raise ValueError("Division by zero")
            result = x / y
        elif operator in {'<', '>', '<=', '>=', '==', '!='}:
            # Evaluate comparison
            if operator == '<':
                result = x < y
            elif operator == '>':
                result = x > y
            elif operator == '<=':
                result = x <= y
            elif operator == '>=':
                result = x >= y
            elif operator == '==':
                result = x == y
            elif operator == '!=':
                result = x != y
            return '1' if result else '0'  # Boolean result as 1 or 0
        else:
            raise ValueError(f"Unknown operator: {operator}")
        
        # Return integer if both inputs are integers and result is whole
        if is_integer(op1) and is_integer(op2) and result.is_integer():
            return str(int(result))
        return str(result)

    # Step 1: Identify loop structure and modified variables
    labels = {}
    loop_start = None
    loop_body_start = None
    loop_end = None
    loop_modified_vars = set()

    # Collect labels and detect loop
    for i, instr in enumerate(tac):
        if instr.type == 'label':
            labels[instr.target] = i
        if instr.type == 'label' and instr.target == 'L1':
            loop_start = i
            loop_body_start = i + 1
        if instr.type == 'goto' and instr.target in labels and labels[instr.target] < i:
            loop_end = i

    # Collect variables modified in the loop
    if loop_start is not None and loop_body_start is not None and loop_end is not None:
        for i in range(loop_body_start, loop_end + 1):
            instr = tac[i]
            if instr.type in {'assign', 'binop', 'cmp'}:
                loop_modified_vars.add(instr.result)

    print("Loop-modified variables:", loop_modified_vars)

    # Step 2: Constant propagation
    constants = {}  # Tracks known constant values
    new_tac = []
    in_loop = False

    for i, instr in enumerate(tac):
        # Track if we're inside the loop
        if instr.type == 'label' and instr.target == 'L1':
            in_loop = True
            # Clear constants for loop-modified variables
            for var in loop_modified_vars:
                constants.pop(var, None)
        elif instr.type == 'label' and instr.target == 'L2':
            in_loop = False

        # Pass through non-computational instructions
        if instr.type in {'label', 'ifFalse', 'goto', 'print'}:
            new_tac.append(instr)
            continue
        
        # Case 1: Assignment (e.g., t1 = 8 or i = t3)
        if instr.type == 'assign':
            op1_val = constants.get(instr.op1, instr.op1)
            if is_constant(op1_val) and (not in_loop or instr.result not in loop_modified_vars):
                # Fold to direct constant assignment
                constants[instr.result] = op1_val
                new_tac.append(TACInstruction(type='assign', result=instr.result, op1=op1_val))
            else:
                # Keep non-constant assignment
                new_tac.append(TACInstruction(type='assign', result=instr.result, op1=op1_val))
                constants[instr.result] = op1_val
        
        # Case 2: Binary or comparison operation (e.g., t3 = t1 * t2, t5 = i < t4)
        elif instr.type in {'binop', 'cmp'}:
            op1_val = instr.op1 if in_loop and instr.op1 in loop_modified_vars else constants.get(instr.op1, instr.op1)
            op2_val = instr.op2 if in_loop and instr.op2 in loop_modified_vars else constants.get(instr.op2, instr.op2)

            # Fold if both operands are constants
            if is_constant(op1_val) and is_constant(op2_val) and (not in_loop or instr.result not in loop_modified_vars):
                result = evaluate(op1_val, instr.operator, op2_val)
                new_tac.append(TACInstruction(type='assign', result=instr.result, op1=result))
                constants[instr.result] = result
            else:
                # Keep instruction with propagated operands
                new_tac.append(TACInstruction(
                    type=instr.type,
                    result=instr.result,
                    op1=op1_val,
                    operator=instr.operator,
                    op2=op2_val
                ))
                constants[instr.result] = instr.result

    return new_tac

def save_tac_to_file_2(tac: List[TACInstruction], file_path: str):
    """Save optimized TAC to a text file."""
    with open(file_path, 'w') as f:
        for instr in tac:
            if instr.type == 'label':
                f.write(f"{instr.target}:\n")
            elif instr.type == 'goto':
                f.write(f"goto {instr.target}\n")
            elif instr.type == 'ifFalse':
                f.write(f"ifFalse {instr.op1} goto {instr.target}\n")
            elif instr.type == 'print':
                f.write(f"print {instr.value}\n")
            elif instr.type == 'assign':
                f.write(f"{instr.result} = {instr.op1}\n")
            elif instr.type in {'binop', 'cmp'}:
                f.write(f"{instr.result} = {instr.op1} {instr.operator} {instr.op2}\n")


