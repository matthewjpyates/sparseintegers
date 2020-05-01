#ifndef SPARSEINT_H
#define SPARSEINT_H
#include <vector>
#include <utility>
#include <string>
#include <iostream>
#include <math.h>
template<typename S=unsigned short, typename T=unsigned long>
//template<typename T=unsigned long>
class SparseInt {
    public:
        T topBit;
        std::vector<S> diffs;
        std::vector<bool> signs;   // true  = positive 
        // false = negitive
        /*
         * IMPORTANT: New Position must be greater than or 
         * equal to old position
         *
         * takes a new positive postion and                     
         * adds it to the sparese int as a 
         * difference from the last
         */
        SparseInt& operator=(const T& other)
        {
            (*this)=SparseInt(other);
            return this;
        }
        
        SparseInt& operator=(const long long& other)
        {
            (*this)=SparseInt(other);
            return this;
        }
        

        SparseInt operator+(const SparseInt<S,T>& other)
        {
            SparseInt<S,T> out;
            this->add(out,other);
            return out;
        }

        SparseInt operator-(const SparseInt<S,T>& other)
        {
            SparseInt<S,T> out;
            this->sub(out,other);
            return out;
        }

        SparseInt operator*(const SparseInt<S,T>& other)
        {
            SparseInt<S,T> out;
            this->multSparse(out,other);
            return out;
        }
        
        SparseInt operator/(const SparseInt<S,T>& other)
        {
            SparseInt<S,T> out;
            this->div(out,other);
            return out;
        }
        
        SparseInt operator%(const SparseInt<S,T>& other)
        {
            SparseInt<S,T> out;
            this->mod(out,other);
            return out;
        }
        
        bool operator==(const SparseInt<S,T>& other)
        {
            return this->eq(other);
        }
        
        bool operator==(const long long other)
        {
            SparseInt<S,T> temp = SparseInt<S,T>(other);
            return this->eq(temp);
        }

        bool operator<(const SparseInt<S,T>& other)
        {
            return this->lt(other);
        }

        bool operator>(const SparseInt<S,T>& other)
        {
            return this->gt(other);
        }

        bool operator<=(const SparseInt<S,T>& other)
        {
            return this->lte(other);
        }

        bool operator>=(const SparseInt<S,T>& other)
        {
            return this->gte(other);
        }

        bool operator!=(const SparseInt<S,T>& other)
        {
            return this->neq(other);
        }
        
        bool operator!=(const long long & other)
        {
            SparseInt<S,T> temp = SparseInt<S,T>(other);
            return this->neq(temp);
        }
        

        // loops through the bits of the number
        void resetTopBit()
        {
            S* diffArr = &this->diffs[0];
            this->topBit = 0;
            for(T ii=0;ii<this->diffs.size();ii++)
                this->topBit += diffArr[ii];
        }   

        S addPosIndex(S newPos, S oldPos)   
        {                                      
            if(signs.size()==0)     // if there is no previous bit add the actual position
            {
                addPosDiff(newPos);
            }
            else if(newPos==oldPos)
            {                        // is they are same position either carry or cancel the bit 
                if(signs.back())    // based on the sign
                {    
                    diffs.back() += 1;
                    return oldPos + 1;
                }
                else
                {            // pop from both lists to remove the position
                    removeBackDiff();
                    return oldPos;
                }
            }
            else if(newPos==oldPos+1) // last bit is to close have to solve for sparseness
            {
                if(signs.back())    // last bit is positive
                {                   // ++ ==> -0+
                    signs.pop_back();
                    signs.push_back(false);
                    addPosDiff(newPos-oldPos+1);
                }
                else
                {                // last bit is negitive                 
                    signs.back() = true;  // -+ ==> +0
                }
            }
            else
            {
                addPosDiff(newPos-oldPos);
            }
            return oldPos + this->diffs.back();
        }

        void addListOfPostions(std::vector<T> pos)
        {

            if(pos.size()==0)
                return;
            if(pos.size()==1)
            {
                addPosIndex(0,pos[0]);
                return;
            }
            SparseInt<S,T> tmp, swp;
            tmp = SparseInt<S,T>();
            tmp.diffs.push_back(0);
            tmp.signs.push_back(true);
            if(pos.size()>0)
            {
                for(T ii =0;ii<pos.size();ii++)
                {
                    tmp.diffs[0] = pos[ii];
                    tmp.topBit = pos[ii];
                    this->add(swp,tmp);
                    this->diffs = swp.diffs;
                    this->signs = swp.signs;
                    this->topBit = swp.topBit;
                }
            }
        }

        void removeBackDiff() // removes the last sign and difference 
        {
            signs.pop_back();
            diffs.pop_back();
        }

        bool isZero() const
        {
            return this->signs.size()==0;
        }

        void negateAndCopy(SparseInt<S,T>& out) const
        {
            out = *this;
            for(T ii=0; ii<out.signs.size();ii++)
                out.signs[ii] = !out.signs[ii];
        }

        // performs checks to make use that addSparse is not handed any empty
        // operands
        void add(SparseInt<S,T>& result, const SparseInt<S,T>& other) const
        {
            if(other.isZero())
                result = *this;
            else if(this->isZero())
                result = other;
            else this->addDiffs(result, other);
        }

        void multSparse(SparseInt<S,T>& result, const SparseInt<S,T>& other) const
        {
            if(other.isZero() || this->isZero()) // if either is 0 return 0
            {
                result = SparseInt<S,T>(0);
                return;
            }
            else if(this->diffs.size()==1)  // if you are of size 1 then you are 
            {                               // multiple of 2 and it is just a shitf
                result = other;             // make result other
                if(this->signs.front())
                    result.posBitInc(this->diffs.front());
                else
                    result.negBitInc(this->diffs.front());
                return;
            }
            else if(other.diffs.size()==1) // just like above only other is the one that
            {                               // is shifted by
                result = *this;             // make result this
                if(other.signs.front())
                    result.posBitInc(other.diffs.front());
                else
                    result.negBitInc(other.diffs.front());
                return;
            }
            // at this point both numbers have at least 2 diffs
            T otherSize = other.diffs.size();
            T selfSize = this->diffs.size();
            result = SparseInt<S,T>(0);
            T place = 0;
            if(otherSize>selfSize)
            {
                for(T ii=0; ii<otherSize;ii++)
                {
                    SparseInt<S,T> temp = SparseInt<S,T>(0);
                    place += other.diffs[ii];
                    this->bitShift(temp,place,other.signs[ii]);
                    result.increment(temp);
                }
            }
            else
            {
                for(T ii=0; ii<selfSize;ii++)
                {
                    SparseInt<S,T> temp = SparseInt<S,T>(0);
                    place += this->diffs[ii];
                    other.bitShift(temp,place,this->signs[ii]);
                    result.increment(temp);
                }
            }
            return;
        }


        // performs the same checks as add, but flips the result if self is empty
        // also flips other beofre calling addSparse
        void sub(SparseInt<S,T>& result, const SparseInt<S,T>& other) const
        {
            if(other.isZero())
                result = *this;
            else if(this->isZero())
                other.negateAndCopy(result);
            else {
                SparseInt<S,T> temp;
                other.negateAndCopy(temp);
                this->addDiffs(result, temp);
            }
        }

        void increment(const SparseInt<S,T>& other)
        {
            SparseInt<S,T> temp;
            this->add(temp,other);
            this->diffs = temp.diffs;
            this->signs = temp.signs;
        }

        void decrement(const SparseInt<S,T>& other)
        {
            SparseInt<S,T> temp;
            this->sub(temp,other);
            this->diffs = temp.diffs;
            this->signs = temp.signs;
        }

        // returns this == other
        bool eq(const SparseInt<S,T>& other) const
        {
            if(this->signs.size() != other.signs.size())
                return false;
            for(T ii = 0; ii<this->signs.size(); ii++)
            {   
                if(this->signs[ii]!=other.signs[ii] ||this->diffs[ii]!=other.diffs[ii])
                    return false;
            }
            return true;
        }

        // returns this != other
        bool neq(const SparseInt<S,T>& other) const
        {
            return (!this->eq(other));
        }

        // returns this < other
        bool lt(const SparseInt<S,T>& other) const
        {
            if(this->isZero())
            {
                if(other.isZero())
                    return false;
                return other.signs.back(); // return if other is +
            }

            if(other.isZero()) // already know that this is nonZero
                return (!this->signs.back()); // return if this is -
            // now both numbers are non zero
            // check signs
            if(this->signs.back()) // this is +
            {
                if(!other.signs.back()) // for no numbers can +<- so...
                    return false;
            }
            else // this is -
            {
                if(other.signs.back()) // for all numbers  -<+ so...
                    return true;
            }
            // now both numbers are non zero with the same sign
            T ii = this->diffs.size()  - 1;
            T jj = other.diffs.size() - 1;
            T thisTop  = this->topBit;
            T otherTop = other.topBit;
            while(true)
            {
                if(thisTop>otherTop)
                    return !this->signs[ii];
                else if(thisTop == otherTop)
                {
                    if(this->signs[ii]!=other.signs[jj])
                        return !this->signs[ii];
                }
                else if(thisTop< otherTop)
                    if(this->signs[ii]!=other.signs[jj])
                        return !this->signs[ii];
                    else 
                        return this->signs[ii];
                if(ii == 0 || jj ==0 )
                {
                    break;
                }
                thisTop  -= this->diffs[ii];
                otherTop -= other.diffs[jj];
                ii--;
                jj--;
            }
            if(((int)ii -1)>((int)jj-1))
                return !this->signs[ii-1]; // this is bigger
            if(((int)jj -1)>((int)ii-1))
                return other.signs[jj-1]; // other is bigger
            return false;
        }

        void powMod(SparseInt<S,T>& out,const SparseInt<S,T>& power, const SparseInt<S,T>& modulo) const
        {

            if(modulo.isZero())
            {
                throw "mod by zero error";
                //std::cerr << "mod by zero error in pow mod\n";
                return;
            }
            if(power.isZero())
            {
                if(modulo.diffs.size()==1 && modulo.diffs[0]==0 && modulo.signs[0])
                {
                    out = SparseInt<S,T>();
                    return;
                }

                SparseInt<S,T> temp  = SparseInt<S,T>();
                temp.diffs.push_back(0);
                temp.signs.push_back(true);
                temp.topBit=0;
                temp.mod(out,modulo);
                return;
            }
            if(!power.signs.back())
            {
                std::cerr << "Sparse ints can't handle negitive powers";
                return;
            }
            if(this->isZero())
            {
                out=  SparseInt<S,T>();
                return;
            }
            if(power.diffs.size()==1 && power.diffs[0]==0)
            {
                this->mod(out,modulo);
                return;
            }
            out =  SparseInt<S,T>(1);
            bool sn = false;
            SparseInt<S,T> temp = *this;
            SparseInt<S,T> swap;
            for(T ii =0;  ii<power.diffs.size(); ii++)
            {
                //sn=!power.signs[ii]; 
                for(T jj =0; power.diffs[ii]>0; jj++)
                {
                    temp.multSparse(swap,temp);
                    swap.resetTopBit();
                    swap.mod(temp,modulo);

                    if (jj == power.diffs[ii]-1) break;

                    if(sn)
                    {
                        temp.multSparse(swap,out);
                        swap.resetTopBit();
                        swap.mod(out,modulo);
                    }
                }
                if(!sn)
                {
                    temp.multSparse(swap,out);
                    swap.resetTopBit();
                    swap.mod(out,modulo);
                }
                sn=!power.signs[ii];
            }
            return;
        }

        // returns this <= other
        bool lte(const SparseInt<S,T>& other) const
        {
            if(this->isZero())
            {
                if(other.isZero())
                    return true;
                return other.signs.back(); // return if other is +
            }

            if(other.isZero()) // already know that this is nonZero
                return (!this->signs.back()); // return if this is -
            // now both numbers are non zero
            // check signs
            if(this->signs.back()) // this is +
            {
                if(!other.signs.back()) // for no numbers can +<- so...
                    return false;
            }
            else // this is -
            {
                if(other.signs.back()) // for all numbers  -<+ so...
                    return true;
            }
            // now both numbers are non zero with the same sign
            T ii = this->diffs.size()  - 1;
            T jj = other.diffs.size() - 1;
            T thisTop  = this->topBit;
            T otherTop = other.topBit; 
            while(true)
            {
                if(thisTop>otherTop)
                    return !this->signs[ii];
                else if(thisTop == otherTop)
                {
                    if(this->signs[ii]!=other.signs[jj])
                        return !this->signs[ii];
                }
                else if(thisTop< otherTop)
                    if(this->signs[ii]!=other.signs[jj])
                        return !this->signs[ii];
                    else 
                        return this->signs[ii];
                if(ii == 0 || jj ==0 )
                {
                    break;
                }
                thisTop  -= this->diffs[ii];
                otherTop -= other.diffs[jj];
                ii--;
                jj--;
            }
            if(ii!=0)
                return !this->signs[ii-1]; // this is bigger
            else if(jj!=0)
                return other.signs[jj-1]; // other is bigger
            return true;
        }

        // this is used in div and mod
        // 0 means this > other
        // 1 means this < other
        // 2 means this == other 
        char cmpQuoRem(const SparseInt<S,T>& other) const
        {
            if(this->isZero())
            {
                if(other.isZero())
                    return 2;
                return other.signs.back() ? 1: 0; // return if other is +
            }

            if(other.isZero()) // already know that this is nonZero
                return (!this->signs.back()) ? 1 :0; // return if this is -
            // now both numbers are non zero
            // check signs
            if(this->signs.back()) // this is +
            {
                if(!other.signs.back()) // for no numbers can +<- so...
                    return 0;
            }
            else // this is -
            {
                if(other.signs.back()) // for all numbers  -<+ so...
                    return 1;
            }
            // now both numbers are non zero with the same sign
            T ii = this->diffs.size()  - 1;
            T jj = other.diffs.size() - 1;
            T thisTop  = this->topBit;
            T otherTop = other.topBit; 
            while(true)
            {
                if(thisTop>otherTop)
                    return !this->signs[ii];
                else if(thisTop == otherTop)
                {
                    if(this->signs[ii]!=other.signs[jj])
                        return !this->signs[ii];
                }
                else if(thisTop< otherTop)
                {
                    if(this->signs[ii]!=other.signs[jj])
                        return !this->signs[ii] ? 1: 0;
                    else 
                        return this->signs[ii] ? 1: 0;
                }
                if(ii == 0 || jj ==0 )
                {
                    break;
                }
                thisTop  -= this->diffs[ii];
                otherTop -= other.diffs[jj];
                ii--;
                jj--;
            }
            if(((int)ii -1)>((int)jj-1))
                return !this->signs[ii-1] ? 1 : 0; // this is bigger
            else if(((int)jj -1)>((int)ii-1))
                return other.signs[jj-1] ? 1 : 0; // other is bigger
            return 2;
        }
        
        // returns >
        bool gt(const SparseInt<S,T>& other) const 
        {
            return !this->lte(other);
        }

        void toBits(std::vector<T> &out) const
        {
            T place =0;
            for(T ii=0; ii<((T)(this->diffs.size()));ii++)
            {
                place += ((T)(this->diffs[ii]));  
                out.push_back(place);
            }
        }

        void div(SparseInt<S,T>& result, const SparseInt<S,T>& other) const
        {
            if(this->signs.back()==other.signs.back())
            {
                if(this->signs.back())
                {
                    this->divSparse(result,other);
                }
                else
                {
                    SparseInt<S,T> temp,tempOther;
                    this->negateAndCopy(temp);
                    other.negateAndCopy(tempOther);
                    temp.divSparse(result,tempOther);
                }
            }
            else
            {
                SparseInt<S,T> temp;
                if(this->signs.back()) 
                {
                    other.negateAndCopy(temp);
                    this->divSparse(result,temp);
                }
                else
                {
                    this->negateAndCopy(temp);
                    temp.divSparse(result,other);
                }
                result.negateAndCopy(result);
            }
        }

        // makes result = this/other
        // only works for positive and positive numbers
        void divSparse(SparseInt<S,T>& result, const SparseInt<S,T>& other) const
        {
            if(other.isZero())
            {
                std::cerr << "Divide by 0 error, jerk\n";
                return;
            }
            if(this->isZero())
            {
                result=*this;
                return;
            }
            if(other.diffs.size()==1 && other.diffs[0]==0) // either 1 or -1
            {
                if(other.signs[0]) // this/1
                {
                    result=*this;
                    return;
                }
                // this/-1
                this->negateAndCopy(result);
                return;
            }
            char cmp = this->cmpQuoRem(other);
            if(cmp ==2)
            {
                result = SparseInt<S,T>(1);
                return;
            }
            if(cmp == 1)
            {
                result = SparseInt<S,T>();
                return;
            }
            // now this > other
            // other is non zero
            // this is non zero
            // other is not 1
            // time for math

            // set up ...
            T diff;
            SparseInt<S,T> numerator, denominator, swap, swapOther;
            // lets do this... 
            // ... LEROOOOOY JEEEENKINS!!!!
            numerator = *this;                      // set the numerator as this
            result = SparseInt<S,T>(0);             // zero out the resulti
            swap.diffs.push_back(0);
            swap.signs.push_back(true);
            while(numerator.gte(other))
            {
                if(numerator.topBit == other.topBit)
                {
                    swap.diffs[0] = 0;
                    result.add(swapOther,swap);                 // calculate result + theShift
                    result = swapOther;                         // store the new result
                    return;
                }

                diff = numerator.topBit - other.topBit -1;

                swap.diffs[0] =diff; 
                result.add(swapOther,swap);                 // calculate result + theShift
                result = swapOther;                         // store the new result

                other.leftShift(denominator,diff);
                numerator.sub(swapOther,denominator);            // subtract the numerator from the denominator
                numerator = swapOther;                // store the new numerator
                numerator.resetTopBit();
            }
            return;
        }

        void mod(SparseInt<S,T>& result, const SparseInt<S,T>& other) const
        {
            if(this->signs.back()==other.signs.back())
            {
                if(this->signs.back())
                {
                    this->modSparse(result,other);
                }
                else
                {
                    SparseInt<S,T> temp,tempOther;
                    this->negateAndCopy(temp);
                    other.negateAndCopy(tempOther);
                    temp.modSparse(result,tempOther);
                    result.negateAndCopy(result);
                }
            }
            else
            {
                SparseInt<S,T> temp;
                if(this->signs.back()) 
                {
                    other.negateAndCopy(temp);
                    this->modSparse(result,temp);
                }
                else
                {
                    this->negateAndCopy(temp);
                    temp.modSparse(result,other);
                    result.negateAndCopy(result);
                }
            }
        }


        // makes result = this % other
        // only works for positive and positive numbers
        void modSparse(SparseInt<S,T>& result, const SparseInt<S,T>& other) const
        {
            result = SparseInt<S,T>(0);
            if(other.isZero())
            {
                std::cerr << "Mod by 0 error, jerk\n";
                return;
            }
            if(this->isZero())
            {
                result=*this;
                return;
            }
            if(other.diffs.size()==1 && other.diffs[0]==0) // either 1 or -1
            {
                if(other.signs[0]) // this%1
                {
                    return;
                }
                // this/-1
                this->negateAndCopy(result);
                return;
            }
            char cmp = this->cmpQuoRem(other);
            if(cmp ==2)
            {
                result = SparseInt<S,T>(0);
                return;
            }
            if(cmp == 1)
            {
                result = *this;
                return;
            }
            // now this > other
            // other is non zero
            // this is non zero
            // other is not 1
            // time for math

            // set up ...
            T diff;
            SparseInt<S,T> denominator, swap;
            // lets do this... 
            // ... LEROOOOOY JEEEENKINS!!!!
            result = *this;                   // set the numerator as this
            while(result.gte(other))
            {
                if(result.topBit == other.topBit)
                {
                    result.sub(swap,other);
                    result = swap;
                    return;
                }

                diff = result.topBit - other.topBit -1;
                other.leftShift(denominator,diff);
                result.sub(swap,denominator);            // subtract the numerator from the denominator
                result = swap;
                result.resetTopBit();
            }
            return;
        }

        void modNegSparse(SparseInt<S,T>& result, const SparseInt<S,T>& other, bool isEqual) const
        {
            if(other.isZero())
            {
                std::cerr << "Mod by 0 error, jerk\n";
                return;
            }
            if(this->isZero())
            {
                result=*this;
                return;
            }
            if(other.diffs.size()==1 && other.diffs[0]==0) // either 1 or -1
            {
                if(other.signs[0]) // this%1
                {
                    result=SparseInt<S,T>(0);
                    return;
                }
                // this/-1
                this->negateAndCopy(result);
                return;
            }
            char cmp = this->cmpQuoRem(other);
            if(cmp ==2)
            {
                result = SparseInt<S,T>(0);
                return;
            }
            if(cmp == 1)
            {
                result = *this;
                return;
            }
            // now this > other
            // other is non zero
            // this is non zero
            // other is not 1
            // time for math

            // set up ...
            T diff;
            SparseInt<S,T> denominator, swap;
            // lets do this... 
            // ... LEROOOOOY JEEEENKINS!!!!
            result = *this;                      // set the numerator as this
            while(result.gte(other))
            {
                if(result.topBit == other.topBit)
                {
                    result.sub(swap,other);
                    result = swap;
                    return;
                }

                diff = result.topBit - other.topBit -1;
                other.leftShift(denominator,diff);
                result.sub(swap,denominator);            // subtract the numerator from the denominator
                result = swap;
                result.resetTopBit();
            }
            return;
        }

        void abs(SparseInt<S,T>& out)
        {
            if(this->signs.back())
            {
                out = *this;
                return;
            }

            this->negateAndCopy(out);
            return;
        }

        // this gets the chunk that the number can be shifted over in 
        // division
        void getChunk(SparseInt<S,T> &out,T& amount) const
        {
            out = SparseInt<S,T>(0);
            T place = this->diffs.size() -1;
            T firstDiff = this->topBit;
            while((amount - this->diffs[place])>0)
            {
                amount -=  this->diffs[place];
                out.diffs.insert(out.diffs.begin(),this->diffs[place]);
                out.signs.insert(out.signs.begin(),this->signs[place]);
                if(place == 0)
                    break;
                place--;
            }

            for(T ii = 0; ii< out.diffs.size();  ii++)
                firstDiff -= out.diffs[ii];

            if(out.diffs.size()>0)
                out.diffs[0]=firstDiff;
            else
            {
                out = SparseInt<S,T>(1); 
            }

        }
        
        // makes sure that carries are done properly
        // probably the most used method in the whole 
        // libary
        void carryLogic(const T newBit,const  bool &newSign)
        {
            if(this->isZero())
            {
                this->diffs.push_back(newBit);
                this->signs.push_back(newSign);
                this->topBit = newBit;
                return;
            }
            if(this->topBit>newBit)
                std::cerr << "\n Error \n";
            if(this->topBit==newBit)
            {
                if(this->signs.back()==newSign)
                {
                    this->diffs.back() += 1;
                    this->topBit += 1;
                    return;
                }
                this->topBit -= this->diffs.back();
                this->diffs.pop_back();
                this->signs.pop_back();
                return;
            }

            if(this->topBit+1==newBit)
            {
                if(this->signs.back()==newSign)
                {
                    this->signs.back() = !signs.back();
                    this->diffs.push_back(2);
                    this->signs.push_back(newSign);
                    this->topBit += 2;
                    return;
                }
                this->signs.back() = !(this->signs.back());
                return;
            }
            this->diffs.push_back(newBit-this->topBit);
            this->topBit = newBit;
            this->signs.push_back(newSign);
            return;
        }
        
        bool gte( const SparseInt<S,T>& other) const
        {
            return !this->lt(other);
        }

        void addDiffs(SparseInt<S,T>& result, const SparseInt<S,T> other) const
        {
            T selfIndex = 0;
            T otherIndex = 0;
            T selfPlace = 0;
            T otherPlace = 0;
            result = SparseInt<S,T>();
            while(((T)selfPlace) <((T) (this->diffs.size())) || ((T)otherPlace) < ((T)(other.diffs.size())))
            {

                if(((T)selfPlace) < ((T)(this->diffs.size())) &&((T) otherPlace) <((T) (other.diffs.size())))
                {
                    if(((T)(this->diffs[selfPlace]))+selfIndex==((T)(other.diffs[otherPlace]))+otherIndex)
                    {

                        if(this->signs[selfPlace]==other.signs[otherPlace])
                        {
                            result.carryLogic(((T)(this->diffs[selfPlace]))+selfIndex + 1, this->signs[selfPlace]);
                        }
                        otherIndex += other.diffs[otherPlace];
                        selfIndex += this->diffs[selfPlace];
                        selfPlace++;
                        otherPlace++;
                    }
                    else if(this->diffs[selfPlace]+selfIndex>other.diffs[otherPlace]+otherIndex)
                    {
                        result.carryLogic(((T)other.diffs[otherPlace])+otherIndex, ((T)other.signs[otherPlace]));
                        otherIndex += other.diffs[otherPlace];
                        otherPlace++;
                    }
                    else  
                    {
                        result.carryLogic(((T)this->diffs[selfPlace]+selfIndex), this->signs[selfPlace]);
                        selfIndex += this->diffs[selfPlace];
                        selfPlace++;
                    }

                }
                else if(selfPlace < this->diffs.size())
                {
                    for(T ii = selfPlace; ii < this->diffs.size(); ii++)
                    {
                        result.carryLogic(((T) this->diffs[ii]+selfIndex), this->signs[ii]);
                        selfIndex += this->diffs[ii];
                    }
                    break;

                }
                else
                {
                    for(T ii = otherPlace; ii < other.diffs.size(); ii++)
                    {
                        result.carryLogic(((T)other.diffs[ii]+otherIndex), other.signs[ii]);
                        otherIndex += other.diffs[ii];
                    }
                    break;
                }


            }
            //result.resetTopBit();
            return;
        }

        long long toLongLong()
        {
            long long out=0;
            T place = 0;
            for(T ii=0;ii<this->signs.size(); ii++)
            {
                place  += this->diffs[ii];
                out += pow(2,(place))*((this->signs[ii])?1:-1);
            }
            return out;

        }
        S addNegIndex(S newPos, S oldPos)
        {
            if(signs.size()==0)     // if there is no previous bit add the actual position
                addNegDiff(newPos);
            else if(newPos==oldPos)
            {                       // is they are same position either carry or cancel the bit 
                if(!signs.back())   // based on the sign
                {
                    diffs.back() += 1;
                    return oldPos +1;
                }
                else            // pop from both lists to remove the position
                    removeBackDiff();
                return oldPos;

            }
            else if(newPos==oldPos+1) // last bit is to close have to solve for sparseness
                if(!signs.back())    // last bit is negitive
                {                   // -- ==> +0-
                    signs.back() = true;
                    addNegDiff(newPos-oldPos+1);
                }
                else                // last bit is positive
                    signs.back() = false;  // +- ==> -0
            else
                addNegDiff(newPos-oldPos);
            return oldPos + this->diffs.back();
        }

        void addPosDiff(S diff) //  puts a new positive difference on the number
        {
            signs.push_back(true);
            diffs.push_back(diff);
        }

        std::string bitsToString()   // loops through the number and returns a string
        {                       // that has all the indecies with their signs
            std::string out = " ";
            T place = 0;
            if(this->signs.size()==0)
                return "";
            else
            {
                place = this->diffs[0];
                out += ((this->signs[0])?1:-1)*diffs[0];
            }
            for(T ii=1; ii<this->signs.size(); ii++)
            {
                place += this->diffs[ii];
                out += " " + ((this->signs[0])?1:-1)*place;
            }
            return out;
        }

        void printBits() const   // loops through the number and returns a string
        {                       // that has all the indecies with their signs
            T place = 0;
            if(this->signs.size()==0)
                return;
            else
            {
                place = this->diffs[0];
                std::cout <<  ((this->signs[0])?'+':'-') << (unsigned int) diffs[0];
            }
            for(T ii=1; ii<this->signs.size(); ii++)
            {
                place += this->diffs[ii];
                std::cout << " " << ((this->signs[ii])?'+':'-') <<  place;
            }
            std::cout << "\n";
            return;
        }

        std::string diffsToString()  // loops through the number and returns a string
        {                       // prints the differences with the corrasponding sign
            std::string out;
            out = "";

            if(this->signs.size()==0)
                return "";
            else
                out += ((this->signs[0])?1:-1)*(this->diffs[0]);

            for(T ii=1; ii<this->signs.size(); ii++)
                out += " " + ((this->signs[ii])?1:-1)*this->diffs[ii];
            return out;
        }

        // only will increase position
        void posBitInc(S shift) // shifts the number over by the shift
        {
            if(this->signs.empty())
                return;
            this->diffs.front() += shift;
        }

        // will shift the bits ncreasesition
        void bitShift(SparseInt<S,T>& out, S shift, bool sign) const // shifts the number over by the shift
        {
            out = *this;
            if(sign)
                out.posBitInc(shift);
            else
                out.negBitInc(shift);
            return;
        }

        // only will increase position
        void negBitInc(S shift)   // shifts the number over by the shift
        {                           // also flips the signs
            if(this->signs.empty()) 
                return;
            this->diffs.front() += shift;
            for(T ii=0; ii<this->signs.size(); ii++)
                this->signs[ii] = !(this->signs[ii]);
        }


        void addNegDiff(S diff) // places a new negitive difference
        {
            this->signs.push_back(false);
            this->diffs.push_back(diff);
        }


        int toInt() const // loops through the diffs and converts them to indecies
        {           // subtacting away the negitive signed bits 
            int out=0;
            T place = 0;
            for(T ii=0;ii<this->signs.size(); ii++)
            {
                place  += this->diffs[ii];
                out += pow(2,(place))*((this->signs[ii])?1:-1);
            }
            return out;
        }

        // returns this >> shift
        // FIXME this does not work quite yet
        void rightShift(SparseInt<S,T>& result, T other) const
        {
            result = *this;
            T temp;
            while(result.diffs.size()>0 && result.diffs[0] < other)
            {
                temp = result.diffs[0];
                result.diffs.erase (result.diffs.begin());
                result.signs.erase (result.signs.begin());
                other -= temp;
            }
            if(result.isZero())
            {
                if((!(this->isZero())) && (!(this->signs.back())))
                {
                    result.diffs.push_back(0);
                    result.signs.push_back(false);
                }
                return;
            }
            result.diffs[0] -= other;
        }

        void leftShift(SparseInt<S,T>& result, const T &other) const
        {
            result = *this;
            if(result.isZero())
                return;
            result.diffs[0] += other;
        }

        T getLastBit(T lastIndex)
        {
            return lastIndex + this->diffs.back();
        }

        
        SparseInt(long long inNumber = 0)
        {
            if(inNumber ==0)
                return;
            S   index   = 0;
            S   last    = 0;
            bool inc = false;
            if(inNumber>0)
            {
                while(inNumber != 0)
                {
                    if(inNumber&1)
                    {
                        last = addPosIndex(index,last);
                        inNumber -= 1;
                    }
                    index++;
                    inNumber = inNumber/2;
                }
            }
            else
            {
                while(inNumber != 0)
                {
                    if(inNumber&1)
                    {
                        last = addNegIndex(index,last);
                        inNumber += 1;
                    }
                    index++;
                    inNumber = inNumber/2;
                }
            }
        resetTopBit();
        }
};

template<typename S, typename T>
bool operator==(long long other, const SparseInt<S,T>& x) {
    return x->eq(SparseInt<S,T>(other));
}
#endif
