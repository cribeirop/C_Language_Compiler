import sys

class Calculator():
    def __init__(self):
        self.expression = sys.argv[1]
        self.tokens = []

    def is_valid(self):
        is_space_digit = False
        pcharacter = ''

        if not self.expression[0].isdigit() or not self.expression[-1].isdigit() or self.expression.replace(' ', '') == '':
            return False
        
        for character in self.expression:
            if character.isspace() and not is_space_digit:
                if pcharacter.isdigit():
                    is_space_digit = True
            elif not character.isspace() and not character.isdigit():
                is_space_digit = False
            elif character.isdigit() and is_space_digit:
                return False
            pcharacter = character
            

    
        return True
    
    def lexer(self):
        self.expression = self.expression.replace(" ", "")
        self.tokens = [self.expression[0]]

        for character in self.expression[1::]:
            if self.tokens[-1].isdigit() and character.isdigit():
                self.tokens[-1] += character
            else:
                self.tokens.append(character)

        print(self.tokens)

    def calculator(self):
        result = 0
        operator = ''
        for token in self.tokens:
            if token in ['+', '-']:
                operator = token
            else:
                if operator == '+':
                    result += int(token)
                elif operator == '-':
                    result -= int(token)
                else:
                    result = int(token)

        return result

    def main(self):
        if self.is_valid():
            self.lexer()
            return self.calculator()
        else:
            print('A')

if __name__ == "__main__":
    calculator = Calculator()
    result = calculator.main()
    print(result)