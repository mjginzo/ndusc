# -*- coding: utf-8 -*-
"""Problem class module."""

# Python packages
import pyomo.environ as _pyenv
from pyomo.repn import collect

# Package modules
import ndusc.problem.problem_functions as _prob_func
import ndusc.problem.integer_utils as _int_u
import ndusc.problem.cuts as _cuts


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

    # fix_vars ----------------------------------------------------------------
    def fix_vars(self, vars_val):
        """Fix or unfix integer variables.

        Args:
            problem (:obj:`pyomo.environ.ConcreteModel`): concrete model of
                pyomo.
            vars_val (:obj:`dict`): dictionary with variables value
                information.

        Example:
        """
        vars_val
        _prob_func.fix_vars(self, vars_val)
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

    # solve -------------------------------------------------------------------
    def solve(self, solver='gurobi', relaxed=False):
        """Solve.

        Solve the problem.

        Args:
            solver (:obj:`str`, opt): solver name. The disered solver must be
                in the path. Defaults to ``'gurobi'``.
            relaxed (:obj:`bool`, opt): if ``True`` solve problem relaxation.
                Defaults to ``False``.

        Return:
            :obj:`tuple`: problem and solver results information.
        """
        return _prob_func.solve(self, solver, relaxed)
    # ----------------------------------------------------------------------- #

    # solve_node --------------------------------------------------------------
    def solve_node(self, solver='gurobi', get_duals=False):
        """Solve a node problem.

        Solve a node of the nested decomposition algorithm.

        Args:
            solver (:obj:`str`, opt): solver name. The disered solver must be
                in the path. Defaults to ``'gurobi'``.
            get_duals (:obj:`bool`, opt): ``True`` to return dual information
                of the relaxed problem.

        Return:
            :obj:`dict`: results information.
        """
        if get_duals:
            info = ['variables', 'objective', 'solver_info', 'duals']
        else:
            info = ['variables', 'objective', 'solver_info']
        return _prob_func.solve_node(self, solver, info)
    # ----------------------------------------------------------------------- #

    # create_cuts -------------------------------------------------------------
    def create_cuts(self, cuts):
        """Create cuts.

        Args:
            cuts (:obj:`ndusc.cut.cut.Cut`): cuts information.
        """
        if 'opt' in cuts.keys():
            opt_cuts = cuts['opt']
            _cuts.create_opt_cuts(self, opt_cuts)
        if 'feas' in cuts.keys():
            feas_cuts = cuts['feas']
            _cuts.create_feas_cuts(self, feas_cuts)
        if 'bin_opt' in cuts.keys():
            bin_opt_cuts = cuts['bin_opt']
            _cuts.create_bin_opt_cuts(self, bin_opt_cuts)
        if 'bin_feas' in cuts.keys():
            bin_feas_cuts = cuts['bin_feas']
            _cuts.create_bin_feas_cuts(self, bin_feas_cuts)
    # ----------------------------------------------------------------------- #

    # relax -------------------------------------------------------------------
    def relax(self):
        """Relax the integer variables.

        Change domain of all integer variables to the Real set insted of
        Integer set.
        """
        _int_u.relax(self)
    # ----------------------------------------------------------------------- #
# --------------------------------------------------------------------------- #
