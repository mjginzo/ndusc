# -*- coding: utf-8 -*-
"""Functions to compute new cuts in the nested decomposition method.

Todo: Could be tree methods?
"""


# compute_feas_cut ------------------------------------------------------------
def compute_feas_cut(vars, dual, cons):
    """Compute feasibility cuts parameters.

    Args:
        vars (:obj:`dict`): variables to get information.
        dual (:obj:`dict`): dual variables information.
        cons (:obj:`dict`): constraints information.

    Return:
        :obj:`dict`: feasibility cut parameters.

    Example:
        >>> import ndusc.cut.cut_functions as cf
        >>> vars = {'y': [1]}
        >>> dual = {2: {'lp': {2: 0.0}, 'td': {2: 1.0}}}
        >>> cons = {2: {'A': {'w': {2: [{'coef': 1, 'ndx': 2, 'var': 'td'}]},
                              'x': {2: [{'coef': 1, 'ndx': 2, 'var': 'lp'},
                                        {'coef': 1, 'ndx': 2, 'var': 'td'}]},
                              'y': {1: [{'coef': 1, 'ndx': 2, 'var': 'td'}],
                                    2: [{'coef': -1, 'ndx': 2, 'var': 'td'}]}},
                        'rhs': {('lp', 2): 2.0, ('td', 2): 1.0}}}
        >>> cf.compute_feas_cut(vars, dual, cons)
            [{'D': {'y': {1: 1.0}}, 'd': 1.0}]
    """
    feas_cuts = []
    for n in dual.keys():
        n_d = dual[n]
        n_c = cons[n]
        A = n_c['A']
        rhs = n_c['rhs']

        D = {v: {i: sum([c['coef']*n_d[c['var']][c['ndx']] for c in A[v][i]])}
             for v in vars for i in vars[v]}
        d = sum([rhs[(c, i)]*n_d[c][i] for c in n_d.keys()
                 for i in n_d[c].keys()])
        feas_cuts += [{'A': D, 'rhs': d}]
    return feas_cuts
# --------------------------------------------------------------------------- #


# compute_opt_cut -------------------------------------------------------------
def compute_opt_cut(vars, dual, cons, probs):
    """Compute optimality cuts parameters.

    Args:
        vars (:obj:`dict`): variables to get information.
        dual (:obj:`dict`): dual variables information.
        cons (:obj:`dict`): constraints information.
        probs (:obj:`dict`): nodes probability.

    Return:
        :obj:`dict`: optimality cut parameters.

    Example:
        >>> import ndusc.cut.cut_functions as cf
        >>> vars = {'y': [1]}
        >>> dual = {2: {'lp': {2: 0.0}, 'td': {2: 1.0}},
                    3: {'lp': {2: -2.0}, 'td': {2: 3.0}}}
        >>> cons = {2: {'A': {'w': {2: [{'coef': 1, 'ndx': 2, 'var': 'td'}]},
                              'x': {2: [{'coef': 1, 'ndx': 2, 'var': 'lp'},
                                        {'coef': 1, 'ndx': 2, 'var': 'td'}]},
                              'y': {1: [{'coef': 1, 'ndx': 2, 'var': 'td'}],
                                    2: [{'coef': -1, 'ndx': 2, 'var': 'td'}]}},
                        'rhs': {('lp', 2): 2.0, ('td', 2): 1.0}},
                    3: {'A': {'w': {2: [{'coef': 1, 'ndx': 2, 'var': 'td'}]},
                              'x': {2: [{'coef': 1, 'ndx': 2, 'var': 'lp'},
                                        {'coef': 1, 'ndx': 2, 'var': 'td'}]},
                              'y': {1: [{'coef': 1, 'ndx': 2, 'var': 'td'}],
                                    2: [{'coef': -1, 'ndx': 2, 'var': 'td'}]}},
                        'rhs': {('lp', 2): 2.0, ('td', 2): 3.0}}}
        >>> probs = {2: 0.5, 3: 0.5}
        >>> cf.compute_opt_cut(vars, dual, cons, probs)
            [{'E': {'y': {1: 2.0}}, 'e': 3.0}]
    """
    total_prob = sum([probs[k] for k in probs.keys()])

    e = 0
    E = {}

    it = 0
    for n in dual.keys():
        it += 1
        n_d = dual[n]
        n_c = cons[n]
        A = n_c['A']
        rhs = n_c['rhs']

        for v in vars:
            if it == 1:
                E[v] = {}
            for i in vars[v]:
                if it == 1:
                    E[v][i] = 0

                E[v][i] += probs[n]/total_prob *\
                    sum([c['coef']*n_d[c['var']][c['ndx']] for c in A[v][i]])

        e += probs[n]/total_prob*sum([rhs[(c, i)]*n_d[c][i]
                                     for c in n_d.keys()
                                     for i in n_d[c].keys()])

    return [{'A': E, 'rhs': e}]
# --------------------------------------------------------------------------- #


# compute_bin_feas_cut --------------------------------------------------------
def compute_bin_feas_cut(vars, vars_val):
    """Compute binary feasibility cuts parameters.

    Args:
        vars (:obj:`dict`): variables to get information.
        vars_vale (:obj:`dict`): variables information.


    Example:
        >>> import ndusc.cut.cut_functions as cf
        >>> vars = {'y': [1]}
        >>> vars_val = {'w': {2: 1.0}, 'x': {2: 2.0}, 'y': {1: 0.0, 2: 0.0}}
        >>> cf.compute_bin_feas_cut(vars, vars_val)
            [{'G': {'y': {1: 1}}, 'g': 1.0}]
    """
    G = {v: {i: -1 if vars_val[v][i] == 1 else 1}
         for v in vars for i in vars[v]}
    g = 1 - sum([vars_val[v][i] for v in vars for i in vars[v]])
    return [{'A': G, 'rhs': g}]
# --------------------------------------------------------------------------- #


# compute_bin_opt_cut --------------------------------------------------------
def compute_bin_opt_cut(vars, vars_val, EV, L):
    """Compute binary feasibility cuts parameters.

    Args:
        vars (:obj:`dict`): variables to get information.
        vars_vale (:obj:`dict`): variables information.
        EV (:obj:`float`): expected value of the selected nodes.
        L (:obj:`float`): lower bound for the expected value. It may obtained
            by solving the relaxed integer problem.


    Example:
        >>> import ndusc.cut.cut_functions as cf
        >>> vars = {'y': [1]}
        >>> vars_val = {'w': {2: 1.0}, 'x': {2: 2.0}, 'y': {1: 0.0, 2: 0.0}}
        >>> EV = 1000.0
        >>> L = 500.0
        >>> cf.compute_bin_opt_cut(vars, vars_val, EV, L)
            [{'F': {'y': {1: 500.0}}, 'f': 1000.0}]
    """
    F = {v: {i: L-EV if vars_val[v][i] == 1 else EV-L}
         for v in vars for i in vars[v]}
    f = (L-EV)*(sum([vars_val[v][i] for v in vars for i in vars[v]]) - 1) + L
    return [{'A': F, 'rhs': f}]
# --------------------------------------------------------------------------- #
