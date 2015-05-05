#! /usr/bin/env python

import sys
import collections
import util 


def random_search(domain, fitness, iterations):
    best_candidate = util.random_solution(domain)
    best_fitness = fitness(best_candidate)

    print "initial fitness: %0.2f" % (best_fitness)

    for i in xrange(iterations):
        if best_fitness == 0:
            break

        candidate = util.random_solution(domain)
        f = fitness(candidate)

        if f < best_fitness:
            best_fitness = f
            best_candidate = candidate
            print "new best fitness found: %0.2f" % (best_fitness)

    return best_candidate
