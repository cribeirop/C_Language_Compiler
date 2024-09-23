# Compilador

![git status](http://3.129.230.99/svg/cribeirop/Compilador_LogComp/)

## EBNF

```bash
BLOCK = "{", { STATEMENT }, "}";
STATEMENT = ( λ | ASSIGNMENT, ";"  | PRINT, ";"  | BLOCK | IF | WHILE ) ;
ASSIGNMENT = IDENTIFIER, "=", RELATIONAL_EXPRESSION ;
PRINT = "printf", "(", RELATIONAL_EXPRESSION, ")" ;
SCANF = "scanf", "(",")" ;
IF = "if", "(", RELATIONAL_EXPRESSION, ")", STATEMENT, [ "else", STATEMENT ] ;
WHILE = "while", "(", RELATIONAL EXPRESSION, ")", STATEMENT ;
RELATIONAL_EXPRESSION = EXPRESSION, { ("==" | ">" | "<"), EXPRESSION } ;
EXPRESSION = TERM, { ("||" | "+" | "-"), TERM } ;
TERM = FACTOR, { ("&&" | "*" | "/"), FACTOR } ;
FACTOR = (("+" | "-" | "!"), FACTOR) | NUMBER | "(", RELATIONAL_EXPRESSION, ")" | IDENTIFIER | SCANF;
IDENTIFIER = LETTER, { LETTER | DIGIT | "_" } ;
NUMBER = DIGIT, { DIGIT } ;
LETTER = ( a | ... | z | A | ... | Z ) ;
DIGIT = ( 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 ) ;
```