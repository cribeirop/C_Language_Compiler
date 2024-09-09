import sys

class PrePro:
    def __init__(self):
        pass

    def filter(self, source: str) -> str:
        source = source.strip()
        result = []
        skip = False
        i = 0
        while i < len(source):
            if not skip and source[i:i+2] == '/*':
                skip = True
                i += 2
            elif skip and source[i:i+2] == '*/':
                skip = False
                i += 2
            elif not skip:
                result.append(source[i])
                i += 1
            else:
                i += 1
        return ''.join(result).strip()
    
class Token:
    def __init__(self, type: str = None, value: None = None):
        self.type = type
        self.value = value

class Tokenizer:
    def __init__(self, source: str, position: int):
        self.source = source
        self.position = position
        self.next = Token()
        self.token_map = {
            '+': "PLUS",
            '-': "MINUS",
            '*': "MULT",
            '/': "DIV",
            '(': "OP",
            ')': "CP"
        }

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

        elif character in self.token_map:
            self.next = Token(self.token_map[character])

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
            return IntVal(value=resultado)
        if self.tokenizer.next.type == "PLUS":
            self.tokenizer.select_next()
            resultado = UnOp(value='+', child=[self.parse_factor()])
        elif self.tokenizer.next.type == "MINUS":
            self.tokenizer.select_next()
            resultado = UnOp(value='-', child=[self.parse_factor()])
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
                resultado = BinOp(value='*', children=[resultado, self.parse_factor()])
            elif self.tokenizer.next.type == "DIV":
                self.tokenizer.select_next()
                resultado = BinOp(value='/', children=[resultado, self.parse_factor()])
        return resultado

    def parse_expression(self):
        resultado = self.parse_term()

        while self.tokenizer.next.type in ["PLUS", "MINUS"]:
            if self.tokenizer.next.type == "PLUS":
                self.tokenizer.select_next()
                resultado = BinOp(value='+', children=[resultado, self.parse_term()])
            elif self.tokenizer.next.type == "MINUS":
                self.tokenizer.select_next()
                resultado = BinOp(value='-', children=[resultado, self.parse_term()])
        return resultado
    
    def run(self, code: str):
        tokenizer = Tokenizer(source = code, position = 0)
        parser = Parser(tokenizer = tokenizer)
        ast = parser.parse_expression()
        return ast
    
class Node:
    def __init__(self, value, children=None):
        self.value = value
        self.children = children
    
    def evaluate():
        pass

class BinOp(Node):
    def __init__(self, value, children):
        super().__init__(value, children)
    
    def evaluate(self):
        if self.value == '+':
            return self.children[0].evaluate() + self.children[1].evaluate()
        elif self.value == '-':
            return self.children[0].evaluate() - self.children[1].evaluate()
        elif self.value == '*':
            return self.children[0].evaluate() * self.children[1].evaluate()
        elif self.value == '/':
            return self.children[0].evaluate() // self.children[1].evaluate()

class UnOp(Node):
    def __init__(self, value, child):
        super().__init__(value, child)
    
    def evaluate(self):
        if self.value == '+':
            return +(self.children[0].evaluate())
        elif self.value == '-':
            return -(self.children[0].evaluate())

class IntVal(Node):
    def __init__(self, value):
        super().__init__(value)
    
    def evaluate(self):
        return self.value

class NoOp(Node):
    def __init__(self):
        super().__init__(None)
    
    def evaluate(self):
        return None

if __name__ == "__main__":
    file = sys.argv[1]

    with open(file, "r") as arquivo:
        linhas = arquivo.readlines()

    expressoes = [PrePro().filter(linha.strip()) for linha in linhas]
    for expressao in expressoes:
        tokenizer = Tokenizer(source=expressao, position=0)
        parser = Parser(tokenizer=tokenizer)
        ast_root = parser.run(code=expressao)
        value = ast_root.evaluate()
        print(value)