# -*- coding: utf-8 -*-
"""Functions to compute new cuts in the nested decomposition method.

Todo: Create cut functions.
Todo: Could be tree methods?
"""


# compute_feas_cut ------------------------------------------------------------
def compute_feas_cut(dual, cons):
    """Compute feasibility cuts parameters.

    Args:
        dual (:obj:`dict`): dual variables information.
        cons (:obj:`dict`): constraints information.

    Return:
        :obj:`dict`: feasibility cut parameters.

    Example:
        >>> import ndusc.cut.cut_functions as cf
        >>> dual = {1: {'lp': {2: 0.0}, 'td': {2: 1.0}}}
        >>> cons = {1: {'A': {'w': {2: [{'coef': 1, 'ndx': 2, 'var': 'td'}]},
                              'x': {2: [{'coef': 1, 'ndx': 2, 'var': 'lp'},
                                        {'coef': 1, 'ndx': 2, 'var': 'td'}]},
                              'y': {1: [{'coef': 1, 'ndx': 2, 'var': 'td'}],
                                    2: [{'coef': -1, 'ndx': 2, 'var': 'td'}]}},
                        'rhs': {('lp', 2): 2.0, ('td', 2): 1.0}}}
        >>> cf.compute_feas_cut(dual, cons)
            [{'D': {'w': {2: 1.0}, 'x': {2: 1.0}, 'y': {2: -1.0}}, 'd': 1.0}]
    """
    feas_cuts = []
    for n in dual.keys():
        n_d = dual[n]
        n_c = cons[n]
        A = n_c['A']
        rhs = n_c['rhs']

        D = {k: {i: sum([c['coef']*n_d[c['var']][c['ndx']] for c in A[k][i]])}
             for k in A.keys() for i in A[k].keys()}
        d = sum([rhs[(c, i)]*n_d[c][i] for c in n_d.keys()
                 for i in n_d[c].keys()])
        feas_cuts += [{'D': D, 'd': d}]
    return feas_cuts
# --------------------------------------------------------------------------- #


# compute_opt_cut -------------------------------------------------------------
def compute_opt_cut(dual, cons, probs):
    """Compute optimality cuts parameters.

    Args:
        dual (:obj:`dict`): dual variables information.
        cons (:obj:`dict`): constraints information.
        probs (:obj:`dict`): nodes probability.

    Return:
        :obj:`dict`: optimality cut parameters.

    Example:
        >>> import ndusc.cut.cut_functions as cf
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
        >>> cf.compute_opt_cut(dual, cons, probs)
            [{'D': {'w': {2: 1.0}, 'x': {2: 1.0}, 'y': {2: -1.0}}, 'd': 1.0}]
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

        for k in A.keys():
            if it == 1:
                E[k] = {}
            for i in A[k].keys():
                if it == 1:
                    E[k][i] = 0

                E[k][i] += probs[n]/total_prob *\
                    sum([c['coef']*n_d[c['var']][c['ndx']] for c in A[k][i]])

        e += probs[n]/total_prob*sum([rhs[(c, i)]*n_d[c][i]
                                     for c in n_d.keys()
                                     for i in n_d[c].keys()])

    return [{'E': E, 'e': e}]
# --------------------------------------------------------------------------- #


# compute_int_feas_cut --------------------------------------------------------
def compute_int_feas_cut(duals):
    """Compute integer feasibility cuts parameters.

    Args:
        node (:obj:`int` or `str`): node id.
        tree (:obj:`Tree`): tree.
    """
    return duals
# --------------------------------------------------------------------------- #


# compute_int_opt_cut --------------------------------------------------------
def compute_int_opt_cut(duals):
    """Compute integer optimality cuts parameters.

    Args:
        node (:obj:`int` or `str`): node id.
        tree (:obj:`Tree`): tree.
    """
    return duals
# --------------------------------------------------------------------------- #
