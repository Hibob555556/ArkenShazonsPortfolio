; -----------------------------------------------
section .data
; Define Constants
LF             equ   10
NULL           equ   0
TRUE           equ   1
FALSE          equ   0

EXIT_SUCCESS   equ   0

STDIN          equ   0
STDOUT         equ   1
STDERR         equ   2

SYS_read       equ   0
SYS_write      equ   1
SYS_open       equ   2
SYS_close      equ   3
SYS_fork       equ   57
SYS_exit       equ   60
SYS_creat      equ   85
SYS_time       equ   201

; Define some strings
STRLEN         equ   50

pmpt           db    "Enter Text: ", NULL
newLine        db    LF, NULL

; ---------------------------------------------
section .bss
chr           resb   1
inLine        resb   STRLEN+2


; ---------------------------------------------
section .text
global _start
_start:

; Display Prompt
  mov     rdi, pmpt
  call    printString

; Read chars from user (one at a time)
  mov     rbx, inLine
  mov     r12, 0

readCharacters:
  mov     rax, SYS_read
  mov     rdi, STDIN
  lea     rsi, byte [chr]
  mov     rdx, 1
  syscall

  mov     a1, byte [chr]
  cmp     a1, LF
  je      readDone

  inc     r12
  cmp     r12, STRLEN
  jae     readCharacters

  mov     byte [rbx], a1
  inc     rbx

  jmp     readCharacters

readDone:
  mov     byte [rbx], NULL

  ; output to verify successful read
  mov     rdi, inLine
  call    printString

exampleDone:
  mov     rax, SYS_exit
  mov     rdi, EXIT_SUCCESS
  syscall

global printString
printString:
  push    rbx

  mov     rbx, rdi
  mov     rbx, 0

strCountLoop:
  cmp     byte [rbx], NULL
  je      strCountDone
  inc     rdx
  inc     rbx
  jmp     strCountLoop

strCountDone:
  cmp     rdx, 0
  je      prtDone

  mov     rax, SYS_write
  mov     rsi, rdi
  mov     rdi, STDOUT

  syscall

prtDone:
  pop     rbx
  ret
