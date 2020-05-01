#!/usr/bin/python3

from sys import argv
from re import match
from os.path import basename, splitext, exists
from os import system, remove

def usage(exitval=None):
    print("Usage: {} datafile".format(argv[0]))
    print("Filename must be like opXnumYhighZtest.")
    if exitval is not None:
        exit(exitval)

if __name__ == '__main__':
    if len(argv) != 2:
        usage(1)

    datafile = argv[1]
    fname = splitext(basename(datafile))[0]
    parsename = match('^(\w+)(\d+)num(\d+)high(\d+)test$', fname)
    if parsename is None:
        print('ERROR: file name "{}" not in correct format'.format(fname))
        usage(2)
    opname = parsename.group(1)
    xres = int(parsename.group(2))
    yres = int(parsename.group(3))

    outgp = fname + '.gnu'
    outdata = fname + '.data'
    outpng = fname + '.png'

    try:
        '''
        for f in outgp, outdata, outpng:
            if exists(f):
                ans = input('WARNING: {} already exists. Overwrite? '.format(f))
                if ans.lower() != 'y':
                    exit(4)
        '''

        print('Reading data from', datafile)
        rawdata = {}
        with open(datafile,'r') as filein:
            for line in filein:
                if line.startswith('#'):
                    continue
                lineparts = line.strip().split(',')
                x, y = (int(lineparts[i]) for i in range(2))
                sp, gmp = (float(lineparts[i]) for i in range(2,4))
                if (x,y) not in rawdata:
                    rawdata[(x,y)] = []
                rawdata[(x,y)].append((sp-gmp) / max(gmp,sp))

        data = {}
        for ((x,y),vals) in rawdata.items():
            data[x,y] = sum(vals)/len(vals)

        xvals = sorted(set(pos[0] for pos in data))
        yvals = sorted(set(pos[1] for pos in data))
        print('Writing sorted data to', outdata)
        with open(outdata,'w') as df:
            for x in xvals:
                for y in yvals:
                    print('{} {} {}'.format(x, y, data.get((x,y),0)),file=df)
                print(file=df)
        
        print('Writing gnuplot instructions to', outgp)
        with open(outgp,'w') as ogf:
            print(
                'set terminal png',
                "set title 'Timing data for {}".format(opname),
                "set cblabel 'Sparse Ints vs. GMP'",
                "unset cbtics",
                "set xlabel 'Highest set bit'",
                "set ylabel 'Number of set bits'",
                "set output '{}.png'".format(fname),
                "set palette defined (0 'red', .5 'gray', 1 'green')",
                "set cbrange [-1:1]",
                "set xrange [{}:{}]".format(xvals[0]-1,xvals[-1]+1), 
                "set yrange [{}:{}]".format(yvals[0]-1,yvals[-1]+1), 
                "plot '{}' using 1:2:3 with image".format(outdata),
                sep='\n', file=ogf
            )

        print('Running gnulot to create', outpng)
        system('gnuplot "{}"'.format(outgp))

        print('Cleaning up extra files')
        for f in outdata, outgp:
            remove(f)

    except IOError:
        print('ERROR: couldn\'t open "{}"'.format(datafile))
        usage(3)

