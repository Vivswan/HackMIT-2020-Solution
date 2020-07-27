addi x2, x1, 1024 ##1024 = location of array
addi x4, x1, 255  ##
addi x5, x2, 0
loop:
    beq x3, x4, endLoop
    sb x3, 0(x5)
    addi x5, x5, 32
    addi x3, x3, 1
    jal r0, loop
endLoop:
    xor x3, x3, x3 #resets x3 = 0
    addi x5, x2, 0 #resets x5 = x2
    addi x6, x6, 2

    cflush

    lb x7, 104598(x1)
    muli x7, x7, 32
    add x8, x8, x7
    lb x9, 0(x8)

exception:
loop2:
    beq x3, x4, endLoop2
    rdcycles x10
    lb x12, 0(x5)
    rdcycles x11
    sub x11, x11, x10
    beq x11, x6, endLoop2
    addi x5, x5, 32
    addi x3, x3, 1
    jal r0, loop2
endLoop2: