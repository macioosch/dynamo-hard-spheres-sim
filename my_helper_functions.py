from matplotlib import pyplot as plt
from scipy.sparse import csr_matrix
import numpy as np

def my_pressure(n_atoms, n_coll, delta_t):
    # only when m = \sigma = \beta = \gamma(n_atoms) = 1.0
    # const_var is a static variable
    if "const_var" not in my_pressure.__dict__:
        my_pressure.const_var = np.sqrt(np.pi) / 3
    return 1.0 + my_pressure.const_var * n_coll / (n_atoms * delta_t)

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

def uderivative(x0, y0):
    x1 = 0.5 * (x0[:-1] + x0[1:])
    y1 = np.diff(y0) / np.diff(x0)
    return x1, y1

def uplot(x, y, derivative=0, fmt='.-'):
    for i in range(derivative):
        x, y = uderivative(x, y)
    yn = [ i.n for i in y ]
    ys = [ i.s for i in y ]
    plt.errorbar(x, yn, fmt=fmt, yerr=ys)
