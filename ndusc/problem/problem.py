# -*- coding: utf-8 -*-
"""Problem class module."""

# Python packages
import pyomo.environ as _pyenv
from pyomo.repn import collect

# Package modules
from ndusc.problem import problem_functions as _prob_func
from ndusc.problem import cuts as _cuts


# Problem ---------------------------------------------------------------------
class Problem(_pyenv.ConcreteModel):
    """Problem class.

    Problem class is a ConcreteModel class but adding utilities for the ndusc
    algorithm.

    Example:
        >>> from ndusc.problem.problem import Problem
        >>> problem = Problem()
    """

    # __init__ ----------------------------------------------------------------
    def __init__(self):
        """Initialize as ConcreteModel.

        Initialize the object as pyomo.environ.ConcreteModel.
        """
        super(Problem, self).__init__()
    # ----------------------------------------------------------------------- #

    # load_from_file ----------------------------------------------------------
    def load_from_file(self, file, function, data):
        """Load ConcreteModel from file.

        Load ConcreteModel from a function defined in a file and initialize the
        model with data information.

        Args:
            file (:obj:`str`): model filename.
            function (:obj:`str`): model function name.
            data (:obj:`dict`): dictionary with model data information.

        Example:
            >>> from ndusc import examples
            >>> prob_info = examples.problem_info.problem_info_example()
            >>> problem.load_from_file(**prob_info)
        """
        _prob_func.load_from_file(self, file, function, data)
    # ----------------------------------------------------------------------- #

    # get_constrain_coeffs ----------------------------------------------------
    def get_constrain_coeffs(self):
        """Get constraints coefficients and optimality cuts.

        Args:
            node (:obj:`ndusc.node.Node`): tree node.
        """
        # A, rhs, obj_coef, c_sense, d_sense, cnames, vnames, cnames, v_domain
        return collect.collect_linear_terms(self, [])[0]
    # ----------------------------------------------------------------------- #

    # get_rhs -----------------------------------------------------------------
    def get_rhs(self):
        """Get constraints coefficients and optimality cuts.

        Args:
            node (:obj:`ndusc.node.Node`): tree node.
        """
        return collect.collect_linear_terms(self, [])[1]
    # ----------------------------------------------------------------------- #

    # update_cuts -------------------------------------------------------------
    def update_cuts(self, node):
        """Update feasibility and optimality cuts.

        Args:
            node (:obj:`ndusc.node.Node`): tree node.
        """
        _cuts.update_cuts(self, node)
    # ----------------------------------------------------------------------- #

    # solve -------------------------------------------------------------------
    def solve(self, solver='gurobi', duals=True):
        """Solve.

        Solve the problem.

        Args:
            solver (:obj:`str`, opt): solver name. The disered solver must be
                in the path. Defaults to ``'gurobi'``.
            duals (:obj:`bool`, opt): if ``True`` return dual information.
                Defaults to ``True``.

        Return:
            :obj:`dict`: results information.
        """
        return _prob_func.solve(self, solver, duals)
    # ----------------------------------------------------------------------- #

    # create_feas_cuts --------------------------------------------------------
    def create_feas_cuts(self, feas_cuts):
        """Create feasibility cuts.

        Args:
            feas_cuts (:obj:`dict`): feasibility cuts of the current node.
        """
        if hasattr(self, '_feas_cuts'):
            _cuts.update_feas_cuts(self, feas_cuts)
        else:
            _cuts.create_feas_cuts(self, feas_cuts)
    # ----------------------------------------------------------------------- #

    # create_opt_cuts ---------------------------------------------------------
    def create_opt_cuts(self, opt_cuts):
        """Create optimality cuts.

        Args:
            opt_cuts (:obj:`dict`): optimality cuts of the current node.
        """
        _cuts.create_opt_cuts(self, opt_cuts)
    # ----------------------------------------------------------------------- #
# --------------------------------------------------------------------------- #
