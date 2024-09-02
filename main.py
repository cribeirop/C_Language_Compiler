import sys

class Token:
    def __init__(self, type: str = None, value: None = None):
        self.type = type
        self.value = value

class Tokenizer:
    def __init__(self, source: str, position: int):
        self.source = source
        self.position = position
        self.next = Token()

        if not self.is_valid():
            raise ValueError("Error")
        
        self.select_next()

    def is_valid(self):
        is_space_digit = False
        pcharacter = ''

        if self.source.replace(' ', '') == '' or self.source.count('(') != self.source.count(')'):
            return False
        
        for character in self.source:
            if character.isspace() and not is_space_digit:
                if pcharacter.isdigit():
                    is_space_digit = True
            elif not character.isspace() and not character.isdigit():
                is_space_digit = False
            elif character.isdigit() and is_space_digit:
                return False
            pcharacter = character
            
        return True
    
    def select_next(self):
        if self.position >= len(self.source):
            self.next = Token("EOF")
            return None
        
        while self.source[self.position] == ' ':
            self.position += 1

        character = self.source[self.position]
        if character.isdigit():
            num_str = ""
            while self.position < len(self.source) and self.source[self.position].isdigit():
                num_str += self.source[self.position]
                self.position += 1
            self.position -= 1
            self.next = Token("INT", int(num_str))

        elif character == '+':
            self.next = Token("PLUS")

        elif character == '-':
            self.next = Token("MINUS")
        
        elif character == '*':
            self.next = Token("MULT")

        elif character == '/':
            self.next = Token("DIV")
        
        elif character == '(':
            self.next = Token("OP")
        
        elif character == ')':
            self.next = Token("CP")

        else:
            raise ValueError("Error")
        
        self.position += 1

class Parser:
    def __init__(self, tokenizer: Tokenizer):
        self.tokenizer = tokenizer

    def parse_factor(self):
        resultado = self.tokenizer.next.value
        if self.tokenizer.next.type == "INT":
            self.tokenizer.select_next()
            return resultado
        if self.tokenizer.next.type == "PLUS":
            self.tokenizer.select_next()
            resultado = +(self.parse_factor())
        elif self.tokenizer.next.type == "MINUS":
            self.tokenizer.select_next()
            resultado = -(self.parse_factor())
        if self.tokenizer.next.type == "OP":
            self.tokenizer.select_next()
            resultado = self.parse_expression()
            if self.tokenizer.next.type == "CP":
                self.tokenizer.select_next()
        return resultado

    def parse_term(self):
        resultado = self.parse_factor()

        while self.tokenizer.next.type in ["MULT", "DIV"]:
            if self.tokenizer.next.type == "MULT":
                self.tokenizer.select_next()
                resultado *= self.parse_factor()
            elif self.tokenizer.next.type == "DIV":
                self.tokenizer.select_next()
                resultado //= self.parse_factor()
        return resultado

    def parse_expression(self):
        resultado = self.parse_term()

        while self.tokenizer.next.type in ["PLUS", "MINUS"]:
            if self.tokenizer.next.type == "PLUS":
                self.tokenizer.select_next()
                resultado += self.parse_term()
            elif self.tokenizer.next.type == "MINUS":
                self.tokenizer.select_next()
                resultado -= self.parse_term()
        return resultado
    
    def run(self, code: str):
        tokenizer = Tokenizer(source = code, position = 0)
        parser = Parser(tokenizer = tokenizer)
        return parser.parse_expression()

if __name__ == "__main__":
    code = sys.argv[1]
    tokenizer = Tokenizer(source = code, position = 0)
    parser = Parser(tokenizer = tokenizer)
    run = parser.run(code = code)
    print(run)