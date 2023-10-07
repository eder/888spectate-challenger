def prepare_data_for_insert(data_dict):
    processed_data = {key: value for key, value in data_dict.items() if value is not None}
    set_clause = ", ".join([f"{key}=${i}" for i, (key, value) in enumerate(processed_data.items(), start=1)])
    values = list(processed_data.values())
    return {
        "original_data": data_dict,  # Inclua o dicionário original como parte do retorno
        "set_clause": set_clause,
        "values": values
    }

