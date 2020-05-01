#include "sparseInt.h"
#include <iostream>
#include <string>
#include <vector>
#include <gmp.h>
#include <gmpxx.h> 
#include <ctime>    // For time()
#include <cstdlib>  // For srand() and rand()
#include <stdlib.h>
#include <unistd.h>
#include <sys/time.h>


// DIFFTYPE is the datatype that will be used in holding the differences between
// the positions in the sparsInt
#define DIFFTYPE unsigned short


//INDEXTYPE is the datatype that is used to represent the position of the bits in 
// the sarse int therfore the sparse int will be limited by the 
// 2^(largest possible number of Data type +1 ) -1
#define INDEXTYPE unsigned long


using namespace std; 

mpz_class makeMpzClassNum(vector<INDEXTYPE> inBits)
{
    mpz_t temp;
    mpz_class num;
    mpz_init(temp);
    for(INDEXTYPE ii =0; ii<inBits.size();ii++)
    {
        mpz_ui_pow_ui(temp,2,inBits[ii]);
        mpz_add(num.get_mpz_t(),temp,num.get_mpz_t());
    }
    mpz_clear(temp);
    return num;
}


// the class to be overloaded
class sparseOperator
{
    public:
        sparseOperator() {return;}
        void operator()(SparseInt<DIFFTYPE,INDEXTYPE> a, SparseInt<DIFFTYPE,INDEXTYPE> b, SparseInt<DIFFTYPE,INDEXTYPE> &out) {return;}
};
class addSparse: public sparseOperator {
    public:
        addSparse() {return;} 
        void operator()(SparseInt<DIFFTYPE,INDEXTYPE> a, SparseInt<DIFFTYPE,INDEXTYPE> b, SparseInt<DIFFTYPE,INDEXTYPE> &out) 
        {
            a.add(out,b);
            return;
        }
};


class subSparse: public sparseOperator {
    public:
        void operator()(SparseInt<DIFFTYPE,INDEXTYPE> a, SparseInt<DIFFTYPE,INDEXTYPE> b, SparseInt<DIFFTYPE,INDEXTYPE> &out) 
        {
            a.sub(out,b);
            return;
        }
};

class multSparse: public sparseOperator {
    public:
        void operator()(SparseInt<DIFFTYPE,INDEXTYPE> a, SparseInt<DIFFTYPE,INDEXTYPE> b, SparseInt<DIFFTYPE,INDEXTYPE> &out) 
        {
            a.multSparse(out,b);
            return;
        }
};


class divSparse: public sparseOperator {
    public:
        void operator()(SparseInt<DIFFTYPE,INDEXTYPE> a, SparseInt<DIFFTYPE,INDEXTYPE> b, SparseInt<DIFFTYPE,INDEXTYPE> &out) 
        {
            a.div(out,b);
            return;
        }
};





class modSparse: public sparseOperator {
    public:
        void operator()(SparseInt<DIFFTYPE,INDEXTYPE> a, SparseInt<DIFFTYPE,INDEXTYPE> b, SparseInt<DIFFTYPE,INDEXTYPE> &out) 
        {
            a.mod(out,b);
            return;
        }
};



class powModSparse: public sparseOperator {
    public:
        void operator()(SparseInt<DIFFTYPE,INDEXTYPE> a, SparseInt<DIFFTYPE,INDEXTYPE> b, SparseInt<DIFFTYPE,INDEXTYPE> c,  SparseInt<DIFFTYPE,INDEXTYPE> &out) 
        {
            a.powMod(out,b,c);
            return;
        }
};

class gmpOperator
{
    public:
        gmpOperator(){return;}
        void operator()(mpz_class a, mpz_class b, mpz_class &out) {return;}
};


class addGMP: public gmpOperator
{
    public:
        void operator()(mpz_class a, mpz_class b, mpz_class &out) 
        {
            out = a+b;
            return;
        }
};

class subGMP: public gmpOperator
{
    public:
        void operator()(mpz_class a, mpz_class b, mpz_class &out) 
        {
            out = a-b;
            return;
        }
};

class multGMP: public gmpOperator
{
    public:
        void operator()(mpz_class a, mpz_class b, mpz_class &out) 
        {
            out = a*b;
            return;
        }
};


class divGMP: public gmpOperator
{
    public:
        void operator()(mpz_class a, mpz_class b, mpz_class &out) 
        {
            out = a/b;
            return;
        }
};


class modGMP: public gmpOperator
{
    public:
        void operator()(mpz_class a, mpz_class b, mpz_class &out) 
        {
            out = a%b;
            return;
        }
};

class powModGMP: public gmpOperator
{
    public:
        void operator()(mpz_class a, mpz_class b, mpz_class c, mpz_class &out) 
        {
            out = a%b;
            return;
        }
};




bool contains(vector<INDEXTYPE> v,INDEXTYPE x)
{
    for(int ii =0; ii< v.size();ii++)
    {
        if(x==v[ii])
            return true;
    }
    return false;
}

void make_gmp_number(vector<INDEXTYPE> inBits,mpz_t &num)
{
    mpz_t temp;
    mpz_init(temp);
    for(INDEXTYPE ii =0; ii<inBits.size();ii++)
    {
        mpz_ui_pow_ui(temp,2,inBits[ii]);
        mpz_add(num,temp,num);
    }
    mpz_clear(temp);
}

vector<INDEXTYPE> makeBitsSmart(INDEXTYPE maxBit, INDEXTYPE numberOfBits)
{
    vector<INDEXTYPE> out;
    vector<INDEXTYPE> s;
    for( INDEXTYPE i = 0; i <= maxBit; ++i ) s.push_back(i);
    if(maxBit<=numberOfBits)
        return s;
    INDEXTYPE index,r;
    bool found;
    if(s.size()>0)
    {
        out.push_back(s[s.size()-1]);
        s.pop_back();
    }
    if(s.size()>0)
    {
        for(INDEXTYPE jj=0; s.size()>0 && jj<numberOfBits; jj++)
        {
            index = rand() % s.size();
            r = s[index];
            s.erase(s.begin()+index);
            found = false;
            for(INDEXTYPE ii=0; ii<out.size();ii++)
            {
                if(r<out[ii])
                {
                    found = true;
                    out.insert(out.begin()+ii,r);
                    break;
                }
            }
            if(!found)
                out.push_back(r);
        }
    }
    return out;

}

void setTimeInMilli(long double &milli)
{
    struct timeval tv;
    gettimeofday(&tv, NULL);
    milli = tv.tv_usec;
    milli /= 1000.0;
    milli += (tv.tv_sec * 1000.0);
}

    template<typename S>  
void runTestImproved(vector<INDEXTYPE> bits1, vector<INDEXTYPE> bits2, 
        S sparseIntFunc, gmpOperator gmpFunc)
{
    SparseInt<DIFFTYPE,INDEXTYPE> si1;
    SparseInt<DIFFTYPE,INDEXTYPE> si2;     
    SparseInt<DIFFTYPE,INDEXTYPE> si3;     
    si1.addListOfPostions(bits1); 
    si2.addListOfPostions(bits2);
    mpz_class num1, num2, num3;

    num1 = makeMpzClassNum(bits1);
    num2 = makeMpzClassNum(bits2);

    long double start = 0;
    long double stop = 0;
    long double resultSparse = 0;
    long double resultGMP = 0;
    int numberOfTimesSparse = 1;
    int numberOfTimesGMP = 1;
    do
    {
        int ii=0;
        setTimeInMilli(start);
        for(;ii<numberOfTimesSparse;ii++)
            sparseIntFunc(si1,si2,si3);
        setTimeInMilli(stop);
        resultSparse = stop - start;
        numberOfTimesSparse*=2;
    }
    while(resultSparse<250);
    cout << "," << (1000 * (numberOfTimesSparse*1.0)/resultSparse) << ",";
    do
    {
        int ii=0;
        setTimeInMilli(start);
        for(;ii<numberOfTimesGMP;ii++)
            gmpFunc(num1,num2,num3);
        setTimeInMilli(stop);
        resultGMP = stop - start;
        numberOfTimesGMP*=2;
    }
    while(resultGMP<250);
    cout << (1000.0*(numberOfTimesGMP*1.0)/resultGMP);
}

void runTest(vector<INDEXTYPE> bits1, vector<INDEXTYPE> bits2, void (*pt2SparseFunc)(SparseInt<DIFFTYPE,INDEXTYPE> a, SparseInt<DIFFTYPE,INDEXTYPE> b, SparseInt<DIFFTYPE,INDEXTYPE> &out),
        void (*pt2GMPFunc)(mpz_t a, mpz_t b, mpz_t &out))
{
    SparseInt<DIFFTYPE,INDEXTYPE> si1;
    SparseInt<DIFFTYPE,INDEXTYPE> si2;     
    SparseInt<DIFFTYPE,INDEXTYPE> si3;     
    si1.addListOfPostions(bits1); 
    si2.addListOfPostions(bits2);
    mpz_t num1;
    mpz_init(num1);
    make_gmp_number(bits1,num1);
    mpz_t num2;
    mpz_init(num2);
    make_gmp_number(bits2,num2);
    mpz_t num3;
    mpz_init(num3);
    long double start = 0;
    long double stop = 0;
    long double resultSparse = 0;
    long double resultGMP = 0;
    int numberOfTimesSparse = 1;
    int numberOfTimesGMP = 1;
    do
    {
        int ii=0;
        setTimeInMilli(start);
        for(;ii<numberOfTimesSparse;ii++)
            (*pt2SparseFunc)(si1,si2,si3);
        setTimeInMilli(stop);
        resultSparse = stop - start;
        numberOfTimesSparse*=2;
    }
    while(resultSparse<250);
    cout << "," << (resultSparse/(numberOfTimesSparse*1.0))*1000.0 << ",";
    do
    {
        int ii=0;
        setTimeInMilli(start);
        for(;ii<numberOfTimesGMP;ii++)
            (*pt2GMPFunc)(num1,num2,num3);
        setTimeInMilli(stop);
        resultGMP = stop - start;
        numberOfTimesGMP*=2;
    }
    while(resultGMP<250);
    cout << (resultGMP/(numberOfTimesGMP*1.0))*1000.0;
}

void runTestPowMod(vector<INDEXTYPE> bits1,vector<INDEXTYPE> bits2,vector<INDEXTYPE> bits3)
{
    SparseInt<DIFFTYPE,INDEXTYPE> si1;
    SparseInt<DIFFTYPE,INDEXTYPE> si2;     
    SparseInt<DIFFTYPE,INDEXTYPE> si3;     
    SparseInt<DIFFTYPE,INDEXTYPE> si4;     
    si1.addListOfPostions(bits1); 
    si2.addListOfPostions(bits2);
    si3.addListOfPostions(bits3);
    mpz_class num1, num2, num3,num4;

    num1 = makeMpzClassNum(bits1);
    num2 = makeMpzClassNum(bits2);
    num3 = makeMpzClassNum(bits2);

    long double start = 0;
    long double stop = 0;
    long double resultSparse = 0;
    long double resultGMP = 0;
    int numberOfTimesSparse = 1;
    int numberOfTimesGMP = 1;
    do
    {
        int ii=0;
        setTimeInMilli(start);
        for(;ii<numberOfTimesSparse;ii++)
            si1.powMod(si4,si2,si3);
        setTimeInMilli(stop);
        resultSparse = stop - start;
        numberOfTimesSparse*=2;
    }
    while(resultSparse<250);
    cout << "," << (1000 * (numberOfTimesSparse*1.0)/resultSparse) << ",";
    do
    {
        int ii=0;
        setTimeInMilli(start);
        for(;ii<numberOfTimesGMP;ii++)
            mpz_powm (num4.get_mpz_t(),num1.get_mpz_t(), num2.get_mpz_t(),num3.get_mpz_t());
        setTimeInMilli(stop);
        resultGMP = stop - start;
        numberOfTimesGMP*=2;
    }
    while(resultGMP<250);
    cout << (1000.0*(numberOfTimesGMP*1.0)/resultGMP);

}

// sparse functions    
void sparsePlus     (SparseInt<DIFFTYPE,INDEXTYPE> a, SparseInt<DIFFTYPE,INDEXTYPE> b, SparseInt<DIFFTYPE,INDEXTYPE> &out) { /*return a+b;*/ }
void sparseMinus    (SparseInt<DIFFTYPE,INDEXTYPE> a, SparseInt<DIFFTYPE,INDEXTYPE> b, SparseInt<DIFFTYPE,INDEXTYPE> &out) { /*return a-b;*/ }
void sparseMultiply (SparseInt<DIFFTYPE,INDEXTYPE> a, SparseInt<DIFFTYPE,INDEXTYPE> b, SparseInt<DIFFTYPE,INDEXTYPE> &out) { /*return a*b;*/ }
void sparseDivide   (SparseInt<DIFFTYPE,INDEXTYPE> a, SparseInt<DIFFTYPE,INDEXTYPE> b, SparseInt<DIFFTYPE,INDEXTYPE> &out) { /*return a/b;*/ }
void sparseMod      (SparseInt<DIFFTYPE,INDEXTYPE> a, SparseInt<DIFFTYPE,INDEXTYPE> b, SparseInt<DIFFTYPE,INDEXTYPE> &out) { usleep(250000); }
// gmp functions
void gmpPlus     (mpz_t a, mpz_t b, mpz_t &out) { /*return a+b;*/ }
void gmpMinus    (mpz_t a, mpz_t b, mpz_t &out) { /*return a-b;*/ }
void gmpMultiply (mpz_t a, mpz_t b, mpz_t &out) { /*return a*b;*/ }
void gmpDivide   (mpz_t a, mpz_t b, mpz_t &out) { /*return a/b;*/ }
void gmpMod      (mpz_t a, mpz_t b, mpz_t &out) { usleep(250000); }

vector<INDEXTYPE> makeBits(INDEXTYPE maxBit, INDEXTYPE numberOfBits)
{
    vector<INDEXTYPE> out;
    INDEXTYPE r = 0;
    for(INDEXTYPE ii =0; ii< numberOfBits; ii++)
    {
        do
        {
            r = rand() % (maxBit+1); // a integer 0 to maxBit in size
        }
        while( contains(out,r));
        bool found = false;
        for(INDEXTYPE ii=0; ii<out.size();ii++)
        {
            if(r<out[ii])
            {
                found = true;
                out.insert(out.begin()+ii,r);
            }
        }
        if(!found)
            out.push_back(r);
    }   
    return out;
}



int main(int argc, char *argv[])
{
    srand(time(0));  // Initialize random number generator.
    /*vector<INDEXTYPE> testArray = makeBitsSmart(15,10);
      for(int ii =0; ii<testArray.size(); ii++)
      cout << testArray[ii] << " ";
      cout << "\n";
      mpz_class a = makeMpzClassNum(testArray);
      cout << a << endl;
      SparseInt<DIFFTYPE,INDEXTYPE> si;
      si.addListOfPostions(testArray);
      cout << si.toInt() << endl;
      return 0;*/

    if(argc != 5)
    {
        cout << "./timeTest number_of_bits_resolution hightest_bit_resolution number_of_tests_per_run operand_to_test\n";
        return 0;
    }
    int bitRes = atoi(argv[1]);
    if(bitRes<=0)
    {
        cout << "Need a bit resolution that is an integer greater than zero";
        return 0;
    }
    int sizeRes = atoi(argv[2]);
    if(sizeRes<=0)
    {
        cout << "Need a size resolution that is an integer greater than zero";
        return 0;
    }
    int numberOfRuns = atoi(argv[3]);
    if(sizeRes<=0)
    {
        cout << "Need a number of runs per test is an integer greater than zero";
        return 0;
    }
    string opStr (argv[4]);
    // void (*sparseMath)(SparseInt<DIFFTYPE,INDEXTYPE>, SparseInt<DIFFTYPE,INDEXTYPE>, SparseInt<DIFFTYPE,INDEXTYPE>&);
    // void (*gmpMath)(mpz_t,mpz_t,mpz_t&);

    // sparseOperator spfun;
    // gmpOperator gmpfun;
    cout << "# Running tests on operation: " << opStr << "\n";
    cout << "# Results are in this format:\n";
    cout << "#<highest bit>,<number of bits>,<number of operations per second for sparse Math>,<number of operations per second for GMP Math>\n";
    INDEXTYPE maxNumberOfBits = 1;
    INDEXTYPE maxSizeOfBit = 0;
    INDEXTYPE lastMaxSizeOfBit = 0;
    INDEXTYPE lastMaxNumberOfBits = 0;
    INDEXTYPE numberOfBits =0;
    while(true)
    {
        for(INDEXTYPE ii=lastMaxSizeOfBit; ii < maxSizeOfBit; ii+=sizeRes)
        {
            for(INDEXTYPE jj =0; jj <= ii && jj <maxNumberOfBits; jj+=bitRes)
            {
                for(INDEXTYPE kk=0; kk<numberOfRuns; kk++)
                {
                    if(jj==0)
                        numberOfBits = jj + 1;
                    else
                        numberOfBits = jj;
                    vector<INDEXTYPE> number1 = makeBitsSmart(ii, numberOfBits);
                    vector<INDEXTYPE> number2 = makeBitsSmart(ii, numberOfBits);
                    cout << ii << "," << numberOfBits;
                    if (opStr.compare("add") == 0)
                        runTestImproved(number1,number2,addSparse(), addGMP());
                    else if(opStr.compare("sub") == 0)
                        runTestImproved(number1,number2,subSparse(), subGMP());
                    else if (opStr.compare("mult") == 0)
                        runTestImproved(number1,number2,multSparse(), multGMP());
                    else if(opStr.compare("div") == 0)
                    {
                        number2 = makeBitsSmart(ii, numberOfBits/2); 
                        runTestImproved(number1,number2,modSparse(), modGMP());
                    }
                    else if(opStr.compare("mod") == 0)
                    {
                        number2 = makeBitsSmart(ii, numberOfBits/2);
                        runTestImproved(number1,number2,modSparse(), modGMP());
                    }
                    else if(opStr.compare("powMod") == 0)
                    {
                        vector<INDEXTYPE> number3 = makeBitsSmart(ii, numberOfBits);
                        runTestPowMod(number1,number2,number3);
                    }
                    else
                    {
                        cout << "\"" << opStr << "\" is an invalid op string.\n";
                        return 0;
                    }
                    cout << endl;
                }
            }
        }
        lastMaxSizeOfBit  = maxSizeOfBit;
        lastMaxNumberOfBits = maxNumberOfBits;
        maxNumberOfBits  += bitRes;
        for(INDEXTYPE ii=0; ii < lastMaxSizeOfBit; ii+=sizeRes)
            for(INDEXTYPE jj = lastMaxNumberOfBits; jj<=ii && jj <maxNumberOfBits; jj+=bitRes)
            {
                for(INDEXTYPE kk=0; kk<numberOfRuns; kk++)
                {
                    vector<INDEXTYPE> number1 = makeBitsSmart(ii, numberOfBits);
                    vector<INDEXTYPE> number2 = makeBitsSmart(ii, numberOfBits);
                    cout << ii << "," << numberOfBits;
                    if (opStr.compare("add") == 0)
                        runTestImproved(number1,number2,addSparse(), addGMP());
                    else if(opStr.compare("sub") == 0)
                        runTestImproved(number1,number2,subSparse(), subGMP());
                    else if (opStr.compare("mult") == 0)
                        runTestImproved(number1,number2,multSparse(), multGMP());
                    else if(opStr.compare("div") == 0)
                    {
                        number2 = makeBitsSmart(ii, numberOfBits/2); 
                        runTestImproved(number1,number2,modSparse(), modGMP());
                    }
                    else if(opStr.compare("mod") == 0)
                    {
                        number2 = makeBitsSmart(ii, numberOfBits/2);
                        runTestImproved(number1,number2,modSparse(), modGMP());
                    }
                    else if(opStr.compare("powMod") == 0)
                    {
                        vector<INDEXTYPE> number3 = makeBitsSmart(ii, numberOfBits);
                        runTestPowMod(number1,number2,number3);
                    }
                    else
                    {
                        cout << "\"" << opStr << "\" is an invalid op string.\n";
                        return 0;
                    }
                    cout << "\n";
                }
            }

        maxNumberOfBits  += bitRes;
        maxSizeOfBit     += sizeRes;
    }
}
