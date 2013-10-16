from matplotlib import pyplot as plt
from scipy.sparse import csr_matrix
from scipy.special import gammaln
import numpy as np

def my_means_std(args):
    N = len(args)
    if N <= 1:
        return 0.0
    return np.std(args) / np.sqrt(N)

def my_gamma_factor(N):
        return np.exp(gammaln((3*(N-1)+1)/2.) - gammaln(3*(N-1)/2.) - 0.5*np.log(3*N/2.))

def my_pressure(n_atoms, n_coll, delta_t):
    # only when m = \sigma = \beta = 1.0
    return 1.0 + my_gamma_factor(n_atoms)*sqrt(pi)*n_coll / (3.*n_atoms*delta_t)

def xml_get_float(parsed_xml, param_tuple):
    return float(parsed_xml.getElementsByTagName(
        param_tuple[0])[0].attributes[param_tuple[1]].value)

def nufd(x):
    # D f = f'
    n = len(x)
    h = x[1:]-x[:n-1]
    a0 = -(2*h[0]+h[1])/(h[0]*(h[0]+h[1]))
    ak = -h[1:]/(h[:n-2]*(h[:n-2]+h[1:]))
    an = h[-1]/(h[-2]*(h[-1]+h[-2]))
    b0 = (h[0]+h[1])/(h[0]*h[1]) 
    bk = (h[1:] - h[:n-2])/(h[:n-2]*h[1:])
    bn = -(h[-1]+h[-2])/(h[-1]*h[-2])
    c0 = -h[0]/(h[1]*(h[0]+h[1]))
    ck = h[:n-2]/(h[1:]*(h[:n-2]+h[1:]))
    cn = (2*h[-1]+h[-2])/(h[-1]*(h[-2]+h[-1]))
    val = np.hstack((a0,ak,an,b0,bk,bn,c0,ck,cn))
    row = np.tile(np.arange(n),3)
    dex = np.hstack((0,np.arange(n-2),n-3))
    col = np.hstack((dex,dex+1,dex+2))
    D = csr_matrix((val,(row,col)),shape=(n,n))
    return D

def uderivative_simple(x0, y0):
    x1 = 0.5 * (x0[:-1] + x0[1:])
    y1 = np.diff(y0) / np.diff(x0)
    return x1, y1

def uderivative_oh4(x0, y0):
    assert(len(x0) > 4)
    x1 = x0[2:-2]
    y1 = [ -y0[i+2] + 8*y0[i+1] - 8*y0[i-1] + y0[i-2]
            for i in range(2, len(y0)-2) ] / (12*np.diff(x0[2:-1]))
    return x1, y1

def uderivative_2_oh4(x0, y0):
    assert(len(x0) > 4)
    x1 = x0[2:-2]
    y1 = [ -y0[i+2] + 16*y0[i+1] - 30*y0[i] + 16*y0[i-1] - y0[i-2]
            for i in range(2, len(y0)-2) ] / (12*np.diff(x0[2:-1])**2)
    return x1, y1

def uplot(x, y, derivative=0, fmt='.-'):
    for i in range(derivative):
        x, y = uderivative(x, y)
    yn = [ i.n for i in y ]
    ys = [ i.s for i in y ]
    plt.errorbar(x, yn, fmt=fmt, yerr=ys)
