
# create_feas_cuts -------------------------------------------------------------
def create_cuts(model, node):
    """
    """
    if 'cuts' in node.keys():
        log.info('Add cuts:')
        if 'feas' in node['cuts'].keys():
            log.info('\t- feasibility cuts')
            create_feas_cuts(model, node['cuts']['feas'])
        if 'opt' in node['cuts'].keys():
            log.info('\t- optimality cuts')
            create_opt_cuts(model, node['cuts']['opt'])
# ---------------------------------------------------------------------------- #


# create_feas_cuts -------------------------------------------------------------
def create_feas_cuts(model, cuts):
    #
    # Sets
    #

    model._Cuts_Feas = Set(initialize=cuts['sets']['Cuts_Feas'])

    #
    # Parameters
    #

    model._D = Param(model._Cuts_Feas,
                    initialize=cuts['params']['D'])

    model._d = Param(model._Cuts_Feas,
                    initialize=cuts['params']['d'])

    #
    # Constraints
    #

    def _opt_feas_rule(model, l):
        return sum(model.D[l,i]*model.Z[i] for i in model.Resources) >= model.d[l]

    model._opt_cuts = Constraint(model._Cuts_Feas, rule=_opt_feas_rule)
# ---------------------------------------------------------------------------- #


# create_opt_cuts --------------------------------------------------------------
def create_opt_cuts(model, cuts):
    #
    # Sets
    #

    model._Cuts_Opt = Set(initialize=cuts['sets']['Cuts_Opt'])

    #
    # Parameters
    #

    model._E = Param(model._Cuts_Opt,
                    initialize=cuts['params']['E'])

    model._e = Param(model._Cuts_Opt,
                    initialize=cuts['params']['e'])

    #
    # Variables
    #

    model.Aux_Obj = Var()

    #
    # Obj
    #

    for o in problem.component_objects(Objective, active=True):
        if o.active:
            problem._Obj = Objective(rule=o.rule+model.Aux_Obj)
            o.deactivate()

    #
    # Constraints
    #

    def _opt_cuts_rule(model, l):
        return sum(model.E[l,i]*model.Z[i] for i in model.Resources) >= model.e[l]

    model._opt_cuts = Constraint(model._Cuts_Opt, rule=_opt_cuts_rule)
# ---------------------------------------------------------------------------- #


# compute_cuts -----------------------------------------------------------------
def compute_feas_cuts(node, tree):
    """
    """

    tree = compute_feas_cuts(tree)
    tree = compute_feas_cuts(tree)

    return tree
# ---------------------------------------------------------------------------- #


# compute_feas_cuts ------------------------------------------------------------
def compute_feas_cuts(node, tree):
    """
    """



    return tree
# ---------------------------------------------------------------------------- #


# compute_opt_cuts -------------------------------------------------------------
def compute_feas_cuts(node, tree):
    """
    """
    return tree
# ---------------------------------------------------------------------------- #
