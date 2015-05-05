#! /usr/bin/env python

import sys
import collections
import optimize
import optimize.util

def make_aggregates(t, ignores, weights=None):
    aggs = collections.defaultdict(int)
    if not weights:
        weights = [1 for r in t]

    for (row, weight) in zip(t, weights):
        aggs['total'] += weight
        for i in range(len(row)):
            if i in ignores:
                continue
            key = "col_%s_%s" % (i, row[i])
            aggs["col_%s_%s" % (i, row[i])] += weight

    return aggs
                                                        
def mean_square_error(t1,t2,n):
    keys = set(t1.keys() + t2.keys())
    error = 0.0
    for k in keys:
        error += (t1[k] - t2[k]) ** 2

    return error/n

def rmse(t1,t2,n):
    return mean_square_error(t1,t2,n) ** (0.5)
        
def fitness_closure(t1, t2, ignores):
    a1 = make_aggregates(t1, ignores)
    n = len(t2)
    def fit(weights):
        a2 = make_aggregates(t2, ignores, weights)
        return rmse(a1,a2,n)

    return fit

table = [line.strip().split('\t') for line in sys.stdin if line[0] != '#']

control = [r for r in table if r[1] == '1']
test = [r for r in table if r[1] != '1']

ignored_columns = (0,1)
fitness = fitness_closure(control, test, ignored_columns)

domain = [optimize.util.make_loguniform(3.0)]  * len(test)
#best = optimize.random_search(domain, fitness, 100000)
best = optimize.ga_search(domain, fitness, 500)

a1 = make_aggregates(control, ignored_columns)
a2 = make_aggregates(test, ignored_columns, best)

print "control"
print "\n".join( ["%s: %0.3f" % (k,a1[k]) for k in a1] )
print "test"
print "\n".join( ["%s: %0.3f" % (k,a2[k]) for k in a2] )

for (i,w) in zip(test,best):
   print "%s\t%s" % (i[0], w)
