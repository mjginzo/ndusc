# -*- coding: utf-8 -*-
"""Modulo con..."""

import pyomo.environ as pyenv

# Package modules
import ndusc.problem_nd.problem_functions as prob_func
import ndusc.problem_nd.cuts as cuts


class Problem(pyenv.ConcreteModel):
    """Problem class.

    Problem class is a ConcreteModel class but adding utilities for ndusc
    algorithm.
    """

    def __init__(self):
        """Initialize as ConcreteModel.

        Initialize the object as pyomo.environ.ConcreteModel.
        """
        super(Problem, self).__init__()

    def load_from_file(self, file, function, data):
        """Load ConcreteModel from file.

        Load ConcreteModel from a function defined in a file and initialize the
        model with data information.

        Args:
            file (:obj:`str`): model filename.
            function (:obj:`str`): model function name.
            data (:obj:`dict`): dictionary with model data information.
        """
        prob_func.load_from_file(self, file, function, data)

    def update_cuts(self, node):
        """Update feasibility and optimality cuts.

        Args:
            node (:obj:`ndusc.node.Node`): tree node.
        """
        cuts.update_cuts(self, node)

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
        return prob_func.solve(self, solver, duals)

    def create_feas_cuts(self, feas_cuts):
        """Create feasibility cuts.

        Args:
            feas_cuts (:obj:`dict`): feasibility cuts of the current node.
        """
        if hasattr(self, '_feas_cuts'):
            cuts.update_feas_cuts(self, feas_cuts)
        else:
            cuts.create_feas_cuts(self, feas_cuts)

    def create_opt_cuts(self, opt_cuts):
        """Create optimality cuts.

        Args:
            opt_cuts (:obj:`dict`): optimality cuts of the current node.
        """
        cuts.create_opt_cuts(self, opt_cuts)
