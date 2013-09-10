from __future__ import division
from math import pi, sqrt

def my_linspace(x0, x1, xc):
    return [ x0 + (x1-x0) * i/(xc-1) for i in xrange(xc) ]

def my_log_linspace(x0, x1, xc):
    return [ x0 * (x1/x0)**(i/(xc-1)) for i in xrange(xc) ]

def my_mean(*args):
    return sum(args)/len(args)

def my_means_std(*args):
    N = len(args)
    mean_value = my_mean(args)
    sum_squares = sum([ (x - mean_value)**2.0 for x in args ])
    return sqrt(sum_squares / (N*(N-1.0)))

def my_pressure(n_atoms, n_coll, delta_t):
    # only when m = \sigma = \beta = \gamma(n_atoms) = 1.0
    # const_var is a static variable
    if "const_var" not in my_pressure.__dict__:
        my_pressure.const_var = sqrt(pi) / 3.
    return 1.0 + my_pressure.const_var * n_coll / (n_atoms * delta_t)
