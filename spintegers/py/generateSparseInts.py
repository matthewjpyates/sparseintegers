#!/usr/bin/python
# generates random numbers
import random
import sys

def bits2int(bits):
	out = 0
	for bit in bits:
		out += 2**bit
	return out
def addToList(bit,bitList):
    if(len(bitList)==0):
        out = []
        out.append(bit)
        return out
    for ii in xrange(len(bitList)):
        if(bitList[ii]==bit):
            return bitList
        if(bitList[ii]>bit):
            bitList.insert(ii,bit)
            return bitList
    bitList.append(bit)
    return bitList
def naiveRandom(numberOfBits,maxmiumSize,howManyNumbers):
    out = []
    for ii in xrange(howManyNumbers):
        setBits = random.randrange(numberOfBits)
        num = bits2int(random.sample(xrange(maxmiumSize),setBits))
        out.append([setBits,num])
    return out

def smartRandom(numberOfBits,maxmiumSize,howManyNumbers):
    out = []
    for ii in xrange(howManyNumbers):
        bits = []
        for jj in xrange(numberOfBits):
            bits = addToList(random.randrange(maxmiumSize), bits)
        setBits = len(bits)
        num = bits2int(bits)
        out.append([setBits,num])
    return out

def smartRandomHighestBit(numberOfBits,maxmiumSize,howManyNumbers):
    out = []
    for ii in xrange(howManyNumbers):
        bits = []
        for jj in xrange(numberOfBits):
            bits = addToList(random.randrange(maxmiumSize), bits)
        setBits = len(bits)
        num = bits2int(bits)
	bits.sort()
        out.append([bits[-1],setBits,num])
    return out

def main():
    if(len(sys.argv) < 4):
        print "./generateSparseInts.py maxNumberOfBits highestBit howManyNumbers [useNaiveMethod]"
        sys.exit()
    numberOfBits = int(sys.argv[1])
    maxmiumSize = int(sys.argv[2])
    howManyNumbers = int(sys.argv[3])
    if(len(sys.argv) > 4 and bool(sys.argv[4])):
        nums = naiveRandom(numberOfBits,maxmiumSize,howManyNumbers)
    else:
        nums = smartRandom(numberOfBits,maxmiumSize,howManyNumbers)
    for num in nums:
        print str(num[0]) +","+str(num[1])
if (__name__ == "__main__" ): main()
