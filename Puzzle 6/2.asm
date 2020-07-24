#; Unprotected Memory:  0 KB -  64 KB or     0 to 65535
#; Protected Memory:   64 KB - 128 KB or 65536 to 131071
#;
#; Key Location: 102 KB or 104447
#;   Key offset: 6, 12, 18...
#;
#;  r0       = 0
#;  r1 - r2  = addressing
#;       r21 = location id
#;       r22 = temp
#; r24 - r29 = cycle counter
#;       r29 = temp cycle counter

main:
            cflush                          #; Cache flush
            addi            r1, r0, 104447

            #; Loading non cache protected memory  : 7 cycles
            addi            r21, r0, 1
            cflush
            rdcycles        r24
            lb              r3, 0(r1)
exception_1:
            rdcycles        r25
            sub             r6, r29, r24

            #; Loading cached protected memory      : 5 cycles
            addi            r21, r0, 2
            rdcycles        r27
            lb              r3, 0(r1)
exception_2:
            rdcycles        r28
            sub             r7, r29, r27


toend:
            beq             r0, r0 end

exception:
            rdcycles        r29

            beq             r21, r0 end

            addi            r22, r0, 1
            beq             r21, r22 exception_1

            addi            r22, r0, 2
            beq             r21, r22 exception_2
end: