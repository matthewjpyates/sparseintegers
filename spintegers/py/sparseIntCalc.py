#!/usr/bin/python
import sys
import cProfile
import random

def stressTest():
	"""
	A randomized tesster of operands with numbers
	between 0 and 10000
	"""
	a = random.randint(0,10000)
        b = random.randint(0,10000)
	sparseA = convertSparse(a)
	sparseB = convertSparse(b)
	listOfOps = ["add","mult","mod","sub","eq","gt","gte"]
	op= random.choice(listOfOps)
	if((op=="sub" or op=="mod") and b>a):
		c = a
		a = b
		b = c
		sparseA = convertSparse(a)
        	sparseB = convertSparse(b)
	while(op=="mod" and (b==0 or a==0)):
		a = random.randint(0,10000)
        	b = random.randint(0,10000)
        	sparseA = convertSparse(a)
	        sparseB = convertSparse(b)
		if(b>a):
			c = a
                	a = b
                	b = c
        	        sparseA = convertSparse(a)
	                sparseB = convertSparse(b)

	if(op == "add"):
		if(not(convertInt(sparseAdd(sparseA,sparseB))==(a+b))):
			print "Failed on add with "+ str(a)+ " and "+ str(b) 
                        return False
                else:
                        return True
	elif(op == "mult"):
		if(not(convertInt(sparseMult(sparseA,sparseB))==(a*b))):
                        print "Failed on mult with "+ str(a)+ " and "+ str(b)
                        return False
                else:
                        return True
	elif(op == "mod"):
		if(not(convertInt(decMod(sparseA,sparseB))==(a%b))):
                        print "Failed on mod with "+ str(a)+ " and "+ str(b)
                        return False
                else:
                        return True
	elif(op =="sub"):
		if(not(convertInt(sparseSub(sparseA,sparseB))==(a-b))):
                        print "Failed on sub with "+ str(a)+ " and "+ str(b)
                        return False
                else:
                        return True
	elif(op == "eq"):
		if(not(eq(sparseA,sparseB)==(a==b))):
                        print "Failed on eq with "+ str(a)+ " and "+ str(b)
                        return False
                else:
                        return True
	elif(op == "gt"):
		if(not(gt(list(sparseA),list(sparseB))==(a>b))):
                        print "Failed on gt with "+ str(a)+ " and "+ str(b)
                        return False
                else:
                        return True
	elif(op =="gte"):
		if(not(gte(sparseA,sparseB)==(a>=b))):
                        print "Failed on gte with "+ str(a)+ " and "+ str(b)
			return False
		else:
			return True

def decMod(n,m):
	if(len(m)==1 and m[len(m)-1]==0):
		return []
	if(len(n)<1):
		return []
	if(len(m)<1):
		return n
	if(eq(n,m)):
		return []
  # FIXME must switch methods when n is not a chunk larger than m
	if(gte(m,n)):
		return n
	else:
		if(len(m)==1):
			return sparseMod(n,m)
		bits = m[len(m)-1]-m[len(m)-2]
		factor = filter(lambda x: x+bits > n[len(n)-1], n)
		factor = sparseSub(factor,[0])
		delta = 0
		if(not(len(n)>=1) and not(len(factor)>=1)):
			delta = n[len(n)-1] - factor[len(factor)-1]
		else:
			return sparseMod(n,m) 
		if(delta<0):
			return sparseMod(n,m)
		factor = map(lambda x: x + delta, factor)
		if(gte(factor,n)):
			return sparseMod(n,m)
		decMod(sparseSub(n,factor),m)
	
def sparseMod(n,m):
	if(len(m)==0):
		return n
	if(len(n)==0):
		return 0
	while(gt(list(n),list(m))):
		if(len(m)==0):
			return n
		if(len(n)==0):
			return []
		n = sparseSub(list(n),list(m))
	if(eq(list(n),list(m))):
		return []
	return n

def gt(a,b):
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

def makeBitArray(a):
	out = []
	for ii in range(0,a[len(a)-1]+1):
		if(ii in a):
			out.append(1)
		else:
			out.append(0)
	return out

def grabXBits(a,bits):
	out = []
	i =1
	while(i-1<bits):
		out.insert(0,a[len(a)-i])
		i+=1
	return out

def unbit(a):
	out =0
	for ii in range(0,len(a)):
		out += 2**ii
	return out

def isInt(a):
	return isinstance( a, ( int, long ) )

def sparseSub(a,b):
	if(isInt(a)):
		a = [a]
	if(isInt(b)):
		b = [b]
	if(len(b)==0):
		return a
	if(len(a)==0):
		return []
	if(a[0]==b[0]):
		a.pop(0)
		b.pop(0)
		return sparseSub(a,b)
	if(a[0]<b[0]):
		temp = []
		temp.append(a.pop(0))
		temp.extend(sparseSub(a,b))
		return temp
	temp = []
	if(a[0]>b[0]):
		place = 0
		for i in range(b[0],a[0]):
			a.insert(place,i)
			place += 1
		a.pop(place)
		b.pop(0)
		return sparseSub(a,b)
	return a
						
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
		result = addSparse(result,temp)
	return result
def addLists(a,b):
	lastIndex = 0
	while(b[0]<a[0]):
		a.insert(0,b.pop(0))
	while(len(b)>0 and lastIndex<len(a)):
		if(b[0]>a[lastIndex]):
			if(lastIndex+2>len(a)):
				a.append(b.pop(0))
			elif(b[0]<a[lastIndex+1]):
				a.insert(lastIndex+1,b.pop(0))
			elif(b[0]==a[lastIndex+1]):
				a.pop(lastIndex+1)
				b[0] = b[0] + 1

		elif(b[0]==a[lastIndex]):
			a.pop(lastIndex)
			b[0] = b[0] + 1
		lastIndex += 1
		while(len(b)>0 and len(a)>0 and b[0]<a[0]):
	                a.insert(0,b.pop(0))
	if(len(b)>0):
		i =0
		while(len(b)>0 and i<len(a)):
			if(b[0]<a[i]):
				a.insert(i,b.pop(0))
			i += 1
	for ae in range(0,len(a)):
		if(ae+1<len(a) and a[ae] ==a[ae+1]):
			a[ae] = a.pop(ae) + 1
	return a
def carry(a, newE):
	if(len(a)>0 and newE == a[len(a)-1]):
		a[len(a)-1] = a[len(a)-1] + 1
	else:
		a.append(newE)
	return a
def addSparse(a,b):
	ai = 0
	bi = 0
	out = []
	while(len(a)>ai or len(b)>bi):
		if(len(a)>ai and not(len(b)>bi)):
			for ii in range(ai,len(a)):
				out = carry(out, a[ii])
			ai=len(a)
		elif(len(b)>bi and not(len(a)>ai)):
	        	for ii in range(bi,len(b)):
                        	out = carry(out, b[ii])
			bi=len(b)
		elif(a[ai]==b[bi]):
			out = carry(out, a[ai]+1)
			ai += 1
			bi += 1
		elif(a[ai]<b[bi]):
			out = carry(out, a[ai])
			ai += 1
		elif(a[ai]>b[bi]):
        	        out = carry(out, b[bi])
                	bi += 1	
	return out
def sparseAdd(a,b):
	return addSparse(a,b)
				
def convertInt(inSparse):
	out =0
	for index in inSparse:
		out += 2**index
	return out
def convertSparse(inNum):
	place=0
	out =[]
	inNum = int(inNum)
	while(2**place<=inNum):
		if((1<<place)&(inNum)):
			out.append(place)
		place += 1	
	return out
def eq(a,b):
	if(len(a)!=len(b)):
		return False
	for ii in range(0,len(a)):
		if(a[ii]!=b[ii]):
			return False
	return True
def gte(a,b):
	return gt(a,b) or eq(a,b)
def doMath(a,b,op):
	if(op=="add"):
		return sparseAdd(a,b)
	elif(op=="mult"):
		return sparseMult(a,b)
	elif(op=="mod"):
		return decMod(a,b)
	elif(op=="sub"):
		return sparseSub(a,b)
	elif(op=="eq"):
		return eq(a,b)
	elif(op=="gt"):
		return gt(a,b)
	elif(op=="gte"):
		return gte(a,b)
	return []
def calcFunction(one,two):
  first  = int(one)
  second = int(two)
  op = sys.argv[1]
  num1 = convertSparse(first)
  num2 = convertSparse(second)
  print "Converted numbers"
  print num1
  print num2
  result = doMath(num1,num2,op)
  if(op=="eq" or op=="gt" or op=="gte"):
    print "Result"
    print result
  else:
    print "Set indecies"
    print result
    print "As an integer"
    print convertInt(result)
  print "What old fashion math says"
  if(op=="add"):
    print first+second
  elif(op=="mult"):
    print first*second
  elif(op=="mod"):
    print first%second
  elif(op=="sub"):
    print first - second
  elif(op=="eq"):
    print first == second
  elif(op=="gt"):
    print first>second
  elif(op=="gte"):
    print first>=second

def testFunctionLimit(num):
        count =0
        while(num>count and stressTest()):
                count += 1
        print "worked "+str(count)+" many times"


def testFunction():
	count =0
	while(stressTest()):
                count += 1
        print "worked "+str(count)+" many times"

def main():
  profile=False
  # Use cProfile package to do profiling
  if(len(sys.argv)>1 and sys.argv[len(sys.argv)-1]=="profile"):
	profile = True
	sys.argv.pop()
  if(len(sys.argv)==2 and sys.argv[1]=="test"):
	count = 0
	if(profile):
		cProfile.run('testFunction()')
		sys.exit()
	while(stressTest()):
		count += 1
	print "worked "+str(count)+" many times"
	sys.exit()
  if(len(sys.argv)==3 and sys.argv[1]=="test"):
        if(profile):
                cProfile.run('testFunctionLimit(int('+sys.argv[2]+'))')
                sys.exit()
        else:
		testFunctionLimit(int(sys.argv[2]))
        sys.exit()

  if(not(len(sys.argv)==4)):
    print "./sparseIntCalc.py operator num1 num2"
    sys.exit()
  if(profile):
	cProfile.run('calcFunction('+sys.argv[2]+','+sys.argv[3]+')')
        sys.exit()

  first  = int(sys.argv[2])
  second = int(sys.argv[3])
  op = sys.argv[1]
  num1 = convertSparse(first)
  num2 = convertSparse(second)
  print "Converted numbers"
  print num1
  print num2
  result = doMath(num1,num2,op)
  if(op=="eq" or op=="gt" or op=="gte"):
    print "Result"
    print result
  else:
    print "Set indecies"
    print result
    print "As an integer"
    print convertInt(result)
  print "What old fashion math says"
  if(op=="add"):
    print first+second
  elif(op=="mult"):
    print first*second
  elif(op=="mod"):
    print first%second 
  elif(op=="sub"):
    print first - second
  elif(op=="eq"):
    print first == second
  elif(op=="gt"):
    print first>second
  elif(op=="gte"):
    print first>=second

if (__name__ == "__main__" ): main()
