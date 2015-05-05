#! /usr/bin/env python

import random
import util 


def make_random_population(domain, fitness, n):
    pop = [util.random_solution(domain) for i in xrange(n)]
    return sorted([(i, fitness(i)) for i in pop], key=lambda a:a[1])

def select(population):
    sum_weights = sum([1.0/ind[1] for ind in population])

    pick = random.uniform(0, sum_weights)
    for ind in population:
        pick -= 1.0 / ind[1] 
        if pick <= 0:
            return ind[0]

def crossover(a, b):
    n = random.randrange(0,len(a))
    c = a[:n] + b[n:]
    d = b[:n] + a[n:]
    return c, d

def mutate(ind, domain, mr):
    return [i if random.random() > mr else f() for (i, f) in zip(ind, domain)]

def generation(domain, population, fitness, mr, elites):
    n = len(population)

    new_pop = population[:elites]

    while len(new_pop) < n:
        p1 = select(population)
        p2 = select(population)
        a,b = crossover(p1,p2)
        new_inds = [mutate(i, domain, mr) for i in (a, b)]
        new_pop += [(i,fitness(i)) for i in new_inds]

    return sorted(new_pop[:n], key=lambda a:a[1])

def ga_search(domain, fitness, iterations, n=500, mr=0.005, elites=1):
    population =  make_random_population(domain, fitness, n)
  
    for i in xrange(iterations):
        population = generation(domain, population, fitness, mr, elites)

        avg_fit = sum([ind[1] for ind in population]) / len(population)
        if i % 10 == 0:
            print "best,average fitness of generation %s: %0.4f, %0.4f" % (i, population[0][1], avg_fit)

        if population[0][1] < 0.005:
            break

    return population[0][0]
