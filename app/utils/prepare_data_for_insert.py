def prepare_data_for_insert(data_dict):
    """
    Prepare data for database insertion by removing keys with None values.

    Args:
        data_dict (dict): The input data dictionary.

    Returns:
        dict: A new dictionary with keys that have non-None values.
    """
    processed_data = {
        key: value for key, value in data_dict.items() if value is not None
    }
    return processed_data
