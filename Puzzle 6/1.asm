#; Unprotected Memory:  0 KB -  64 KB or     0 to 65535
#; Protected Memory:   64 KB - 128 KB or 65536 to 131071
#;
#; Key Location: 102 KB or 104447
#;   Key offset: 6, 12, 18...
#;
#;  r0       = 0
#;  r1 - r2  = addressing
#; r24 - r29 = cycle counter


main:
        cflush                          #; Cache flush
        rdcycles        r26             #; Read cycle counter
        addi            r1, r0, 0
        sb              r26, 0(r1)

        #; Loading non cache memory     : 4 cycles
        cflush
        rdcycles        r24
        lb              r3, 0(r1)
        rdcycles        r25
        sub             r6, r25, r24

        #; Loading cached memory       : 2 cycles
        rdcycles        r27
        lb              r3, 0(r1)
        rdcycles        r28
        sub             r7, r28, r27

        addi            r26, r0, 0