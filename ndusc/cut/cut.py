# -*- coding: utf-8 -*-
"""Module with Cut class."""


# Cuts ------------------------------------------------------------------------
class Cut(dict):
    """Cuts class."""

    # __init__ ----------------------------------------------------------------
    def __init__(self):
        """Initialize class."""
        super(Cut, self).__init__({'feas': {}, 'opt': {}})
    # ----------------------------------------------------------------------- #

    # update_cuts -------------------------------------------------------------
    def update_cuts(self, nodes):
        """Update feasibility and optimality cuts.

        Update feasibility and optimality cuts given the successor nodes.

        Args:
            nodes (:obj:`list`): list of successor nodes.
        """
    # ----------------------------------------------------------------------- #

    # get_cut -----------------------------------------------------------------
    def get_cut(self, type, id):
        """Get cut id.

        Return feasibility or optimality cut id in needed format.

        Args:
            type (:obj:`str`): desired cut: ``'feas'`` or ``'opt'``.
            id (:obj:`int`): cut id.

        Return:
            :obj:`dict`: cut information.
        """
        return {'params': {'D': {(id, var, i): self[type][id]['D'][var][i]
                           for var in self[type][id]['D']
                           for i in self[type][id]['D'][var]},
                           'd': {id: self[type][id]['d']}},
                'sets': {'vars': [(var, i)
                                  for var in self[type][id]['D']
                                  for i in self[type][id]['D'][var]
                                  ],
                         'id': [id]
                         }
                }
    # ----------------------------------------------------------------------- #
# --------------------------------------------------------------------------- #
