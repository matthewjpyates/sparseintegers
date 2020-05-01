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
    runs = []
    for ii in xrange(sampleNum):
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
        runs.append(out)
    base = runs.pop(0)
    for run in runs:
        for ii  in xrange(len(base)):
            base[ii] += run[ii]
    
    for ii in  xrange(len(base)):
        base[ii] /= (1.0*sampleNum)    
    return base




if not(len(sys.argv)==3 or len(sys.argv)== 6):
    print "./timeTest.py (walk |fileName|(gen numBits MaxBit numberToTest)) numOfTrials"
    sys.exit()
bitsWithNumbers = []

filename = sys.argv[1]

if filename != "gen" and filename!="walk":
    infile = open(filename,"r")
    dataLines = infile.readlines()
    for dataLine in dataLines:
        bitsWithNumbers.append([int(dataLine.split(",")[0]),int(dataLine.split(",")[1])])
    infile.close()
elif filename == "walk":
    base = 100
    while True:
        for ii in xrange(1,base,base//4):
            bitsWithNumbers = generateSparseInts.smartRandomHighestBit(base//ii,base,2)
            for bitnum1 in bitsWithNumbers:
                for bitnum2 in bitsWithNumbers:
                    #times =  getTimes(int(sys.argv[1]) ,bitnum1[1],bitnum2[1])
                    times =  runTests(int(sys.argv[2]),bitnum1[2],bitnum2[2])
                    outString = str(bitnum1[0])+","+str(bitnum1[1])+","+str(bitnum2[0])+","+str(bitnum2[1])
                    for t in times:
                        outString += ","+str(t)
                    print outString
        base *=2
        print >> sys.stderr, base-2
    sys.exit()

else:
    numBits = int(sys.argv[2])
    maxBit = int(sys.argv[3])
    numToTest = int(sys.argv[4])
    numTrials = int(sys.argv[5])
    bitsWithNumbers = generateSparseInts.smartRandomHighestBit(numBits,
    maxBit,numToTest)

for bitnum1 in bitsWithNumbers:
    for bitnum2 in bitsWithNumbers:
        #times =  getTimes(int(sys.argv[1]) ,bitnum1[1],bitnum2[1])
        times =  runTests(numTrials,bitnum1[2],bitnum2[2])
        outString = str(bitnum1[0])+","+str(bitnum1[1])+","+str(bitnum2[0])+","+str(bitnum2[1])
        for t in times:
            outString += ","+str(t)
        print outString
    #print bitnum1
    #print bitnum2
    

