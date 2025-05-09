from dataclasses import dataclass
from typing import List, Optional
import os

# TAC instruction representation
@dataclass
class TACInstruction:
    type: str  # 'assign', 'binop', 'cmp', 'if', 'ifFalse', 'goto', 'label', 'print'
    result: Optional[str] = None  # For assign, binop, cmp
    op1: Optional[str] = None  # For assign, binop, cmp, if, ifFalse
    operator: Optional[str] = None  # For binop, cmp
    op2: Optional[str] = None  # For binop, cmp
    target: Optional[str] = None  # For if, ifFalse, goto, label
    value: Optional[str] = None  # For print

def read_tac_from_file(file_path: str) -> List[TACInstruction]:
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
                
                # If (e.g., if t5 goto L2)
                if parts[0] == 'if':
                    if len(parts) != 4 or parts[2] != 'goto':
                        raise ValueError(f"Invalid if: {line}")
                    tac.append(TACInstruction(type='if', op1=parts[1], target=parts[3]))
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

def is_constant(val: str) -> bool:
    """Check if a string is a numeric constant."""
    try:
        float(val)
        return True
    except (ValueError, TypeError):
        return False

def loop_invariant_code_motion(tac: List[TACInstruction]) -> List[TACInstruction]:
    """Perform loop-invariant code motion on TAC."""
    # Step 1: Collect all labels
    labels = {}
    for i, instr in enumerate(tac):
        if instr.type == 'label':
            labels[instr.target] = i

    # Step 2: Identify loop structure
    loop_start = None  # Index of L1
    loop_body_start = None  # Index of first instruction after L1
    loop_condition = None  # Index of ifFalse
    loop_end = None  # Index of goto L1
    loop_exit = None  # Index of L2
    
    for i, instr in enumerate(tac):
        if instr.type == 'goto' and instr.target in labels and labels[instr.target] < i:
            loop_end = i
        if instr.type == 'ifFalse' and instr.target in labels:
            loop_condition = i
            loop_exit = labels[instr.target]
        if instr.type == 'label' and instr.target == 'L1':
            loop_start = i
            loop_body_start = i + 1
    
    if not (loop_start is not None and loop_body_start and loop_condition is not None and loop_end is not None and loop_exit is not None):
        print("No valid while loop found; returning original TAC")
        print(f"Debug: loop_start={loop_start}, loop_body_start={loop_body_start}, loop_condition={loop_condition}, loop_end={loop_end}, loop_exit={loop_exit}")
        return tac

    print(f"Loop detected: start={loop_start}, body_start={loop_body_start}, condition={loop_condition}, end={loop_end}, exit={loop_exit}")

    # Step 3: Identify defined and used variables
    defined_vars = set()
    used_vars = set()
    for instr in tac:
        if instr.type in {'assign', 'binop', 'cmp'}:
            defined_vars.add(instr.result)
        if instr.type in {'binop', 'cmp'}:
            used_vars.add(instr.op1)
            if instr.op2:
                used_vars.add(instr.op2)
        elif instr.type == 'assign':
            used_vars.add(instr.op1)
        elif instr.type in {'if', 'ifFalse'}:
            used_vars.add(instr.op1)
        elif instr.type == 'print':
            used_vars.add(instr.value)

    # Step 4: Find loop-invariant instructions iteratively
    invariant_instrs = []
    loop_vars = set()
    invariant_vars = set()  # Variables defined by invariant instructions
    for i in range(loop_body_start, loop_end + 1):
        instr = tac[i]
        if instr.type in {'assign', 'binop', 'cmp'}:
            loop_vars.add(instr.result)
    
    print("Loop variables (defined in loop):", loop_vars)
    
    # Iteratively find invariant instructions
    changed = True
    while changed:
        changed = False
        for i in range(loop_body_start, loop_end + 1):
            instr = tac[i]
            if (i, instr) in invariant_instrs:
                continue  # Already marked as invariant
            if instr.type == 'binop':
                op1_val = instr.op1
                op2_val = instr.op2
                if ((is_constant(op1_val) or op1_val in invariant_vars or (op1_val not in loop_vars)) and
                    (is_constant(op2_val) or op2_val in invariant_vars or (op2_val not in loop_vars))):
                    invariant_instrs.append((i, instr))
                    invariant_vars.add(instr.result)
                    changed = True
                    print(f"Invariant: {instr}")
            elif instr.type == 'cmp':
                op1_val = instr.op1
                op2_val = instr.op2
                if ((is_constant(op1_val) or op1_val in invariant_vars or (op1_val not in loop_vars)) and
                    (is_constant(op2_val) or op2_val in invariant_vars or (op2_val not in loop_vars))):
                    invariant_instrs.append((i, instr))
                    invariant_vars.add(instr.result)
                    changed = True
                    print(f"Invariant: {instr}")
            elif instr.type == 'assign':
                op1_val = instr.op1
                if is_constant(op1_val) or op1_val in invariant_vars or (op1_val not in loop_vars):
                    invariant_instrs.append((i, instr))
                    invariant_vars.add(instr.result)
                    changed = True
                    print(f"Invariant: {instr}")

    # Step 5: Move invariant instructions to preheader
    
    new_tac = []
    invariant_indices = {i for i, _ in invariant_instrs}
    preheader_inserted = False
    
    for i, instr in enumerate(tac):
        if i == loop_start and invariant_instrs and not preheader_inserted:
            # Sort invariant instructions by original order to maintain dependencies
            for idx, inv_instr in sorted(invariant_instrs, key=lambda x: x[0]):
                new_tac.append(inv_instr)
            preheader_inserted = True
        
        if i in invariant_indices:
            continue
        
        new_tac.append(instr)
    
    return new_tac

def save_tac_to_file(tac: List[TACInstruction], file_path: str):
    """Save optimized TAC to a text file."""
    with open(file_path, 'w') as f:
        for instr in tac:
            if instr.type == 'label':
                f.write(f"{instr.target}:\n")
            elif instr.type == 'goto':
                f.write(f"goto {instr.target}\n")
            elif instr.type == 'if':
                f.write(f"if {instr.op1} goto {instr.target}\n")
            elif instr.type == 'ifFalse':
                f.write(f"ifFalse {instr.op1} goto {instr.target}\n")
            elif instr.type == 'print':
                f.write(f"print {instr.value}\n")
            elif instr.type == 'assign':
                f.write(f"{instr.result} = {instr.op1}\n")
            elif instr.type == 'binop':
                f.write(f"{instr.result} = {instr.op1} {instr.operator} {instr.op2}\n")
            elif instr.type == 'cmp':
                f.write(f"{instr.result} = {instr.op1} {instr.operator} {instr.op2}\n")



