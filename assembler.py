class Assembler:
    header = '''; constantes
SYS_EXIT equ 1
SYS_READ equ 3
SYS_WRITE equ 4
STDIN equ 0
STDOUT equ 1
True equ 1
False equ 0

segment .data
formatin: db "%d" , 0
formatout: db "%d" , 10 , 0 ; newline , nul terminator
scanint: times 4 db 0 ; 32-bits integer = 4 bytes

segment .bss ; variaveis
res RESB 1

section .text
global main ; linux

extern scanf ; linux
extern printf ; linux
extern fflush ; linux
extern stdout ; linux

; subrotinas if / while
binop_je:
JE binop_true
JMP binop_false

binop_jg:
JG binop_true
JMP binop_false

binop_jl:
JL binop_true
JMP binop_false

binop_false:
MOV EAX, False
JMP binop_exit

binop_true:
MOV EAX, True

binop_exit:
RET

main:
PUSH EBP ; guarda o base pointer
MOV EBP, ESP ; estabelece um novo base pointer
'''

    body = '''
'''

    footer = '''
; interrupcao de saida (default)
PUSH DWORD [stdout]
CALL fflush
ADD ESP, 4
MOV ESP, EBP
POP EBP
MOV EAX, 1
XOR EBX, EBX
INT 0x80'''

    def __init__(self):
        with open("code.asm", "w") as file:
            file.write("")
    
    def write(self, file_name : str, code: str):
        Assembler.body += code
    
    def write_header(self, file_name: str):
        file_name = file_name.replace(".c", ".asm")
        with open(file_name, "w") as file:
            file.write(self.header)

    def write_body(self, file_name: str):
        file_name = file_name.replace(".c", ".asm")
        with open(file_name, "a") as file:
            file.write(self.body)

    def write_footer(self, file_name: str):
        file_name = file_name.replace(".c", ".asm")
        with open(file_name, "a") as file:
            file.write(self.footer)