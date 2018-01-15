# -*- coding: utf-8 -*-
"""Node class module."""

# Package modules
import ndusc.error.error as _error


# Node ------------------------------------------------------------------------
class Node(dict):
    """Node class.

    Todo: Check node structure.
    """

    # __init__ ----------------------------------------------------------------
    def __init__(self, *arg, **kw):
        """Initialization."""
        super(Node, self).__init__(*arg, **kw)

    # get_file ----------------------------------------------------------------
    def get_file(self):
        """Get filename."""
        return self['model']['file']
    # ----------------------------------------------------------------------- #

    # get_function ------------------------------------------------------------
    def get_function(self):
        """Get function name."""
        return self['model']['function']
    # ----------------------------------------------------------------------- #

    # ================
    # CUTS INFO
    # ================

    # get_cuts ----------------------------------------------------------------
    def get_cuts(self):
        """Get cuts.

        Return:
            :obj:`ndusc.cut.cut.Cut`: cuts information.
        """
        if 'cuts' not in self.keys():
            return None
        else:
            return self['cuts']
    # ----------------------------------------------------------------------- #

    # ================
    # SOLUTION INFO
    # ================

    # update_solution ---------------------------------------------------------
    def update_solution(self, solution):
        """Update node solution.

        Args:
            solution (:obj:`dict`): solution information.
        """
        self['solution'] = solution
    # ----------------------------------------------------------------------- #

    # is_infeasible -----------------------------------------------------------
    def is_infeasible(self):
        """Check if it has a infeasible solution.

        Return:
            :obj:`bool`: ``True`` if node is infeasible.
        """
        try:
            sol = self['solution']
            return sol['status'] != 'optimal'
        except KeyError:
            raise _error.no_solved(self['id'])
    # ----------------------------------------------------------------------- #

    # get_duals_info ----------------------------------------------------------
    def get_duals_info(self):
        """Get dual information.

        Return:
            :obj:`dict`: dual information.
        """
        try:
            cons = self['solution']['constraints']
            return {c: {i: cons[c][i]['dual']} for c in cons for i in cons[c]}
        except KeyError:
            return None
    # ----------------------------------------------------------------------- #

    # get_variables_info ------------------------------------------------------
    def get_variables_info(self):
        """Get variable information.

        Return:
            :obj:`dict`: variables information.
        """
        try:
            return self['solution']['variables']
        except KeyError:
            return None
    # ----------------------------------------------------------------------- #
# --------------------------------------------------------------------------- #
