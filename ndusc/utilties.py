
    def update_data(main_data, new_data, keys):
        """Update main_data with information of new_data the keys.

        Args:
            main_data (:obj:`dict`): main dictionary.
            new_data (:obj:`dict`): second dictionary.
            keys (:obj:`list`): key list of both dictionaries.

        Return:
            :obj:`dict`: combination of main_data and new_data.
        """
        data = dict(main_data)

        for key in keys:
            if key in new_data.keys():
                if new_data[key]:
                    if key in data.keys():
                        data[key].update(new_data[key])
                    else:
                        data[key] = new_data[key]

        return(data)
