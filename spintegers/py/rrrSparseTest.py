#!/usr/bin/python
import random
import rrrsparse



def stressTest():
    count     = 0
    product   = 0
    sparseAns = 0
    rand1 = random.randint(0,10000000000)
    rand2 = random.randint(0,10000000000)
    if(rand2>rand2):
        temp = rand2
        rand2 = rand1
        rand1 = temp
    productNorm = rand1 * rand2
    sumNorm     = rand1 + rand2
    diffNorm    = rand1 - rand2
    quotNorm    = rand1 / rand2
    modNorm     = rand1 % rand2
    a = rrrsparse.RRRSparse(rand1)
    b = rrrsparse.RRRSparse(rand2)
    if(int(a+b)!=sumNorm):
        print "Failed on "+ str(rand1) + " + " + str(rand2)
        return False
    #if(int(a*b)!=productNorm):
    #    print "Failed on "+ str(rand1) + " * " + str(rand2)
    #    return False
    #if(int(a-b)!=diffNorm):
    #    print "Failed on "+ str(rand1) + " - " + str(rand2)
    #    return False
    #if(int(a/b)!=quotNorm):
    #    print "Failed on "+ str(rand1) + " / " + str(rand2)
    #    return False
    #if(int(a%b)!=modNorm):
    #    print "Failed on "+ str(rand1) + " % " + str(rand2)
    #    return False
    return True

count = 0
while(stressTest()):
    count += 1    

print "It worked "+str(count)+" times"
