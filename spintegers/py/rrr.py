"""Module for Redundant Radix Representation (signed-digit) integers."""

import copy
import functools

@functools.total_ordering
class RRRDense(object):
    
    """A DENSE integer with -1/0/+1 digits"""

    def __init__(self, value=0):
        """Creates a new RRRDense with the given value.
        
        The value can be an integer, an array, or another RRRDense."""

        if isinstance(value, RRRDense):
            self.digits = copy.copy(value.digits)

        elif isinstance(value, list):
            self.digits = copy.copy(value)
        
        else:
            ival = int(value)
            self.digits = []
            sign = 1 if ival >= 0 else -1
            while(ival != 0):
                if ival & 1:  # if odd
                    self.digits.append(sign)
                    ival -= sign
                else:
                    self.digits.append(0)
                ival //= 2

    @staticmethod
    def clearleading(A):
        """Clears the leading zero's from the list of digits A"""
        i = len(A) - 1
        while i >= 0 and A[i] == 0: 
            i -= 1
        del A[i+1:]

    @classmethod
    def digit_sum(cls, A1, A2, clear=True):
        """Returns an array representing the sum of the digits in these two."""
        
        # First get the position sums
        overlap = min(len(A1), len(A2))
        p = [A1[i] + A2[i] for i in xrange(overlap)]
        for i in xrange(overlap, len(A1)):
            p.append(A1[i])
        for i in xrange(overlap, len(A2)):
            p.append(A2[i])

        # Now compute the carry digits
        # There are some "magic formulas" here that I came up with.
        c = [(p[0] + 1) // 3]
        c.extend([(3 * (p[i] + 1) + p[i-1]) // 7 for i in xrange(1, len(p))])

        # Now it's time for the final results.
        res = [p[0] - 2*c[0]]
        res.extend([p[i] + c[i-1] - 2*c[i] for i in xrange(1, len(p))])
        if c[-1] != 0:
            res.append(c[-1])

        if clear: cls.clearleading(res)
        return res

    @classmethod
    def digit_mul(cls, A1, A2):
        """Returns an array representing the product of the digits."""

        # Space to store the result
        res = [0] * (len(A1) + len(A2))

        negA2 = [-d for d in A2]
        a = 0
        b = len(A2) + 1
        while a < len(A1):
            if A1[a] == 1:
                res[a:b] = cls.digit_sum(res[a:b], A2, False)
            elif A1[a] == -1:
                res[a:b] = cls.digit_sum(res[a:b], negA2, False)
            a += 1
            b += 1
        
        cls.clearleading(res)
        return res

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
        o = other if isinstance(other, RRRDense) else RRRDense(other)
        d = self - o
        return len(d.digits) == 0

    def __lt__(self, other):
        o = other if isinstance(other, RRRDense) else RRRDense(other)
        d = self - o
        return len(d.digits) > 0 and d.digits[-1] < 0

    def __neg__(self):
        return RRRDense([-d for d in self.digits])

    def __abs__(self):
        if len(self.digits) == 0 or self.digits[-1] >= 0: 
            return self
        else:
            return -self

    def __add__(self, other):
        o = other if isinstance(other, RRRDense) else RRRDense(other)
        res = RRRDense()
        res.digits = self.digit_sum(self.digits, o.digits)
        return res

    def __sub__(self, other):
        o = other if isinstance(other, RRRDense) else RRRDense(other)
        res = RRRDense()
        oneg = [-a for a in o.digits]
        res.digits = self.digit_sum(self.digits, oneg)
        return res

    def __mul__(self, other):
        o = other if isinstance(other, RRRDense) else RRRDense(other)
        res = RRRDense()
        res.digits = self.digit_mul(self.digits, o.digits)
        return res

    def __long__(self):
        pow2 = 1
        res = 0
        for digit in self.digits:
            res += pow2 * digit
            pow2 *= 2
        return res

    def __int__(self):
        return int(long(self))

    def __str__(self):
        """Returns a string representation of this integer"""
        if len(self.digits) == 0:
          return '0'
        else:
          signdigits = [str(a)[0] if a<=0 else '+' for a in self.digits]
          signdigits.reverse()
          return ''.join(signdigits)

    def __repr__(self):
        """Returns a string that will evaluate to this object"""
        theint = str(int(self))
        return __name__ + '.' + type(self).__name__ + '(' + theint + ')'

    def __hash__(self):
        return int(self)
