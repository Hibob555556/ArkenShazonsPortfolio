; hello.asm - NASM function callable from C

global print_arken       ; export symbol
section .data
    msg db "ArkenAsm", 0xA, "============", 0xA
    len equ $ - msg

section .text
print_arken:
    mov rax, 1          ; syscall: write
    mov rdi, 1          ; stdout
    mov rsi, msg
    mov rdx, len
    syscall
    ret
