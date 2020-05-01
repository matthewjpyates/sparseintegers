import sparseInt
import sys
import heapMult
def doMath(a,b,op):
    if(op=="add"):
        return a+b
    elif(op=="mult"):
        return a - b
    elif(op=="mod"):
        return a % b
    elif(op=="sub"):
        return a -b 
    elif(op=="eq"):
        return a == b
    elif(op=="gt"):
        return a > b
    elif(op=="gte"):
        return a>=b
    elif(op=="heapMult"):
        return sparseInt.SparseInt(heapMult.HeapMult.sparseHeapMult(a.digits,
            b.digits))
    return []


if(not(len(sys.argv)==4)):
    print "python sparseTest.py operator num1 num2"
    sys.exit()

first  = int(sys.argv[2])
second = int(sys.argv[3])
op = sys.argv[1]

result = doMath(sparseInt.SparseInt(first),
        sparseInt.SparseInt(second),op)
print int(result)
