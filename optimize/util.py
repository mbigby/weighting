#! /usr/bin/env python

import random


def make_uniform(lo, hi):
    def f():
        return random.uniform(lo, hi)
    return f


def make_loguniform(base):
    def f():
        return base ** random.uniform(-1,1)
    return f


def random_solution(domain):
     return [f() for f in domain]
