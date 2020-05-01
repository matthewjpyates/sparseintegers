#!/usr/bin/python
import sys
import generateSparseInts
import rrrsparse
import datetime
import timing
def getTimes(sampleNum,a,b):
    test = []
    for ii in xrange(max(sampleNum,1)):
        out =[]
        t1 = datetime.datetime.now()
        z = a+b
        t2 = datetime.datetime.now()
        c = t1 - t2
        out.append( c.seconds + c.microseconds/1000000.0)

        t1 = datetime.datetime.now()
        z = a-b
        t2 = datetime.datetime.now()
        c = t1 - t2
        out.append( c.seconds + c.microseconds/1000000.0)

        t1 = datetime.datetime.now()
        z = a*b
        t2 = datetime.datetime.now()
        c = t1 - t2
        out.append( c.seconds + c.microseconds/1000000.0)

        if(b!= 0):
            t1 = datetime.datetime.now()
            z = a/b
            t2 = datetime.datetime.now()
            c = t1 - t2
            out.append( c.seconds + c.microseconds/1000000.0)
        else:
            out.append(0)

        if(b!= 0):
            t1 = datetime.datetime.now()
            z = a%b
            t2 = datetime.datetime.now()
            c = t1 - t2
            out.append( c.seconds + c.microseconds/1000000.0)
        else:
            out.append(0)

        t1 = datetime.datetime.now()
        z = a==b
        t2 = datetime.datetime.now()
        c = t1 - t2
        out.append( c.seconds + c.microseconds/1000000.0)

        t1 = datetime.datetime.now()
        z = a<b
        t2 = datetime.datetime.now()
        c = t1 - t2
        out.append( c.seconds + c.microseconds/1000000.0)

        t1 = datetime.datetime.now()
        z = a<=b
        t2 = datetime.datetime.now()
        c = t1 - t2
        out.append( c.seconds + c.microseconds/1000000.0)

        t1 = datetime.datetime.now()
        z = a!=b
        t2 = datetime.datetime.now()
        c = t1 - t2
        out.append( c.seconds + c.microseconds/1000000.0)

        t1 = datetime.datetime.now()
        z = a>b
        t2 = datetime.datetime.now()
        c = t1 - t2
        out.append( c.seconds + c.microseconds/1000000.0)

        t1 = datetime.datetime.now()
        z = a>=b
        t2 = datetime.datetime.now()
        c = t1 - t2
        out.append( c.seconds + c.microseconds/1000000.0)

        t1 = datetime.datetime.now()
        z = -a
        t2 = datetime.datetime.now()
        c = t1 - t2
        out.append( c.seconds + c.microseconds/1000000.0)

        ra = rrrsparse.RRRSparse(a)
        rb = rrrsparse.RRRSparse(b)
        t1 = datetime.datetime.now() 
        z = ra + rb 
        t2 = datetime.datetime.now()
        c = t1 - t2
        out.append( c.seconds + c.microseconds/1000000.0)

        ra = rrrsparse.RRRSparse(a)
        rb = rrrsparse.RRRSparse(b)
        t1 = datetime.datetime.now() 
        z = ra - rb 
        t2 = datetime.datetime.now()
        c = t1 - t2
        out.append( c.seconds + c.microseconds/1000000.0)

        ra = rrrsparse.RRRSparse(a)
        rb = rrrsparse.RRRSparse(b)
        t1 = datetime.datetime.now() 
        z = ra * rb 
        t2 = datetime.datetime.now()
        c = t1 - t2
        out.append( c.seconds + c.microseconds/1000000.0)

        if b!=0:
            ra = rrrsparse.RRRSparse(a)
            rb = rrrsparse.RRRSparse(b)
            t1 = datetime.datetime.now() 
            z = ra / rb 
            t2 = datetime.datetime.now()
            c = t1 - t2
            out.append( c.seconds + c.microseconds/1000000.0)
        else:
            out.append(0)
        
        if b!=0:
            ra = rrrsparse.RRRSparse(a)
            rb = rrrsparse.RRRSparse(b)
            t1 = datetime.datetime.now() 
            z = ra % rb 
            t2 = datetime.datetime.now()
            c = t1 - t2
            out.append( c.seconds + c.microseconds/1000000.0)
        else:
            out.append(0)


        ra = rrrsparse.RRRSparse(a)
        rb = rrrsparse.RRRSparse(b)
        t1 = datetime.datetime.now() 
        z = ra == rb 
        t2 = datetime.datetime.now()
        c = t1 - t2
        out.append( c.seconds + c.microseconds/1000000.0)

        ra = rrrsparse.RRRSparse(a)
        rb = rrrsparse.RRRSparse(b)
        t1 = datetime.datetime.now() 
        z = ra < rb 
        t2 = datetime.datetime.now()
        c = t1 - t2
        out.append( c.seconds + c.microseconds/1000000.0)
        
        ra = rrrsparse.RRRSparse(a)
        rb = rrrsparse.RRRSparse(b)
        t1 = datetime.datetime.now() 
        z = ra <= rb 
        t2 = datetime.datetime.now()
        c = t1 - t2
        out.append( c.seconds + c.microseconds/1000000.0)
        
        ra = rrrsparse.RRRSparse(a)
        rb = rrrsparse.RRRSparse(b)
        t1 = datetime.datetime.now() 
        z = ra != rb 
        t2 = datetime.datetime.now()
        c = t1 - t2
        out.append( c.seconds + c.microseconds/1000000.0)
        
        ra = rrrsparse.RRRSparse(a)
        rb = rrrsparse.RRRSparse(b)
        t1 = datetime.datetime.now() 
        z = ra > rb 
        t2 = datetime.datetime.now()
        c = t1 - t2
        out.append( c.seconds + c.microseconds/1000000.0)
        
        ra = rrrsparse.RRRSparse(a)
        rb = rrrsparse.RRRSparse(b)
        t1 = datetime.datetime.now() 
        z = ra >= rb 
        t2 = datetime.datetime.now()
        c = t1 - t2
        out.append( c.seconds + c.microseconds/1000000.0)
        
        ra = rrrsparse.RRRSparse(a)
        rb = rrrsparse.RRRSparse(b)
        t1 = datetime.datetime.now() 
        z = -ra 
        t2 = datetime.datetime.now()
        c = t1 - t2
        out.append( c.seconds + c.microseconds/1000000.0)
        test.append(out)
    result = []    
    for ii in xrange(len(test[-1])):
        result.append(0)
        for jj in xrange(len(test)):
            result[-1]+= test[jj][ii]
        result[-1] /= (len(test)*1.0)
    return result
def runTests(sampleNum,a,b):
    out = []
    ra = rrrsparse.RRRSparse(a)
    rb = rrrsparse.RRRSparse(b)
    out.append(timing.dotest(lambda : a+b))
    out.append(timing.dotest(lambda : ra+rb))
    out.append(timing.dotest(lambda : a-b))
    out.append(timing.dotest(lambda : ra-rb))
    out.append(timing.dotest(lambda : a*b))
    out.append(timing.dotest(lambda : ra*rb))
    if(b!=0):
        out.append(timing.dotest(lambda : a/b))
        out.append(timing.dotest(lambda : ra/rb))
        out.append(timing.dotest(lambda : a%b))
        out.append(timing.dotest(lambda : ra%rb))
    else:
        out.extend([0,0,0,0])
    return out




if not(len(sys.argv)==4 or len(sys.argv)== 6):
    print "./speedTest.py sampleNumber fileName|(gen numBits MaxBit numberToTest)"
    sys.exit()
bitsWithNumbers = []

if sys.argv[2] != "gen":
    infile = open(sys.argv[2],"r")
    dataLines = infile.readlines()
    for dataLine in dataLines:
        bitsWithNumbers.append([int(dataLine.split(",")[0]),int(dataLine.split(",")[1])])
    infile.close()
else:
    bitsWithNumbers = generateSparseInts.smartRandom(int(sys.argv[3]),int(sys.argv[4]),int(sys.argv[5]))

for bitnum1 in bitsWithNumbers:
    for bitnum2 in bitsWithNumbers:
        #times =  getTimes(int(sys.argv[1]) ,bitnum1[1],bitnum2[1])
        times =  runTests(50,bitnum1[1],bitnum2[1])
        outString = str(bitnum1[0])+","+str(bitnum1[1])+","+str(bitnum2[0])+","+str(bitnum2[1])+","+sys.argv[1]
        for t in times:
            outString += ","+str(t)
        print outString
    

