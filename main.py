import sys

def tokenize(expression):
    tokens = []
    i = 0

    while i < len(expression):
        if expression[i].isspace():
            i += 1
            continue
        if expression[i].isdigit():
            j = i
            while j < len(expression) and expression[j].isdigit():
                j += 1
            tokens.append(expression[i:j])
            i = j
        elif expression[i] in ['+', '-']:
            tokens.append(expression[i])
            i += 1
        else:
            raise ValueError(f"Unexpected character {expression[i]}")
    
    return;

def validate_tokens(tokens):
    if not tokens:
        raise ValueError("Expression is empty")
    
    if not tokens[0].isdigit():
        raise ValueError(f"Expression cannot start with {tokens[0]}")
    
    for i in range(1, len(tokens), 2):
        if tokens[i] not in ['+', '-']:
            raise ValueError(f"Expected operator at position {i}, found {tokens[i]}")
        if i + 1 >= len(tokens) or not tokens[i + 1].isdigit():
            raise ValueError(f"Operator {tokens[i]} at position {i} must be followed by a number")

def evaluate(tokens):
    res = int(tokens[0])
    i = 1

    while i < len(tokens):
        if tokens[i] in ['+', '-']:
            if tokens[i] == '+':
                res += int(tokens[i + 1])
            elif tokens[i] == '-':
                res -= int(tokens[i + 1])
            i += 2
        else:
            raise ValueError(f"Unexpected token {tokens[i]} at position {i}")

    return res

if __name__ == "__main__":
    try:
        if len(sys.argv) != 2:
            raise ValueError("Usage: python script.py '<expression>'")
        
        exp = sys.argv[1]
        tokens = tokenize(exp)
        validate_tokens(tokens)
        result = evaluate(tokens)
        print(tokens)
        print(result)
    except Exception as e:
        print(f"Error: {e}")
