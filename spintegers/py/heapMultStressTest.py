#!/usr/bin/python
import random
import heapMult
import sparseInt
from threading import Thread

def stressTest():
    count     = 0
    product   = 0
    sparseAns = 0
    while(product == sparseAns):
        rand1 = random.randint(0,10000000000)
        rand2 = random.randint(0,10000000000)
        product =rand1 *rand2
        a = sparseInt.SparseInt(rand1)
        b= sparseInt.SparseInt(rand2)
        sparseAns = int(sparseInt.SparseInt(
            heapMult.HeapMult.sparseHeapMult(a.digits,b.digits)))
        count += 1
    print "failed with "+str(rand1)+" and  "+str(rand2) 
    print "It worked "+count+" times"
stressTest()
