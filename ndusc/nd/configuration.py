# -*- coding: utf-8 -*-
"""Configuration module."""

# Output_module ---------------------------------------------------------------
class Configuration(object):
    """Configuration module class."""
    # __init__ ----------------------------------------------------------------
    def __init__(self):
        """Create configuration struct with default values

        Args:
            args (:obj:`argparse`):

        Example:
            >>> config = Configuration_module()
        """
        self.solver = "gurobi"
        self.time = 10000000
        self.iters = 10000000
        self.evals = 10000000
        self.debug_flag = False
        self.output_flag = False
# ----------------------------------------------------------------------- #

# set_args_config ------------------------------------------------------- #
    def set_args_config(self, args):
        """Create configuration struct with default values

        Args:
            args (:obj:`argparse`):

        Example:
            >>> parser = _arg.ArgumentParser()
            >>> args = parser.parse_args()
            >>> config = Configuration_module()
            >>> config.set_args_config(args)
        """

        self.solver = args.solver
        self.time = args.time
        self.iters = args.iterations
        self.evals = args.evaluations
        self.debug_flag = args.debug
        self.output_flag = args.output
# --------------------------------------------------------------------------- #
