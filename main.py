class PrePro:
    def __init__(self):
        pass

    def filter(self, source: str) -> str:
        if '/*' in source and not '*/' in source:
            raise ValueError("Error")
        
        source = source.strip()
        result = []
        skip = False
        in_string = False
        i = 0

        while i < len(source):
            if source[i] == '"' and not skip:
                in_string = not in_string
                result.append(source[i])
                i += 1
            elif not skip and not in_string and source[i:i+2] == '/*':
                skip = True
                i += 2
            elif skip and source[i:i+2] == '*/':
                skip = False
                i += 2
            elif not skip:
                if in_string or source[i] != ' ':
                    result.append(source[i])
                i += 1
            else:
                i += 1

        return ''.join(result).replace('\n', '').replace('\t', '')

class SymbolTable:
    def __init__(self):
        self.symbol_table = {}

    def get(self, identifier):
        return self.symbol_table.get(identifier, None)
    
    def set(self, identifier, value):
        if identifier in self.symbol_table:
            self.symbol_table[identifier] = value

    def create(self, identifier, value):
        if self.get(identifier) is None:
            self.symbol_table[identifier] = value

class FuncTable:
    def __init__(self):
        self.func_table = {}

    def get(self, key):
        return self.func_table.get(key)
    
    def set(self, key, value):
        self.func_table[key] = value
    
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
            '!': "NOT",
            ',': "COMMA",
            'int': "INT",
            'str': "STR",
            'void': "VOID",
            'return': "RETURN"
        }

        if not self.is_valid():
            raise ValueError("Error")
        
        self.select_next()

    def is_valid(self):
        is_space_digit = False
        pcharacter = ''

        if self.source.replace(' ', '') == '' or self.source.count('(') != self.source.count(')') or self.source.count('{') != self.source.count('}'):
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
                if identifier in ["else", "int", "str", "void"]:
                    self.position += 1
                    break
                self.position += 1
            self.position -= 1

            if identifier in self.general_map:
                self.next = Token(self.general_map[identifier])
            else:
                self.next = Token("IDENTIFIER", identifier)

        elif character == '"':
            string = ""
            self.position += 1
            while self.position < len(self.source) and self.source[self.position] != '"':
                string += self.source[self.position]
                self.position += 1
            self.next = Token("STR", string)

        elif character in ['=', '&', '|'] and self.position + 1 < len(self.source) and self.source[self.position + 1] == character:
            self.position += 1
            if character == '=':
                self.next = Token("DOUBLE_EQUAL")
            elif character == '&':
                self.next = Token("AND")
            elif character == '|':
                self.next = Token("OR")

        elif character in self.general_map:
            self.next = Token(self.general_map[character])

        else:
            raise ValueError("Error")
        
        self.position += 1

class Parser:
    def __init__(self, tokenizer: Tokenizer):
        self.tokenizer = tokenizer
    
    def parse_program(self):
        functions = []
        while self.tokenizer.next.type != "EOF":
            functions.append(self.parse_function())
        self.tokenizer.select_next()
        functions.append(FuncCall(value="main", children=[]))
        return Block(children=functions)

    def parse_function(self):
        if self.tokenizer.next.type in ["INT", "STR", "VOID"]:
            func_type = self.tokenizer.next.type
            self.tokenizer.select_next()
            if self.tokenizer.next.type == "IDENTIFIER":
                func_ident = self.tokenizer.next.value
                self.tokenizer.select_next()
                if self.tokenizer.next.type == "OPEN_PARENTHESES":
                    var_decs = []
                    self.tokenizer.select_next()
                    while self.tokenizer.next.type != "CLOSE_PARENTHESES":
                        if self.tokenizer.next.type in ["INT", "STR", "VOID"]:
                            var_type = self.tokenizer.next.type
                            self.tokenizer.select_next()
                            if self.tokenizer.next.type == "IDENTIFIER":
                                identifier = Identifier(value=self.tokenizer.next.value)
                                var_decs.append(VarDec(value=var_type, children=[identifier]))
                                self.tokenizer.select_next()
                                if self.tokenizer.next.type == "COMMA":
                                    self.tokenizer.select_next()                
                    self.tokenizer.select_next()
                    block = self.parse_block()
                    var_dec = VarDec(value=func_type, children=var_decs)
                    return FuncDec(value=func_ident, children=[var_dec, block])
        else:
            raise ValueError("Error")

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
            elif self.tokenizer.next.type == "OPEN_PARENTHESES":
                expressions = []
                self.tokenizer.select_next()
                while self.tokenizer.next.type != "CLOSE_PARENTHESES":
                    expressions.append(self.parse_relational_expression())
                    if self.tokenizer.next.type == "COMMA":
                        self.tokenizer.select_next()
                self.tokenizer.select_next()
                statement = FuncCall(value=identifier, children=expressions)
        elif self.tokenizer.next.type == "RETURN":
            self.tokenizer.select_next()
            if self.tokenizer.next.type == "OPEN_PARENTHESES":
                self.tokenizer.select_next()
                expression = self.parse_relational_expression()
                if self.tokenizer.next.type == "CLOSE_PARENTHESES":
                    self.tokenizer.select_next()
                    statement = Return(children=[expression])
        elif self.tokenizer.next.type in ["INT", "STR", "VOID"]:
            var_type = self.tokenizer.next.type
            self.tokenizer.select_next()
            var_declarations = []
            while True:
                if self.tokenizer.next.type == "IDENTIFIER":
                    identifier = self.tokenizer.next.value
                    child = None
                    self.tokenizer.select_next()
                    if self.tokenizer.next.type == "EQUAL":
                        self.tokenizer.select_next()
                        child = self.parse_relational_expression()
                    var_declarations.append(VarDec(value=var_type, children=[identifier, child]))
                    if self.tokenizer.next.type == "COMMA":
                        self.tokenizer.select_next()
                        continue
                    break
            statement = Block(children=var_declarations)
        elif self.tokenizer.next.type == "PRINTF":
            self.tokenizer.select_next()
            if self.tokenizer.next.type == "OPEN_PARENTHESES":
                self.tokenizer.select_next()
                expression = self.parse_relational_expression()
                statement = Printf(child=[expression])
                if self.tokenizer.next.type == "CLOSE_PARENTHESES":
                    self.tokenizer.select_next()
        if self.tokenizer.next.type == "SEMICOLON":
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
        elif self.tokenizer.next.type == "OPEN_BRACES":
            statement = self.parse_block()
        else:
            raise ValueError("Error")
        return statement

    def parse_factor(self):
        resultado = self.tokenizer.next.value
        if self.tokenizer.next.type == "IDENTIFIER":
            identifier = self.tokenizer.next.value
            self.tokenizer.select_next()
            if self.tokenizer.next.type == "OPEN_PARENTHESES":
                args = []
                self.tokenizer.select_next()
                while self.tokenizer.next.type != "CLOSE_PARENTHESES":
                    args.append(self.parse_relational_expression())
                    if self.tokenizer.next.type == "COMMA":
                        self.tokenizer.select_next()
                self.tokenizer.select_next()
                return FuncCall(value=identifier, children=args)
            return Identifier(value=resultado)
        if self.tokenizer.next.type == "INT":
            self.tokenizer.select_next()
            return IntVal(value=resultado)
        if self.tokenizer.next.type == "STR":
            self.tokenizer.select_next()
            return StrVal(value=resultado)
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

        while self.tokenizer.next.type in ["MULT", "DIV", "AND"]:
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

        while self.tokenizer.next.type in ["PLUS", "MINUS", "OR"]:
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
        return parser.parse_program()
    
class Node:
    def __init__(self, value, children=None):
        self.value = value
        self.children = children
    
    def evaluate(self, symbol_table, func_table=None):
        pass

class BinOp(Node):
    def __init__(self, value, children):
        super().__init__(value, children)
    
    def evaluate(self, symbol_table, func_table):
        child_0, type_0 = self.children[0].evaluate(symbol_table, func_table)
        child_1, type_1 = self.children[1].evaluate(symbol_table, func_table)
        if self.value == '+':
            if type_0 == "STR" or type_1 == "STR":
                return (str(child_0) + str(child_1), "STR")
            return (child_0 + child_1, "INT")
        elif self.value == '-':
            return (child_0 - child_1, "INT")
        elif self.value == '*':
            return (child_0 * child_1, "INT")
        elif self.value == '/':
            return (child_0 // child_1, "INT")
        elif self.value == '||':
            return (child_0 or child_1, "INT")
        elif self.value == '&&':
            return (child_0 and child_1, "INT")
        if type_0 != type_1:
            raise ValueError("Error")
        elif self.value == '==':
            return (int(child_0 == child_1), "INT")
        elif self.value == '>':
            return (int(child_0 > child_1), "INT")
        elif self.value == '<':
            return (int(child_0 < child_1), "INT")
        
class UnOp(Node):
    def __init__(self, value, child):
        super().__init__(value, child)
    
    def evaluate(self, symbol_table, func_table):
        if self.value == '+':
            return (+ self.children[0].evaluate(symbol_table, func_table)[0], "INT")
        elif self.value == '-':
            return (- self.children[0].evaluate(symbol_table, func_table)[0], "INT")
        elif self.value == '!':
            child = self.children[0].evaluate(symbol_table, func_table)[0]
            if type(child) == int:
                return (int(not child), "INT")
            raise ValueError("Error")
        
class IntVal(Node):
    def __init__(self, value):
        super().__init__(value)
    
    def evaluate(self, symbol_table, func_table):
        return (self.value, "INT")

class NoOp(Node):
    def __init__(self):
        super().__init__(None)
    
    def evaluate(self, symbol_table, func_table):
        return None
    
class Block(Node):
    def __init__(self, children):
        super().__init__(None, children)
    
    def evaluate(self, symbol_table, func_table):
        for child in self.children:
            result = child.evaluate(symbol_table, func_table)
            if isinstance(child, Return):
                return result

class Assigment(Node):
    def __init__(self, children):
        super().__init__(None, children)
    
    def evaluate(self, symbol_table, func_table):
        if self.children[0] in symbol_table.symbol_table:
            child = self.children[1].evaluate(symbol_table, func_table)
            if child[1] != symbol_table.symbol_table[self.children[0]][1]:
                raise ValueError("Error")
            symbol_table.set(self.children[0], (child[0], child[1]))
        else:
            raise ValueError("Error")

class Identifier(Node):
    def __init__(self, value):
        super().__init__(value)

    def evaluate(self, symbol_table, func_table):
        if symbol_table.get(self.value) is not None:
            return symbol_table.get(self.value)
        else:
            raise ValueError("Error")

class Printf(Node):
    def __init__(self, child):
        super().__init__(self, child)
    
    def evaluate(self, symbol_table, func_table):
        print(self.children[0].evaluate(symbol_table, func_table)[0])
        return;

class While(Node):
    def __init__(self, children):
        super().__init__(None, children)
    
    def evaluate(self, symbol_table, func_table):
        while self.children[0].evaluate(symbol_table, func_table)[0]:
            self.children[1].evaluate(symbol_table, func_table)

class If(Node):
    def __init__(self, children):
        super().__init__(None, children)
    
    def evaluate(self, symbol_table, func_table):
        condition = self.children[0].evaluate(symbol_table, func_table)
        if condition[0]:
            return self.children[1].evaluate(symbol_table, func_table)
        elif len(self.children) > 2:
            return self.children[2].evaluate(symbol_table, func_table)

class Scanf(Node):
    def __init__(self):
        super().__init__(None)

    def evaluate(self, symbol_table, func_table):
        input_value = input()
        if input_value.isdigit():
            return (int(input_value), "INT")
        raise ValueError("Error")

class StrVal(Node):
    def __init__(self, value):
        super().__init__(value)
    
    def evaluate(self, symbol_table, func_table):
        return (self.value, "STR")

class VarDec(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, symbol_table, func_table):
        if self.children[0] in symbol_table.symbol_table:
            raise ValueError("Error")
        elif self.children[1]:
            child = self.children[1].evaluate(symbol_table, func_table)
            symbol_table.create(self.children[0], (child[0], child[1]))
        elif self.children[1] is None:
            symbol_table.create(self.children[0], (None, self.value))
        else:
            raise ValueError("Error")

class FuncDec(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, symbol_table, func_table):
        func_table.set(self.value, self)

class FuncCall(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, symbol_table, func_table):
        func = func_table.get(self.value)
        if len(self.children) != (len(func.children[0].children)):
            raise ValueError("Error")
        local_table = SymbolTable()
        for child, arg_node in zip(func.children[0].children, self.children):
            arg_value, arg_type = arg_node.evaluate(symbol_table, func_table)
            local_table.create(child.children[0].value, (arg_value, child.value))
        return func.children[1].evaluate(local_table, func_table)

class Return(Node):
    def __init__(self, children):
        super().__init__(None, children)

    def evaluate(self, symbol_table, func_table):
        return self.children[0].evaluate(symbol_table, func_table)

if __name__ == "__main__":
    import sys
    file = sys.argv[1]

    with open(file, "r") as source_code:
        code = source_code.read()

    code = PrePro().filter(source=code)
    symbol_table = SymbolTable()
    func_table = FuncTable()
    tokenizer = Tokenizer(source=code, position=0)
    parser = Parser(tokenizer=tokenizer)
    ast_root = parser.run(code=code)
    ast_root.evaluate(symbol_table=symbol_table, func_table=func_table)