import re

import re

def split_string_literals_and_operators(tokens):
    """
    Processes a list of tokens, splitting string literals into individual character tokens
    (excluding quotes) and separating multi-character operators (e.g., 'b++' into 'b', '++').
    
    Args:
        tokens (list): List of token strings (e.g., ['while', '(', 'a', '==', '"hana"', ')', 'b++', ';'])
    
    Returns:
        list: Processed tokens with string literals split into characters (without quotes) and
              operators separated (e.g., ['while', '(', 'a', '==', 'h', 'a', 'n', 'a', ')', 'b', '++', ';'])
    """
    processed_tokens = []
    
    for token in tokens:
        # Check if token is a string literal (e.g., '"hana"')
        if re.match(r'^".*"$', token):
            # Add each character inside the string, excluding quotes
            for char in token[1:-1]:  # Exclude the opening and closing quotes
                if char.isalnum():  # Only allow alphanumeric characters (per grammar)
                    processed_tokens.append(char)
                else:
                    raise ValueError(f"Invalid character in string literal: {char}")
        # Check if token is a multi-character operator (e.g., 'b++')
        elif re.match(r'^[a-zA-Z]+\+\+$', token) or re.match(r'^[a-zA-Z]+--$', token):
            # Split into identifier and operator (e.g., 'b++' → 'b', '++')
            identifier = re.match(r'^[a-zA-Z]+', token).group(0)
            operator = token[len(identifier):]
            processed_tokens.append(identifier)
            processed_tokens.append(operator)
        # Otherwise, keep the token as is
        else:
            processed_tokens.append(token)
    
    return processed_tokens
if __name__ == "__main__":
    # Test input
    input_tokens = ['while', '(', 'a', '==', '"hana"', ')', 'b++', ';']
    print("Input tokens:", input_tokens)
    
    # Process tokens
    result = split_string_literals_and_operators(input_tokens)
    print("Processed tokens:", result)