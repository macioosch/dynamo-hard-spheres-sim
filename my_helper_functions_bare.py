# encoding=utf-8
from __future__ import division
from math import ceil, exp, floor, log, log10, pi, sqrt

def uncertain_number_string(number, error):
    if error == 0:
        return str(number)
    precision = int(1 - floor(log10(error)))
    uncertainty = int(ceil(error / 10**(floor(log10(error)) - 1)))
    if precision > 1:
        return "{:.{:.0f}f}({:.0f})".format(number, precision, uncertainty)
    else:
        return "{:.1f}({:.1f})".format(number, error)

def xml_get_float(parsed_xml, param_tuple):
    return float(parsed_xml.getElementsByTagName(
        param_tuple[0])[0].attributes[param_tuple[1]].value)

def my_linspace(x0, x1, xc):
    if x0 == x1 or xc <= 1:
        return [ (x0+x1)/2.0 ]
    else:
        return [ x0 + (x1-x0) * i/(xc-1) for i in xrange(xc) ]

def my_log_linspace(x0, x1, xc):
    return [ x0 * (x1/x0)**(i/(xc-1)) for i in xrange(xc) ]

def my_mean(args):
    return sum(args)/len(args)

def my_means_std(args):
    N = len(args)
    if N <= 1:
        return 0.0
    mean_value = my_mean(args)
    sum_squares = sum([ (x - mean_value)**2.0 for x in args ])
    return sqrt(sum_squares / (N*(N-1.0)))

def my_std(args):
    N = len(args)
    if N <= 1:
        return 0.0
    mean_value = my_mean(args)
    sum_squares = sum([ (x - mean_value)**2.0 for x in args ])
    return sqrt(sum_squares / (N-1.0))

def my_gammaln(x):
    # Gergő Nemes, 2007
    return 0.5*(log(2*pi)-log(x)) + x*(log(x+1./(12*x-0.1/x))-1)

def my_gamma_factor(N):
    return exp(my_gammaln((3*(N-1)+1)/2.) - my_gammaln(3*(N-1)/2.) - 0.5*log(3*N/2.))

def my_pressure(n_atoms, n_coll, delta_t):
    # only when m = \sigma = \beta = 1.0
    return 1.0 + my_gamma_factor(n_atoms)*sqrt(pi)*n_coll / (3.*n_atoms*delta_t)
