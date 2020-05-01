#!/usr/bin/python
import rrrsparse
def pretendBinary(num):
    if(len(num.digits)==0):
        return "0"
    fb = False
    demoteNext = False
    skips =0
    place =0
    outStr = ""
    for ii in xrange(num.digits[-1][1]):
        if(num.digits[place][1]==ii):
            if(num.digits[place][0]<0):
                if(fb):
                    if(num.digits[place +1][1]>ii+2):
                        demoteNext = True
                        #skips +=1
                        outStr += "0"
                    elif(num.digits[place +1][0]<0):
                        demoteNext = True
                        outStr += "0"
                        fb= True
                    else:
                        if(demoteNext):
                            outStr += "1"
                            demoteNext = False
                        fb= False
                else:
                    fb = True
                    if(demoteNext):
                        pass#outStr += "1"
                    else:
                        outStr += "1"
            else:
                if(fb):
                    outStr += "0"
                    fb= False
                else:
                    outStr += "1"
            place += 1
        else:
            if (skips>0):
                skips -= 1
                outStr += "1"
                fb =True
            elif(fb):
                outStr += "1"
            else:
                outStr += "0"
    if(not(fb)):
        outStr+="1"
    return outStr

def simple(num):
    d = num.digits
    if(len(d)==0):
        return "0"
    sn = False
    p = 0
    outStr = ""
    for ii in xrange(d[-1][1]+1):
        if d[p][1] == ii:
            if sn:
                outStr += "0"
            else:
                outStr += "1"
            sn = d[p][0]<1
            p += 1
        else:
            if sn:
                outStr += "1"
            else:
                outStr += "0"
    if(outStr[-1]=="0"):
        return outStr[:len(outStr)-1]
    return outStr

#print "decimal\tsparse\nbinary reversed"
num = 0
while(True):
    spnum = rrrsparse.RRRSparse(num)
    if(bin(num).split('b')[1][::-1] != simple(spnum)):
        outStr = str(num)+"\t"
        spnum = rrrsparse.RRRSparse(num)
        outStr += spnum.oldStr()+ "\t"
        outStr += bin(num).split('b')[1][::-1]
        print outStr+"\tfliped binary"
        outStr = str(num)+"\t"
        spnum = rrrsparse.RRRSparse(num)
        outStr += spnum.oldStr()+ "\t"
        outStr += simple(spnum)
        print outStr+ "\tcalculated"
        break
    num += 1
