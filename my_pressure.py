def pressure(n_atoms, n_coll, delta_t):
    # only when m = \sigma = \beta = \gamma(n_atoms) = 1.0
    # const_var is a static variable
    if "const_var" not in pressure.__dict__:
        from numpy import sqrt, pi
        pressure.const_var = sqrt(pi) / 3
    return 1.0 + pressure.const_var * n_coll / (n_atoms * delta_t)
