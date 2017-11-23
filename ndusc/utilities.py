def update_tree(tree, results, key):
    """Update main_data[key] with information of new_data[key].
    """
    
    data = dict(main_data)
    
    if key in new_data.keys():
        if new_data[key]:
            if key in data.keys():
                data[key].update(new_data[key])
            else:
                data[key] = new_data[key]
    
    return(data)


def node_data(node, data):
    """Get data information from the node
    
    Args:
        node (:obj:`dict`): node information. 
        data (:obj:`dict`): dictionary with problem data.
    """
    
    data = update_data(data, node, 'params')
    data = update_data(data, node, 'sets')
    return data


def update_data(main_data, new_data, key):
    """Update main_data[key] with information of new_data[key].
    """
    
    data = dict(main_data)
    
    if key in new_data.keys():
        if new_data[key]:
            if key in data.keys():
                data[key].update(new_data[key])
            else:
                data[key] = new_data[key]
    
    return(data)






