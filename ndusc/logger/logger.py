# -*- coding: utf-8 -*-
"""Module to define logging."""

# Python packages
import logging as _log


# log -------------------------------------------------------------------------
def log(debug):
    """Logging function.

    Args:
        debug (:obj:`bool`): if ``True`` logging level is debug.
    """
    # =========================================================================
    # Logging levels
    # -------------------------------------------------------------------------
    # log.debug('debug message')
    # log.info('info message')
    # log.warn('warn message')
    # log.error('error message')
    # log.critical('critical message')
    # -------------------------------------------------------------------------

    # create log with 'my_logger'
    log = _log.getLogger()
    log.setLevel(_log.DEBUG)

    # create console handler with a higher log level
    ch = _log.StreamHandler()
    if debug:
        ch.setLevel(_log.DEBUG)
    else:
        ch.setLevel(_log.INFO)

    # create formatter and add it to the handlers
    formatter_info = _log.Formatter('%(levelname)-8s: %(message)s')
    ch.setFormatter(formatter_info)

    # add the handlers to the log
    log.addHandler(ch)
# --------------------------------------------------------------------------- #


# vars_format -----------------------------------------------------------------
def vars_format(d):
    """Format dictionary as table."""
    # Variables information:
    vars_info = []
    for v in d.keys():
        for i in d[v].keys():
            vars_info += [[str(v) + '[' + str(i) + ']', str(d[v][i])]]

    # Length of variables information
    max_len_vars = max([len(v[0]) for v in vars_info])

    # Formats
    body_format = '\t\t\t{:<' + str(max_len_vars) + '} := {}'

    # Debug
    _log.debug('\t\t* Solution:')
    for v in vars_info:
        _log.debug(body_format.format(*v))
# --------------------------------------------------------------------------- #
