import sys

exp = sys.argv[1]

exp = exp.replace(" ", "")

tokens = []

i = 0
while i < len(exp):
    if exp[i] in ['+', '-', '*', '/']:
        tokens.append(exp[i])
        i += 1
    else:
        num = ""
        while i < len(exp) and exp[i].isdigit():
            num += exp[i]
            i += 1
        tokens.append(num)

res = int(tokens[0])
for i in range(1, len(tokens) - 1):
    if tokens[i] in ['+', '-']:
        if tokens[i] == '+':
            res += int(tokens[i + 1])
        elif tokens[i] == '-':
            res -= int(tokens[i + 1])

print(res)