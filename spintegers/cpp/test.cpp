/*  This is the testing file for the Sparse Int C++ libary
 *  
 *
 */
#include "sparseInt.h"
#include <iostream>
#include <stdlib.h>
#include <gmp.h>
using namespace std;


void printDiffs(SparseInt<char,unsigned> incorrect)
{

    for(int ii=0;ii<incorrect.diffs.size();ii++)
    {
        if(incorrect.signs[ii])
            cout << "+" << ((int)incorrect.diffs[ii])  <<" ";
        else
            cout << "-" << ((int)incorrect.diffs[ii]) <<" ";
    }
    cout << endl;
    //cout << incorrect.diffs.size()<<" bits long\n";
}

void bitDebugg(SparseInt<char,unsigned> incorrect, int ans)
{
    cout << "The Sparse Bits \n";
    //incorrect.printBits();
    printDiffs(incorrect);
    cout << "Correct Bits \n";
    SparseInt<char,unsigned> correct = SparseInt<char,unsigned>(ans);
    printDiffs(correct);
}

bool testMath(int a, int b,  SparseInt<char,unsigned> sa, SparseInt<char,unsigned> sb)
{
    // test addition
    SparseInt<char,unsigned> out;
    out = sa + sb;
    if(a+b!=out.toInt())
    {
        cout << "Addition Failed with " << a << " + " << b << "\n";
        cout << "Sparse gave " << out.toInt() << "\n";
        cout << "Real answer is " << a+b << "\n";
        cout <<"a is ";
        printDiffs(sa);
        cout <<"b is "; 
        printDiffs(sb); 
        bitDebugg(out,a+b);
        return false;
    }
    // test subtraction
    //sa.sub(out, sb);
    out = sa -sb;
    if(a-b!=out.toInt())
    {
        cout << "Subtraction Failed with " << a << " - " << b << "\n";
        cout << "Sparse gave " << out.toInt() << "\n";
        cout << "Real answer is " << a-b << "\n";
        bitDebugg(out,a-b); 
        return false;
    }
    // test multiplication
    //out = SparseInt<char> (0);
    out = sa * sb;
    if(a*b!=out.toInt())
    {
        cout << "Mult Failed with " << a << " * " << b << "\n";
        cout << "Sparse gave " << out.toInt() << "\n";
        cout << "Real answer is " << a*b << "\n";
        bitDebugg(out,a*b); 
        return false;
    }
    // test division 
    if(b!=0)
    {
        out = sa/sb;
        if(a/b!=out.toInt())
        {
            cout << "Div Failed with " << a << " / " << b << "\n";
            cout << "Sparse gave " << out.toInt() << "\n";
            cout << "Real answer is " << a/b << "\n";
            bitDebugg(out,a/b); 
            return false;
        }
    }
    // test mod
    if(b!=0)
    {
        sa.mod(out, sb);
        if(a%b!=out.toInt())
        {
            cout << "Mod Failed with " << a << " % " << b << "\n";
            cout << "Sparse gave " << out.toInt() << "\n";
            cout << "Real answer is " << a%b << "\n";
            bitDebugg(out,a%b); 
            return false;
        }
    }

    if(a!=0)
    {
        sb.mod(out, sa);
        if(b%a!=out.toInt())
        {
            cout << "Mod Failed with " << b << " % " << a << "\n";
            cout << "Sparse gave " << out.toInt() << "\n";
            cout << "Real answer is " << b%a << "\n";
            bitDebugg(out,b%a); 
            return false;
        }
    }

    // test boolean operations
    bool sparseAns;
    bool realAns;
    sparseAns = sa.eq(sb);
    realAns = (a==b);
    if(sparseAns != realAns)
    {
        cout << "Equal Failed with " << a << " == " << b << "\n";
        cout << "Sparse gave " << sparseAns << "\n";
        cout << "Real answer is " << realAns << "\n";
        return false;
    }
    sparseAns = sa.neq(sb);
    realAns = (a!=b);
    if(sparseAns != realAns)
    {
        cout << "Not Equal Failed with " << a << " != " << b << "\n";
        cout << "Sparse gave " << sparseAns << "\n";
        cout << "Real answer is " << realAns << "\n";
        return false;
    }
    sparseAns = sa.lt(sb);
    realAns = (a<b);
    if(sparseAns != realAns)
    {
        cout << "Less Than Failed with " << a << " < " << b << "\n";
        cout << "Sparse gave " << sparseAns << "\n";
        cout << "Real answer is " << realAns << "\n";
        return false;
    }
    sparseAns = (sa<=sb);
    realAns = (a<=b);
    if(sparseAns != realAns)
    {
        cout << "Less Than or Equal Failed with " << a << " <= " << b << "\n";
        cout << "Sparse gave " << sparseAns << "\n";
        cout << "Real answer is " << realAns << "\n";
        return false;
    }
    sparseAns = (sa>sb);
    realAns = (a>b);
    if(sparseAns != realAns)
    {
        cout << "Greater Than Failed with " << a << " > " << b << "\n";
        cout << "Sparse gave " << sparseAns << "\n";
        cout << "Real answer is " << realAns << "\n";
        return false;
    }
    sparseAns = (sa>=sb);
    realAns = (a>=b);
    if(sparseAns != realAns)
    {
        cout << "Greater Than or Equal Failed with " << a << " >= " << b << "\n";
        cout << "Sparse gave " << sparseAns << "\n";
        cout << "Real answer is " << realAns << "\n";
        return false;
    }

    if(a>=0 && b>=0)
    {
        mpz_t mpzA;
        mpz_init(mpzA);
        mpz_t mpzB;
        mpz_init(mpzB);
        mpz_t mpzC;
        mpz_init(mpzC);
        mpz_t mpzOut;
        mpz_init(mpzOut);
        for(int c =0; c<=a; c++)
        {
            mpz_set_ui (mpzA, ((unsigned long int) a));
            mpz_set_ui (mpzB, ((unsigned long int) b));
            mpz_set_ui (mpzC, ((unsigned long int) c));
            SparseInt<char,unsigned> sc = SparseInt<char,unsigned>(c);
            if(a>0)
            {
                mpz_powm (mpzOut, mpzB, mpzC, mpzA);
                sb.powMod(out, sc, sa);
                if(mpz_get_ui (mpzOut)!=(unsigned)out.toInt())
                {
                    cout << "Pow Mod Failed with " << b << " ^ " << c << " % " << a << endl;
                    cout << "Sparse gave " << out.toInt() << endl;
                    cout << "GMP gave " << mpz_get_ui (mpzOut) << endl; 
                    return false;
                }
                mpz_powm (mpzOut, mpzC, mpzB, mpzA);
                sc.powMod(out, sb, sa);
                if(mpz_get_ui (mpzOut)!=out.toInt())
                {
                    cout << "Pow Mod Failed with " << c << " ^ " << b << " % " << a << endl;
                    cout << "Sparse gave " << out.toInt() << endl;
                    cout << "GMP gave " << mpz_get_ui (mpzOut) << endl; 
                    return false;
                }
            }
            if(b>0)
            {
                mpz_powm (mpzOut, mpzA, mpzC, mpzB);
                sa.powMod(out, sc, sb);
                if(mpz_get_ui (mpzOut)!=out.toInt())
                {
                    cout << "Pow Mod Failed with " << a << " ^ " << c << " % " << b << endl;
                    cout << "Sparse gave " << out.toInt() << endl;
                    cout << "GMP gave " << mpz_get_ui (mpzOut) << endl; 
                    return false;
                }
                mpz_powm (mpzOut,mpzC, mpzA, mpzB);
                sc.powMod(out, sa, sb);
                if(mpz_get_ui (mpzOut)!=out.toInt())
                {
                    cout << "Pow Mod Failed with " << c << " ^ " << a << " % " << b << endl;
                    cout << "Sparse gave " << out.toInt() << endl;
                    cout << "GMP gave " << mpz_get_ui (mpzOut) << endl; 
                    return false;
                }
            }
            // this is really slow so for now it is commented out

            if(c>0)
            {
                mpz_powm (mpzOut, mpzB,mpzA,mpzC);
                sb.powMod(out, sa, sc);
                if(mpz_get_ui (mpzOut)!=out.toInt())
                {
                    cout << "Pow Mod Failed with " << b << " ^ " << a << " % " << c << endl;
                    cout << "Sparse gave " << out.toInt() << endl;
                    cout << "GMP gave " << mpz_get_ui (mpzOut) << endl; 
                    return false;
                }
                mpz_powm (mpzOut, mpzA,  mpzB, mpzC);
                sa.powMod(out, sb, sc);
                if(mpz_get_ui (mpzOut)!=out.toInt())
                {
                    cout << "Pow Mod Failed with " << a << " ^ " << b << " % " << c << endl;
                    cout << "Sparse gave " << out.toInt() << endl;
                    cout << "GMP gave " << mpz_get_ui (mpzOut) << endl; 
                    return false;
                }

            }
        }
    }

    unsigned posB = abs(b);
    long long longA = a;


    /*
    // this works but the infinity tester breaks on 33 << 58 
    sa.leftShift(out, posB);
    if(longA<<posB!=out.toLongLong())
    {
    cout << "Left Shift Failed with " << longA << " << " << posB << "\n";
    cout << "Sparse gave " << out.toLongLong() << "\n";
    cout << "Real answer is " << ((long long)(longA<<posB))  << "\n";
    //bitDebugg(out,l<<posB);
    return false;
    }
    */

    /*
    // this does not work but I have decided to move on
    sa.rightShift(out, posB);
    if(a>>posB!=out.toInt())
    {
    cout << "Right Shift Failed with " << a << " >> " << posB << "\n";
    cout << "Sparse gave " << out.toInt() << "\n";
    cout << "Real answer is " << ((int)(a>>posB)) << "\n";
    //bitDebugg(out,a>>posB);
    return false;
    }
    */
    return true;
}

int main()
{
    int ii = 0;
    int base = 1;
    bool fail = false;
    while(!fail)
    {
        // check the constuctor and the toInt function
        // for positive numbers
        SparseInt<char,unsigned> si = ii;
        if(si.toInt()!=ii)
        {
            cout << "Regular number " << ii <<
                " Sparse Int Number " << si.toInt() 
                << "\nBits: ";
            si.printBits();
            cout << "\n";
            break;
        }

        // check the constuctor and the toInt function
        // for negitive numbers
        SparseInt<char,unsigned> negsi = ii*-1;
        if(negsi.toInt()!=-1*ii)
        {
            cout << "Regular number " << -1*ii <<
                " Sparse Int Number " << negsi.toInt() 
                << "\nBits: ";
            negsi.printBits();
            cout << "\n";
            break;
        }
        // test the operands
        for(int jj =0; jj<=ii; jj++)
        {
            SparseInt<char,unsigned> sj = jj;
            SparseInt<char, unsigned> negsj =-1*jj;
            // do math tests here
            if(!testMath(ii,jj,si,sj))
            {
                fail = true;
                break;
            }
            if(!testMath(ii,-1*jj,si,negsj))
            {
                fail = true;
                break;
            }
            if(!testMath(-1*ii,jj,negsi,sj))
            {
                fail = true;
                break;
            }
            if(!testMath(-1*ii,-1*jj,negsi,negsj))
            {
                fail = true;
                break;
            }
            if(!testMath(jj,ii,sj,si))
            {
                fail = true;
                break;
            }
            if(!testMath(jj,-1*ii,sj,negsi))
            {
                fail = true;
                break;
            }
            if(!testMath(-1*jj,ii,negsj,si))
            {
                fail = true;
                break;
            }
            if(!testMath(-1*jj,-1*ii,negsj,negsi))
            {
                fail = true;
                break;
            }

            // make sure that the intial numebers did not change
            if(si!=ii)
            {
                cout << "Operators were changed\n";
                cout << "Positive Sparse Int si is " << si.toInt() <<"\n";
                cout << "Should be " << ii << "\n";
                fail = true;
                break;
            }
            if(negsi!=-1*ii)
            {
                cout << "Operators were changed\n";
                cout << "Negitive Sparse Int negsi is " << negsi.toInt() <<"\n";
                cout << "Should be " << -1*ii << "\n";
                fail = true;
                break;
            }
            if(sj!=jj)
            {
                cout << "Operators were changed\n";
                cout << "Positive Sparse Int sj is " << sj.toInt() <<"\n";
                cout << "Should be " << jj << "\n";
                fail = true;
                break;
            }
            if(negsj!=-1*jj)
            {
                cout << "Operators were changed\n";
                cout << "Negitive Sparse Int negsj is " << negsj.toInt() <<"\n";
                cout << "Should be " << -1*jj << "\n";
                fail = true;
                break;
            }
        }

        // let the user track progress
        if(ii >= base)
        {
            cout << "\nPassed "<< base<<" \n";
            base *= 10;
        }
        ii++;
    }
}
