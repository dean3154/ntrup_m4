import sys

def genHead(s : str):
    print(".p2align 2,,3")
    print(".syntax unified")
    print(".text")
    print(".global " + s)
    print(".type " + s + ", %function")
    print(s + ":")

def genEncodeRq(p : int, q : int, basecase : int):
    tailradix = q
    radix = q
    len = p
    genHead("Encode_Rq_asm")
    print("\tpush {r2-r12, lr}")
    print("\tvmov.w s1, r1 @ input")
    print("\tmovw.w r12, #" + str((q-1)//2))
    print("\tmovt.w r12, #" + str((q-1)//2))
    print("\tvmov.w r2, s1")
    # iter 1
    iter = 1
    print("@ iteration " + str(iter))
    print("@ len = " + str(len))
    print("@ tail radix = " + str(tailradix))
    iter = iter + 1
    print("\tadd.w lr, r1, #" + str( (2*(len) // 16) * 16 ))
    print("\tmov.w r3, #" + str(radix))
    print("Encode_Rq_asm_radix" + str(radix) + ":")
    print("\tldr.w r6, [r1, #4]")
    print("\tldr.w r7, [r1, #8]")
    print("\tldr.w r8, [r1, #12]")
    print("\tldr.w r5, [r1], #16")
    print("\tsadd16 r5, r5, r12")
    print("\tsadd16 r6, r6, r12")
    print("\tsadd16 r7, r7, r12")
    print("\tsadd16 r8, r8, r12")
    print("\tsxth r9, r5")
    print("\tsmlabt r5, r3, r5, r9")
    print("\tsxth r9, r6")
    print("\tsmlabt r6, r3, r6, r9")
    print("\tsxth r9, r7")
    print("\tsmlabt r7, r3, r7, r9")
    print("\tsxth r9, r8")
    print("\tsmlabt r8, r3, r8, r9")
    print("\tpkhbt r4, r5, r6, lsl #16")
    print("\tpkhtb r5, r6, r5, asr #16")
    print("\tpkhbt r6, r7, r8, lsl #16")
    print("\tpkhtb r7, r8, r7, asr #16")
    print("\tstr.w r6, [r0, #4]")
    print("\tstr.w r4, [r0], #8")
    print("\tstr.w r7, [r2, #4]")
    print("\tstr.w r5, [r2], #8")
    print("\tcmp.w r1, lr")
    print("\tbne.w Encode_Rq_asm_radix" + str(radix))
    if len % 8 == 5:
        print("\tldr.w r6, [r1, #4]")
        print("\tldr.w r5, [r1], #8")
        print("\tsadd16 r5, r5, r12")
        print("\tsadd16 r6, r6, r12")
        print("\tsxth r9, r5")
        print("\tsmlabt r5, r3, r5, r9")
        print("\tsxth r9, r6")
        print("\tsmlabt r6, r3, r6, r9")
        print("\tpkhbt r4, r5, r6, lsl #16")
        print("\tpkhtb r5, r6, r5, asr #16")
        print("\tstr.w r4, [r0], #4")
        print("\tstr.w r5, [r2], #4")
        print("\tldrh.w r5, [r1]")
        print("\tsadd16 r5, r5, r12")
        print("\tstrh.w r5, [r2]")
    else:
        print("\tldrh.w r5, [r1]")
        print("\tsadd16 r5, r5, r12")
        print("\tstrh.w r5, [r2]")

    radix = pow(radix, 2)
    while radix >= 16384:
        radix = (radix+255)//256
    len = (len+1)//2
    
    while len > basecase:
        print("\tvmov r1, s1")
        print("\tvmov r2, s1")
        print("@ iteration " + str(iter))
        print("@ len = " + str(len))
        print("@ tail radix = " + str(tailradix))

        iter += 1
        print("\tmov.w r3, #" + str(radix))
        cntOutputBytes = 0
        oldradix = radix
        radix = pow(radix, 2)
        while radix >= 16384:
            radix = (radix+255)//256
            cntOutputBytes += 1
        
        ss = 0
        if len % 2 == 0:
            ss = 2

        if cntOutputBytes == 2:
            print("\tadd.w lr, r1, #" + str((2*(len-ss) // 16) * 16))
        else:
            print("\tadd.w lr, r1, #" + str((2*(len-ss) // 32) * 32))

        print("Encode_Rq_asm_radix" + str(oldradix) + ":")

        if cntOutputBytes == 2:
            print("\tldr.w r6, [r1, #4]")
            print("\tldr.w r7, [r1, #8]")
            print("\tldr.w r8, [r1, #12]")
            print("\tldr.w r5, [r1], #16")
            print("\tsxth r9, r5")
            print("\tsmlabt r5, r3, r5, r9")
            print("\tsxth r9, r6")
            print("\tsmlabt r6, r3, r6, r9")
            print("\tsxth r9, r7")
            print("\tsmlabt r7, r3, r7, r9")
            print("\tsxth r9, r8")
            print("\tsmlabt r8, r3, r8, r9")
            print("\tpkhbt r4, r5, r6, lsl #16")
            print("\tpkhtb r5, r6, r5, asr #16")
            print("\tpkhbt r6, r7, r8, lsl #16")
            print("\tpkhtb r7, r8, r7, asr #16")
            print("\tstr.w r6, [r0, #4]")
            print("\tstr.w r4, [r0], #8")
            print("\tstr.w r7, [r2, #4]")
            print("\tstr.w r5, [r2], #8")
            print("\tcmp.w r1, lr")
            print("\tbne.w Encode_Rq_asm_radix" + str(oldradix))
            left = (len-ss) % 8
            if left // 2 == 3:
                print("\tldr.w r6, [r1, #4]")
                print("\tldr.w r7, [r1, #8]")
                print("\tldr.w r5, [r1], #12")
                print("\tsxth r9, r5")
                print("\tsmlabt r5, r3, r5, r9")
                print("\tsxth r9, r6")
                print("\tsmlabt r6, r3, r6, r9")
                print("\tsxth r9, r7")
                print("\tsmlabt r7, r3, r7, r9")
                print("\tpkhbt r4, r5, r6, lsl #16")
                print("\tpkhtb r5, r6, r5, asr #16")
                print("\tubfx r6, r7, #0, #16")
                print("\tubfx r7, r7, #16, #16")
                print("\tstrh.w r6, [r0, #4]")
                print("\tstr.w r4, [r0], #6")
                print("\tstrh.w r7, [r2, #4]")
                print("\tstr.w r5, [r2], #6")
            elif left // 2 == 2:
                print("\tldr.w r6, [r1, #4]")
                print("\tldr.w r5, [r1], #8")
                print("\tsxth r9, r5")
                print("\tsmlabt r5, r3, r5, r9")
                print("\tsxth r9, r6")
                print("\tsmlabt r6, r3, r6, r9")
                print("\tpkhbt r4, r5, r6, lsl #16")
                print("\tpkhtb r5, r6, r5, asr #16")
                print("\tstr.w r4, [r0], #4")
                print("\tstr.w r5, [r2], #4")
            elif left // 2 == 1:
                print("\tldr.w r5, [r1], #4")
                print("\tsxth r9, r5")
                print("\tsmlabt r5, r3, r5, r9")
                print("\tubfx r6, r5, #16, #16")
                print("\tstrh.w r5, [r0], #2")
                print("\tstrh.w r6, [r2], #2")
            if len % 2 == 1:
                print("\tldrh.w r4, [r1]")
                print("\tstrh.w r4, [r2]")
            else:
                cnttail = 0

                if len % 2 == 0:
                    tailradix = oldradix * tailradix

                while tailradix >= 16384:
                    tailradix = (tailradix + 255) // 256
                    cnttail += 1

                print("\tldr.w r5, [r1], #4")
                print("\tsxth r9, r5")
                print("\tsmlabt r5, r3, r5, r9")
                if cnttail == 2:
                    print("\tubfx r6, r5, #16, #16")
                    print("\tstrh.w r5, [r0], #2")
                    print("\tstrh.w r6, [r2], #2")
                elif cnttail == 1:
                    print("\tubfx r6, r5, #8, #16")
                    print("\tstrb.w r5, [r0], #1")
                    print("\tstrh.w r6, [r2], #2")
                elif cnttail == 0:
                    print("\tstrh.w r5, [r2], #2")


        elif cntOutputBytes == 1:
            print("\tldr.w r5, [r1, #4]")
            print("\tldr.w r6, [r1, #8]")
            print("\tldr.w r7, [r1, #12]")
            print("\tldr.w r8, [r1, #16]")
            print("\tldr.w r9, [r1, #20]")
            print("\tldr.w r10, [r1, #24]")
            print("\tldr.w r11, [r1, #28]")
            print("\tldr.w r4, [r1], #32")

            for i in range(4, 12):
                print("\tsxth r12, r" + str(i))
                print("\tsmlabt r" + str(i) + ", r3, r" + str(i) + ", r12")

            for i in range(4):
                print("\tbfi r12, r" + str(i+8) + ", #" + str(i*8) + ", #8")

            print("\tlsr.w r10, #8")
            print("\tpkhbt r11, r10, r11, lsl #8") # str #12
            print("\tlsr.w r8, #8")
            print("\tpkhbt r10, r8, r9, lsl #8") # str # 8

            for i in range(4):
                print("\tbfi r9, r" + str(i+4) + ", #" + str(i*8) + ", #8")

            print("\tlsr.w r6, #8")
            print("\tpkhbt r8, r6, r7, lsl #8") # str # 4
            print("\tlsr.w r4, #8")
            print("\tpkhbt r7, r4, r5, lsl #8") # str # 0
            print("\tstr.w r12, [r0, #4]")
            print("\tstr.w r9, [r0], #8")
            print("\tstr.w r8, [r2, #4]")
            print("\tstr.w r10, [r2, #8]")
            print("\tstr.w r11, [r2, #12]")
            print("\tstr.w r7, [r2], #16")
            print("\tcmp.w r1, lr")
            print("\tbne.w Encode_Rq_asm_radix" + str(oldradix))
            left = (len-ss) % 16

            if left >= 8:
                print("\tldr.w r5, [r1, #4]")
                print("\tldr.w r6, [r1, #8]")
                print("\tldr.w r7, [r1, #12]")
                print("\tldr.w r4, [r1], #16")

                for i in range(4, 8):
                    print("\tsxth r12, r" + str(i))
                    print("\tsmlabt r" + str(i) + ", r3, r" + str(i) + ", r12")

                for i in range(4):
                    print("\tbfi r9, r" + str(i+4) + ", #" + str(i*8) + ", #8")

                print("\tlsr.w r6, #8")
                print("\tpkhbt r8, r6, r7, lsl #8") # str # 4
                print("\tlsr.w r4, #8")
                print("\tpkhbt r7, r4, r5, lsl #8") # str # 0
                print("\tstr.w r9, [r0], #4")
                print("\tstr.w r8, [r2, #4]")
                print("\tstr.w r7, [r2], #8")
                left -= 8

            if left // 2 == 3:
                print("\tldr.w r5, [r1, #4]")
                print("\tldr.w r6, [r1, #8]")
                print("\tldr.w r4, [r1], #12")

                for i in range(4, 7):
                    print("\tsxth r12, r" + str(i))
                    print("\tsmlabt r" + str(i) + ", r3, r" + str(i) + ", r12")

                for i in range(2):
                    print("\tbfi r9, r" + str(i+4) + ", #" + str(i*8) + ", #8")

                print("\tlsr.w r4, #8")
                print("\tpkhbt r4, r4, r5, lsl #8")
                print("\tubfx r7, r6, #8, #16")
                print("\tstrh.w r9, [r0], #2")
                print("\tstrb.w r6, [r0], #1")
                print("\tstr.w r4, [r2], #4")
                print("\tstrh.w r7, [r2], #2")

            elif left // 2 == 2:
                print("\tldr.w r5, [r1, #4]")
                print("\tldr.w r4, [r1], #8")

                for i in range(4, 6):
                    print("\tsxth r12, r" + str(i))
                    print("\tsmlabt r" + str(i) + ", r3, r" + str(i) + ", r12")

                for i in range(2):
                    print("\tbfi r9, r" + str(i+4) + ", #" + str(i*8) + ", #8")

                print("\tlsr.w r4, #8")
                print("\tpkhbt r4, r4, r5, lsl #8")
                print("\tstrh.w r9, [r0], #2")
                print("\tstr.w r4, [r2], #4")

            elif left // 2 == 1:
                print("\tldr.w r4, [r1], #4")
                print("\tsxth r12, r4")
                print("\tsmlabt r4, r3, r4, r12")
                print("\tubfx r5, r4, #8, #16")
                print("\tstrb.w r4, [r0], #1")
                print("\tstrh.w r5, [r2], #2")

            if left % 2 == 1:
                print("\tldrh.w r4, [r1]")
                print("\tstrh.w r4, [r2]")
            else:
                cnttail = 0

                if len % 2 == 0:
                    tailradix = oldradix * tailradix

                while tailradix >= 16384:
                    tailradix = (tailradix + 255) // 256
                    cnttail += 1

                print("\tldr.w r5, [r1], #4")
                print("\tsxth r9, r5")
                print("\tsmlabt r5, r3, r5, r9")
                if cnttail == 2:
                    print("\tubfx r6, r5, #16, #16")
                    print("\tstrh.w r5, [r0], #2")
                    print("\tstrh.w r6, [r2], #2")
                elif cnttail == 1:
                    print("\tubfx r6, r5, #8, #16")
                    print("\tstrb.w r5, [r0], #1")
                    print("\tstrh.w r6, [r2], #2")
                elif cnttail == 0:
                    print("\tstrh.w r5, [r2], #2")


        elif cntOutputBytes == 0:
            print("\tldr.w r5, [r1, #4]")
            print("\tldr.w r6, [r1, #8]")
            print("\tldr.w r7, [r1, #12]")
            print("\tldr.w r8, [r1, #16]")
            print("\tldr.w r9, [r1, #20]")
            print("\tldr.w r10, [r1, #24]")
            print("\tldr.w r11, [r1, #28]")
            print("\tldr.w r4, [r1], #32")

            for i in range(4, 12):
                print("\tsxth r12, r" + str(i))
                print("\tsmlabt r" + str(i) + ", r3, r" + str(i) + ", r12")

            for i in range(4):
                print("\tpkhbt r" + str(12-i) + ", r" + str(10-i*2) + ", r" + str(11-i*2) + ", lsl #16")

            print("\tstr.w r10, [r2, #4]")
            print("\tstr.w r11, [r2, #8]")
            print("\tstr.w r12, [r2, #12]")
            print("\tstr.w r9, [r2], #16")
            print("\tcmp.w r1, lr")
            print("\tbne.w Encode_Rq_asm_radix" + str(oldradix))
            left = (len-ss) % 16

            for i in range(left // 2 - 1):
                print("\tldr.w r" + str(5+i) + ", [r1, #" + str((i+1)*4) + "]")

            print("\tldr.w r4, [r1], #" + str((left//2)*4))

            for i in range(4, 4 + (left//2)):
                print("\tsxth r12, r" + str(i))
                print("\tsmlabt r" + str(i) + ", r3, r" + str(i) + ", r12")

            for i in range((left//2)//2):
                print("\tpkhbt r" + str(4+i) + ", r" + str(4+i*2) + ", r" + str(5+i*2) + ", lsl #16")

            for i in range((left//2)//2):
                print("\tstr.w r" + str(4+i) + ", [r2], #4")

            if (left//2) % 2 == 1:
                print("\tstrh.w r" + str(3+(left//2)) + ", [r2], #2")
            
            if left % 2 == 1:
                print("\tldrh.w r4, [r1]")
                print("\tstrh.w r4, [r2]")
            else:
                cnttail = 0

                if len % 2 == 0:
                    tailradix = oldradix * tailradix

                while tailradix >= 16384:
                    tailradix = (tailradix + 255) // 256
                    cnttail += 1

                print("\tldr.w r5, [r1], #4")
                print("\tsxth r9, r5")
                print("\tsmlabt r5, r3, r5, r9")
                if cnttail == 2:
                    print("\tubfx r6, r5, #16, #16")
                    print("\tstrh.w r5, [r0], #2")
                    print("\tstrh.w r6, [r2], #2")
                elif cnttail == 1:
                    print("\tubfx r6, r5, #8, #16")
                    print("\tstrb.w r5, [r0], #1")
                    print("\tstrh.w r6, [r2], #2")
                elif cnttail == 0:
                    print("\tstrh.w r5, [r2], #2")
        
        len = (len+1)//2

    while len > 2:
        print("\tvmov r1, s1")
        print("\tvmov r2, s1")
        print("@ iteration " + str(iter))
        print("@ len = " + str(len))
        print("@ tail radix = " + str(tailradix))
        iter += 1
        print("\tmov.w r3, #" + str(radix))

        ss = 0
        cnttail = 0
        if len % 2 == 0:
            ss = 2
            tailradix = radix * tailradix
            while tailradix > 16384:
                tailradix = (tailradix+255) // 256
                cnttail += 1

        cntOutputBytes = 0
        radix = pow(radix, 2)
        while radix >= 16384:
            radix = (radix+255)//256
            cntOutputBytes += 1

        left = (len-ss)
        if cntOutputBytes == 2:
            for i in range(left//4):
                print("\tldr.w r5, [r1, #4]")
                print("\tldr.w r4, [r1], #8")
                print("\tsxth r12, r4")
                print("\tsmlabt r4, r3, r4, r12")
                print("\tsxth r12, r5")
                print("\tsmlabt r5, r3, r5, r12")
                print("\tpkhbt r6, r4, r5, lsl #16")
                print("\tpkhtb r7, r5, r4, asr #16")
                print("\tstr.w r6, [r0], #4")
                print("\tstr.w r7, [r2], #4")
            
            if (left % 4) // 2 == 1:
                print("\tldr.w r4, [r1], #4")
                print("\tsxth r12, r4")
                print("\tsmlabt r4, r3, r4, r12")
                print("\tubfx r5, r4, #16, #16")
                print("\tstrh.w r4, [r0], #2")
                print("\tstrh.w r5, [r2], #2")

            if left % 2 == 1:
                print("\tldrh.w r4, [r1]")
                print("\tstrh.w r4, [r2]")
            else:
                print("\tldr.w r5, [r1], #4")
                print("\tsxth r9, r5")
                print("\tsmlabt r5, r3, r5, r9")
                if cnttail == 2:
                    print("\tubfx r6, r5, #16, #16")
                    print("\tstrh.w r5, [r0], #2")
                    print("\tstrh.w r6, [r2], #2")
                elif cnttail == 1:
                    print("\tubfx r6, r5, #8, #16")
                    print("\tstrb.w r5, [r0], #1")
                    print("\tstrh.w r6, [r2], #2")
                elif cnttail == 0:
                    print("\tstrh.w r5, [r2], #2")

        elif cntOutputBytes == 1:
            for i in range(left // 8):
                print("\tldr.w r5, [r1, #4]")
                print("\tldr.w r6, [r1, #8]")
                print("\tldr.w r7, [r1, #12]")
                print("\tldr.w r4, [r1], #16")
                
                for i in range(4, 8):
                    print("\tsxth r12, r" + str(i))
                    print("\tsmlabt r" + str(i) + ", r3, r" + str(i) + ", r12")

                for i in range(4):
                    print("\tbfi r9, r" + str(i+4) + ", #" + str(i*8) + ", #8")

                print("\tlsr.w r6, #8")
                print("\tpkhbt r8, r6, r7, lsl #8") # str # 4
                print("\tlsr.w r4, #8")
                print("\tpkhbt r7, r4, r5, lsl #8") # str # 0
                print("\tstr.w r9, [r0], #4")
                print("\tstr.w r8, [r2, #4]")
                print("\tstr.w r7, [r2], #8")

            left = left % 8
            if left // 2 == 3:
                print("\tldr.w r5, [r1, #4]")
                print("\tldr.w r6, [r1, #8]")
                print("\tldr.w r4, [r1], #12")

                for i in range(4, 7):
                    print("\tsxth r12, r" + str(i))
                    print("\tsmlabt r" + str(i) + ", r3, r" + str(i) + ", r12")

                for i in range(2):
                    print("\tbfi r9, r" + str(i+4) + ", #" + str(i*8) + ", #8")

                print("\tlsr.w r4, #8")
                print("\tpkhbt r4, r4, r5, lsl #8")
                print("\tubfx r7, r6, #8, #16")
                print("\tstrh.w r9, [r0], #2")
                print("\tstrb.w r6, [r0], #1")
                print("\tstr.w r4, [r2], #4")
                print("\tstrh.w r7, [r2], #2")

            elif left // 2 == 2:
                print("\tldr.w r5, [r1, #4]")
                print("\tldr.w r4, [r1], #8")

                for i in range(4, 6):
                    print("\tsxth r12, r" + str(i))
                    print("\tsmlabt r" + str(i) + ", r3, r" + str(i) + ", r12")

                for i in range(2):
                    print("\tbfi r9, r" + str(i+4) + ", #" + str(i*8) + ", #8")

                print("\tlsr.w r4, #8")
                print("\tpkhbt r4, r4, r5, lsl #8")
                print("\tstrh.w r9, [r0], #2")
                print("\tstr.w r4, [r2], #4")

            elif left // 2 == 1:
                print("\tldr.w r4, [r1], #4")
                print("\tsxth r12, r4")
                print("\tsmlabt r4, r3, r4, r12")
                print("\tubfx r5, r4, #8, #16")
                print("\tstrb.w r4, [r0], #1")
                print("\tstrh.w r5, [r2], #2")

            if left % 2 == 1:
                print("\tldrh.w r4, [r1]")
                print("\tstrh.w r4, [r2]")
            else:
                print("\tldr.w r5, [r1], #4")
                print("\tsxth r9, r5")
                print("\tsmlabt r5, r3, r5, r9")
                if cnttail == 2:
                    print("\tubfx r6, r5, #16, #16")
                    print("\tstrh.w r5, [r0], #2")
                    print("\tstrh.w r6, [r2], #2")
                elif cnttail == 1:
                    print("\tubfx r6, r5, #8, #16")
                    print("\tstrb.w r5, [r0], #1")
                    print("\tstrh.w r6, [r2], #2")
                elif cnttail == 0:
                    print("\tstrh.w r5, [r2], #2")
        
        elif cntOutputBytes == 0:
            for i in range(left // 8):
                print("\tldr.w r5, [r1, #4]")
                print("\tldr.w r6, [r1, #8]")
                print("\tldr.w r7, [r1, #12]")
                print("\tldr.w r4, [r1], #16")
                
                for i in range(4, 8):
                    print("\tsxth r12, r" + str(i))
                    print("\tsmlabt r" + str(i) + ", r3, r" + str(i) + ", r12")

                print("\tpkhbt r8, r6, r7, lsl #16") # str # 4
                print("\tpkhbt r7, r4, r5, lsl #16") # str # 0
                print("\tstr.w r8, [r2, #4]")
                print("\tstr.w r7, [r2], #8")

            left = left % 8
            for i in range(left//2 - 1):
                print("\tldr.w r" + str(5+i) + ", [r1, #" + str((i+1)*4) + "]")

            print("\tldr.w r4, [r1], #" + str((left//2) * 4))
        
            for i in range(4, 4 + (left//2)):
                print("\tsxth r12, r" + str(i))
                print("\tsmlabt r" + str(i) + ", r3, r" + str(i) + ", r12")

            for i in range((left//2)//2):
                print("\tpkhbt r" + str(4+i) + ", r" + str(4+i*2) + ", r" + str(5+i*2) + ", lsl #16")

            for i in range((left//2)//2):
                print("\tstr.w r" + str(4+i) + ", [r2], #4")

            if (left//2) % 2 == 1:
                print("\tstrh.w r" + str(3+(left//2)) + ", [r2], #2")
            
            if left % 2 == 1:
                print("\tldrh.w r4, [r1]")
                print("\tstrh.w r4, [r2]")
            else:
                print("\tldr.w r5, [r1], #4")
                print("\tsxth r9, r5")
                print("\tsmlabt r5, r3, r5, r9")
                if cnttail == 2:
                    print("\tubfx r6, r5, #16, #16")
                    print("\tstrh.w r5, [r0], #2")
                    print("\tstrh.w r6, [r2], #2")
                elif cnttail == 1:
                    print("\tubfx r6, r5, #8, #16")
                    print("\tstrb.w r5, [r0], #1")
                    print("\tstrh.w r6, [r2], #2")
                elif cnttail == 0:
                    print("\tstrh.w r5, [r2], #2")

        len = (len+1)//2    

    print("@ len == 2")
    print("@ tail radix = " + str(tailradix))
    print("\tvmov.w r1, s1")
    print("\tvmov.w r2, s1")
    print("\tmov.w r3, #" + str(radix))
    cntOutputBytes = 0
    tailradix = radix * tailradix
    while tailradix > 16384:
        tailradix = (tailradix + 255) // 256
        cntOutputBytes += 1
    
    print("\tldr.w r4, [r1], #4")
    print("\tsxth r9, r4")
    print("\tsmlabt r4, r3, r4, r9")
    if cntOutputBytes == 2:
        print("\tubfx r5, r4, #16, #16")
        print("\tstrh.w r4, [r0], #2")
        print("\tstrh.w r5, [r2], #2")
    elif cntOutputBytes == 1:
        print("\tubfx r5, r4, #8, #16")
        print("\tstrb.w r4, [r0], #1")
        print("\tstrh.w r5, [r2], #2")
    elif cntOutputBytes == 0:
        print("\tstrh.w r4, [r2], #2")

    print("@ len == 1")

    cntOutputBytes = 0
    while tailradix > 1:
        tailradix = (tailradix + 255) // 256
        cntOutputBytes += 1

    print("\tvmov.w r1, s1")
    print("\tldrh.w r2, [r1]")
    if cntOutputBytes == 1:
        print("\tstrb.w r2, [r0]")
    elif cntOutputBytes == 2:
        print("\tstrh.w r2, [r0]")
    
    print("\tpop {r2-r12, pc}\n")

def genEncodeRounded(p : int, q : int, basecase : int):
    radix = (q+2)//3
    tailradix = radix
    oldradix = radix
    cntOutputBytes = 0
    radix = pow(radix, 2)
    while radix >= 16384:
        radix = (radix+255)//256
        cntOutputBytes += 1
    len = p
    genHead("Encode_Rounded_asm")
    print("\tpush {r2-r12, lr}")
    print("\tvmov.w s1, r1 @ input")
    print("\tmovw.w r12, #" + str((q-1)//2))
    print("\tmovt.w r12, #" + str((q-1)//2))
    print("\tmovw.w r11, #0x5556")
    print("\tmovt.w r11, #0x5555")
    # print("\tmov.w r11, #0x55555555")
    print("\tvmov.w r2, s1")
    # iter 1
    iter = 1
    print("@ iteration " + str(iter))
    print("@ len = " + str(len))
    print("@ tail radix = " + str(tailradix))
    iter = iter + 1
    print("\tadd.w lr, r1, #" + str( (2*(len) // 16) * 16 ))
    print("\tmov.w r3, #" + str(oldradix))
    print("Encode_Rounded_asm_radix" + str(oldradix) + ":")
    print("\tldr.w r6, [r1, #4]")
    print("\tldr.w r7, [r1, #8]")
    print("\tldr.w r8, [r1, #12]")
    print("\tldr.w r5, [r1], #16")
    print("\tsadd16 r5, r5, r12")
    print("\tsadd16 r6, r6, r12")
    print("\tsadd16 r7, r7, r12")
    print("\tsadd16 r8, r8, r12")
    for i in range(4):
        print("\tsmulwb r4, r11, r" + str(5+i))
        print("\tsmulwt r" + str(5+i) + ", r11, r" + str(5+i))
        print("\tlsr.w r4, #16")
        print("\tsmlabt r" + str(5+i) + ", r3, r" + str(5+i) + ", r4")
    if cntOutputBytes == 1:
        for i in range(4):
            print("\tbfi.w r4, r" + str(5+i) + ", #" + str(i*8) + ", #8")
        print("\tlsr.w r5, #8")
        print("\tpkhbt r5, r5, r6, lsl #8")
        print("\tlsr.w r7, #8")
        print("\tpkhbt r6, r7, r8, lsl #8")
        print("\tstr.w r4, [r0], #4")
        print("\tstr.w r6, [r2, #4]")
        print("\tstr.w r5, [r2], #8")
    elif cntOutputBytes == 2:
        print("\tpkhbt r4, r5, r6, lsl #16")
        print("\tpkhtb r5, r6, r5, asr #16")
        print("\tpkhbt r6, r7, r8, lsl #16")
        print("\tpkhtb r7, r8, r7, asr #16")
        print("\tstr.w r6, [r0, #4]")
        print("\tstr.w r4, [r0], #8")
        print("\tstr.w r7, [r2, #4]")
        print("\tstr.w r5, [r2], #8")
    print("\tcmp.w r1, lr")
    print("\tbne.w Encode_Rounded_asm_radix" + str(oldradix))
    if len % 8 == 5:
        print("\tldr.w r6, [r1, #4]")
        print("\tldr.w r5, [r1], #8")
        print("\tsadd16 r5, r5, r12")
        print("\tsadd16 r6, r6, r12")
        print("\tsmulwb r4, r11, r5")
        print("\tsmulwt r5, r11, r5")
        print("\tlsr.w r4, #16")
        print("\tsmlabt r5, r3, r5, r4")
        print("\tsmulwb r4, r11, r6")
        print("\tsmulwt r6, r11, r6")
        print("\tlsr.w r4, #16")
        print("\tsmlabt r6, r3, r6, r4")
        if cntOutputBytes == 1:
            print("\tbfi.w r4, r5, #0, #8")
            print("\tbfi.w r4, r6, #8, #8")
            print("\tlsr.w r5, #8")
            print("\tpkhbt r5, r5, r6, lsl #8")
            print("\tstrh.w r4, [r0], #2")
            print("\tstr.w r5, [r2], #4")
        elif cntOutputBytes == 2:
            print("\tpkhbt r4, r5, r6, lsl #16")
            print("\tpkhtb r5, r6, r5, asr #16")
            print("\tstr.w r4, [r0], #4")
            print("\tstr.w r5, [r2], #4")

    print("\tldrh.w r5, [r1]")
    print("\tsadd16 r5, r5, r12")
    print("\tsmulwb r5, r11, r5")
    print("\tlsr.w r5, #16")
    print("\tstrh.w r5, [r2]")
    len = (len+1)//2
    
    while len > basecase:
        print("\tvmov r1, s1")
        print("\tvmov r2, s1")
        print("@ iteration " + str(iter))
        print("@ len = " + str(len))
        print("@ tail radix = " + str(tailradix))

        iter += 1
        print("\tmov.w r3, #" + str(radix))
        cntOutputBytes = 0
        oldradix = radix
        radix = pow(radix, 2)
        while radix >= 16384:
            radix = (radix+255)//256
            cntOutputBytes += 1
        
        ss = 0
        if len % 2 == 0:
            ss = 2

        if cntOutputBytes == 2:
            print("\tadd.w lr, r1, #" + str((2*(len-ss) // 16) * 16))
        else:
            print("\tadd.w lr, r1, #" + str((2*(len-ss) // 32) * 32))

        print("Encode_Rounded_asm_radix" + str(oldradix) + ":")

        if cntOutputBytes == 2:
            print("\tldr.w r6, [r1, #4]")
            print("\tldr.w r7, [r1, #8]")
            print("\tldr.w r8, [r1, #12]")
            print("\tldr.w r5, [r1], #16")
            print("\tsxth r9, r5")
            print("\tsmlabt r5, r3, r5, r9")
            print("\tsxth r9, r6")
            print("\tsmlabt r6, r3, r6, r9")
            print("\tsxth r9, r7")
            print("\tsmlabt r7, r3, r7, r9")
            print("\tsxth r9, r8")
            print("\tsmlabt r8, r3, r8, r9")
            print("\tpkhbt r4, r5, r6, lsl #16")
            print("\tpkhtb r5, r6, r5, asr #16")
            print("\tpkhbt r6, r7, r8, lsl #16")
            print("\tpkhtb r7, r8, r7, asr #16")
            print("\tstr.w r6, [r0, #4]")
            print("\tstr.w r4, [r0], #8")
            print("\tstr.w r7, [r2, #4]")
            print("\tstr.w r5, [r2], #8")
            print("\tcmp.w r1, lr")
            print("\tbne.w Encode_Rounded_asm_radix" + str(oldradix))
            left = (len-ss) % 8
            if left // 2 == 3:
                print("\tldr.w r6, [r1, #4]")
                print("\tldr.w r7, [r1, #8]")
                print("\tldr.w r5, [r1], #12")
                print("\tsxth r9, r5")
                print("\tsmlabt r5, r3, r5, r9")
                print("\tsxth r9, r6")
                print("\tsmlabt r6, r3, r6, r9")
                print("\tsxth r9, r7")
                print("\tsmlabt r7, r3, r7, r9")
                print("\tpkhbt r4, r5, r6, lsl #16")
                print("\tpkhtb r5, r6, r5, asr #16")
                print("\tubfx r6, r7, #0, #16")
                print("\tubfx r7, r7, #16, #16")
                print("\tstrh.w r6, [r0, #4]")
                print("\tstr.w r4, [r0], #6")
                print("\tstrh.w r7, [r2, #4]")
                print("\tstr.w r5, [r2], #6")
            elif left // 2 == 2:
                print("\tldr.w r6, [r1, #4]")
                print("\tldr.w r5, [r1], #8")
                print("\tsxth r9, r5")
                print("\tsmlabt r5, r3, r5, r9")
                print("\tsxth r9, r6")
                print("\tsmlabt r6, r3, r6, r9")
                print("\tpkhbt r4, r5, r6, lsl #16")
                print("\tpkhtb r5, r6, r5, asr #16")
                print("\tstr.w r4, [r0], #4")
                print("\tstr.w r5, [r2], #4")
            elif left // 2 == 1:
                print("\tldr.w r5, [r1], #4")
                print("\tsxth r9, r5")
                print("\tsmlabt r5, r3, r5, r9")
                print("\tubfx r6, r5, #16, #16")
                print("\tstrh.w r5, [r0], #2")
                print("\tstrh.w r6, [r2], #2")
            if len % 2 == 1:
                print("\tldrh.w r4, [r1]")
                print("\tstrh.w r4, [r2]")
            else:
                cnttail = 0

                if len % 2 == 0:
                    tailradix = oldradix * tailradix

                while tailradix >= 16384:
                    tailradix = (tailradix + 255) // 256
                    cnttail += 1

                print("\tldr.w r5, [r1], #4")
                print("\tsxth r9, r5")
                print("\tsmlabt r5, r3, r5, r9")
                if cnttail == 2:
                    print("\tubfx r6, r5, #16, #16")
                    print("\tstrh.w r5, [r0], #2")
                    print("\tstrh.w r6, [r2], #2")
                elif cnttail == 1:
                    print("\tubfx r6, r5, #8, #16")
                    print("\tstrb.w r5, [r0], #1")
                    print("\tstrh.w r6, [r2], #2")
                elif cnttail == 0:
                    print("\tstrh.w r5, [r2], #2")


        elif cntOutputBytes == 1:
            print("\tldr.w r5, [r1, #4]")
            print("\tldr.w r6, [r1, #8]")
            print("\tldr.w r7, [r1, #12]")
            print("\tldr.w r8, [r1, #16]")
            print("\tldr.w r9, [r1, #20]")
            print("\tldr.w r10, [r1, #24]")
            print("\tldr.w r11, [r1, #28]")
            print("\tldr.w r4, [r1], #32")

            for i in range(4, 12):
                print("\tsxth r12, r" + str(i))
                print("\tsmlabt r" + str(i) + ", r3, r" + str(i) + ", r12")

            for i in range(4):
                print("\tbfi r12, r" + str(i+8) + ", #" + str(i*8) + ", #8")

            print("\tlsr.w r10, #8")
            print("\tpkhbt r11, r10, r11, lsl #8") # str #12
            print("\tlsr.w r8, #8")
            print("\tpkhbt r10, r8, r9, lsl #8") # str # 8

            for i in range(4):
                print("\tbfi r9, r" + str(i+4) + ", #" + str(i*8) + ", #8")

            print("\tlsr.w r6, #8")
            print("\tpkhbt r8, r6, r7, lsl #8") # str # 4
            print("\tlsr.w r4, #8")
            print("\tpkhbt r7, r4, r5, lsl #8") # str # 0
            print("\tstr.w r12, [r0, #4]")
            print("\tstr.w r9, [r0], #8")
            print("\tstr.w r8, [r2, #4]")
            print("\tstr.w r10, [r2, #8]")
            print("\tstr.w r11, [r2, #12]")
            print("\tstr.w r7, [r2], #16")
            print("\tcmp.w r1, lr")
            print("\tbne.w Encode_Rounded_asm_radix" + str(oldradix))
            left = (len-ss) % 16

            if left >= 8:
                print("\tldr.w r5, [r1, #4]")
                print("\tldr.w r6, [r1, #8]")
                print("\tldr.w r7, [r1, #12]")
                print("\tldr.w r4, [r1], #16")

                for i in range(4, 8):
                    print("\tsxth r12, r" + str(i))
                    print("\tsmlabt r" + str(i) + ", r3, r" + str(i) + ", r12")

                for i in range(4):
                    print("\tbfi r9, r" + str(i+4) + ", #" + str(i*8) + ", #8")

                print("\tlsr.w r6, #8")
                print("\tpkhbt r8, r6, r7, lsl #8") # str # 4
                print("\tlsr.w r4, #8")
                print("\tpkhbt r7, r4, r5, lsl #8") # str # 0
                print("\tstr.w r9, [r0], #4")
                print("\tstr.w r8, [r2, #4]")
                print("\tstr.w r7, [r2], #8")
                left -= 8

            if left // 2 == 3:
                print("\tldr.w r5, [r1, #4]")
                print("\tldr.w r6, [r1, #8]")
                print("\tldr.w r4, [r1], #12")

                for i in range(4, 7):
                    print("\tsxth r12, r" + str(i))
                    print("\tsmlabt r" + str(i) + ", r3, r" + str(i) + ", r12")

                for i in range(2):
                    print("\tbfi r9, r" + str(i+4) + ", #" + str(i*8) + ", #8")

                print("\tlsr.w r4, #8")
                print("\tpkhbt r4, r4, r5, lsl #8")
                print("\tubfx r7, r6, #8, #16")
                print("\tstrh.w r9, [r0], #2")
                print("\tstrb.w r6, [r0], #1")
                print("\tstr.w r4, [r2], #4")
                print("\tstrh.w r7, [r2], #2")

            elif left // 2 == 2:
                print("\tldr.w r5, [r1, #4]")
                print("\tldr.w r4, [r1], #8")

                for i in range(4, 6):
                    print("\tsxth r12, r" + str(i))
                    print("\tsmlabt r" + str(i) + ", r3, r" + str(i) + ", r12")

                for i in range(2):
                    print("\tbfi r9, r" + str(i+4) + ", #" + str(i*8) + ", #8")

                print("\tlsr.w r4, #8")
                print("\tpkhbt r4, r4, r5, lsl #8")
                print("\tstrh.w r9, [r0], #2")
                print("\tstr.w r4, [r2], #4")

            elif left // 2 == 1:
                print("\tldr.w r4, [r1], #4")
                print("\tsxth r12, r4")
                print("\tsmlabt r4, r3, r4, r12")
                print("\tubfx r5, r4, #8, #16")
                print("\tstrb.w r4, [r0], #1")
                print("\tstrh.w r5, [r2], #2")

            if left % 2 == 1:
                print("\tldrh.w r4, [r1]")
                print("\tstrh.w r4, [r2]")
            else:
                cnttail = 0

                if len % 2 == 0:
                    tailradix = oldradix * tailradix

                while tailradix >= 16384:
                    tailradix = (tailradix + 255) // 256
                    cnttail += 1

                print("\tldr.w r5, [r1], #4")
                print("\tsxth r9, r5")
                print("\tsmlabt r5, r3, r5, r9")
                if cnttail == 2:
                    print("\tubfx r6, r5, #16, #16")
                    print("\tstrh.w r5, [r0], #2")
                    print("\tstrh.w r6, [r2], #2")
                elif cnttail == 1:
                    print("\tubfx r6, r5, #8, #16")
                    print("\tstrb.w r5, [r0], #1")
                    print("\tstrh.w r6, [r2], #2")
                elif cnttail == 0:
                    print("\tstrh.w r5, [r2], #2")


        elif cntOutputBytes == 0:
            print("\tldr.w r5, [r1, #4]")
            print("\tldr.w r6, [r1, #8]")
            print("\tldr.w r7, [r1, #12]")
            print("\tldr.w r8, [r1, #16]")
            print("\tldr.w r9, [r1, #20]")
            print("\tldr.w r10, [r1, #24]")
            print("\tldr.w r11, [r1, #28]")
            print("\tldr.w r4, [r1], #32")

            for i in range(4, 12):
                print("\tsxth r12, r" + str(i))
                print("\tsmlabt r" + str(i) + ", r3, r" + str(i) + ", r12")

            for i in range(4):
                print("\tpkhbt r" + str(12-i) + ", r" + str(10-i*2) + ", r" + str(11-i*2) + ", lsl #16")

            print("\tstr.w r10, [r2, #4]")
            print("\tstr.w r11, [r2, #8]")
            print("\tstr.w r12, [r2, #12]")
            print("\tstr.w r9, [r2], #16")
            print("\tcmp.w r1, lr")
            print("\tbne.w Encode_Rounded_asm_radix" + str(oldradix))
            left = (len-ss) % 16

            for i in range(left // 2 - 1):
                print("\tldr.w r" + str(5+i) + ", [r1, #" + str((i+1)*4) + "]")

            print("\tldr.w r4, [r1], #" + str((left//2)*4))

            for i in range(4, 4 + (left//2)):
                print("\tsxth r12, r" + str(i))
                print("\tsmlabt r" + str(i) + ", r3, r" + str(i) + ", r12")

            for i in range((left//2)//2):
                print("\tpkhbt r" + str(4+i) + ", r" + str(4+i*2) + ", r" + str(5+i*2) + ", lsl #16")

            for i in range((left//2)//2):
                print("\tstr.w r" + str(4+i) + ", [r2], #4")

            if (left//2) % 2 == 1:
                print("\tstrh.w r" + str(3+(left//2)) + ", [r2], #2")
            
            if left % 2 == 1:
                print("\tldrh.w r4, [r1]")
                print("\tstrh.w r4, [r2]")
            else:
                cnttail = 0

                if len % 2 == 0:
                    tailradix = oldradix * tailradix

                while tailradix >= 16384:
                    tailradix = (tailradix + 255) // 256
                    cnttail += 1

                print("\tldr.w r5, [r1], #4")
                print("\tsxth r9, r5")
                print("\tsmlabt r5, r3, r5, r9")
                if cnttail == 2:
                    print("\tubfx r6, r5, #16, #16")
                    print("\tstrh.w r5, [r0], #2")
                    print("\tstrh.w r6, [r2], #2")
                elif cnttail == 1:
                    print("\tubfx r6, r5, #8, #16")
                    print("\tstrb.w r5, [r0], #1")
                    print("\tstrh.w r6, [r2], #2")
                elif cnttail == 0:
                    print("\tstrh.w r5, [r2], #2")
        
        len = (len+1)//2

    while len > 2:
        print("\tvmov r1, s1")
        print("\tvmov r2, s1")
        print("@ iteration " + str(iter))
        print("@ len = " + str(len))
        print("@ tail radix = " + str(tailradix))
        iter += 1
        print("\tmov.w r3, #" + str(radix))

        ss = 0
        cnttail = 0
        if len % 2 == 0:
            ss = 2
            tailradix = radix * tailradix
            while tailradix > 16384:
                tailradix = (tailradix+255) // 256
                cnttail += 1

        cntOutputBytes = 0
        radix = pow(radix, 2)
        while radix >= 16384:
            radix = (radix+255)//256
            cntOutputBytes += 1

        left = (len-ss)
        if cntOutputBytes == 2:
            for i in range(left//4):
                print("\tldr.w r5, [r1, #4]")
                print("\tldr.w r4, [r1], #8")
                print("\tsxth r12, r4")
                print("\tsmlabt r4, r3, r4, r12")
                print("\tsxth r12, r5")
                print("\tsmlabt r5, r3, r5, r12")
                print("\tpkhbt r6, r4, r5, lsl #16")
                print("\tpkhtb r7, r5, r4, asr #16")
                print("\tstr.w r6, [r0], #4")
                print("\tstr.w r7, [r2], #4")
            
            if (left % 4) // 2 == 1:
                print("\tldr.w r4, [r1], #4")
                print("\tsxth r12, r4")
                print("\tsmlabt r4, r3, r4, r12")
                print("\tubfx r5, r4, #16, #16")
                print("\tstrh.w r4, [r0], #2")
                print("\tstrh.w r5, [r2], #2")

            if left % 2 == 1:
                print("\tldrh.w r4, [r1]")
                print("\tstrh.w r4, [r2]")
            else:
                print("\tldr.w r5, [r1], #4")
                print("\tsxth r9, r5")
                print("\tsmlabt r5, r3, r5, r9")
                if cnttail == 2:
                    print("\tubfx r6, r5, #16, #16")
                    print("\tstrh.w r5, [r0], #2")
                    print("\tstrh.w r6, [r2], #2")
                elif cnttail == 1:
                    print("\tubfx r6, r5, #8, #16")
                    print("\tstrb.w r5, [r0], #1")
                    print("\tstrh.w r6, [r2], #2")
                elif cnttail == 0:
                    print("\tstrh.w r5, [r2], #2")

        elif cntOutputBytes == 1:
            for i in range(left // 8):
                print("\tldr.w r5, [r1, #4]")
                print("\tldr.w r6, [r1, #8]")
                print("\tldr.w r7, [r1, #12]")
                print("\tldr.w r4, [r1], #16")
                
                for i in range(4, 8):
                    print("\tsxth r12, r" + str(i))
                    print("\tsmlabt r" + str(i) + ", r3, r" + str(i) + ", r12")

                for i in range(4):
                    print("\tbfi r9, r" + str(i+4) + ", #" + str(i*8) + ", #8")

                print("\tlsr.w r6, #8")
                print("\tpkhbt r8, r6, r7, lsl #8") # str # 4
                print("\tlsr.w r4, #8")
                print("\tpkhbt r7, r4, r5, lsl #8") # str # 0
                print("\tstr.w r9, [r0], #4")
                print("\tstr.w r8, [r2, #4]")
                print("\tstr.w r7, [r2], #8")

            left = left % 8
            if left // 2 == 3:
                print("\tldr.w r5, [r1, #4]")
                print("\tldr.w r6, [r1, #8]")
                print("\tldr.w r4, [r1], #12")

                for i in range(4, 7):
                    print("\tsxth r12, r" + str(i))
                    print("\tsmlabt r" + str(i) + ", r3, r" + str(i) + ", r12")

                for i in range(2):
                    print("\tbfi r9, r" + str(i+4) + ", #" + str(i*8) + ", #8")

                print("\tlsr.w r4, #8")
                print("\tpkhbt r4, r4, r5, lsl #8")
                print("\tubfx r7, r6, #8, #16")
                print("\tstrh.w r9, [r0], #2")
                print("\tstrb.w r6, [r0], #1")
                print("\tstr.w r4, [r2], #4")
                print("\tstrh.w r7, [r2], #2")

            elif left // 2 == 2:
                print("\tldr.w r5, [r1, #4]")
                print("\tldr.w r4, [r1], #8")

                for i in range(4, 6):
                    print("\tsxth r12, r" + str(i))
                    print("\tsmlabt r" + str(i) + ", r3, r" + str(i) + ", r12")

                for i in range(2):
                    print("\tbfi r9, r" + str(i+4) + ", #" + str(i*8) + ", #8")

                print("\tlsr.w r4, #8")
                print("\tpkhbt r4, r4, r5, lsl #8")
                print("\tstrh.w r9, [r0], #2")
                print("\tstr.w r4, [r2], #4")

            elif left // 2 == 1:
                print("\tldr.w r4, [r1], #4")
                print("\tsxth r12, r4")
                print("\tsmlabt r4, r3, r4, r12")
                print("\tubfx r5, r4, #8, #16")
                print("\tstrb.w r4, [r0], #1")
                print("\tstrh.w r5, [r2], #2")

            if left % 2 == 1:
                print("\tldrh.w r4, [r1]")
                print("\tstrh.w r4, [r2]")
            else:
                print("\tldr.w r5, [r1], #4")
                print("\tsxth r9, r5")
                print("\tsmlabt r5, r3, r5, r9")
                if cnttail == 2:
                    print("\tubfx r6, r5, #16, #16")
                    print("\tstrh.w r5, [r0], #2")
                    print("\tstrh.w r6, [r2], #2")
                elif cnttail == 1:
                    print("\tubfx r6, r5, #8, #16")
                    print("\tstrb.w r5, [r0], #1")
                    print("\tstrh.w r6, [r2], #2")
                elif cnttail == 0:
                    print("\tstrh.w r5, [r2], #2")
        
        elif cntOutputBytes == 0:
            for i in range(left // 8):
                print("\tldr.w r5, [r1, #4]")
                print("\tldr.w r6, [r1, #8]")
                print("\tldr.w r7, [r1, #12]")
                print("\tldr.w r4, [r1], #16")
                
                for i in range(4, 8):
                    print("\tsxth r12, r" + str(i))
                    print("\tsmlabt r" + str(i) + ", r3, r" + str(i) + ", r12")

                print("\tpkhbt r8, r6, r7, lsl #16") # str # 4
                print("\tpkhbt r7, r4, r5, lsl #16") # str # 0
                print("\tstr.w r8, [r2, #4]")
                print("\tstr.w r7, [r2], #8")

            left = left % 8
            for i in range(left//2 - 1):
                print("\tldr.w r" + str(5+i) + ", [r1, #" + str((i+1)*4) + "]")

            print("\tldr.w r4, [r1], #" + str((left//2) * 4))
        
            for i in range(4, 4 + (left//2)):
                print("\tsxth r12, r" + str(i))
                print("\tsmlabt r" + str(i) + ", r3, r" + str(i) + ", r12")

            for i in range((left//2)//2):
                print("\tpkhbt r" + str(4+i) + ", r" + str(4+i*2) + ", r" + str(5+i*2) + ", lsl #16")

            for i in range((left//2)//2):
                print("\tstr.w r" + str(4+i) + ", [r2], #4")

            if (left//2) % 2 == 1:
                print("\tstrh.w r" + str(3+(left//2)) + ", [r2], #2")
            
            if left % 2 == 1:
                print("\tldrh.w r4, [r1]")
                print("\tstrh.w r4, [r2]")
            else:
                print("\tldr.w r5, [r1], #4")
                print("\tsxth r9, r5")
                print("\tsmlabt r5, r3, r5, r9")
                if cnttail == 2:
                    print("\tubfx r6, r5, #16, #16")
                    print("\tstrh.w r5, [r0], #2")
                    print("\tstrh.w r6, [r2], #2")
                elif cnttail == 1:
                    print("\tubfx r6, r5, #8, #16")
                    print("\tstrb.w r5, [r0], #1")
                    print("\tstrh.w r6, [r2], #2")
                elif cnttail == 0:
                    print("\tstrh.w r5, [r2], #2")

        len = (len+1)//2    

    print("@ len == 2")
    print("@ tail radix = " + str(tailradix))
    print("\tvmov.w r1, s1")
    print("\tvmov.w r2, s1")
    print("\tmov.w r3, #" + str(radix))
    cntOutputBytes = 0
    tailradix = radix * tailradix
    while tailradix > 16384:
        tailradix = (tailradix + 255) // 256
        cntOutputBytes += 1
    
    print("\tldr.w r4, [r1], #4")
    print("\tsxth r9, r4")
    print("\tsmlabt r4, r3, r4, r9")
    if cntOutputBytes == 2:
        print("\tubfx r5, r4, #16, #16")
        print("\tstrh.w r4, [r0], #2")
        print("\tstrh.w r5, [r2], #2")
    elif cntOutputBytes == 1:
        print("\tubfx r5, r4, #8, #16")
        print("\tstrb.w r4, [r0], #1")
        print("\tstrh.w r5, [r2], #2")
    elif cntOutputBytes == 0:
        print("\tstrh.w r4, [r2], #2")

    print("@ len == 1")

    cntOutputBytes = 0
    while tailradix > 1:
        tailradix = (tailradix + 255) // 256
        cntOutputBytes += 1

    print("\tvmov.w r1, s1")
    print("\tldrh.w r2, [r1]")
    if cntOutputBytes == 1:
        print("\tstrb.w r2, [r0]")
    elif cntOutputBytes == 2:
        print("\tstrh.w r2, [r0]")
    
    print("\tpop {r2-r12, pc}\n")

p=761
q=4591
b=16

if len(sys.argv) == 2 or len(sys.argv) > 4:
    print("usage: $python3 genEncode.py [polylength] [prime] [basesize of unroll](optional)")
    sys.exit()
elif len(sys.argv) == 3:
    p = int(sys.argv[1])
    q = int(sys.argv[2])
elif len(sys.argv) == 4:
    p = int(sys.argv[1])
    q = int(sys.argv[2])
    b = int(sys.argv[3])

genEncodeRq(p,q,b)
genEncodeRounded(p,q,b)
    