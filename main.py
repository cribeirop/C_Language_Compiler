import sys

exp = sys.argv[1]

tokens = []

is_space = False
is_number = False

i = 0

while i < len(exp):
    if exp[i] == ' ':
        i += 1
        continue

    if exp[i] in ['+', '-']:
        if i == len(exp) - 1:
            raise ValueError('Error: invalid expression')
        tokens.append(exp[i])
        i += 1
    
    elif exp[i].isdigit():
        j = i
        while j < len(exp) and exp[j] not in ['+', '-']:
            if is_space:
                raise ValueError('Error: invalid expression')
            if exp[j] == ' ':
                is_space = True
            j += 1
        tokens.append(exp[i:j])
        is_space = False
        i = j
    
    else:
        raise ValueError('Error: invalid expression')

print(tokens)

res = int(tokens[0])
for i in range(1, len(tokens)):
    if tokens[i] in ['+', '-']:
        if tokens[i] == '+':
            res += int(tokens[i + 1])
        elif tokens[i] == '-':
            res -= int(tokens[i + 1])

print(res)