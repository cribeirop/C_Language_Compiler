import sys

class Calculator:
    def __init__(self):
        self.expression = sys.argv[1]
        self.operatings = []
    
    def isvalid(self):
        prev_isdigit, hasnumber = 0, 0
        prev_caractere, prev_existing_caractere = '', ''
        if not self.expression[0].isdigit() or not self.expression[-1].isdigit():
            return False
        if self.expression.replace(" ",'') == '':
            return False
        for caractere in self.expression:
            if caractere.isdigit() and not prev_isdigit:
                hasnumber = 1
                prev_isdigit = 1
            elif not caractere.isdigit() and not caractere == ' ':
                prev_isdigit = 0
            elif caractere.isdigit() and prev_isdigit and prev_caractere == ' ':
                return False
            if not caractere.isdigit() and not caractere == ' ' and not prev_existing_caractere.isdigit():
                return False
            prev_caractere = caractere
            if caractere != ' ':
                prev_existing_caractere = caractere
            if self.expression.index(caractere) == len(self.expression)-1 and hasnumber == 0:
                return False
            if not caractere.isdigit() and caractere not in ['+', '-', ' ']:
                return False 
        return True
    
    def lexicon_exploration(self):
        self.expression = self.expression.replace(" ", "")
        self.operatings = [self.expression[0]]
        for caractere in self.expression[1::]:
            if caractere.isdigit() and self.operatings[-1].isdigit():
                self.operatings[-1] += caractere
            if caractere.isdigit() and not self.operatings[-1].isdigit():
                self.operatings.append(caractere)
            if not caractere.isdigit():
                self.operatings.append(caractere)
        return self.operatings

    def calculator(self):
        self.result = int(self.operatings[0])
        operation = ''
        for element in self.operatings[1::]:
            if not element.isdigit():
                operation = element
            else:
                if operation == '+':
                    self.result += int(element)
                else:
                    self.result -= int(element)

        return self.result

    def main(self):
        if self.isvalid():
            self.lexicon_exploration()
            return self.calculator()
        else:
            raise ValueError("Invalido")
            
if __name__ == "__main__":
    calculator = Calculator()
    result = calculator.main()
    print(result)