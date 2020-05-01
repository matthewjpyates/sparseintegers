#!/usr/bin/python
import rrrsparse
import heapMult
import sparseInt
def doMath(a,b,c):
    # get the correct answers
    if(c==0):
        c=1
    powModNorm = a**b % c
    ra = rrrsparse.RRRSparse(a)
    rb = rrrsparse.RRRSparse(b)
    rc = rrrsparse.RRRSparse(c)
    result = rrrsparse.RRRSparse()
    result = result.powMod(ra,rb,rc)
    if(result != powModNorm):
        print "Pow Mod Failed"
        print "Sparse gave " + str(int(result))
        print "Normal math gave " + str(powModNorm)
        return False
    return True

stillTrue = True
base = 10
lastBase = -1
while(stillTrue):
    for i in xrange(base):
        for j in xrange(i):
            for k in xrange(i):
                stillTrue = doMath(i,j,k)
                if(not(stillTrue)):
                    print "Failed on: "+str(i) +"^"+str(j)+"%"+str(k)
                    break
            if(not(stillTrue)):
                break
        if(not(stillTrue)):
            break
    if(stillTrue):
        print "Proven up to "+str(base)
        lastBase = base
        base *= 10

