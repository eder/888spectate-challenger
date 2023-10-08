def search_query(payload):
    """
    Build an SQL query based on the given payload.

    Args:
    - payload (dict): A dictionary containing keys as table names (in singular form, e.g., "sport")
                      and values as dictionaries with column names as keys and desired values.

    Returns:
    - str: An SQL query generated from the payload.
    """

    # Function to convert payload name to table name
    def to_table_name(key):
        return key.capitalize() + "s"

    # Define potential relations between tables
    relations = {"Sports": [], "Events": ["Sports"], "Selections": ["Events"]}

    tables_in_payload = [to_table_name(k) for k in payload.keys()]

    # Determine all necessary tables for the query based on the relations
    required_tables = set(tables_in_payload)
    for table in tables_in_payload:
        required_tables.update(relations[table])

    # Base of the query
    base_table = list(required_tables)[0]  # Start with one of the tables
    query = f"SELECT * FROM {base_table}"

    # Add other tables with JOINs
    for table in required_tables:
        if table != base_table:
            if "Events" in [base_table, table]:
                foreign_key = "sport_id"
            else:
                foreign_key = "event_id"
            query += f" JOIN {table} ON {table}.{foreign_key} = {base_table}.id"

    # Build WHERE clauses
    where_clauses = []
    for key, value in payload.items():
        if value is not None:
            table_name = to_table_name(key)
            for column, column_value in value.items():
                if isinstance(column_value, str):
                    where_clauses.append(f"{table_name}.{column} = '{column_value}'")
                else:
                    where_clauses.append(f"{table_name}.{column} = {column_value}")

    if where_clauses:
        query += " WHERE " + " AND ".join(where_clauses)

    return query
