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
            raise ValueError("Errosr")
        self.select_next()

    def is_valid(self):
        is_space_digit = False
        pcharacter = ''

        if not self.source[0].isdigit() or not self.source[-1].isdigit() or self.source.replace(' ', '') == '':
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
            self.next = Token("EOF", None)
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
            self.next = Token("PLUS", None)

        elif character == '-':
            self.next = Token("MINUS", None)

        else:
            raise ValueError("Error")
        
        self.position += 1

class Parser:
    def __init__(self, tokenizer: Tokenizer):
        self.tokenizer = tokenizer

    def parse_expression(self):
        if self.tokenizer.next.type == "INT":
            resultado = self.tokenizer.next.value
            self.tokenizer.select_next()

            while self.tokenizer.next.type != "EOF":
                if self.tokenizer.next.type == "PLUS":
                    self.tokenizer.select_next()
                    if self.tokenizer.next.type == "INT":
                        resultado += self.tokenizer.next.value
                    else:
                        raise ValueError("Error")
                elif self.tokenizer.next.type == "MINUS":
                    self.tokenizer.select_next()
                    if self.tokenizer.next.type == "INT":
                        resultado -= self.tokenizer.next.value
                    else:
                        raise ValueError("Error")
                self.tokenizer.select_next()
            return resultado
        raise ValueError("Error")
    
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