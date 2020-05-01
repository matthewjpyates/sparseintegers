"""Module for sparse Redundant Radix Representation (signed-digit) integers."""

import copy
import functools
import heapMult
import sparseInt
@functools.total_ordering
class RRRSparse(object):
    
    """A Sparse integer with -1/+1 digits"""

    def __init__(self, value=0):
        """Creates a new RRRSparse with the given value.
        
        The value can be an integer, an array, or another RRRSparse."""
        
        self.digits = []
        if isinstance(value, RRRSparse):
            self.digits = value.digits

        elif isinstance(value, list):
            self.digits = value
        
        else:
            ival = int(value)
            tempdigits = []
            sign = 1 if ival >= 0 else -1
            while(ival != 0):
                if ival & 1:  # if odd
                    tempdigits.append(sign)
                    ival -= sign
                else:
                    tempdigits.append(0)
                ival //= 2

            index=0
            for i in tempdigits:
                if(i!=0):
                    self.digits = self.sparseExt(list(self.digits),list([i,index]))
                index+=1

    def oldStr(self):
        outStr = ""
        place = 0
        if(len(self.digits)==0):
            return ""
        for d in xrange(0,self.digits[-1][1]+1):
            if(self.digits[place][1] == d):
                if(self.digits[place][0]>0):
                    outStr += "+"
                else:
                    outStr += "-"
                place += 1
            else:
                outStr += "0"
        return outStr

    def powMod(self,base,power,mod):
        if(len(mod.digits)==0):
            raise Exception("Modded by 0 in powMod")
        if(len(power.digits)==0):
            if(mod==1):
                return RRRSparse()
            elif(base.digits[-1][0]>0):
                return RRRSparse(1)%mod
            else:
                return RRRSparse(-1)%mod
        if(power.digits[-1][0]<0):
            raise Exception("That is a negitive power, these are sparse Ints not sparse floating points")
        if(len(base.digits)==0):
            return RRRSparse()
        result = RRRSparse(1)
        sn = False
        p = 0
        d = power.digits
        for ii in xrange(d[-1][1]+1):
            if d[p][1] == ii:
                if not(sn):
                    result = (result* base.deepcopy()) %  mod.deepcopy()
                sn = d[p][0]<1
                p += 1
            else:
                if sn:
                    result = (result* base.deepcopy()) %  mod.deepcopy()
            base  = (base * base.deepcopy()) % mod.deepcopy()
        return result
     
    def sparseHeapMult(self,a, b):
        if(len(a)==0 or len(b)==0):
            return []
        out = []
        heap = []
        if(len(a)<len(b)):
            shiftList = a
            suppList = b
        else:
            shiftList = b
            suppList = a
        shift = 1
        place = 0
        x  = shiftList[0]
        for e in suppList:
            heap.append(0)
            temp = [e[0]*x[0],x[1]+e[1]]
            heap[-1] = temp
        heap=self.getMin(heap)
        out.append(heap.pop(0))
        while(len(heap)>0 and shift<len(shiftList)):
            if(heap[0][1] == shiftList[shift][1]+suppList[place][1]):
                if(heap[0][0]==suppList[place][0]*shiftList[place][0]):
                    heap = self.getMin(heap)
                    temp = heap.pop(0)
                    temp[1] += 1
                    heap = self.heapEnque(heap,temp)
                place += 1
            elif(heap[0][1] < shiftList[shift][1]+suppList[place][1]):
                heap = self.getMin(heap)
                z = heap.pop(0)
                out = sparseExt(out,z)
                place += 1
            if(place  == len(suppList)):
                 place = 0
                 shift += 1
        while(shift<len(shiftList)):
            heap = self.heapEnque(heap,[shiftList[shift][0]*suppList[place][0],shiftList[shift][1]+suppList[place][1]])
            place += 1
            if(place  == len(suppList)):
                 place = 0
                 shift += 1
        while(len(heap)>0):
            heap = self.getMin(heap)
            z = heap.pop(0)
            out = sparseExt(out,z)

        return out

    def signedsparseMod(self, num, mod):
        if(len(num)==0):
            return []
        if(len(mod)==0):
            return []
        out = []
        pos1=[]
        neg1=[]
        pos2=[]
        neg2=[]
        for ii in xrange(len(num)):
            if(mod[ii][0]>0):
                pos1.append(num[ii][1])
            else:
                neg1.append(num[ii][1])
        for ii in xrange(len(mod)):
            if(mod[ii][0]>0):
                pos2.append(mod[ii][1])
            else:
                neg2.append(mod[ii][1])
        posResult = sparseInt.SparseInt.decMod(pos1,neg2)
        negResult = sparseInt.SparseInt.decMod(neg1,neg2)
        for ii in xrange(len(posResult)):
            posResult[ii]=[1,posResult[ii]]
        for ii in xrange(len(negResult)):
            negResult[ii]=[1,negResult[ii]]
        return self.smartAdd(posResult,negResult)

    def bitSort(self,num):
        index = 0
        for ii in xrange(len(num)):
            minbit = num[ii][1]
            minplace = 0
            for jj in xrange(ii,len(num)):
                if(num[jj][1]<minbit):
                    minplace = jj
                    minbit = num[jj][1]
            temp = num[ii]
            num[ii] = num[minplace]
            num[minplace]=temp
        return num

    def bitFix(self,inNum):
        outNum = []
        inNum = self.bitSort(inNum)
        for ii in inNum:
            outNum = self.sparseExt(outNum,ii)
        return outNum


    def bitShift(self, realnum, amt):
        out =[]
        num = self.godDamnPythonWithYourLists(realnum)
        for n in xrange(len(num)):
            out.append(0)
            out[-1] = [num[n][0],num[n][1]+amt]
        return out
    def bitFlip(self, realnum, mod):
        out =[]
        num = self.godDamnPythonWithYourLists(realnum)
        for n in num:
            out.append(0)
            out[-1] = [n[0]*mod,n[1]]
        return out


    """In essence, if you're doing Q = N/D:
    1. Align the most-significant ones of N and D.
    2. Compute t = (N - D);.
    3. If (t >= 0), then set the lsb of Q to 1, and set N = t.
    4. Left-shift N by 1.
    5. Left-shift Q by 1.
    6. Go to step 2."""
    def bitwiselongdivWrapper(self,num1,num2):
        if(num1[-1][1]<num2[-1][1]):
            return []
        if(len(num2)==1 and num2[0][1]==1):
            return self.bitFlip(num1,num2[0][0]) 
        def bitwiselongdiv(self,num1,num2,count):
            if(self.lessThan(num1,num2)):
                return RRRSparse(count).digits
            if(self.equal(num1,num2)):
                return RRRSparse(count +1).digits
            #shift = num1[-1][1] - num2[-1][1]
            #block = self.bitShift(num2,shift)
            num1 = self.sparsesub(num1,num2)
            count += 1
            return bitwiselongdiv(self,num1,num2,count)
        return bitwiselongdiv(self,num1,num2,1)
    
    
    def reallyStupidDiv(self,n1,n2):
        if(len(n2)==0):
            return []
        if(len(n1)==0):
            return []
        big = []
        small = []
        out = RRRSparse()
        while():
            big.digits= sparsesub(big.digits,small.digits)
            out += RRRSparse(1)
    class SignedHeap:
        """ A list based implementation of a min heap logic for signed bits"""
        def __init__(self,initHeap=[]):
            self.heap = initHeap
            self.buff = []
            self.isBuffSet = False

        def enque(self, bit):
            if len(self.heap) == 0:
                self.heap == copy.deepcopy(bit)
            else:
                self.heap.append(0)
                self.heap[-1] = copy.deepcopy(bit)
                # fix the heap
                place = len(self.heap) -1
                while(place>0 and self.heap[place][1]<self.heap[(place-1)/2][1]):
                    temp = copy.deepcopy(self.heap[place])
                    self.heap[place] = copy.deepcopy(self.heap[(place-1)/2])
                    self.heap[(place-1)/2]= temp
                    place = (place -1)/2

        def deque(self):
            """Returns the least bit on the heap"""
            if len(self.heap) == 0:
                raise Exception("The Heap is empty jerk");
            elif len(self.heap) <= 2:
                return self.heap.pop()
            else:
                holder = self.heap.pop(0)
                #fix the heap
                temp = self.heap.pop(len(self.heap)-1)
                self.heap.insert(0,temp)
                place = 0
                while (place + 1)*2 - 1 < len(self.heap):
                    if((place + 1)*2  < len(self.heap)):
                        if self.heap[(place+1)*2][1]>= self.heap[place][1] and self.heap[(place+1)*2 -1][1]>= self.heap[place][1]:
                            break
                        elif self.heap[(place+1)*2][1] < self.heap[place][1] and self.heap[(place+1)*2 -1][1]>= self.heap[place][1]:
                            temp = copy.deepcopy(self.heap[(place+1)*2])
                            self.heap[(place+1)*2] = copy.deepcopy(self.heap[place])
                            self.heap[place] = temp
                            place = (place+1)*2
                        else:
                            temp = copy.deepcopy(self.heap[(place+1)*2-1])
                            self.heap[(place+1)*2 -1] = copy.deepcopy(self.heap[place])
                            self.heap[place] = temp
                            place = (place+1)*2 - 1
                    else:
                        if self.heap[(place+1)*2 -1][1]>= self.heap[place][1]:
                            break
                        else:
                            temp = copy.deepcopy(self.heap[(place+1)*2-1])
                            self.heap[(place+1)*2 -1] = copy.deepcopy(self.heap[place])
                            self.heap[place] = temp
                            break
                return holder

        def bufferedPop(self):
            if(not(self.isBuffSet)):
                self.isBuffSet = True
                self.buff = self.deque()
            if len(self.heap) ==0:
                self.isBuffSet = False
                return self.buff    
            top = self.heap[0]
            while top[1] == self.buff[1]+1 or top[1]==self.buff[1]:
                if(top[1]==self.buff[1]):
                    # +*2  --> 0+
                    # (+|-) --> 0
                    if(top[0]==self.buff[0]):
                        top = self.deque()
                        top[1] += 1
                        self.enque(top)
                    self.buff= self.deque()
                    if len(self.heap) ==0:
                        self.isBuffSet = False
                        top = self.buff
                        self.buff = []
                        break
                    top = self.heap[0]
                else:
                    # ++ -> -0+
                    # -- -> +0-
                    if(top[0]==self.buff[0]):
                        top = self.deque()
                        top[1] += 1
                        self.enque(top)
                        self.buff[1] *= -1
                        top = self.heap[0]
                    else:
                        # -+ --> +0
                        # +- --> -0
                        self.buff = self.deque()
                        self.buff[0] *= -1
                        if len(self.heap) ==0:
                            self.isBuffSet = False
                            top = self.buff
                            self.buff = []
                            break
                        top = self.heap[0]
            if not(self.isBuffSet):
                return top
            top = self.buff
            buff = self.deque() 
            if(len(self.heap)==0):
                self.heap.append(0)
                self.heap[0] = self.buff
                self.buff = []
                self.isBuffSet = False
            return top




    def deepcopy(self):
        other = RRRSparse()
        other.digits = self.godDamnPythonWithYourLists(self.digits)
        return other
    
    def __copy__(self):
        other = RRRSparse()
        other.digits = copy.copy(self.digits)
        return other


    def anotherBitShift(self,shift):
        for d in self.digits:
            d[1] += shift[1]
            d[0] *= shift[0]


    def simpleMult(self, n1, n2):
        """Takes 2 RRRSparse objects and performs a bitwise 
        multiplication and returns the product"""
        if(len(n1.digits) ==0 or len(n2.digits) ==0):
            self.digits= []
        elif len(n1.digits) ==1:
            self = n2.deepcopy()
            self.anotherBitShift(n1.digits[-1])
        elif len(n2.digits) ==1:
            self = n1.deepcopy()
            self.anotherBitShift(n2.digits[-1])
        else:
            self = n1.deepcopy()
            self.anotherBitShift(n2.digits[0])
            for i in xrange(1,len(n2.digits)):
                temp = n1.deepcopy()
                temp.anotherBitShift(n2.digits[i])
                self.digits = self.smartAdd(self.digits, temp.digits)
        return self


    def anotherMult(self,n1,n2):
        if(len(n1.digits) ==0 or len(n2.digits) ==0):
            self.digits= []
        elif len(n1.digits) ==1:
            self = n2.deepcopy()
            self.anotherBitShift(n1.digits[-1])
        elif len(n2.digits) ==1:
            self = n1.deepcopy()
            self.anotherBitShift(n2.digits[-1])
        else:
            nonHeapWay = True
            if(nonHeapWay):
                # nonheap implemenatation
                self = n1.deepcopy()
                self.anotherBitShift(n2.digits[0])
                for i in xrange(1,len(n2.digits)):
                    temp = n1.deepcopy()
                    temp.anotherBitShift(n2.digits[i])
                    self.digits = self.smartAdd(self.digits, temp.digits)

            else:
                # Heap implementation
                self =  n1.deepcopy()
                self.anotherBitShift(n2.digits[0])
                multheap = self.SignedHeap(self.digits)
                self.digits = []
                i =1
                j = 0
                while i<len(n2.digits):
                    temp = [n1.digits[j][0]*n2.digits[i][0],n1.digits[j][1]+n2.digits[i][1]] 
                    multheap.enque(temp)
                    temp = multheap.bufferedPop()
                    self.digits = self.sparseExt(self.digits,temp) 
                    j += 1
                    if(j>=len(n1.digits)):
                        j = 0
                        i += 1
                while(len(multheap.heap)>0):
                    temp = multheap.bufferedPop()
                    self.digits = self.sparseExt(self.digits,temp)
        return self

    def eq(self, other):
        return not(self.neBit(self.digits,other.digits))
   
    def lte(self,other):
        return self.ltBit(self.digits,other.digits)

    def lteBit(self,first,other):
        fl =len(first)
        ol = len(other)
        if(fl == 0):
            if(ol==0):
                return False
            return other[-1][0]>0
        if(ol==0):
            return first[-1][0]<0
        shift = 1
        sl = min(len(first),len(other))
        while shift<=sl:
            if(first[fl-shift][0] != other[ol-shift][0]):
                return first[fl-shift][0] < other[ol-shift][0]
            if(first[fl-shift][1] != other[ol-shift][1]):
                return first[fl-shift][1]*first[fl-shift][0] < other[ol-shift][1]* other[ol-shift][0] 
            shift += 1
        if shift<= fl:
            return first[fl-shift][0] < 0
        if shift <= ol:
            return other[ol-shift][0] > 0
        return True
    
    def ltBitNoSign(self,first,other):
        fl =len(first)
        ol = len(other)
        if(fl == 0):
            return ol!=0
        if(ol==0):
            return True
        shift = 1
        if(fl ==1):
            if(ol==1):
                return first[0][1]<other[0][1]
            elif(first[0][1]<other[-1][1]):
                return True
            elif(first[0][1]>other[-1][1]):
                return False
            else:
                return other[len(other)-2][0]>0
        elif(ol ==1):
            if(first[-1][1]<other[-1][1]):
                return True
            elif(first[-1][1]>other[-1][1]):
                return False
            else:
                return first[len(first)-2][0]<0

            
        sl = min(len(first),len(other))
        while shift<=sl:
            if(first[fl-shift][1] != other[ol-shift][1]):
                return first[fl-shift][1] < other[ol-shift][1] 
            shift += 1
        if shift<= fl:
            return first[fl-shift][0]*first[-1][0] < 0
        if shift <= ol:
            return other[ol-shift][0]*other[-1][0]  > 0
        return False

    def ltBitNoSignOther(self,first,other):
        first = self.absBit(copy.deepcopy(first))
        other =  self.absBit(copy.deepcopy(other))
        return self.ltBit(first,other)

    def ltBit(self,first,other):
        fl =len(first)
        ol = len(other)
        if(fl == 0):
            if(ol==0):
                return False
            return other[-1][0]>0
        if(ol==0):
            return first[-1][0]<0
        shift = 1
        sl = min(len(first),len(other))
        while shift<=sl:
            if(first[fl-shift][0] != other[ol-shift][0]):
                return first[fl-shift][0] < other[ol-shift][0]
            if(first[fl-shift][1] != other[ol-shift][1]):
                return first[fl-shift][1]*first[fl-shift][0] < other[ol-shift][1]* other[ol-shift][0] 
            shift += 1
        if shift<= fl:
            return first[fl-shift][0] < 0
        if shift <= ol:
            return other[ol-shift][0] > 0
        return False

    def lt(self,other):
        return self.ltBit(self.digits,other.digits)


    def gtBit(self,first,other):
        return not(self.lteBit(first,other))

    def gt(self,other):
        return self.gtBit(self.digits, other.digits)
    
    def gteBit(self,first,other):
        return not(self.ltBit(first,other))

    def gte(self,other):
        return self.gteBit(self.digits, other.digits)






    def ne(self,other):
        return self.neBit(self.digits,other.digits)

    def neBit(self,first,other):
        selfl = len(first)
        otherl = len(other)
        if(selfl != otherl):
            return True
        if(selfl==0):
            return False
        if(selfl==1):
            if(first[0][1] == other[0][1]):
                if(first[0][0] == other[0][0]):
                    return False
            return True

        shift = 1
        while shift<=selfl:
            if(first[selfl-shift][1] != other[selfl-shift][1]):
                return True
            else:
                if(first[selfl-shift][0] != other[selfl-shift][0]):
                    return True
            shift += 1
        return False

    def quorem(self,num,div):
        """calculates the quotient and remainder at once"""
        if len(div.digits) == 0:
            raise Exception("Oh no!!! Divide by zero");
        if len(num.digits) ==0:
            return [[],[]]
        if abs(num.deepcopy())<abs(div.deepcopy()):
            if (num.digits[-1][0] < 0 and  div.digits[-1][0] >0) or (num.digits[-1][0] > 0 and div.digits[-1][0] <0 ):
                return [RRRSparse(-1).digits,[]]
            return  [[],[]]
        if self.ltBitNoSignOther(num.deepcopy().digits, div.deepcopy().digits):
            return [[],div.deepcopy().digits]
        if len(num.digits)==1 and len(div.digits)==1:
            temp = []
            temp.append(0)
            temp.append(0)
            temp[0] = num.digits[0][0]*div.digits[0][0] 
            temp[1] = num.digits[0][1]-div.digits[0][1]
            out = []
            out.append(0)
            out[0] = [temp]
            out.append(0)
            out[1] = []
            return out
        if not(self.neBit(num.deepcopy().digits,div.deepcopy().digits)):
            return [[[1,0]],[]]
        stupid = []
        isFliped = False
        #num.digits = self.sparsesub(num.deepcopy().digits,div.deepcopy().digits)
        if num.digits[-1][0]>0 and div.digits[-1][0]>0 or num.digits[-1][0]<0 and div.digits[-1][0]<0:
            if num.digits[-1][0]<0:
                isFliped = True
                num  = abs(num)
                div = abs(div)
            while (len(num.digits)>0) and not(self.ltBit(num.deepcopy().digits, div.deepcopy().digits)):
                temp = []
                diff = max(num.digits[-1][1] - div.digits[-1][1] -1,0)
                temp = [[1,diff]]
                """for ii in xrange(len(num.digits)):
                    if(num.digits[-1][1]-num.digits[ii][1]<diff):
                        temp.append(0)
                        temp[-1] = copy.deepcopy(num.digits[ii])"""
                stupid = self.smartAdd(stupid,copy.deepcopy(temp))
                #stupid = self.sparsesub(stupid,[[1,0]])
                temp = self.smartMult(temp, div.deepcopy().digits)
                num.digits = self.sparsesub(num.deepcopy().digits,temp)
            if(isFliped):
                num.digits = self.bitFlip(num.digits, -1)
            return [stupid,num.digits]
        startSign = num.digits[-1][0]
        finalSign = num.digits[-1][0]*div.digits[-1][0]
        divS = div.digits[-1][0]
        divcopy = div.deepcopy()
        if divS>0:
            num  = abs(num)
        else:
            div = abs(div)
        while (len(num.digits)>0) and not(self.ltBit(num.deepcopy().digits, div.deepcopy().digits)):
            temp = []
            diff = max(num.digits[-1][1] - div.digits[-1][1] -1,0)
            temp = [[1,diff]]
            """for ii in xrange(len(num.digits)):
                if(num.digits[-1][1]-num.digits[ii][1]<diff):
                    temp.append(0)
                    temp[-1] = copy.deepcopy(num.digits[ii])"""
            stupid = self.smartAdd(stupid,copy.deepcopy(temp))
            #stupid = self.sparsesub(stupid,[[1,0]])
            temp = self.smartMult(temp, div.deepcopy().digits)
            num.digits = self.sparsesub(num.deepcopy().digits,temp)
        if len(num.digits)>0 :
            stupid = self.smartAdd(stupid,[[1,0]])
            num.digits = self.sparsesub(divcopy.digits,self.bitFlip(num.deepcopy().digits,-1))
            #num.digits = self.bitFlip(num.deepcopy().digits, -1) 
        stupid = self.bitFlip(stupid, -1)
        #if divS < 0:
        #    num.digits = self.bitFlip(num.digits, -1)
        #else:
        #    num.digits =self.smartAdd(num.digits,[[1,0]])

        return [stupid,num.digits]
        

    def quoremMOD(self,num,div):
        """calculates the quotient and remainder at once"""
        if len(div.digits) == 0:
            raise Exception("Oh no!!! Divide by zero");
        if len(num.digits) ==0:
            return [[],[]]
        if self.ltBitNoSignOther(num.deepcopy().digits, div.deepcopy().digits):
            return [[],div.deepcopy().digits]
        if len(num.digits)==1 and len(div.digits)==1:
            temp = []
            temp.append(0)
            temp.append(0)
            temp[0] = num.digits[0][0]*div.digits[0][0] 
            temp[1] = num.digits[0][1]-div.digits[0][1]
            out = []
            out.append(0)
            out[0] = [temp]
            out.append(0)
            out[1] = []
            return out
        if not(self.neBit(num.deepcopy().digits,div.deepcopy().digits)):
            return [[[1,0]],[]]
        stupid = []
        isFliped = False
        #num.digits = self.sparsesub(num.deepcopy().digits,div.deepcopy().digits)
        if num.digits[-1][0]>0 and div.digits[-1][0]>0 or num.digits[-1][0]<0 and div.digits[-1][0]<0:
            if num.digits[-1][0]<0:
                isFliped = True
                num  = abs(num)
                div = abs(div)
            while (len(num.digits)>0) and not(self.ltBit(num.deepcopy().digits, div.deepcopy().digits)):
                temp = []
                diff = max(num.digits[-1][1] - div.digits[-1][1] -1,0)
                temp = [[1,diff]]
                """for ii in xrange(len(num.digits)):
                    if(num.digits[-1][1]-num.digits[ii][1]<diff):
                        temp.append(0)
                        temp[-1] = copy.deepcopy(num.digits[ii])"""
                stupid = self.smartAdd(stupid,copy.deepcopy(temp))
                #stupid = self.sparsesub(stupid,[[1,0]])
                temp = self.smartMult(temp, div.deepcopy().digits)
                num.digits = self.sparsesub(num.deepcopy().digits,temp)
            if(isFliped):
                num.digits = self.bitFlip(num.digits, -1)
            return [stupid,num.digits]
        startSign = num.digits[-1][0]
        finalSign = num.digits[-1][0]*div.digits[-1][0]
        divS = div.digits[-1][0]
        divcopy = div.deepcopy()
        if divS>0:
            num  = abs(num)
        else:
            out = self.quorem(-num,-div)
            out[0] = self.bitFlip(out[0],-1)
            out[1] = self.bitFlip(out[1],-1)
            return out
        while (len(num.digits)>0) and not(self.ltBit(num.deepcopy().digits, div.deepcopy().digits)):
            temp = []
            diff = max(num.digits[-1][1] - div.digits[-1][1] -1,0)
            temp = [[1,diff]]
            """for ii in xrange(len(num.digits)):
                if(num.digits[-1][1]-num.digits[ii][1]<diff):
                    temp.append(0)
                    temp[-1] = copy.deepcopy(num.digits[ii])"""
            stupid = self.smartAdd(stupid,copy.deepcopy(temp))
            #stupid = self.sparsesub(stupid,[[1,0]])
            temp = self.smartMult(temp, div.deepcopy().digits)
            num.digits = self.sparsesub(num.deepcopy().digits,temp)
        if len(num.digits)>0 :
            stupid = self.smartAdd(stupid,[[1,0]])
            #num.digits = self.sparsesub(divcopy.digits,self.bitFlip(num.deepcopy().digits,-1))
            #num.digits = self.bitFlip(num.deepcopy().digits, -1) 
        stupid = self.bitFlip(stupid, -1)
        #if divS < 0:
        #    num.digits = self.bitFlip(num.digits, -1)
        #else:
        #    num.digits =self.smartAdd(num.digits,[[1,0]])

        return [stupid,num.digits]
    def quoremwrapper(self,num,div):
        """sovles the signed mod problem and the 0 issues and the divide by 1"""
        if len(div.digits) == 0:
            raise Exception("Oh no!!! Divide by zero");
        if len(num.digits) ==0:
            return [[],[]]
        if abs(div)>abs(num):
            return [[],num.digits]
        if self.ltBitNoSignOther(num.deepcopy().digits, div.deepcopy().digits):
            return [[],div.deepcopy().digits]
        if len(num.digits)==1 and len(div.digits)==1:
            temp = []
            temp.append(0)
            temp.append(0)
            temp[0] = num.digits[0][0]*div.digits[0][0] 
            temp[1] = num.digits[0][1]-div.digits[0][1]
            out = []
            out.append(0)
            out[0] = [temp]
            out.append(0)
            out[1] = []
            return out
        if not(self.neBit(num.deepcopy().digits,div.deepcopy().digits)):
            return [[[1,0]],[]]
        if num.digits[-1][0] == div.digits[-1][0]:
            if num.digits[-1][0] <0:
                numCopy = num.deepcopy()
                divCopy = div.deepcopy()
                numCopy.digits = self.bitFlip(numCopy.digits,-1)
                divCopy.digits = self.bitFlip(divCopy.digits,-1)
                out = self.quoremworker(numCopy,divCopy)
                return [out[0],self.bitFlip(out[1],-1)]
            else:
                return self.quoremworker(num,div)
        else:
            if  div.digits[-1][0]<0:
                numCopy = num.deepcopy()
                divCopy = div.deepcopy()
                numCopy.digits = self.bitFlip(numCopy.digits,-1)
                divCopy.digits = self.bitFlip(divCopy.digits,-1)

                out =  self.quoremwrapper(numCopy,divCopy)
                return [self.bitFlip(out[0],-1),self.bitFlip(out[1],-1)]
            else:
                divcopy = div.deepcopy()
                numCopy = num.deepcopy()
                numCopy.digits = self.bitFlip(numCopy.digits,-1)
                out = self.quoremwrapper(numCopy,div) 
                if len(out[1]) ==0:
                    return [self.bitFlip(out[0],-1),[]]
                else:
                    return [self.sparsesub(self.bitFlip(out[0],-1),[[1,0]]),
                            self.sparsesub(divcopy.digits,out[1])]



    def quoremworker(self,num,div):
        stupid = []
        if(div==num):
            return [[],[]]
        if(div>num):
            return [[],num.digits]
        while (len(num.digits)>0) and not(self.ltBit(num.deepcopy().digits, div.deepcopy().digits)):
            temp = []
            diff = max(num.digits[-1][1] - div.digits[-1][1] -1,0)
            temp = [[1,diff]]
            """for ii in xrange(len(num.digits)):
                if(num.digits[-1][1]-num.digits[ii][1]<diff):
                    temp.append(0)
                    temp[-1] = copy.deepcopy(num.digits[ii])"""
            stupid = self.smartAdd(stupid,copy.deepcopy(temp))
            #stupid = self.sparsesub(stupid,[[1,0]])
            temp = self.smartMult(temp, div.deepcopy().digits)
            num.digits = self.sparsesub(num.deepcopy().digits,temp)
        return [stupid,num.digits]

    def godDamnPythonWithYourLists(self,n):
        out = []
        for e in n:
            out.append(0)
            out[-1]=copy.deepcopy(e)
        return out
    def sumBits(self,n):
        out =0
        for ii in n:
           out += ii[0]*ii[1]
        return out

    def lessThan(self,n1real,n2real):
        n1 = self.godDamnPythonWithYourLists(n1real)
        n2 = self.godDamnPythonWithYourLists(n2real)
        if(len(n1)==0):
            if(len(n2)==0):
                return False
            if(n2[-1][0]<0):
                return False
            return True
        if(len(n2)==0):
            if(n1[-1][0]<0):
                return True
            return False
        place = 0
        while(place<min(len(n1),len(n2))):
            if(n1[-1 - place][0]>n2[-1 - place][0]):
                return False
            if(n1[-1 - place][0]<n2[-1 - place][0]):
                return True
            if(n1[-1 - place][1]*n1[-1 - place][0]<n2[-1 - place][1]*n2[-1 - place][0]):
                return True
            if(n1[-1 - place][1]*n1[-1 - place][0]>n2[-1 - place][1]*n2[-1 - place][0]):
                return False
            place += 1
        if(len(n1)>len(n2)):
            return n1[-1 - place][0]<0
        if(len(n1)<len(n2)):
            return n2[-1 - place][0]>0
        return False

    
    def lessThanOrEqualTo(self,n1real,n2real):
        n1 = self.godDamnPythonWithYourLists(n1real)
        n2 = self.godDamnPythonWithYourLists(n2real)
        if(len(n1)==0):
            if(len(n2)==0):
                return True
            if(n2[-1][0]<0):
                return False
            return True
        if(len(n2)==0):
            if(n1[-1][0]<0):
                return True
            return False
        place = 0
        while(place<min(len(n1),len(n2))):
            if(n1[-1 - place][0]>n2[-1 - place][0]):
                return False
            if(n1[-1 - place][0]<n2[-1 - place][0]):
                return True
            if(n1[-1 - place][1]*n1[-1 - place][0]<n2[-1 - place][1]*n2[-1 - place][0]):
                return True
            if(n1[-1 - place][1]*n1[-1 - place][0]>n2[-1 - place][1]*n2[-1 - place][0]):
                return False
            place += 1
        if(len(n1)>len(n2)):
            return n1[-1 - place][0]<0
        if(len(n1)<len(n2)):
            return n2[-1 - place][0]>0
        return True


    def sparseMod(self,n,m):
        
        if(len(m)==0):
            return n
        if(len(n)==0):
            return 0
        if(len(n)==1 and len(m)==1):
            return []
        while(self.lessThanOrEqualTo(m,n )):
            """if(len(m)==0):
                return n
            if(len(n)==0):
                return []
            if(n[-1][1] - m[-1][1]>1):
                n = self.sparsesub(list(n),self.bitshift(m,-1*(n[-1][1] - m[-1][1] -1)))
            else:"""
            n = self.sparsesub(n,m)


        if(self.equal(n,m)):
            return []
        return n

    def equal(self,n1,n2):
        n12 = self.godDamnPythonWithYourLists(n1)
        n22= self.godDamnPythonWithYourLists(n2) 
        return len(self.sparsesub(n12,n22))==0

    def getMin(self, heap):
        out = heap.pop(0)
        if(len(heap)==0):
            return out
        heap.insert(0,heap.pop(len(heap)-1))
        index = 0
        size = len(heap)
        while(index<size and
                (((index*2+1)<size and heap[index*2+1][1]<heap[index][1])
                    or ((index*2+2)<size and heap[index*2+2][1]<heap[index][1]))):
                if(index*2+2<size):
                    if(heap[index*2+2][1]<heap[index*2+1][1]):
                        temp = heap[index]
                        heap[index] = heap[index*2+2]
                        heap[index*2+2] = temp
                        index = index*2 +2
                    else:
                        temp = heap[index]
                        heap[index] = heap[index*2+1]
                        heap[index*2+1] = temp
                        index = index*2 + 1
                else:
                    temp = heap[index]
                    heap[index] = heap[index*2+1]
                    heap[index*2+1] = temp
                    index = index*2 + 1
        heap.insert(0,out)
        return heap

    def heapEnque(self, heap, item):
        heap.append(0)
        heap[-1] = item
        if(len(heap)==1):
            return heap
        index = len(heap) - 1
        while(index>0 and (index-1)/2>=0 and 
                heap[(index-1)/2][1]>heap[index][1]):
            temp = heap[index]
            heap[index] = heap[(index-1)/2]
            heap[(index-1)/2] = temp
        return heap
    
    def sparseExtOther(self,number,digit):
        """Takes a number representation as a list and a single
           sign-index pair for a single bit and adds them up.
           SHOULD have index of digit greater than any index in number."""
        if(len(number) == 0):
            number.insert(0,0)
            number[0]=digit
            self.digits = number
            return self
        if(len(digit)==0):
            self.digits = number
            return self
        if(number[-1][1]==digit[1]):
            if(number[-1][0]!=digit[0]):
                number.pop(len(number)-1)
            else:
                number[-1][1] += 1
            self.digits = number
            return self
        if(number[-1][1]+1==digit[1]):
            if(number[-1][0]!=digit[0]):
                number[-1][0] *= -1
            else:
                number[-1][0] *= -1
                digit[1] += 1
                number.append(0)
                number[-1] = digit
            self.digits = number
            return self
        if(number[-1][1]<digit[1]):
            number.append(0)
            number[-1] = digit
            self.digits = number
            return self 
        if(number[-1][1]==digit[1]+1):
            if(number[-1][0]==digit[0]):
                number.insert(len(number)-1,0)
                number[len(number)-2] = digit
                number[len(number)-2][0] *= -1
                number[-1][1] += 1
            else:
                number[-1][1] -= 1
                temp = number.pop(len(number)-1)
                number = self.sparseExt(number,temp).digits
            self.digits = number
            return self
            
    def sparseExt(self,number,digit):
        """Takes a number representation as a list and a single
           sign-index pair for a single bit and adds them up.
           SHOULD have index of digit greater than any index in number."""
        if(len(number) == 0):
            number.insert(0,0)
            number[0]=digit
            return number
        if(len(digit)==0):
            return number
        if(number[-1][1]==digit[1]):
            if(number[-1][0]!=digit[0]):
                number.pop(len(number)-1)
            else:
                number[-1][1] += 1
            return number
        if(number[-1][1]+1==digit[1]):
            if(number[-1][0]!=digit[0]):
                number[-1][0] *= -1
            else:
                number[-1][0] *= -1
                digit[1] += 1
                number.append(0)
                number[-1] = digit
            return number
        if(number[-1][1]<digit[1]):
            number.append(0)
            number[-1] = digit
            return number
        if(number[-1][1]==digit[1]+1):
            if(number[-1][0]==digit[0]):
                number.insert(len(number)-1,0)
                number[len(number)-2] = digit
                number[len(number)-2][0] *= -1
                number[-1][1] += 1
            else:
                number[-1][1] -= 1
                temp = number.pop(len(number)-1)
                number = self.sparseExt(number,temp)
            return number
        if(number[-1][1]>digit[1]):
            temp = list(number.pop(len(number)-1))
            number = self.sparseExt(number,digit)
            number = self.sparseExt(number,temp)
            return number
        # something has gone wrong if you are still in the 
        # funciton at htis point
        # but lets return anyway and call it a feature
        return number

    def anotherSparseExt(self, newdigit):
        """Extends digits with the new sign-index pair"""
        if len(self.digits) == 0:
            self.digits[:] = [newdigit]
            return
        leading = self.digits[-1]
        if newdigit[1] < leading[1]:
            raise Exception("Oh jeez");
        elif newdigit[1] > leading[1] + 1:
            self.digits.append(newdigit)
        elif newdigit[1] == leading[1] + 1:
            leading[0] *= -1
            if newdigit[0] == leading[0]:
                self.digits.append([newdigit[0],newdigit[1]+1])
        else:
            if newdigit[0] == leading[0]:
                leading[1] += 1
            else:
                self.digits.pop()

    def anotherSub(self,n1,n2):
        i = 0
        j = 0
        while(i<len(n1.digits) and j<len(n2.digits)):
            if(n1.digits[i][1]==n2.digits[j][1]):
                if(n1.digits[i][0]==n2.digits[j][0]*-1):
                    self.anotherSparseExt([n1.digits[i][0],n1.digits[i][1]+1])
                i += 1
                j += 1
            elif(n1.digits[i][1]>n2.digits[j][1]):
                self.anotherSparseExt([n2.digits[j][0]*-1,n2.digits[j][1]])
                j += 1
            else:
                self.anotherSparseExt([n1.digits[i][0],n1.digits[i][1]])
                i += 1
        while(i<len(n1.digits)):
            self.anotherSparseExt([n1.digits[i][0],n1.digits[i][1]])
            i += 1
        while(j<len(n2.digits)):
            self.anotherSparseExt([n2.digits[j][0]*-1,n2.digits[j][1]])
            j += 1

    def anotherAdd(self,n1,n2):
        i = 0
        j = 0
        while(i<len(n1.digits) and j<len(n2.digits)):
            if(n1.digits[i][1]==n2.digits[j][1]):
                if(n1.digits[i][0]==n2.digits[j][0]):
                    self.anotherSparseExt([n1.digits[i][0],n1.digits[i][1]+1])
                i += 1
                j += 1
            elif(n1.digits[i][1]>n2.digits[j][1]):
                self.anotherSparseExt([n2.digits[j][0],n2.digits[j][1]])
                j += 1
            else:
                self.anotherSparseExt([n1.digits[i][0],n1.digits[i][1]])
                i += 1
        while(i<len(n1.digits)):
            self.anotherSparseExt([n1.digits[i][0],n1.digits[i][1]])
            i += 1
        while(j<len(n2.digits)):
            self.anotherSparseExt([n2.digits[j][0],n2.digits[j][1]])
            j += 1
    
    def increment(self,n1):
        n2 = self.deepcopy()
        self.digits = []
        i = 0
        j = 0
        while(i<len(n1.digits) and j<len(n2.digits)):
            if(n1.digits[i][1]==n2.digits[j][1]):
                if(n1.digits[i][0]==n2.digits[j][0]):
                    self.anotherSparseExt([n1.digits[i][0],n1.digits[i][1]+1])
                i += 1
                j += 1
            elif(n1.digits[i][1]>n2.digits[j][1]):
                self.anotherSparseExt([n2.digits[j][0],n2.digits[j][1]])
                j += 1
            else:
                self.anotherSparseExt([n1.digits[i][0],n1.digits[i][1]])
                i += 1
        while(i<len(n1.digits)):
            self.anotherSparseExt([n1.digits[i][0],n1.digits[i][1]])
            i += 1
        while(j<len(n2.digits)):
            self.anotherSparseExt([n2.digits[j][0],n2.digits[j][1]])
            j += 1


    def smartAdd(self,n1real,n2real):
        x = 0
        y = 0
        n1=copy.copy(n1real)
        n2=copy.copy(n2real)
        out = []
        if(len(n1)==0):
            return n2
        if(len(n2)==0):
            return n1
        while(x<len(n1) or y<len(n2)):
            if(x>=len(n1)):
                while(y<len(n2)):
                    out = self.sparseExt(out,n2[y])
                    y += 1
            elif(y>=len(n2)):
                while(x<len(n1)):
                    out = self.sparseExt(out,n1[x])
                    x += 1
            elif(n1[x][1]==n2[y][1]):
                if(n1[x][0]==n2[y][0]):
                    out = self.sparseExt(out,[n1[x][0],n1[x][1]+1])
                x += 1
                y += 1
            elif(n1[x][1]<n2[y][1]):
                out = self.sparseExt(out,n1[x])
                x += 1
            elif(n1[x][1]>n2[y][1]):
                out = self.sparseExt(out,n2[y])
                y += 1
        return out


    def sparsesub(self,n1,n2):
        out =[]
        temp = self.godDamnPythonWithYourLists(n2)
        temp1 = n1
        for bit in temp:
            bit[0] *= -1
            out.append(0)
            out[-1] = bit
        return self.smartAdd(temp1,out)


    def stupidAdd(self,digits1, digits2):
        out = []
        for d in digits1:
            out.append(d)
        for d in digits2:
            out.append(d)
        return out

    def stupidMult(self,digits1, digits2):
        if(len(digits1)==0 or len(digits2)==0):
            return []
        out = []
        for ii in xrange(len(digits1)):
            for jj in xrange(len(digits2)):
                out = self.sparseExt(out, [digits1[ii][0]*digits2[jj][0],digits1[ii][1] + digits2[jj][1]])
        return out

    def smartMult(self,digits1, digits2):
        if(len(digits1)==0 or len(digits2)==0):
            return []
        out = []
        pos1=[]
        neg1=[]
        pos2=[]
        neg2=[]
        for ii in xrange(len(digits1)):
            if(digits1[ii][0]>0):
                pos1.append(digits1[ii][1])
            else:
                neg1.append(digits1[ii][1])
        for ii in xrange(len(digits2)):
            if(digits2[ii][0]>0):
                pos2.append(digits2[ii][1])
            else:
                neg2.append(digits2[ii][1])
    
        a = heapMult.HeapMult.sparseHeapMult(pos1,pos2)
        b = heapMult.HeapMult.sparseHeapMult(pos1,neg2)
        c = heapMult.HeapMult.sparseHeapMult(neg1,pos2)
        d = heapMult.HeapMult.sparseHeapMult(neg1,neg2)
        for ii in xrange(len(a)):
            a[ii] = [1,a[ii]]
        a= self.bitFix(a)
        for ii in xrange(len(b)):
            b[ii] = [1,b[ii]]
        b = self.bitFix(b)
        for ii in xrange(len(c)):
            c[ii] = [1,c[ii]]
        c= self.bitFix(c)
        for ii in xrange(len(d)):
            d[ii] = [1,d[ii]]
        d = self.bitFix(d)
        out = self.smartAdd(a,d)
        out = self.sparsesub(out,b)
        out = self.sparsesub(out,c)
        return out
    
    def stupidDiv(self,digits1, digits2):
        if(len(digits1)==0 or len(digits2)==0):
            return []
        out = []
        for ii in xrange(len(digits1)):
            for jj in xrange(len(digits2)):
                out = self.sparseExt(out, [digits1[ii][0]*digits2[jj][0],digits1[ii][1] - digits2[jj][1]])
        return out

    def absBit(self, bits):
        if len(bits) == 0 or bits[-1][0] > 0: 
            return bits
        else:
            for b in bits:
                b[0] *= -1
            return bits



    def normalize(self):
        """Makes all digits the same sign"""

        if len(self.digits) == 0: return
        sign = self.digits[-1]
        
        def norm(L):
            i = 0
            while True:
                #FIXME index out of bounds here?
                while L[i] != -sign:
                    i += 1
                    if i == len(L): return
                L[i] = sign
                i += 1
                start = i
                while L[i] != sign: i += 1
                L[start:i] = [d + sign for d in L[start:i]]
                L[i] -= sign
                i += 1

        norm(self.digits)
        self.clearleading(self.digits)

    def __nonzero__(self):
        return len(self.digits) > 0

    def __eq__(self, other):
        o = other if isinstance(other, RRRSparse) else RRRSparse(other)
        return self.eq(o)

    def __ne__(self, other):
        o = other if isinstance(other, RRRSparse) else RRRSparse(other)
        return self.ne(o)

    def __lt__(self, other):
        o = other if isinstance(other, RRRSparse) else RRRSparse(other)
        return self.lt(o)

    def __gt__(self, other):
        o = other if isinstance(other, RRRSparse) else RRRSparse(other)
        return self.gt(o)
    
    def __ge__(self, other):
        o = other if isinstance(other, RRRSparse) else RRRSparse(other)
        return self.gte(o)
    
    def __le__(self,other):
        o = other if isinstance(other,RRRSparse) else RRRSparse(other)
        return self.lte(o)
    
    def __neg__(self):
        temp = self.digits
        for d in temp:
            d[0] *= -1
        res = RRRSparse()
        res.digits = temp
        return res 
    def __xor__(self, other):
        return 1 
    def __abs__(self):
        if len(self.digits) == 0 or self.digits[-1][0] > 0: 
            return self
        else:
            return -self

    def __add__(self, other):
        o = other if isinstance(other, RRRSparse) else RRRSparse(other)
        res = RRRSparse()
        #res.anotherAdd(self, o)
        res.digits = self.smartAdd(self.deepcopy().digits, o.deepcopy().digits)
        return res

    def __sub__(self, other):
        o = other if isinstance(other, RRRSparse) else RRRSparse(other)
        temp=[]
        index = 0
        res = RRRSparse()
        res.digits = self.sparsesub(self.deepcopy().digits,o.deepcopy().digits)
        return res

    def __mul__(self, other):
        o = other if isinstance(other, RRRSparse) else RRRSparse(other)
        res = RRRSparse()
        return res.simpleMult(self, o)
    
    def __mod__(self, other):
        o = other if isinstance(other, RRRSparse) else RRRSparse(other)
        res = RRRSparse()
        #res.digits = self.sparseMod(self.digits, o.digits)
        res.digits = self.quoremwrapper(self.deepcopy(), o.deepcopy())[1]
        return res
   
    def __div__(self, other):
        o = other if isinstance(other, RRRSparse) else RRRSparse(other)
        res = RRRSparse()
        res.digits = self.quorem(self.deepcopy(), o.deepcopy())[0]
        return res

    def __long__(self):
        res = 0
        for digit in self.digits:
            res += (2**digit[1])* digit[0]
        return res

    def __int__(self):
        return int(long(self))

    def __str__(self):
        """Returns a string representation of this integer"""
        if len(self.digits) == 0:
            return '[]'
        out = "["
        for d in self.digits:
            out += str(d[0]*d[1])+","
        out = out[:-1]
        out += "]"
        return out

    def __repr__(self):
        """Returns a string that will evaluate to this object"""
        theint = str(int(self))
        return __name__ + '.' + type(self).__name__ + '(' + theint + ')'

    def __hash__(self):
        return int(self)
