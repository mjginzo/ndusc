# -*- coding: utf-8 -*-
"""Module with Cut class."""

# Package modules
import ndusc.cut.cut_functions as _cf


# Cuts ------------------------------------------------------------------------
class Cut(dict):
    """Cuts class."""

    # __init__ ----------------------------------------------------------------
    def __init__(self):
        """Initialize class."""
        super(Cut, self).__init__()
    # ----------------------------------------------------------------------- #

    # get_last_index ----------------------------------------------------------
    def get_last_index(self, cut_type):
        """Get last index of desired cut type.

        Args:
            cut_type (:obj:`str`): cut type. Options: ``'feas'``, ``'opt'``,
                ``'bin_feas'`` or ``'bin_opt'``.

        Return:
            :obj:`int`: last cut index.
        """
        if cut_type not in self.keys():
            return 0
        else:
            return max(self[cut_type].keys())
    # ----------------------------------------------------------------------- #

    # add_feas ----------------------------------------------------------------
    def add_feas(self, vars, dual, cons):
        """Add feasibility cuts parameters.

        Args:
            vars (:obj:`dict`): variables to get information.
            dual (:obj:`dict`): dual variables information.
            cons (:obj:`dict`): constraints information.
        """
        last_i = self.get_last_index('feas')
        if last_i == 0:
            self['feas'] = {}

        new_cuts = _cf.compute_feas_cut(vars, dual, cons)
        self['feas'].update({last_i + 1 + i: new_cuts[i]
                             for i in range(len(new_cuts))})
    # ----------------------------------------------------------------------- #

    # add_opt ----------------------------------------------------------------
    def add_opt(self, vars, dual, cons, probs):
        """Add optimality cuts parameters.

        Args:
            vars (:obj:`dict`): variables to get information.
            dual (:obj:`dict`): dual variables information.
            cons (:obj:`dict`): constraints information.
            probs (:obj:`dict`): nodes probability.
        """
        last_i = self.get_last_index('opt')
        if last_i == 0:
            self['opt'] = {}

        new_cuts = _cf.compute_opt_cut(vars, dual, cons, probs)
        self['opt'].update({last_i + 1 + i: new_cuts[i]
                            for i in range(len(new_cuts))})
    # ----------------------------------------------------------------------- #

    # add_bin_feas ------------------------------------------------------------
    def add_bin_feas(self, vars, vars_val):
        """Add binary feasibility cuts parameters.

        Args:
            vars (:obj:`dict`): variables to get information.
            vars_vale (:obj:`dict`): variables information.
        """
        last_i = self.get_last_index('bin_feas')
        if last_i == 0:
            self['bin_feas'] = {}

        new_cuts = _cf.compute_bin_feas_cut(vars, vars_val)
        self['bin_feas'].update({last_i + 1 + i: new_cuts[i]
                                 for i in range(len(new_cuts))})
    # ----------------------------------------------------------------------- #

    # add_bin_opt ------------------------------------------------------------
    def add_bin_opt(self, vars, vars_val, EV, L):
        """Add binary optimality cuts parameters.

        Args:
            vars (:obj:`dict`): variables to get information.
            vars_vale (:obj:`dict`): variables information.
            EV (:obj:`float`): expected value of the selected nodes.
            L (:obj:`float`): lower bound for the expected value. It may
                obtained by solving the relaxed integer problem.
        """
        last_i = self.get_last_index('bin_opt')
        if last_i == 0:
            self['bin_opt'] = {}

        new_cuts = _cf.compute_bin_feas_cut(vars, vars_val)
        self['bin_opt'].update({last_i + 1 + i: new_cuts[i]
                                for i in range(len(new_cuts))})
    # ----------------------------------------------------------------------- #
# --------------------------------------------------------------------------- #
