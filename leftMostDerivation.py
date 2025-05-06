import re

# Grammar definition (unchanged)
grammar = {
    'Start': [['L']],
    'S': [
        ['while', '(', 'E', ')', 'S'],
        ['id', '=', 'E', ';'],
        ['id', '++', ';'],
        ['id', '--', ';'],
        ['++', 'id', ';'],
        ['--', 'id', ';'],
        ['{', 'L', '}'],
        ['L']
    ],
    'L': [['S', 'L'], ['ε']],
    'E': [['E1']],
    'E1': [['E2', 'E1\'']],
    'E1\'': [['OP1', 'E2', 'E1\''], ['ε']],
    'E2': [['E3', 'E2\'']],
    'E2\'': [['OP2', 'E3', 'E2\''], ['ε']],
    'E3': [['E4', 'E3\'']],
    'E3\'': [['OP3', 'E4', 'E3\''], ['ε']],
    'E4': [['E5', '++'], ['E5', '--'], ['++', 'E5'], ['--', 'E5'], ['E5']],
    'E5': [['digits'], ['float_literal'], ['string_literal'], ['bool_literal'], ['id'], ['(', 'E', ')']],
    'OP1': [['=='], ['!='], ['<'], ['>'], ['<='], ['>=']],
    'OP2': [['+'], ['-']],
    'OP3': [['*'], ['/']],
    'id': [['letter', 'Z']],
    'Z': [['letter', 'Z'], ['num', 'Z'], ['_', 'Z'], ['ε']],
    'letter': [
        ['a'], ['b'], ['c'], ['d'], ['e'], ['f'], ['g'], ['h'], ['i'], ['j'],
        ['k'], ['l'], ['m'], ['n'], ['o'], ['p'], ['q'], ['r'], ['s'], ['t'],
        ['u'], ['v'], ['w'], ['x'], ['y'], ['z'],
        ['A'], ['B'], ['C'], ['D'], ['E'], ['F'], ['G'], ['H'], ['I'], ['J'],
        ['K'], ['L'], ['M'], ['N'], ['O'], ['P'], ['Q'], ['R'], ['S'], ['T'],
        ['U'], ['V'], ['W'], ['X'], ['Y'], ['Z']
    ],
    'num': [['0'], ['1'], ['2'], ['3'], ['4'], ['5'], ['6'], ['7'], ['8'], ['9']],
    'float_literal': [['digits', '.', 'digits']],
    'digits': [['num', 'digits'], ['num'], ['ε']],
    'string_literal': [['"', 'string_characters', '"']],
    'string_characters': [
        ['letter', 'string_characters'],
        ['num', 'string_characters'],
        ['ε']
    ],
    'bool_literal': [['true'], ['false']]
}

# Terminals (unchanged)
terminals = {
    'while', '(', ')', '++', '--', '==', '!=', '<', '>', '<=', '>=', '+', '-', '*', '/', '"', '.',
    'true', 'false', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
    'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',
    'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1',
    '2', '3', '4', '5', '6', '7', '8', '9', '_', ';', '{', '}', '='
}

# FIRST sets (unchanged)
first_sets = {
    'Start': {'while', 'id', '++', '--', '{', '='},
    'S': {'while', 'id', '++', '--', '{', '='},
    'L': {'while', 'id', '++', '--', '{', '=', 'ε'},
    'E': {'id', 'digits', 'float_literal', 'string_literal', 'bool_literal', '(', '++', '--'},
    'E1': {'id', 'digits', 'float_literal', 'string_literal', 'bool_literal', '(', '++', '--'},
    'E1\'': {'==', '!=', '<', '>', '<=', '>=', 'ε'},
    'E2': {'digits', 'float_literal', 'string_literal', 'bool_literal', '(', '++', '--', 'id'},
    'E2\'': {'+', '-', 'ε'},
    'E3': {'id', 'digits', 'float_literal', 'string_literal', 'bool_literal', '(', '++', '--'},
    'E3\'': {'*', '/', 'ε'},
    'E4': {'id', 'digits', 'float_literal', 'string_literal', 'bool_literal', '(', '++', '--'},
    'E5': {'digits', 'float_literal', 'string_literal', 'bool_literal', 'id', '('},
    'OP1': {'==', '!=', '<', '>', '<=', '>='},
    'OP2': {'+', '-'},
    'OP3': {'*', '/'},
    'id': {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
           'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
           'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'},
    'Z': {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
          'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
          'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7',
          '8', '9', '_', 'ε'},
    'letter': {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
               'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
               'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'},
    'num': {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'},
    'float_literal': {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'},
    'digits': {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'ε'},
    'string_literal': {'"'},
    'string_characters': {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                          'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
                          'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7',
                          '8', '9', 'ε'},
    'bool_literal': {'true', 'false'}
}

# Validation functions (modified to handle .5)
def is_identifier(token):
    return re.match(r'^[a-zA-Z][a-zA-Z0-9_]*$', token) is not None and token not in {'true', 'false'} and not is_digits(token)

def is_float_literal(token):
    return re.match(r'^\d*\.\d+$', token) is not None or token.startswith('.') and re.match(r'^\.\d+$', token) is not None

def is_string_literal(token):
    return re.match(r'^".*"$', token) is not None

def is_digits(token):
    return re.match(r'^\d+$', token) is not None

def is_bool_literal(token):
    return token in {'true', 'false'}

# Preprocessing functions (modified)
def preprocess_numbers(tokens):
    processed = []
    i = 0
    while i < len(tokens):
        if i < len(tokens) and tokens[i] in '0123456789.':
            num = tokens[i]
            i += 1
            while i < len(tokens) and tokens[i] in '0123456789':
                num += tokens[i]
                i += 1
            if i < len(tokens) and tokens[i] == '.':
                num += '.'
                i += 1
                while i < len(tokens) and tokens[i] in '0123456789':
                    num += tokens[i]
                    i += 1
                processed.append(num)  # Keep float literal as single token (e.g., .5, 123.456)
            else:
                processed.append(num)  # Integer or partial float starting with .
        else:
            processed.append(tokens[i])
            i += 1
    return processed

def preprocess_tokens(tokens):
    processed = []
    i = 0
    while i < len(tokens):
        if i + 1 < len(tokens) and tokens[i] == '+' and tokens[i + 1] == '+':
            processed.append('++')
            i += 2
        elif i + 1 < len(tokens) and tokens[i] == '-' and tokens[i + 1] == '-':
            processed.append('--')
            i += 2
        elif re.match(r'^[a-zA-Z]+\+\+$', tokens[i]) or re.match(r'^[a-zA-Z]+--$', tokens[i]):
            identifier = re.match(r'^[a-zA-Z]+', tokens[i]).group(0)
            operator = tokens[i][len(identifier):]
            processed.append(identifier)
            processed.append(operator)
            i += 1
        else:
            processed.append(tokens[i])
            i += 1
    return processed

# Leftmost derivation function (modified)
def leftmost_derivation(tokens):
    tokens = preprocess_numbers(tokens)
    tokens = preprocess_tokens(tokens)
    derivation_steps = [['Start']]
    token_index = 0
    step_count = 0
    max_steps = 10000  # Safeguard against infinite loops

    print(f"Step {step_count}: {' '.join(derivation_steps[-1])}")

    while token_index < len(tokens) or any(s in grammar for s in derivation_steps[-1]):
        if step_count > max_steps:
            print("Error: Infinite loop detected. Exceeding maximum steps.")
            return False

        current_form = derivation_steps[-1]
        new_form = current_form[:]
        replaced = False

        for i, symbol in enumerate(current_form):
            # Handle float_literal specially to derive digits . digits
            if symbol == 'float_literal' and token_index < len(tokens) and is_float_literal(tokens[token_index]):
                float_token = tokens[token_index]
                print(f"Processing float_literal for token {float_token} at index {token_index}")
                # Apply float_literal → digits . digits
                new_form = new_form[:i] + ['digits', '.', 'digits'] + new_form[i+1:]
                derivation_steps.append(new_form)
                step_count += 1
                print(f"Step {step_count}: {' '.join(new_form)} (Applied float_literal → digits . digits)")
                # Split float token into integer and fractional parts
                if float_token.startswith('.'):
                    integer_part = '0'
                    fractional_part = float_token[1:]
                else:
                    integer_part, fractional_part = float_token.split('.')
                tokens[token_index] = integer_part
                tokens.insert(token_index + 1, '.')
                tokens.insert(token_index + 2, fractional_part)
                replaced = True
                break

            # Handle digits non-terminal to derive num or num digits
            if symbol == 'digits' and token_index < len(tokens) and is_digits(tokens[token_index]):
                digit_token = tokens[token_index]
                print(f"Processing digits for token {digit_token} at index {token_index}")
                
                # Convert digit token into num or num digits
                if len(digit_token) == 1:
                    # Single digit: apply digits → num
                    new_form = new_form[:i] + ['num'] + new_form[i+1:]
                    derivation_steps.append(new_form)
                    step_count += 1
                    print(f"Step {step_count}: {' '.join(new_form)} (Applied digits → num)")
                    replaced = True
                    break
                else:
                    # Multi-digit: apply digits → num digits
                    new_form = new_form[:i] + ['num', 'digits'] + new_form[i+1:]
                    derivation_steps.append(new_form)
                    step_count += 1
                    print(f"Step {step_count}: {' '.join(new_form)} (Applied digits → num digits)")
                    # Split token into first digit and rest
                    first_digit = digit_token[0]
                    rest_digits = digit_token[1:]
                    tokens[token_index] = first_digit
                    tokens.insert(token_index + 1, rest_digits)
                    replaced = True
                    break

            # Handle num non-terminal to substitute with terminal digits
            if symbol == 'num' and token_index < len(tokens):
                current_token = tokens[token_index]
                if len(current_token) == 1 and current_token in {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}:
                    # Substitute num with the corresponding digit terminal
                    new_form = new_form[:i] + [current_token] + new_form[i+1:]
                    derivation_steps.append(new_form)
                    step_count += 1
                    print(f"Step {step_count}: {' '.join(new_form)} (Applied num → {current_token})")
                    replaced = True
                    break
                else:
                    print(f"Error: Expected single digit for num, got {current_token}")
                    return False

            # Handle other non-terminals
            if symbol in grammar:
                for production in grammar[symbol]:
                    if production == ['ε']:
                        if token_index >= len(tokens) or \
                           (token_index < len(tokens) and tokens[token_index] not in first_sets[symbol] - {'ε'}):
                            print(f"Applying {symbol} → ε at token index {token_index}")
                            new_form = new_form[:i] + new_form[i+1:]
                            derivation_steps.append(new_form)
                            step_count += 1
                            print(f"Step {step_count}: {' '.join(new_form)} (Applied {symbol} → ε)")
                            replaced = True
                            break
                    else:
                        can_apply = True
                        temp_index = token_index
                        print(f"Checking production {symbol} → {' '.join(production)} at token index {temp_index}")
                        for prod_symbol in production:
                            print(f"  Evaluating symbol {prod_symbol}")
                            if prod_symbol in grammar and prod_symbol not in {'id', 'digits', 'float_literal', 'string_literal', 'bool_literal'}:
                                if temp_index < len(tokens):
                                    current_token = tokens[temp_index]
                                    if current_token in first_sets[prod_symbol] or \
                                       ('id' in first_sets[prod_symbol] and is_identifier(current_token)) or \
                                       ('digits' in first_sets[prod_symbol] and is_digits(current_token)) or \
                                       ('float_literal' in first_sets[prod_symbol] and is_float_literal(current_token)) or \
                                       ('string_literal' in first_sets[prod_symbol] and is_string_literal(current_token)) or \
                                       ('bool_literal' in first_sets[prod_symbol] and is_bool_literal(current_token)):
                                        print(f"    Non-terminal {prod_symbol} can derive token {current_token}")
                                        break
                                    else:
                                        print(f"    Non-terminal {prod_symbol} cannot derive token {current_token}")
                                        can_apply = False
                                        break
                                else:
                                    print(f"    Non-terminal {prod_symbol} encountered with no tokens left")
                                    can_apply = False
                                    break
                            elif prod_symbol in terminals:
                                if temp_index < len(tokens) and tokens[temp_index] == prod_symbol:
                                    print(f"    Matched terminal {prod_symbol} with token {tokens[temp_index]}")
                                    temp_index += 1
                                else:
                                    print(f"    Failed to match terminal {prod_symbol} with token {tokens[temp_index] if temp_index < len(tokens) else 'EOF'}")
                                    can_apply = False
                                    break
                            elif prod_symbol == 'id':
                                if temp_index < len(tokens) and is_identifier(tokens[temp_index]):
                                    print(f"    Matched id with token {tokens[temp_index]}")
                                    temp_index += 1
                                else:
                                    print(f"    Failed to match id with token {tokens[temp_index] if temp_index < len(tokens) else 'EOF'}")
                                    can_apply = False
                                    break
                            elif prod_symbol == 'digits':
                                if temp_index < len(tokens) and is_digits(tokens[temp_index]):
                                    print(f"    Matched digits with token {tokens[temp_index]}")
                                    temp_index += 1
                                else:
                                    print(f"    Failed to match digits with token {tokens[temp_index] if temp_index < len(tokens) else 'EOF'}")
                                    can_apply = False
                                    break
                            elif prod_symbol == 'float_literal':
                                if temp_index < len(tokens) and is_float_literal(tokens[temp_index]):
                                    print(f"    Matched float_literal with token {tokens[temp_index]}")
                                    temp_index += 1
                                else:
                                    print(f"    Failed to match float_literal with token {tokens[temp_index] if temp_index < len(tokens) else 'EOF'}")
                                    can_apply = False
                                    break
                            elif prod_symbol == 'string_literal':
                                if temp_index < len(tokens) and is_string_literal(tokens[temp_index]):
                                    print(f"    Matched string_literal with token {tokens[temp_index]}")
                                    temp_index += 1
                                else:
                                    print(f"    Failed to match string_literal with token {tokens[temp_index] if temp_index < len(tokens) else 'EOF'}")
                                    can_apply = False
                                    break
                            elif prod_symbol == 'bool_literal':
                                if temp_index < len(tokens) and is_bool_literal(tokens[temp_index]):
                                    print(f"    Matched bool_literal with token {tokens[temp_index]}")
                                    temp_index += 1
                                else:
                                    print(f"    Failed to match bool_literal with token {tokens[temp_index] if temp_index < len(tokens) else 'EOF'}")
                                    can_apply = False
                                    break
                            else:
                                print(f"    Unrecognized symbol {prod_symbol}")
                                can_apply = False
                                break
                        if symbol == 'E4' and production in [['E5', '++'], ['E5', '--'], ['++', 'E5'], ['--', 'E5']]:
                            if temp_index >= len(tokens) or tokens[temp_index] not in {'++', '--'}:
                                print(f"    Production {symbol} → {' '.join(production)} not applicable due to lookahead {tokens[temp_index] if temp_index < len(tokens) else 'EOF'}")
                                can_apply = False
                        if can_apply:
                            print(f"Applying production {symbol} → {' '.join(production)}")
                            new_form = new_form[:i] + production + new_form[i+1:]
                            derivation_steps.append(new_form)
                            step_count += 1
                            print(f"Step {step_count}: {' '.join(new_form)} (Applied {symbol} → {' '.join(production)})")
                            replaced = True
                            break
                        else:
                            print(f"Production {symbol} → {' '.join(production)} not applicable")
                if replaced:
                    break

            # Handle terminals and pseudo-terminals
            elif symbol in terminals or symbol in {'id', 'digits', 'float_literal', 'string_literal', 'bool_literal'}:
                if token_index < len(tokens):
                    current_token = tokens[token_index]
                    if symbol == current_token or \
                       (symbol == 'id' and is_identifier(current_token)) or \
                       (symbol == 'digits' and is_digits(current_token)) or \
                       (symbol == 'float_literal' and is_float_literal(current_token)) or \
                       (symbol == 'string_literal' and is_string_literal(current_token)) or \
                       (symbol == 'bool_literal' and is_bool_literal(current_token)):
                        print(f"Step {step_count + 1}: {' '.join(new_form[:i] + new_form[i+1:])} (Matched {symbol} with {current_token})")
                        new_form = new_form[:i] + new_form[i+1:]
                        derivation_steps.append(new_form)
                        step_count += 1
                        token_index += 1
                        replaced = True
                        break
                else:
                    print(f"Error: Expected {symbol}, but no more tokens available")
                    return False
            else:
                print(f"Error: Unrecognized symbol {symbol}")
                return False

        if not replaced:
            print("Error: Cannot proceed with derivation. No applicable production or terminal match.")
            return False

        if not new_form and token_index == len(tokens):
            print("Derivation successful!")
            return True
        elif not new_form and token_index < len(tokens):
            print("Error: Input not fully consumed")
            return False
        elif new_form and token_index == len(tokens) and not any(s in grammar for s in new_form):
            print("Error: No more tokens, but terminals remain:", new_form)
            return False

    return True

# Test cases
