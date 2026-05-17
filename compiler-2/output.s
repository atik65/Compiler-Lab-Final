.section .data
fmt: .string "%d\n"

.section .text
.globl main
main:
    pushq %rbp
    movq %rsp, %rbp
    subq $24, %rsp
    # # Program Start
    # Declare x as int
    movq $10, [rbp-0]
    # Declare y as int
    movq $20, [rbp-4]
    # Declare z as int
    movq [rbp-0], %rax
    addq [rbp-4], %rax
    movq %rax, [rbp-8]
    movq [rbp-8], %rax
    imulq $2, %rax
    # Declare result as int
    movq %rax, [rbp-12]
    cmpq $0, %rcx
    je L0
    # Declare a as int
    movq $100, [rbp-16]
    movq [rbp-16], %rsi
    leaq fmt(%rip), %rdi
    xorq %rax, %rax
    call printf
    jmp L1
L0:
L1:
    # Declare counter as int
    movq $0, [rbp-20]
L2:
    cmpq $0, %rdx
    je L3
    movq [rbp-20], %rax
    addq $1, %rax
    movq %rax, [rbp-20]
    jmp L2
L3:
    movq [rbp-12], %rsi
    leaq fmt(%rip), %rdi
    xorq %rax, %rax
    call printf
    movq %rdi, %rax
    # # Program End

    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    ret