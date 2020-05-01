import time

def dotest(func):
    """returns the number of ops in a sec"""
    def timeit(n):
        start = time.clock()
        x = 1
        for i in xrange(n):
            x = func() ^ x
        return time.clock() - start

    numtrials = 1
    while timeit(numtrials) < .5:
        numtrials *= 2

    results = [timeit(numtrials) for i in xrange(3)]
    results.sort()
    return round(numtrials/results[1],2)
