import sys

def tokenize(expression):
    tokens = []
    i = 0
    
    while i < len(expression):
        if expression[i] == ' ':
            i += 1
            continue
        if expression[i].isdigit():
            j = i
            while j < len(expression) and expression[j].isdigit():
                j += 1
            tokens.append(expression[i:j])
            i = j
        else:
            if expression[i] in ['+', '-']:
                tokens.append(expression[i])
                i += 1
            else:
                raise ValueError(f"Unexpected character {expression[i]}")
    
    return tokens

def evaluate(tokens):
    if not tokens:
        raise ValueError("No tokens to evaluate")
    
    # Ensure the first token is a number
    if not tokens[0].isdigit():
        raise ValueError(f"Expression cannot start with {tokens[0]}")

    res = int(tokens[0])
    i = 1

    while i < len(tokens):
        if tokens[i] in ['+', '-']:
            if i + 1 >= len(tokens) or not tokens[i + 1].isdigit():
                raise ValueError(f"Operator {tokens[i]} at position {i} must be followed by a number")
            if tokens[i] == '+':
                res += int(tokens[i + 1])
            elif tokens[i] == '-':
                res -= int(tokens[i + 1])
            i += 2  # Skip to the next operator or end of tokens
        else:
            raise ValueError(f"Unexpected token {tokens[i]} at position {i}")

    return res

if __name__ == "__main__":
    try:
        exp = sys.argv[1]
        tokens = tokenize(exp)
        result = evaluate(tokens)
        print(tokens)
        print(result)
    except Exception as e:
        print(f"Error: {e}")
