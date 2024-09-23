class PrePro:
    def __init__(self):
        pass

    def filter(self, source: str) -> str:
        if '/*' in source and not '*/' in source:
            raise ValueError("Error")
        
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
        return ''.join(result).replace(' ','').replace('\n', '').replace('\t', '')

class SymbolTable:
    def __init__(self):
        self.symbol_table = {}

    def get(self, identifier):
        return self.symbol_table[identifier]
    
    def set(self, identifier, value):
        self.symbol_table[identifier] = value
        return;
    
class Token:
    def __init__(self, type: str = None, value: None = None):
        self.type = type
        self.value = value

class Tokenizer:
    def __init__(self, source: str, position: int):
        self.source = source
        self.position = position
        self.next = Token()
        self.general_map = {
            '+': "PLUS",
            '-': "MINUS",
            '*': "MULT",
            '/': "DIV",
            '(': "OPEN_PARENTHESES",
            ')': "CLOSE_PARENTHESES",
            '{': "OPEN_BRACES",
            '}': "CLOSE_BRACES",
            '=': "EQUAL",
            ';': "SEMICOLON",
            'printf': "PRINTF",
            'if': "IF",
            'else': "ELSE",
            'while': "WHILE",
            'scanf': "SCANF",
            '||': "OR",
            '&&': "AND",
            '==': "DOUBLE_EQUAL",
            '>': "GREATER_THAN",
            '<': "LESS_THAN",
            '!': "NOT"
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
            if self.position < len(self.source) and self.source[self.position].isalpha():
                raise ValueError("Error")
            self.position -= 1
            self.next = Token("INT", int(num_str))

        elif character.isalpha() or character == '_':
            identifier = ""
            while self.position < len(self.source) and (self.source[self.position].isalpha() or self.source[self.position].isdigit() or self.source[self.position] == '_'):
                identifier += str(self.source[self.position])
                self.position += 1
            self.position -= 1

            if identifier in self.general_map:
                self.next = Token(self.general_map[identifier])
            else:
                self.next = Token("IDENTIFIER", identifier)

        elif character == '=':
            if self.position + 1 < len(self.source) and self.source[self.position + 1] == '=':
                self.position += 1  # Consome o próximo '='
                self.next = Token("DOUBLE_EQUAL")
            else:
                self.next = Token("EQUAL")

        elif character in self.general_map:
            self.next = Token(self.general_map[character])

        else:
            raise ValueError("Error")
        
        self.position += 1

class Parser:
    def __init__(self, tokenizer: Tokenizer):
        self.tokenizer = tokenizer
    
    def parse_block(self):
        statements = []
        if self.tokenizer.next.type == "OPEN_BRACES":
            self.tokenizer.select_next()
            while self.tokenizer.next.type != "CLOSE_BRACES":
                statements.append(self.parse_statement())
            self.tokenizer.select_next()
        return Block(children=statements)

    def parse_statement(self):
        statement = NoOp()
        if self.tokenizer.next.type == "IDENTIFIER":
            identifier = self.tokenizer.next.value
            self.tokenizer.select_next()
            if self.tokenizer.next.type == "EQUAL":
                self.tokenizer.select_next()
                expression = self.parse_relational_expression()
                statement = Assigment(children=[identifier, expression])
        elif self.tokenizer.next.type == "PRINTF":
            self.tokenizer.select_next()
            if self.tokenizer.next.type == "OPEN_PARENTHESES":
                self.tokenizer.select_next()
                expression = self.parse_relational_expression()
                statement = Printf(child=[expression])
                if self.tokenizer.next.type == "CLOSE_PARENTHESES":
                    self.tokenizer.select_next()
        elif self.tokenizer.next.type == "IF":
            self.tokenizer.select_next()
            if self.tokenizer.next.type == "OPEN_PARENTHESES":
                self.tokenizer.select_next()
                condition = self.parse_relational_expression()
                if self.tokenizer.next.type == "CLOSE_PARENTHESES":
                    self.tokenizer.select_next()
                    true_statement = self.parse_statement()
                    if self.tokenizer.next.type == "ELSE":
                        self.tokenizer.select_next()
                        false_statement = self.parse_statement()
                        statement = If(children=[condition, true_statement, false_statement])
                    else:
                        statement = If(children=[condition, true_statement])
        elif self.tokenizer.next.type == "WHILE":
            self.tokenizer.select_next()
            if self.tokenizer.next.type == "OPEN_PARENTHESES":
                self.tokenizer.select_next()
                condition = self.parse_relational_expression()
                if self.tokenizer.next.type == "CLOSE_PARENTHESES":
                    self.tokenizer.select_next()
                    body = self.parse_statement()
                    statement = While(children=[condition, body])
        if self.tokenizer.next.type == "OPEN_BRACES":
            statement = self.parse_block()
            # self.tokenizer.select_next()
            # return statement
        elif self.tokenizer.next.type == "SEMICOLON":
            self.tokenizer.select_next()
        # else:
        #     raise ValueError("Error")

        return statement

    def parse_factor(self):
        resultado = self.tokenizer.next.value
        if self.tokenizer.next.type == "IDENTIFIER":
            self.tokenizer.select_next()
            return Identifier(value=resultado)
        if self.tokenizer.next.type == "INT":
            self.tokenizer.select_next()
            return IntVal(value=resultado)
        if self.tokenizer.next.type == "PLUS":
            self.tokenizer.select_next()
            resultado = UnOp(value='+', child=[self.parse_factor()])
        elif self.tokenizer.next.type == "MINUS":
            self.tokenizer.select_next()
            resultado = UnOp(value='-', child=[self.parse_factor()])
        elif self.tokenizer.next.type == "NOT":
            self.tokenizer.select_next()
            resultado = UnOp(value='!', child=[self.parse_factor()])
        if self.tokenizer.next.type == "OPEN_PARENTHESES":
            self.tokenizer.select_next()
            resultado = self.parse_relational_expression()
            if self.tokenizer.next.type == "CLOSE_PARENTHESES":
                self.tokenizer.select_next()
        if self.tokenizer.next.type == "SCANF":
            self.tokenizer.select_next()
            if self.tokenizer.next.type == "OPEN_PARENTHESES":
                self.tokenizer.select_next()
                resultado = Scanf()
                if self.tokenizer.next.type == "CLOSE_PARENTHESES":
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
            elif self.tokenizer.next.type == "AND":
                self.tokenizer.select_next()
                resultado = BinOp(value='&&', children=[resultado, self.parse_factor()])
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
            elif self.tokenizer.next.type == "OR":
                self.tokenizer.select_next()
                resultado = BinOp(value='||', children=[resultado, self.parse_term()])
        return resultado
    
    def parse_relational_expression(self):
        resultado = self.parse_expression()

        while self.tokenizer.next.type in ["DOUBLE_EQUAL", "GREATER_THAN", "LESS_THAN"]:
            if self.tokenizer.next.type == "DOUBLE_EQUAL":
                self.tokenizer.select_next()
                resultado = BinOp(value='==', children=[resultado, self.parse_expression()])
            elif self.tokenizer.next.type == "GREATER_THAN":
                self.tokenizer.select_next()
                resultado = BinOp(value='>', children=[resultado, self.parse_expression()])
            elif self.tokenizer.next.type == "LESS_THAN":
                self.tokenizer.select_next()
                resultado = BinOp(value='<', children=[resultado, self.parse_expression()])
        return resultado
    
    def run(self, code: str):
        tokenizer = Tokenizer(source=code, position=0)
        parser = Parser(tokenizer=tokenizer)
        return parser.parse_block()
    
class Node:
    def __init__(self, value, children=None):
        self.value = value
        self.children = children
    
    def evaluate(self, symbol_table):
        pass

class BinOp(Node):
    def __init__(self, value, children):
        super().__init__(value, children)
    
    def evaluate(self, symbol_table):
        if self.value == '+':
            return self.children[0].evaluate(symbol_table) + self.children[1].evaluate(symbol_table)
        elif self.value == '-':
            return self.children[0].evaluate(symbol_table) - self.children[1].evaluate(symbol_table)
        elif self.value == '*':
            return self.children[0].evaluate(symbol_table) * self.children[1].evaluate(symbol_table)
        elif self.value == '/':
            return self.children[0].evaluate(symbol_table) // self.children[1].evaluate(symbol_table)
        elif self.value == '||':
            return self.children[0].evaluate(symbol_table) or self.children[1].evaluate(symbol_table)
        elif self.value == '&&':
            return self.children[0].evaluate(symbol_table) and self.children[1].evaluate(symbol_table)
        elif self.value == '==':
            return self.children[0].evaluate(symbol_table) == self.children[1].evaluate(symbol_table)
        elif self.value == '>':
            return self.children[0].evaluate(symbol_table) > self.children[1].evaluate(symbol_table)
        elif self.value == '<':
            return self.children[0].evaluate(symbol_table) < self.children[1].evaluate(symbol_table)
        
class UnOp(Node):
    def __init__(self, value, child):
        super().__init__(value, child)
    
    def evaluate(self, symbol_table):
        if self.value == '+':
            return +(self.children[0].evaluate(symbol_table))
        elif self.value == '-':
            return -(self.children[0].evaluate(symbol_table))
        elif self.value == '!':
            return not(self.children[0].evaluate(symbol_table))

class IntVal(Node):
    def __init__(self, value):
        super().__init__(value)
    
    def evaluate(self, symbol_table):
        return self.value

class NoOp(Node):
    def __init__(self):
        super().__init__(None)
    
    def evaluate(self, symbol_table):
        return None
    
class Block(Node):
    def __init__(self, children):
        super().__init__(children)
    
    def evaluate(self, symbol_table):
        for child in self.value:
            child.evaluate(symbol_table)
        return;

class Assigment(Node):
    def __init__(self, children):
        super().__init__(self, children)
    
    def evaluate(self, symbol_table):
        symbol_table.set(self.children[0], self.children[1].evaluate(symbol_table))
        return;

class Identifier(Node):
    def __init__(self, value):
        super().__init__(self, value)

    def evaluate(self, symbol_table):
        if self.children in symbol_table.symbol_table:
            return symbol_table.get(self.children)
        else:
            raise ValueError("Error")

class Printf(Node):
    def __init__(self, child):
        super().__init__(self, child)
    
    def evaluate(self, symbol_table):
        print(self.children[0].evaluate(symbol_table))
        return;

class While(Node):
    def __init__(self, children):
        super().__init__(self, children)
    
    def evaluate(self, symbol_table):
        while self.children[0].evaluate(symbol_table):
            self.children[1].evaluate(symbol_table)
        return;

class If(Node):
    def __init__(self, children):
        super().__init__(self, children)
    
    def evaluate(self, symbol_table):
        if self.children[0].evaluate(symbol_table):
            self.children[1].evaluate(symbol_table)
        elif len(self.children) > 2:
            self.children[2].evaluate(symbol_table)
        return;

class Scanf(Node):
    def __init__(self):
        super().__init__(None)

    def evaluate(self, symbol_table):
        return int(input())

if __name__ == "__main__":
    import sys
    file = sys.argv[1]

    with open(file, "r") as source_code:
        code = source_code.read()

    code = PrePro().filter(source=code)
    symbol_table = SymbolTable()
    tokenizer = Tokenizer(source=code, position=0)
    parser = Parser(tokenizer=tokenizer)
    ast_root = parser.run(code=code)
    ast_root.evaluate(symbol_table=symbol_table)