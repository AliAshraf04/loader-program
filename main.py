import re
import string


def stringtoInt(String):
    return int(String)


def hextoDec(hexaString):
    return int(hexaString, 16)


def dectoHex(decimal):
    Hexa = hex(decimal)[2:].upper()
    return Hexa


def main():
    VectorFile = []
    OpcodeByte = []
    MemoryAddress = []
    OpcodeMemory = []
    OpLength = []
    Header = ""
    Text = []
    End = ""

    # Read the file content
    with open("HTE.txt", "r") as myfile:
        VectorFile = myfile.readlines()

    VectorFile = [line.strip() for line in VectorFile]

    Header = VectorFile[0]
    MemoryAddress.append(dectoHex(hextoDec(Header[7:13])))
    startLength = hextoDec(MemoryAddress[0])

    if len(MemoryAddress[0]) < 4:
        zeros = "0" * (4 - len(MemoryAddress[0]))
        MemoryAddress[0] = zeros + MemoryAddress[0]

    length = dectoHex(hextoDec(Header[13:19]))
    memoryLength = hextoDec(length)

    End = VectorFile[-1]
    endLength = startLength + memoryLength

    for i in range(1, len(VectorFile) - 1):
        Text.append(VectorFile[i])

    for i in range(len(Text)):
        byteCounter = 0
        OpcodeMemory.append(dectoHex(hextoDec(Text[i][1:7])))
        OpLength.append(hextoDec(Text[i][7:9]))

        for j in range(OpLength[-1]):
            OpcodeByte.append(Text[i][9 + byteCounter:11 + byteCounter])
            byteCounter += 2

    totalLength = sum(OpLength)
    z = 0
    j = 0
    remainder = hextoDec(dectoHex(endLength)[:3] + "F") - endLength

    for i in range(startLength, endLength + 1):
        MemoryAddress.append(dectoHex(i + 1))

        if (hextoDec(MemoryAddress[i - startLength]) % 16 == 0 and
                (OpcodeMemory[z][:3] + "F" >= MemoryAddress[i - startLength] >= OpcodeMemory[z][:3] + "0")):
            if len(MemoryAddress[i - startLength]) == 0:
                print("0000" + MemoryAddress[i - startLength], end='\t')
            elif len(MemoryAddress[i - startLength]) == 1:
                print("000" + MemoryAddress[i - startLength], end='\t')
            elif len(MemoryAddress[i - startLength]) == 2:
                print("00" + MemoryAddress[i - startLength], end='\t')
            elif len(MemoryAddress[i - startLength]) == 3:
                print("0" + MemoryAddress[i - startLength], end='\t')
            else:
                print(MemoryAddress[i - startLength], end='\t')

        if (hextoDec(MemoryAddress[i - startLength]) >= hextoDec(OpcodeMemory[z]) and
                hextoDec(MemoryAddress[i - startLength]) < hextoDec(OpcodeMemory[z]) + OpLength[z]):
            print(OpcodeByte[j], end='')
            if (hextoDec(MemoryAddress[i - startLength]) + 1 == hextoDec(OpcodeMemory[z]) + OpLength[z] and
                    z < len(OpcodeMemory) - 1):
                z += 1
            j += 1
        else:
            rem = hextoDec(MemoryAddress[i - startLength][:3] + "F") - hextoDec(MemoryAddress[i - startLength])
            if 0 < rem <= 15:
                print("xx", end='')
            elif rem == 0:
                print("xx\n", end='')

        if hextoDec(MemoryAddress[i - startLength + 1]) % 4 == 0:
            print('\t', end='')

    for i in range(endLength + 1, endLength + remainder + 1):
        if i % 4 == 0:
            print('\t', end='')
        print("xx", end='')


if __name__ == "__main__":
    main()
