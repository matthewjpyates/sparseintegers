"""Module for Sparse Integer modulus."""

import copy
import functools


class SparseMod(object):

    @staticmethod
    def carry(a, newE):
        if(len(a)>0 and newE == a[len(a)-1]):
            a[len(a)-1] = a[len(a)-1] + 1
        else:
            a.append(newE)
        return a
    @staticmethod 
    def addSparse(a,b):
        ai = 0
        bi = 0
        out = []
        while(len(a)>ai or len(b)>bi):
            if(len(a)>ai and not(len(b)>bi)):
                for ii in range(ai,len(a)):
                    out = SparseInt.carry(out, a[ii])
                ai=len(a)
            elif(len(b)>bi and not(len(a)>ai)):
                for ii in range(bi,len(b)):
                    out = SparseInt.carry(out, b[ii])
                bi=len(b)
            elif(a[ai]==b[bi]):
                out = SparseInt.carry(out, a[ai]+1)
                ai += 1
                bi += 1
            elif(a[ai]<b[bi]):
                out = SparseInt.carry(out, a[ai])
                ai += 1
            elif(a[ai]>b[bi]):
                out = SparseInt.carry(out, b[bi])
                bi += 1    
        return out


    @staticmethod
    def sparseMult(a,b):
        result = []
        if(len(a)==0 or len(b)==0):
            return []
        for eb in b:
            result.append(eb+a[0])
        aNum = range(1,len(a))
        for ea in aNum:
            temp = []
            for eb in b:
                temp.append(a[ea]+eb)
            result = SparseInt.addSparse(result,temp)
        return result

    @staticmethod 
    def equal(a,b):
        if(len(a)!=len(b)):
            return False
        for ii in range(0,len(a)):
            if(a[ii]!=b[ii]):
                return False
        return True

    @staticmethod 
    def convertInt(inSparse):
        out =0
        for index in inSparse:
            out += 2**index
        return out

    @staticmethod 
    def greaterThanOrEqualTo(a,b):
        if(len(b)==0):
            return True
        if(len(a)==0):
            return False
        if(a[len(a)-1]>b[len(b)-1]):
            return True
        if(a[len(a)-1]<b[len(b)-1]):
                    return False
        if(len(b)>len(a)):
            shortLen = len(a)
        else:
            shortLen = len(b)
        for ii in range(1,shortLen+1):
            if(a[len(a)-ii]!=b[len(b)- ii]):
                return a[len(a)-ii]>=b[len(b)-ii]
        return len(a)>=len(b)

    @staticmethod
    def sparseMod(n,m):
        if(len(m)==0):
            return n
        if(len(n)==0):
            return 0
        while(SparseMod.greaterThan(list(n),list(m))):
            if(len(m)==0):
                return n
            if(len(n)==0):
                return []
            if(n[-1] - m[-1]>1):
                 n = SparseInt.sparseSub(list(n),
                 map(lambda x:(n[-1] - m[-1] -1)+ x,m))
            else:
                n = SparseInt.sparseSub(list(n),
                list(m))
        if(SparseInt.equal(list(n),list(m))):
            return []
        return n


    @staticmethod
    def decMod(n,m):
        if(len(m)==1 and m[len(m)-1]==0):
            return []
        if(len(n)<1):
            return []
        if(len(m)<1):
            return n
        if(SparseInt.equal(n,m)):
            return []
        if(SparseInt.greaterThanOrEqualTo(m,n)):
            return n
        else:
            if(len(m)==1):
                return SparseInt.sparseMod(n,m)
            bits = m[len(m)-1]-m[len(m)-2]
            factor = filter(lambda x: x+bits > n[len(n)-1], n)
            factor = SparseInt.sparseSub(factor,[0])
            delta = 0
            if(not(len(n)>=1) and not(len(factor)>=1)):
                delta = n[len(n)-1] - factor[len(factor)-1]
            else:
                return SparseInt.sparseMod(n,m)
            if(delta<0):
                return SpraseInt.sparseMod(n,m)
        factor = map(lambda x: x + delta, factor)
        if(gte(factor,n)):
            return SparseInt.sparseMod(n,m)
        return SparseInt.decMod(SparseInt.sparseSub(n,factor),m)

    
    def convertSparse(inNum):
        place=0
        out =[]
        inNum = int(inNum)
        while(2**place<=inNum):
            if((1<<place)&(inNum)):
                out.append(place)
            place += 1    
        return out

    @staticmethod
    def sparseMult(a,b):
        result = []
        if(len(a)==0 or len(b)==0):
            return []
        for eb in b:
            result.append(eb+a[0])
        aNum = range(1,len(a))
        for ea in aNum:
            temp = []
            for eb in b:
                temp.append(a[ea]+eb)
            result = SparseInt.addSparse(result,temp)
        return result


    @staticmethod
    def greaterThan(a,b):
        if(len(a)==0):
            return False
        if(len(b)==0):
            return True
        if(a[len(a)-1]>b[len(b)-1]):
            return True
        if(a[len(a)-1]<b[len(b)-1]):
                    return False
        if(len(b)>len(a)):
            shortLen = len(a)
        else:
            shortLen = len(b)
        for ii in range(1,shortLen+1):
            if(a[len(a)-ii]!=b[len(b)- ii]):
                return a[len(a)-ii]>b[len(b)-ii]
        return len(a)>len(b)

    @staticmethod
    def isInt(a):
        return isinstance( a, ( int, long ) )
    
    @staticmethod
    def sparseSub(a,b):
        if(SparseInt.isInt(a)):
            a = [a]
        if(SparseInt.isInt(b)):
            b = [b]
        if(len(b)==0):
            return a
        if(len(a)==0):
            return []
        if(a[0]==b[0]):
            a.pop(0)
            b.pop(0)
            return SparseInt.sparseSub(a,b)
        if(a[0]<b[0]):
            temp = []
            temp.append(a.pop(0))
            temp.extend(SparseInt.sparseSub(a,b))
            return temp
        temp = []
        if(a[0]>b[0]):
            place = 0
            for i in range(b[0],a[0]):
                a.insert(place,i)
                place += 1
            a.pop(place)
            b.pop(0)
            return SparseInt.sparseSub(a,b)
        return a


    def __nonzero__(self):
        return len(self.digits) > 0


    def __eq__(self, other):
        o = other if isinstance(other, SparseInt) else SparseInt(other)
        return SparseInt.equal(self.digits,o.digits)

    def __lt__(self, other):
        o = other if isinstance(other, SparseInt) else SparseInt(other)
        return SparseInt.greaterThanOrEqualTo(o.digits,self.digits)

    def __gt__(self,other):
        o = other if isinstance(other, SparseInt) else SparseInt(other)
        return SparseInt.greaterThan(o.digits,self.digits)

    def __neg__(self):
        return []
    
    def __add__(self, other):
        o = other if isinstance(other, SparseInt) else SparseInt(other)
        res = SparseInt()
        res.digits = SparseInt.addSparse(self.digits, o.digits)
        return res

    def __sub__(self, other):
        o = other if isinstance(other, SparseInt) else SparseInt(other)
        res.digits = SparseInt.sparseSub(self.digits, oneg)
        return res


    def __abs__(self):
        return self

    def __mod__(self, other):
        o = other if isinstance(other, SparseInt) else SparseInt(other)
        res = SparseInt(SparseInt.decMod(self.digits,
            o.digits))
        return res


    def __mul__(self, other):
        o = other if isinstance(other, RRRDense) else SparseInt(other)
        res = SparseInt()
        res.digits = SparseInt.sparseMult(self.digits, o.digits)
        return res

    def __long__(self):
        return SparseInt.convertInt(self.digits)

    def __int__(self):
        return int(long(self))

    def __str__(self):
        """Returns a string representation of this integer"""
        return str(self.digits)

    def __repr__(self):
        """Returns a string that will evaluate to this object"""
        theint = str(int(self))
        return __name__ + '.' + type(self).__name__ + '(' + theint + ')'

    def __hash__(self):
        return int(self)

