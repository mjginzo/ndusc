# -*- coding: utf-8 -*-
"""Configuration module."""
from timeit import default_timer as timer

# Output_module ---------------------------------------------------------------
class Execution_vars(object):
    """Global variables used during the execution time."""
    # __init__ ----------------------------------------------------------------
    def __init__(self, problem_type):
        """Create configuration struct with default values

        Args:
            self (:obj:`self`):

        Example:
            >>> exec_vars = Execution_vars()
        """

        self.LB = -float('inf')
        self.UB = -float('inf')
        self.iters = 0
        self.evals = 0
        self.start = timer()
        self.stopcontion = 0
        if problem_type == 'continuous':
            self.bin_cuts = False
        else:
            self.bin_cuts = True

# ----------------------------------------------------------------------- #
