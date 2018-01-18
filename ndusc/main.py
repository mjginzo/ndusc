# -*- coding: utf-8 -*-
"""Main module.

Main module to execute the Nested Decomposition (allowing binary variables) by
command line. This module reads the input to execute the
:func:`~ndusc.nd.nested_decomposition` function.
"""
# Python packages
import argparse as _arg

# Package modules
import ndusc.logger.logger as _log
import ndusc.input.input_module as _im
import ndusc.nd.ndusc as _ndusc
import ndusc.nd.configuration as _config

# parse_args ------------------------------------------------------------------
def parse_args():
    """Argument parser function.

    Reference: http://newcoder.io/api/part-4/.
    """
    # general parser and info
    parser = _arg.ArgumentParser(
        prog='ndusc',
        description="""Nested decomposition algorithm.\n Implementation made by
        researchers of the Santiago de Compostela University.""",
        formatter_class=_arg.ArgumentDefaultsHelpFormatter
        )

    parser.add_argument("tree",
                        help="Path to the tree file in yaml format."
                        )

    parser.add_argument("data",
                        help="Path to the general data file in yaml format."
                        )

    parser.add_argument("-s",
                        "--solver",
                        default='gurobi',
                        help="Solver name."
                        )

    parser.add_argument("-d",
                        "--debug",
                        action="store_true",
                        help="Write debug output.",
                        required=False
                        )

    parser.add_argument("-t",
                        "--time",
                        help="Maximum execution time",
                        default='100000',
                        type=float,
                        required=False
                        )

    parser.add_argument("-it",
                        "--iterations",
                        help="Maximum iterations",
                        default='100000',
                        type=float,
                        required=False
                        )

    parser.add_argument("-ev",
                        "--evaluations",
                        help="Maximum evaluations",
                        default='100000',
                        type=float,
                        required=False
                        )

    parser.add_argument("-o",
                        "--output",
                        action="store_true",
                        help="Generate output files",
                        required=False
                        )

    args = parser.parse_args()

    return args
# --------------------------------------------------------------------------- #


# main ------------------------------------------------------------------------
def main():
    """Main function.

    Reads the input from command line (if you don't enter an input file) or
    from an input file (you can get an example input typinf the option -w).
    Then, it executes the :func:`~umipkg.create_package.create_package`
    function.
    """

    # =========================================================================
    # Load input
    # -------------------------------------------------------------------------
    args = parse_args()

    tree_path = args.tree
    data_path = args.data

    # =========================================================================
    # Create configuration struct
    # -------------------------------------------------------------------------
    config = _config.Configuration()
    config.set_args_config(args)

    # =========================================================================
    # Logging format
    # -------------------------------------------------------------------------
    # log.debug('debug message')
    # log.info('info message')
    # log.warn('warn message')
    # log.error('error message')
    # log.critical('critical message')
    # -------------------------------------------------------------------------

    # create log with 'my_logger'
    _log.log(args.debug)

    # =========================================================================
    # Execute the function
    # -------------------------------------------------------------------------

    # Read data
    data = _im.Input_module(data_path, tree_path)
    tree_dic = data.load_tree()
    data_dic = data.load_data()

    # Nested decomposition
    output = _ndusc.ndusc(tree_dic, data_dic, config)

    print(output)


# --------------------------------------------------------------------------- #

# execute only if run as a script
# An example of execution:
# $ python3 ndusc -s gurobi -d
#                       tests/datas/data1/tree.yaml tests/datas/data1/data.yaml
if __name__ == '__main__':
    # call to main module
    main()
