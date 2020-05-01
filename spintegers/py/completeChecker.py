#!/usr/bin/python
import rrrsparse
import heapMult
import sparseInt
def doMath(a,b):
    # get the correct answers
    normSum = a + b
    normDiff = a - b
    normMult = a * b
    normNe = a != b
    normEq = a==b
    normLt = a<b
    normLte = a<=b
    normGt = a>b
    normGte = a>=b

    if(b!=0):
        normDiv = a // b
    if(b!=0):
        normMod = a % b
    # first test sparse int
    """asp = sparseInt.SparseInt(a)
    bsp = sparseInt.SparseInt(b)
    if(asp + bsp != normSum):
        print "Sum Failed"
        return False
    if(asp - bsp != normDiff):
        print "Difference Failed"
        return False
    if(asp * bsp != normMult):
        print "Normal Multiplication Failed"
        return False
    if(b>0):
        if(asp / bsp != normDiv):
            print "Division Failed"
            return False
        if(asp % bsp != normMod):
            print "Modulus Failed"
            return False
    if(sparseInt(heapMult.HeapMult.sparseHeapMult(asp.digits,bsp.digits))!=
            normMult):
        print "Heap Mult Failed"
        return False"""
    # Now Test the sparse rrr

    ra = rrrsparse.RRRSparse(a)
    rb = rrrsparse.RRRSparse(b)
    if(ra +rb != normSum):
        print "RRR Sum Failed"
        return False
    #ra = rrrsparse.RRRSparse(a)
    #rb = rrrsparse.RRRSparse(b)
    
    if(ra  - rb != normDiff):
        print "RRR Sub Failed"
        #print "had " +str(int(ra -rb)) + " when it needed "+str(normDiff)
        return False
    #ra = rrrsparse.RRRSparse(a)
    #rb = rrrsparse.RRRSparse(b)
    if(ra * rb != normMult):
        print "RRR Mult Failed"
        return False
    #ra = rrrsparse.RRRSparse(a)
    #rb = rrrsparse.RRRSparse(b)
    if b!=0:
        #ra = rrrsparse.RRRSparse(a)
        #rb = rrrsparse.RRRSparse(b)
        # print (ra / rb).digits
        product = ra/rb
        if( product != normDiv):
            print "RRR Div Failed"
            print "Normal Math gave " + str(normDiv)
            print "Sparse Math gave " + str(product)
            return False
    #ra = rrrsparse.RRRSparse(a)
    #rb = rrrsparse.RRRSparse(b)
    if(b!=0 and b>0 and a>0):  
        temp = ra % rb
        if(temp != normMod):
            print "RRR mod failed"
            print "Sparse gave " +str(int(temp))
            print "Real Math gave "+str(normMod)
            return False
    #return True"""
    # boolean section
    #ra = rrrsparse.RRRSparse(a)
    #rb = rrrsparse.RRRSparse(b)
    if(ra != rb)!=normNe:
        print "RRR Not Equal failed"
        return False
    if(ra == rb)!=normEq:
        print "RRR Equal failed"
        return False
    if(ra < rb)!=normLt:
        print "RRR Less Than failed"
        return False
    if(ra <= rb)!=normLte:
        print "RRR Less Than or Equal failed"
        return False
    if(ra > rb)!=normGt:
        print "RRR Greaer failed"
        return False
    if(ra >= rb)!=normGte:
        print "RRR Greater Than or Equal failed"
        return False
    return True

stillTrue = True
base = 10
lastBase = -1
while(stillTrue):
    for i in xrange(base):
        for j in xrange(i):
            stillTrue = doMath(i,j)
            if(not(stillTrue)):
                print "Failed on "+str(i) +" and "+str(j)
                break
            stillTrue = doMath(-1*i,j)
            if(not(stillTrue)):
                print "Failed on "+str(-1*i) +" and "+str(j)
                break
            stillTrue = doMath(i,-1*j)
            if(not(stillTrue)):
                print "Failed on "+str(i) +" and "+str(-1*j)
                break
            stillTrue = doMath(-1*i,-1*j)
            if(not(stillTrue)):
                print "Failed on "+str(-1*i) +" and "+str(-1*j)
                break
            stillTrue = doMath(j,i)
            if(not(stillTrue)):
                print "Failed on "+str(j) +" and "+str(i)
                break
            stillTrue = doMath(-1*j,i)
            if(not(stillTrue)):
                print "Failed on "+str(-1*j) +" and "+str(i)
                break
            stillTrue = doMath(j,-1*i)
            if(not(stillTrue)):
                print "Failed on "+str(j) +" and "+str(-1*i)
                break
            stillTrue = doMath(-1*j,-1*i)
            if(not(stillTrue)):
                print "Failed on "+str(-1*j) +" and "+str(-1*i)
                break
        if(not(stillTrue)):
            break
    if(stillTrue):
        print "Proven up to "+str(base)
        lastBase = base
        base *= 10

