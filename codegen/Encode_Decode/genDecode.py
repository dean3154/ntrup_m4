import math
import sys

def genHead(s : str):
    print(".p2align 2,,3")
    print(".syntax unified")
    print(".text")
    print(".global " + s)
    print(".type " + s + ", %function")
    print(s + ":")

def barcoef(radix : int) -> int:
    # bar = math.ceil((1<<32)/radix)
    # bar = round((1<<32)/radix)
    bar = (1<<32) // radix
    return bar

def radix_reduce(target_r : str, barcoef_r : str, radix_r : str, bufForConst_r : str, free_r : list, radix : int):
    print("\tsmmul " + free_r[0] + ", " + target_r + ", " + barcoef_r)
    print("\tmls " + target_r + ", " + free_r[0] + ", " + radix_r + ", " + target_r)
    print("\tsmmul " + free_r[1] + ", " + target_r + ", " + bufForConst_r)
    print("\tmls " + target_r + ", " + free_r[1] + ", " + radix_r + ", " + target_r)
    print("\tadd.w " + free_r[0] + ", "+ free_r[0] + ", " + free_r[1])
    print("\tpkhbt " + target_r + ", " + target_r + ", " + free_r[0] + ", lsl #16")
    
def decode_length_4x(outbytes : int):
    print("\tldr.w r4, [r0, #-4]")
    print("\tldr.w r3, [r0, #-8]!")
    if outbytes == 2:
        print("\tldr.w r6, [r1, #-4]")
        print("\tldr.w r5, [r1, #-8]!")
        print("\tpkhtb r8, r4, r6, asr #16")
        print("\tpkhbt r7, r6, r4, lsl #16")
        print("\tpkhtb r6, r3, r5, asr #16")
        print("\tpkhbt r5, r5, r3, lsl #16")
    elif outbytes == 1:
        print("\tldr.w r5, [r1, #-4]!")

        print("\tubfx r8, r4, #16, #16")
        print("\tubfx r7, r5, #24, #8")
        print("\tadd.w r8, r7, r8, lsl #8")

        print("\tubfx r7, r4, #0, #16")
        print("\tubfx r6, r5, #16, #8")
        print("\tadd.w r7, r6, r7, lsl #8")

        print("\tubfx r6, r3, #16, #16")
        print("\tubfx r4, r5, #8, #8")
        print("\tadd.w r6, r4, r6, lsl #8")

        print("\tubfx r4, r5, #0, #8")
        print("\tubfx r5, r3, #0, #16")
        print("\tadd.w r5, r4, r5, lsl #8")
    else:
        assert outbytes == 0
        print("\tubfx r8, r4, #16, #16")
        print("\tubfx r7, r4, #0, #16")
        print("\tubfx r6, r3, #16, #16")
        print("\tubfx r5, r3, #0, #16")

def decode_length_mod4(length : int, outbytes : int):
    assert length < 4

    if length == 3:
        print("\tldrh.w r4, [r0, #-2]")
        print("\tldr.w r3, [r0, #-6]!")
        if outbytes == 2:
            print("\tldrh.w r6, [r1, #-2]")
            print("\tldr.w r5, [r1, #-6]!")
            print("\tpkhbt r7, r6, r4, lsl #16")
            print("\tpkhtb r6, r3, r5, asr #16")
            print("\tpkhbt r5, r5, r3, lsl #16")
        elif outbytes == 1:
            print("\tldrb.w r6, [r1, #-1]")
            print("\tldrh.w r5, [r1, #-3]!")

            print("\tadd.w r7, r6, r4, lsl #8")

            print("\tubfx r6, r3, #16, #16")
            print("\tubfx r4, r5, #8, #8")
            print("\tadd.w r6, r4, r6, lsl #8")

            print("\tubfx r4, r5, #0, #8")
            print("\tubfx r5, r3, #0, #16")
            print("\tadd.w r5, r4, r5, lsl #8")
        else:
            assert outbytes == 0
            print("\tubfx r7, r4, #0, #16")
            print("\tubfx r6, r3, #16, #16")
            print("\tubfx r5, r3, #0, #16")
    elif length == 2:
        print("\tldr.w r3, [r0, #-4]!")
        if outbytes == 2:
            print("\tldr.w r5, [r1, #-4]!")
            print("\tpkhtb r6, r3, r5, asr #16")
            print("\tpkhbt r5, r5, r3, lsl #16")
        elif outbytes == 1:
            print("\tldrh.w r5, [r1, #-2]!")

            print("\tubfx r6, r3, #16, #16")
            print("\tubfx r4, r5, #8, #8")
            print("\tadd.w r6, r4, r6, lsl #8")

            print("\tubfx r4, r5, #0, #8")
            print("\tubfx r5, r3, #0, #16")
            print("\tadd.w r5, r4, r5, lsl #8")
        else:
            assert outbytes == 0
            print("\tubfx r6, r3, #16, #16")
            print("\tubfx r5, r3, #0, #16")
    elif length == 1:
        print("\tldrh.w r3, [r0, #-2]!")
        if outbytes == 2:
            print("\tldrh.w r5, [r1, #-2]!")
            print("\tpkhbt r5, r5, r3, lsl #16")
        elif outbytes == 1:
            print("\tldrb.w r5, [r1, #-1]!")
            print("\tadd.w r5, r5, r3, lsl #8")
        else:
            assert outbytes == 0
            print("\tubfx r5, r3, #0, #16")

def getSettings(length : int, radix : int):
    lengthlist = []
    odd = []
    radixlist = []
    radixoutbytes = []
    tailradixlist = []
    tailoutbytes = []
    tailradix = radix
    serialbytes = 0
    while length > 2:
        lengthlist.append(length)
        radixlist.append(radix)
        tailradixlist.append(tailradix)

        if length % 2 == 1:
            odd.append(True)
        else:
            odd.append(False)

        cnttail = 0
        if length % 2 == 0:
            tailradix = tailradix * radix
            while tailradix >= 16384:
                tailradix = (tailradix+255)//256
                cnttail += 1
        tailoutbytes.append(cnttail)
        serialbytes += cnttail

        cntout = 0
        radix = pow(radix, 2)
        while radix >= 16384:
            radix = (radix+255)//256
            cntout += 1
        radixoutbytes.append(cntout)

        serialbytes += cntout * ((length-1)//2)
        
        length = (length+1)//2

    assert length == 2

    odd.append(False)
    lengthlist.append(2)
    radixlist.append(radix)
    tailradixlist.append(tailradix)
    radixoutbytes.append(0)
    tailradix = tailradix * radix
    cnttail = 0
    while tailradix >= 16384:
        tailradix = (tailradix+255)//256
        cnttail += 1
    tailoutbytes.append(cnttail)
    serialbytes += cnttail

    odd.append(True)
    lengthlist.append(1)
    radixlist.append(tailradix)
    tailradixlist.append(tailradix)
    radixoutbytes.append(0)
    cnttail = 0
    while tailradix > 1:
        tailradix = (tailradix+255)//256
        cnttail += 1
    tailoutbytes.append(cnttail)
    serialbytes += cnttail

    lengthlist.reverse()
    odd.reverse()
    radixlist.reverse()
    radixoutbytes.reverse()
    tailradixlist.reverse()
    tailoutbytes.reverse()

    return lengthlist, odd, radixlist, radixoutbytes, tailradixlist, tailoutbytes, serialbytes
    

def genDecodeRq(p : int, q : int, basecase : int):
    lengthlist, odd, radixlist, radixoutbytes, tailradixlist, tailoutbytes, serialbytes = getSettings(p, q)

    iter = 0
    genHead("Decode_Rq_asm")
    print("\tpush.w {r2-r12, lr}")
    print("\tadd.w r1, r1, #" + str(serialbytes))
    while iter < len(lengthlist)-1:
        length = lengthlist[iter]
        print("@ length = " + str(length) + ", radix = " + str(radixlist[iter]))

        if length == 1:
            assert iter == 0
            if tailoutbytes[iter] == 1:
                print("\tldrb.w r5, [r1, #-1]!")
            elif tailoutbytes[iter] == 2:
                print("\tldrh.w r5, [r1, #-2]!")
            print("\tstrh.w r5, [r0]")
        else:
            assert iter > 0
            barrettcoeff = barcoef(radixlist[iter])
            print("\tadd.w r2, r0, #" + str(lengthlist[iter] * 2) + " @ used for str")
            print("\tadd.w r0, r0, #" + str(lengthlist[iter-1] * 2) + " @ used for ldr")
            print("\tmov.w r11, #" + str(radixlist[iter]) + " @ radix")
            print("\tmovw.w r12, #" + str(barrettcoeff % 65536))
            print("\tmovt.w r12, #" + str(barrettcoeff // 65536) + " @ barrett coefficient")
            print("\tadd.w r10, r12, #1")

            if odd[iter]:
                assert lengthlist[iter-1] > 1 # always : lengthlist[0] = 1, lengthlist[1] = 2
                print("\tldrh.w r5, [r0, #-2]!")
                print("\tstrh.w r5, [r2, #-2]!")
                length -= 1
            else:
                print("\tldrh.w r5, [r0, #-2]!")

                if tailoutbytes[iter] == 1:
                    print("\tldrb.w r6, [r1, #-1]!")
                    print("\tadd.w r5, r6, r5, lsl #8")
                elif tailoutbytes[iter] == 2:
                    print("\tldrh.w r6, [r1, #-2]!")
                    print("\tadd.w r5, r6, r5, lsl #16")

                radix_reduce("r5", "r12", "r11", "r10", ["r3", "r4"], radixlist[iter])
                print("\tstr.w r5, [r2, #-4]!")
                length -= 2
            
            assert length % 2 == 0
            length //= 2 # number of left 16-bit numbers to be load

            if length <= basecase: # unroll
                decode_length_mod4(length % 4, radixoutbytes[iter])
                if length % 4 == 3:
                    radix_reduce("r5", "r12", "r11", "r10", ["r3", "r4"], radixlist[iter])
                    radix_reduce("r6", "r12", "r11", "r10", ["r3", "r4"], radixlist[iter])
                    radix_reduce("r7", "r12", "r11", "r10", ["r3", "r4"], radixlist[iter])
                    print("\tstr.w r7, [r2, #-4]")
                    print("\tstr.w r6, [r2, #-8]")
                    print("\tstr.w r5, [r2, #-12]!")
                elif length % 4 == 2:
                    radix_reduce("r5", "r12", "r11", "r10", ["r3", "r4"], radixlist[iter])
                    radix_reduce("r6", "r12", "r11", "r10", ["r3", "r4"], radixlist[iter])
                    print("\tstr.w r6, [r2, #-4]")
                    print("\tstr.w r5, [r2, #-8]!")
                elif length % 4 == 1:
                    radix_reduce("r5", "r12", "r11", "r10", ["r3", "r4"], radixlist[iter])
                    print("\tstr.w r5, [r2, #-4]!")

                length -= (length % 4)

                while length != 0:
                    decode_length_4x(radixoutbytes[iter])
                    radix_reduce("r5", "r12", "r11", "r10", ["r3", "r4"], radixlist[iter])
                    radix_reduce("r6", "r12", "r11", "r10", ["r3", "r4"], radixlist[iter])
                    radix_reduce("r7", "r12", "r11", "r10", ["r3", "r4"], radixlist[iter])
                    radix_reduce("r8", "r12", "r11", "r10", ["r3", "r4"], radixlist[iter])
                    print("\tstr.w r8, [r2, #-4]")
                    print("\tstr.w r7, [r2, #-8]")
                    print("\tstr.w r6, [r2, #-12]")
                    print("\tstr.w r5, [r2, #-16]!")
                    length -= 4

            else: # loop
                decode_length_mod4(length % 4, radixoutbytes[iter])
                if length % 4 == 3:
                    radix_reduce("r5", "r12", "r11", "r10", ["r3", "r4"], radixlist[iter])
                    radix_reduce("r6", "r12", "r11", "r10", ["r3", "r4"], radixlist[iter])
                    radix_reduce("r7", "r12", "r11", "r10", ["r3", "r4"], radixlist[iter])
                    print("\tstr.w r7, [r2, #-4]")
                    print("\tstr.w r6, [r2, #-8]")
                    print("\tstr.w r5, [r2, #-12]!")
                elif length % 4 == 2:
                    radix_reduce("r5", "r12", "r11", "r10", ["r3", "r4"], radixlist[iter])
                    radix_reduce("r6", "r12", "r11", "r10", ["r3", "r4"], radixlist[iter])
                    print("\tstr.w r6, [r2, #-4]")
                    print("\tstr.w r5, [r2, #-8]!")
                elif length % 4 == 1:
                    radix_reduce("r5", "r12", "r11", "r10", ["r3", "r4"], radixlist[iter])
                    print("\tstr.w r5, [r2, #-4]!")

                length -= (length % 4)

                print("Decode_Rq_asm_radix" + str(radixlist[iter]) + ":")
                decode_length_4x(radixoutbytes[iter])
                radix_reduce("r5", "r12", "r11", "r10", ["r3", "r4"], radixlist[iter])
                radix_reduce("r6", "r12", "r11", "r10", ["r3", "r4"], radixlist[iter])
                radix_reduce("r7", "r12", "r11", "r10", ["r3", "r4"], radixlist[iter])
                radix_reduce("r8", "r12", "r11", "r10", ["r3", "r4"], radixlist[iter])
                print("\tstr.w r8, [r2, #-4]")
                print("\tstr.w r7, [r2, #-8]")
                print("\tstr.w r6, [r2, #-12]")
                print("\tstr.w r5, [r2, #-16]!")
                print("\tcmp.w r0, r2")
                print("\tbne.w Decode_Rq_asm_radix" + str(radixlist[iter]))

        iter += 1

# last iteration    
    assert iter == len(lengthlist) - 1
    assert odd[iter]

    length = lengthlist[iter]
    print("@ length = " + str(length) + ", radix = " + str(radixlist[iter]))
    barrettcoeff = barcoef(radixlist[iter])
    print("\tadd.w r2, r0, #" + str(lengthlist[iter] * 2) + " @ used for str")
    print("\tadd.w r0, r0, #" + str(lengthlist[iter-1] * 2) + " @ used for ldr")
    print("\tmovw.w r9, #" + str(q//2))
    print("\tmovt.w r9, #" + str(q//2))
    print("\tmov.w r11, #" + str(radixlist[iter]) + " @ radix")
    print("\tmovw.w r12, #" + str(barrettcoeff % 65536))
    print("\tmovt.w r12, #" + str(barrettcoeff // 65536) + " @ barrett coefficient")
    print("\tadd.w r10, r12, #1")

    print("\tldrh.w r5, [r0, #-2]!")
    print("\tssub16 r5, r5, r9")
    print("\tstrh.w r5, [r2, #-2]!")

    length -= 1
    assert length % 2 == 0
    length //= 2 # number of left 16-bit numbers to be load

    if length <= basecase: # unroll
        decode_length_mod4(length % 4, radixoutbytes[iter])
        if length % 4 == 3:
            radix_reduce("r5", "r12", "r11", "r10", ["r3", "r4"], radixlist[iter])
            radix_reduce("r6", "r12", "r11", "r10", ["r3", "r4"], radixlist[iter])
            radix_reduce("r7", "r12", "r11", "r10", ["r3", "r4"], radixlist[iter])
            print("\tssub16 r5, r5, r9")
            print("\tssub16 r6, r6, r9")
            print("\tssub16 r7, r7, r9")
            print("\tstr.w r7, [r2, #-4]")
            print("\tstr.w r6, [r2, #-8]")
            print("\tstr.w r5, [r2, #-12]!")
        elif length % 4 == 2:
            radix_reduce("r5", "r12", "r11", "r10", ["r3", "r4"], radixlist[iter])
            radix_reduce("r6", "r12", "r11", "r10", ["r3", "r4"], radixlist[iter])
            print("\tssub16 r5, r5, r9")
            print("\tssub16 r6, r6, r9")
            print("\tstr.w r6, [r2, #-4]")
            print("\tstr.w r5, [r2, #-8]!")
        elif length % 4 == 1:
            radix_reduce("r5", "r12", "r11", "r10", ["r3", "r4"], radixlist[iter])
            print("\tssub16 r5, r5, r9")
            print("\tstr.w r5, [r2, #-4]!")

        length -= (length % 4)

        while length != 0:
            decode_length_4x(radixoutbytes[iter])
            radix_reduce("r5", "r12", "r11", "r10", ["r3", "r4"], radixlist[iter])
            radix_reduce("r6", "r12", "r11", "r10", ["r3", "r4"], radixlist[iter])
            radix_reduce("r7", "r12", "r11", "r10", ["r3", "r4"], radixlist[iter])
            radix_reduce("r8", "r12", "r11", "r10", ["r3", "r4"], radixlist[iter])
            print("\tssub16 r5, r5, r9")
            print("\tssub16 r6, r6, r9")
            print("\tssub16 r7, r7, r9")
            print("\tssub16 r8, r8, r9")
            print("\tstr.w r8, [r2, #-4]")
            print("\tstr.w r7, [r2, #-8]")
            print("\tstr.w r6, [r2, #-12]")
            print("\tstr.w r5, [r2, #-16]!")
            length -= 4

    else: # loop
        decode_length_mod4(length % 4, radixoutbytes[iter])
        if length % 4 == 3:
            radix_reduce("r5", "r12", "r11", "r10", ["r3", "r4"], radixlist[iter])
            radix_reduce("r6", "r12", "r11", "r10", ["r3", "r4"], radixlist[iter])
            radix_reduce("r7", "r12", "r11", "r10", ["r3", "r4"], radixlist[iter])
            print("\tssub16 r5, r5, r9")
            print("\tssub16 r6, r6, r9")
            print("\tssub16 r7, r7, r9")
            print("\tstr.w r7, [r2, #-4]")
            print("\tstr.w r6, [r2, #-8]")
            print("\tstr.w r5, [r2, #-12]!")
        elif length % 4 == 2:
            radix_reduce("r5", "r12", "r11", "r10", ["r3", "r4"], radixlist[iter])
            radix_reduce("r6", "r12", "r11", "r10", ["r3", "r4"], radixlist[iter])
            print("\tssub16 r5, r5, r9")
            print("\tssub16 r6, r6, r9")
            print("\tstr.w r6, [r2, #-4]")
            print("\tstr.w r5, [r2, #-8]!")
        elif length % 4 == 1:
            radix_reduce("r5", "r12", "r11", "r10", ["r3", "r4"], radixlist[iter])
            print("\tssub16 r5, r5, r9")
            print("\tstr.w r5, [r2, #-4]!")

        length -= (length % 4)

        print("Decode_Rq_asm_radix" + str(radixlist[iter]) + ":")
        decode_length_4x(radixoutbytes[iter])
        radix_reduce("r5", "r12", "r11", "r10", ["r3", "r4"], radixlist[iter])
        radix_reduce("r6", "r12", "r11", "r10", ["r3", "r4"], radixlist[iter])
        radix_reduce("r7", "r12", "r11", "r10", ["r3", "r4"], radixlist[iter])
        radix_reduce("r8", "r12", "r11", "r10", ["r3", "r4"], radixlist[iter])
        print("\tssub16 r5, r5, r9")
        print("\tssub16 r6, r6, r9")
        print("\tssub16 r7, r7, r9")
        print("\tssub16 r8, r8, r9")
        print("\tstr.w r8, [r2, #-4]")
        print("\tstr.w r7, [r2, #-8]")
        print("\tstr.w r6, [r2, #-12]")
        print("\tstr.w r5, [r2, #-16]!")
        print("\tcmp.w r0, r2")
        print("\tbne.w Decode_Rq_asm_radix" + str(radixlist[iter]))

    iter += 1
    assert iter == len(lengthlist)
    print("\tpop.w {r2-r12, pc}\n")


def genDecodeRounded(p : int, q : int, basecase : int):
    lengthlist, odd, radixlist, radixoutbytes, tailradixlist, tailoutbytes, serialbytes = getSettings(p, (q+2)//3)

    iter = 0
    genHead("Decode_Rounded_asm")
    print("\tpush.w {r2-r12, lr}")
    print("\tadd.w r1, r1, #" + str(serialbytes))
    while iter < len(lengthlist)-1:
        length = lengthlist[iter]
        print("@ length = " + str(length) + ", radix = " + str(radixlist[iter]))

        if length == 1:
            assert iter == 0
            if tailoutbytes[iter] == 1:
                print("\tldrb.w r5, [r1, #-1]!")
            elif tailoutbytes[iter] == 2:
                print("\tldrh.w r5, [r1, #-2]!")
            print("\tstrh.w r5, [r0]")
        else:
            assert iter > 0
            barrettcoeff = barcoef(radixlist[iter])
            print("\tadd.w r2, r0, #" + str(lengthlist[iter] * 2) + " @ used for str")
            print("\tadd.w r0, r0, #" + str(lengthlist[iter-1] * 2) + " @ used for ldr")
            print("\tmov.w r11, #" + str(radixlist[iter]) + " @ radix")
            print("\tmovw.w r12, #" + str(barrettcoeff % 65536))
            print("\tmovt.w r12, #" + str(barrettcoeff // 65536) + " @ barrett coefficient")
            print("\tadd.w r10, r12, #1")

            if odd[iter]:
                assert lengthlist[iter-1] > 1 # always : lengthlist[0] = 1, lengthlist[1] = 2
                print("\tldrh.w r5, [r0, #-2]!")
                print("\tstrh.w r5, [r2, #-2]!")
                length -= 1
            else:
                print("\tldrh.w r5, [r0, #-2]!")

                if tailoutbytes[iter] == 1:
                    print("\tldrb.w r6, [r1, #-1]!")
                    print("\tadd.w r5, r6, r5, lsl #8")
                elif tailoutbytes[iter] == 2:
                    print("\tldrh.w r6, [r1, #-2]!")
                    print("\tadd.w r5, r6, r5, lsl #16")

                radix_reduce("r5", "r12", "r11", "r10", ["r3", "r4"], radixlist[iter])
                print("\tstr.w r5, [r2, #-4]!")
                length -= 2
            
            assert length % 2 == 0
            length //= 2 # number of left 16-bit numbers to be load

            if length <= basecase: # unroll
                decode_length_mod4(length % 4, radixoutbytes[iter])
                if length % 4 == 3:
                    radix_reduce("r5", "r12", "r11", "r10", ["r3", "r4"], radixlist[iter])
                    radix_reduce("r6", "r12", "r11", "r10", ["r3", "r4"], radixlist[iter])
                    radix_reduce("r7", "r12", "r11", "r10", ["r3", "r4"], radixlist[iter])
                    print("\tstr.w r7, [r2, #-4]")
                    print("\tstr.w r6, [r2, #-8]")
                    print("\tstr.w r5, [r2, #-12]!")
                elif length % 4 == 2:
                    radix_reduce("r5", "r12", "r11", "r10", ["r3", "r4"], radixlist[iter])
                    radix_reduce("r6", "r12", "r11", "r10", ["r3", "r4"], radixlist[iter])
                    print("\tstr.w r6, [r2, #-4]")
                    print("\tstr.w r5, [r2, #-8]!")
                elif length % 4 == 1:
                    radix_reduce("r5", "r12", "r11", "r10", ["r3", "r4"], radixlist[iter])
                    print("\tstr.w r5, [r2, #-4]!")

                length -= (length % 4)

                while length != 0:
                    decode_length_4x(radixoutbytes[iter])
                    radix_reduce("r5", "r12", "r11", "r10", ["r3", "r4"], radixlist[iter])
                    radix_reduce("r6", "r12", "r11", "r10", ["r3", "r4"], radixlist[iter])
                    radix_reduce("r7", "r12", "r11", "r10", ["r3", "r4"], radixlist[iter])
                    radix_reduce("r8", "r12", "r11", "r10", ["r3", "r4"], radixlist[iter])
                    print("\tstr.w r8, [r2, #-4]")
                    print("\tstr.w r7, [r2, #-8]")
                    print("\tstr.w r6, [r2, #-12]")
                    print("\tstr.w r5, [r2, #-16]!")
                    length -= 4

            else: # loop
                decode_length_mod4(length % 4, radixoutbytes[iter])
                if length % 4 == 3:
                    radix_reduce("r5", "r12", "r11", "r10", ["r3", "r4"], radixlist[iter])
                    radix_reduce("r6", "r12", "r11", "r10", ["r3", "r4"], radixlist[iter])
                    radix_reduce("r7", "r12", "r11", "r10", ["r3", "r4"], radixlist[iter])
                    print("\tstr.w r7, [r2, #-4]")
                    print("\tstr.w r6, [r2, #-8]")
                    print("\tstr.w r5, [r2, #-12]!")
                elif length % 4 == 2:
                    radix_reduce("r5", "r12", "r11", "r10", ["r3", "r4"], radixlist[iter])
                    radix_reduce("r6", "r12", "r11", "r10", ["r3", "r4"], radixlist[iter])
                    print("\tstr.w r6, [r2, #-4]")
                    print("\tstr.w r5, [r2, #-8]!")
                elif length % 4 == 1:
                    radix_reduce("r5", "r12", "r11", "r10", ["r3", "r4"], radixlist[iter])
                    print("\tstr.w r5, [r2, #-4]!")

                length -= (length % 4)

                print("Decode_Rounded_asm_radix" + str(radixlist[iter]) + ":")
                decode_length_4x(radixoutbytes[iter])
                radix_reduce("r5", "r12", "r11", "r10", ["r3", "r4"], radixlist[iter])
                radix_reduce("r6", "r12", "r11", "r10", ["r3", "r4"], radixlist[iter])
                radix_reduce("r7", "r12", "r11", "r10", ["r3", "r4"], radixlist[iter])
                radix_reduce("r8", "r12", "r11", "r10", ["r3", "r4"], radixlist[iter])
                print("\tstr.w r8, [r2, #-4]")
                print("\tstr.w r7, [r2, #-8]")
                print("\tstr.w r6, [r2, #-12]")
                print("\tstr.w r5, [r2, #-16]!")
                print("\tcmp.w r0, r2")
                print("\tbne.w Decode_Rounded_asm_radix" + str(radixlist[iter]))

        iter += 1

# last iteration    
    assert iter == len(lengthlist) - 1
    assert odd[iter]

    length = lengthlist[iter]
    print("@ length = " + str(length) + ", radix = " + str(radixlist[iter]))
    barrettcoeff = barcoef(radixlist[iter])
    print("\tadd.w r2, r0, #" + str(lengthlist[iter] * 2) + " @ used for str")
    print("\tadd.w r0, r0, #" + str(lengthlist[iter-1] * 2) + " @ used for ldr")
    print("\tmovw.w r9, #" + str(q//2))
    print("\tmovt.w r9, #" + str(q//2))
    print("\tmov.w r11, #" + str(radixlist[iter]) + " @ radix")
    print("\tmovw.w r12, #" + str(barrettcoeff % 65536))
    print("\tmovt.w r12, #" + str(barrettcoeff // 65536) + " @ barrett coefficient")
    print("\tadd.w r10, r12, #1")

    print("\tldrh.w r5, [r0, #-2]!")
    print("\tuadd16 r4, r5, r5")
    print("\tuadd16 r5, r5, r4")
    print("\tssub16 r5, r5, r9")
    print("\tstrh.w r5, [r2, #-2]!")

    length -= 1
    assert length % 2 == 0
    length //= 2 # number of left 16-bit numbers to be load

    if length <= basecase: # unroll
        decode_length_mod4(length % 4, radixoutbytes[iter])
        if length % 4 == 3:
            radix_reduce("r5", "r12", "r11", "r10", ["r3", "r4"], radixlist[iter])
            radix_reduce("r6", "r12", "r11", "r10", ["r3", "r4"], radixlist[iter])
            radix_reduce("r7", "r12", "r11", "r10", ["r3", "r4"], radixlist[iter])

            print("\tuadd16 r4, r5, r5")
            print("\tuadd16 r5, r5, r4")
            print("\tuadd16 r4, r6, r6")
            print("\tuadd16 r6, r6, r4")
            print("\tuadd16 r4, r7, r7")
            print("\tuadd16 r7, r7, r4")

            print("\tssub16 r5, r5, r9")
            print("\tssub16 r6, r6, r9")
            print("\tssub16 r7, r7, r9")

            print("\tstr.w r7, [r2, #-4]")
            print("\tstr.w r6, [r2, #-8]")
            print("\tstr.w r5, [r2, #-12]!")
        elif length % 4 == 2:
            radix_reduce("r5", "r12", "r11", "r10", ["r3", "r4"], radixlist[iter])
            radix_reduce("r6", "r12", "r11", "r10", ["r3", "r4"], radixlist[iter])

            print("\tuadd16 r4, r5, r5")
            print("\tuadd16 r5, r5, r4")
            print("\tuadd16 r4, r6, r6")
            print("\tuadd16 r6, r6, r4")

            print("\tssub16 r5, r5, r9")
            print("\tssub16 r6, r6, r9")

            print("\tstr.w r6, [r2, #-4]")
            print("\tstr.w r5, [r2, #-8]!")
        elif length % 4 == 1:
            radix_reduce("r5", "r12", "r11", "r10", ["r3", "r4"], radixlist[iter])

            print("\tuadd16 r4, r5, r5")
            print("\tuadd16 r5, r5, r4")

            print("\tssub16 r5, r5, r9")
            print("\tstr.w r5, [r2, #-4]!")

        length -= (length % 4)

        while length != 0:
            decode_length_4x(radixoutbytes[iter])
            radix_reduce("r5", "r12", "r11", "r10", ["r3", "r4"], radixlist[iter])
            radix_reduce("r6", "r12", "r11", "r10", ["r3", "r4"], radixlist[iter])
            radix_reduce("r7", "r12", "r11", "r10", ["r3", "r4"], radixlist[iter])
            radix_reduce("r8", "r12", "r11", "r10", ["r3", "r4"], radixlist[iter])

            print("\tuadd16 r4, r5, r5")
            print("\tuadd16 r5, r5, r4")
            print("\tuadd16 r4, r6, r6")
            print("\tuadd16 r6, r6, r4")
            print("\tuadd16 r4, r7, r7")
            print("\tuadd16 r7, r7, r4")
            print("\tuadd16 r4, r8, r8")
            print("\tuadd16 r8, r8, r4")


            print("\tssub16 r5, r5, r9")
            print("\tssub16 r6, r6, r9")
            print("\tssub16 r7, r7, r9")
            print("\tssub16 r8, r8, r9")
            print("\tstr.w r8, [r2, #-4]")
            print("\tstr.w r7, [r2, #-8]")
            print("\tstr.w r6, [r2, #-12]")
            print("\tstr.w r5, [r2, #-16]!")
            length -= 4

    else: # loop
        decode_length_mod4(length % 4, radixoutbytes[iter])
        if length % 4 == 3:
            radix_reduce("r5", "r12", "r11", "r10", ["r3", "r4"], radixlist[iter])
            radix_reduce("r6", "r12", "r11", "r10", ["r3", "r4"], radixlist[iter])
            radix_reduce("r7", "r12", "r11", "r10", ["r3", "r4"], radixlist[iter])

            print("\tuadd16 r4, r5, r5")
            print("\tuadd16 r5, r5, r4")
            print("\tuadd16 r4, r6, r6")
            print("\tuadd16 r6, r6, r4")
            print("\tuadd16 r4, r7, r7")
            print("\tuadd16 r7, r7, r4")

            print("\tssub16 r5, r5, r9")
            print("\tssub16 r6, r6, r9")
            print("\tssub16 r7, r7, r9")
            print("\tstr.w r7, [r2, #-4]")
            print("\tstr.w r6, [r2, #-8]")
            print("\tstr.w r5, [r2, #-12]!")
        elif length % 4 == 2:
            radix_reduce("r5", "r12", "r11", "r10", ["r3", "r4"], radixlist[iter])
            radix_reduce("r6", "r12", "r11", "r10", ["r3", "r4"], radixlist[iter])

            print("\tuadd16 r4, r5, r5")
            print("\tuadd16 r5, r5, r4")
            print("\tuadd16 r4, r6, r6")
            print("\tuadd16 r6, r6, r4")

            print("\tssub16 r5, r5, r9")
            print("\tssub16 r6, r6, r9")
            print("\tstr.w r6, [r2, #-4]")
            print("\tstr.w r5, [r2, #-8]!")
        elif length % 4 == 1:
            radix_reduce("r5", "r12", "r11", "r10", ["r3", "r4"], radixlist[iter])

            print("\tuadd16 r4, r5, r5")
            print("\tuadd16 r5, r5, r4")

            print("\tssub16 r5, r5, r9")
            print("\tstr.w r5, [r2, #-4]!")

        length -= (length % 4)

        print("Decode_Rounded_asm_radix" + str(radixlist[iter]) + ":")
        decode_length_4x(radixoutbytes[iter])
        radix_reduce("r5", "r12", "r11", "r10", ["r3", "r4"], radixlist[iter])
        radix_reduce("r6", "r12", "r11", "r10", ["r3", "r4"], radixlist[iter])
        radix_reduce("r7", "r12", "r11", "r10", ["r3", "r4"], radixlist[iter])
        radix_reduce("r8", "r12", "r11", "r10", ["r3", "r4"], radixlist[iter])

        print("\tuadd16 r4, r5, r5")
        print("\tuadd16 r5, r5, r4")
        print("\tuadd16 r4, r6, r6")
        print("\tuadd16 r6, r6, r4")
        print("\tuadd16 r4, r7, r7")
        print("\tuadd16 r7, r7, r4")
        print("\tuadd16 r4, r8, r8")
        print("\tuadd16 r8, r8, r4")

        print("\tssub16 r5, r5, r9")
        print("\tssub16 r6, r6, r9")
        print("\tssub16 r7, r7, r9")
        print("\tssub16 r8, r8, r9")

        print("\tstr.w r8, [r2, #-4]")
        print("\tstr.w r7, [r2, #-8]")
        print("\tstr.w r6, [r2, #-12]")
        print("\tstr.w r5, [r2, #-16]!")

        print("\tcmp.w r0, r2")
        print("\tbne.w Decode_Rounded_asm_radix" + str(radixlist[iter]))

    iter += 1
    assert iter == len(lengthlist)
    print("\tpop.w {r2-r12, pc}\n")
    

p=761
q=4591
b=16

if len(sys.argv) == 2 or len(sys.argv) > 4:
    print("usage: $python3 genDecode.py [polylength] [prime] [basesize of unroll](optional)")
    sys.exit()
elif len(sys.argv) == 3:
    p = int(sys.argv[1])
    q = int(sys.argv[2])
elif len(sys.argv) == 4:
    p = int(sys.argv[1])
    q = int(sys.argv[2])
    b = int(sys.argv[3])

genDecodeRq(p, q, b)
genDecodeRounded(p, q, b)