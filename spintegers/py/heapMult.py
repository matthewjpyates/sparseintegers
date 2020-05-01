"""
This is supposed to be an implementatiion of heap 
based multiplication as opposed to repetivie adding
for sparse Integers

I am going to assume that I am passed two in order lists that
are both sparse integers
"""

"""

A special means of heap pop as when ever two identical elements
are found they are added together

"""
class HeapMult(object):
     @staticmethod
     def listSwap(l,a,b):
          temp = l[a]
          l[a]=l[b]
          l[b]=temp
          return l
     @staticmethod
     def fixCarry(heap, index):
          heap[index]+=1
          if((index+1)*2<len(heap) 
          and heap[(index+1)*2]<heap[(index+1)*2-1]):
               flip = 0
          else:
               flip = -1
          tempIndex = (index+1)*2+flip
          while((tempIndex+1)*2-1<len(heap)):
               if(heap[(tempIndex+1)*2-1]==float("inf") and
                    (tempIndex+1)*2<len(heap) and
                    heap[(tempIndex+1)*2-1]==float("inf")):
                    break;
               else:
                    if((tempIndex+1)*2<len(heap) and
                    heap[(tempIndex+1)*2]<
                               heap[(index+1)*2-1]):
                         flip = 0
                    else:
                         flip = -1
                    heap = HeapMult.listSwap(heap,
                            tempIndex,
                            (tempIndex+1)*2+flip)
                    tempIndex = (tempIndex+1)*2+flip
          heap[tempIndex] = float("inf")  # a stopper
          return heap


     @staticmethod
     def fixHeap(heap):
          # since I am going to have to do this in many 
          # places I should do it right once
          index = 0
          if(heap==[]):
              return []
          while(heap!=[] and (index+1)*2-1<len(heap)):
               if((index+1)*2<len(heap) and 
               heap[(index+1)*2]<heap[(index+1)*2-1]):
                    flip = 0
               else:
                    flip = -1
               if(heap[index]== heap[(index+1)*2+flip]):
                    heap = HeapMult.fixCarry(heap,index)
               elif(heap[index] > heap[(index+1)*2+flip]):
                    heap = HeapMult.listSwap(heap,index,(index+1)*2+flip)
                    index = (index+1)*2+flip
               else: # this means that the element at index in the heap must be 
                    break # smaller than its children so we stop the heap is fixed
          return heap

     @staticmethod
     # resorts the list
     def toList(heap):
          tempL = HeapMult.heapPop(heap)
          temp = tempL[0]
          out = [temp]
          heap = tempL[1]
          while(len(heap)>0 and temp != float("inf") and temp > -1):
               out.append(temp)
               tempList = HeapMult.heapPop(heap)
               temp = tempList[0]
               heap = tempList[1]
          return out
    
     @staticmethod
     def getMin(heap):
        out = heap.pop(0)
        if(len(heap)==0):
            return [out]
        heap.insert(0,heap.pop(len(heap)-1))
        index = 0
        size = len(heap)
        #FIXME
        while(index<size and 
                (((index*2+1)<size and heap[index*2+1]<heap[index]) 
                    or ((index*2+2)<size and heap[index*2+2]<heap[index]))):
                if(index*2+2<size):
                    if(heap[index*2+2]<heap[index*2+1]):
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

     @staticmethod
     def heapEnque(heap, item):
        heap.append(item)
        if(len(heap)==1):
            return heap
        index = len(heap) - 1
        while(index>0 and (index-1)/2>=0 and heap[(index-1)/2]>heap[index]):
            temp = heap[index]
            heap[index] = heap[(index-1)/2] 
            heap[(index-1)/2] = temp
        return heap
        
     @staticmethod
     def sparseHeapMult(a, b):
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
        f = lambda  y:  x + y
        heap = map(f,suppList)
        heap=HeapMult.getMin(heap)
        out.append(heap.pop(0))
        while(len(heap)>0 and shift<len(shiftList)):
            if(heap[0] == shiftList[shift]+suppList[place]):
                heap = HeapMult.getMin(heap)
                temp = heap.pop(0)
                temp += 1
                HeapMult.heapEnque(heap,temp)
                place += 1
            elif(heap[0] < shiftList[shift]+suppList[place]):
                heap = HeapMult.getMin(heap)
                z = heap.pop(0)
                if(len(out)>0 and out[-1]==z):
                    temp = out.pop(len(out)-1)
                    temp += 1
                    heap = HeapMult.heapEnque(heap,temp)
                else:
                    out.append(z)
            else:
                z = shiftList[shift]+suppList[place]
                if(len(out)>0 and out[-1]==z):
                    temp = out.pop(len(out)-1)
                    temp += 1
                    heap = HeapMult.heapEnque(heap,temp)
                else:
                    out.append(z)
                place += 1
            if(place  == len(suppList)):
                 place = 0
                 shift += 1
        while(shift<len(shiftList)):
            heap = HeapMult.heapEnque(heap,shiftList[shift]+suppList[place])
            place += 1
            if(place  == len(suppList)):
                 place = 0
                 shift += 1
        while(len(heap)>0):
            heap = HeapMult.getMin(heap)
            z = heap.pop(0)
            if(len(out)>0 and out[-1]==z):
                temp = out.pop(len(out)-1)
                temp += 1
                heap = HeapMult.heapEnque(heap,temp)
            else:
                out.append(z)
            
        return out

                             
     @staticmethod
     def heapPop(heap):
          # this looks easy
          out = heap.pop(0)
          # but now the heap must be fixed
          if(len(heap)==0): # get rid of this empty list garbage
               return [out,[]]
          # put last most element first
          heap.insert(0,heap.pop(len(heap)-1))
          heap = HeapMult.fixHeap(heap)
          return [out,heap]
     @staticmethod
     def heapInsert(heap,num):
               heap.append(num)
               index = len(heap) - 1
               while(((index + index%2)/2 - 1) > -1 and 
                    heap[index]<heap[(index + index%2)/2 - 1]):
                    if(heap[index]==heap[(index + index%2)/2 - 1]):
                         heap = HeapMult.fixCarry(heap,(index + index%2)/2 - 1)
                         index = (index + index%2)/2 - 1
                    else:
                         heap = HeapMult.listSwap(heap,index, (index + index%2)/2 - 1)
                         index = (index + index%2)/2 -1
               return heap
          
     @staticmethod
     def heapMult(a,b):
          # if they are empty return 0 for [] is 0
          out = []
          if(len(a)==0 or len(b)==0):
               return out 
          if(a[0]<b[0]):
               y = a.pop(0)
               heap = map(lambda x: x+y,b)
          else:
               y = b.pop(0)
               heap = map(lambda x: x+y,a)
          # the element in a[0] is the smallest in a
          # and b is alredy in order so a min heap will be made
          
          while(len(a)>0 and len(b)>0):
               print "in heap mult at the top of the while loop"
               print "a is"
               print a
               print "b is"
               print b
               print "heap is"
               print heap
               print "out"
               print out
               if(a[0]<b[0]):
                    y = a.pop(0)
                    tempL = map(lambda x: x+y,b)
               else:
                    y = b.pop(0)
                    tempL = map(lambda x: x+y,a)
               for ele in tempL:
                    heap = HeapMult.heapInsert(heap,ele)
                    tempL = HeapMult.heapPop(heap)
                    heap = tempL[1]
                    out.append(heap[0])
          tempList = list(HeapMult.toList(list(heap)))
          if(len(tempList)>0):
               out.extend(tempList)
          print "about to return the answer"      
          print out
          return out



