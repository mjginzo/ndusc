# -*- coding: utf-8 -*-
"""Modulo con..."""

import pyomo.environ as pyenv
import logging as log
from ndusc import format_sol


class StocasticModel(object):


    def __init__(self, model_dic):
        self.__modeldata = model_dic


    def get_model_data(self):
        return self.__modeldata


    def load(self, node):
        """Titulo.

        Descripcion.

        Args:
            file (:obj:`str`): archivo...
            ...

            Return:

            Example:
            >>> load(asda, asd)
                10.0
        """

        file = node.get_file_node(node)
        function = node.get_file_function(node)
        exec(open(file).read())
        return eval("{}(self.get_model_data())".format(function))


    @staticmethod
    def solve(problem, solver='gurobi', duals=False):
        """Titulo.
        """

        # Create a solver
        opt = pyenv.SolverFactory(solver)

        # Get duals
        problem.dual = pyenv.Suffix(direction=pyenv.Suffix.IMPORT)

        # Create a model instance and optimize
        solver_results = opt.solve(problem)

        # Obtain results
        status = str(solver_results['Solver'][0]['Termination condition'])
        log.info('Status: ' + status)
        if status == 'optimal':
            results = format_sol.get_solution(problem, solver_results, duals)
        elif status == 'infeasible':
            results = None
        else:
            results = None
            return solver_results, results
