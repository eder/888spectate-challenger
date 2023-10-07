from typing import List, Optional, Dict


class QueryBuilder:
    def __init__(self, table_name: str):
        """
        Initialize the QueryBuilder.

        Args:
            table_name (str): The name of the database table.
        """
        self.table_name = table_name
        self.conditions: List[str] = []
        self.insert_data: List[dict] = []
        self.update_data: Optional[Dict[str, str]] = None

    def add_condition(self, field: str, value: str):
        """
        Add a condition to the query.

        Args:
            field (str): The field to use in the condition.
            value (str): The value to compare with in the condition.
        """
        condition = f"{field} = '{value}'"
        self.conditions.append(condition)

    def add_insert_data(self, data: dict):
        """
        Add data for insertion into the table.

        Args:
            data (dict): Dictionary representing the data to insert.
        """
        self.insert_data.append(data)

    def add_update_data(self, data: Dict[str, str]):
        """
        Set data for updating records in the table.

        Args:
            data (Dict[str, str]): Dictionary representing the data to update.
        """
        self.update_data = data

    def build_query(self) -> str:
        """
        Build a SELECT query based on conditions.

        Returns:
            str: The SELECT query.
        """
        if not self.conditions:
            return f"SELECT * FROM {self.table_name}"
        else:
            conditions_str = " AND ".join(self.conditions)
            return f"SELECT * FROM {self.table_name} WHERE {conditions_str}"

    def build_insert_query(self) -> Optional[str]:
        """
        Build an INSERT query.

        Returns:
            Optional[str]: The INSERT query or None if no data to insert.
        """
        if not self.insert_data:
            return None

        columns = list(self.insert_data[0].keys())
        values = []

        for row_data in self.insert_data:
            values.append(", ".join([f"'{row_data[column]}'" for column in columns]))

        columns_str = ", ".join(columns)
        values_str = "), (".join(values)

        query = f"INSERT INTO {self.table_name} ({columns_str}) VALUES ({values_str}) RETURNING *"
        return query

    def build_update_query(self) -> Optional[str]:
        """
        Build an UPDATE query.

        Returns:
            Optional[str]: The UPDATE query or None if no data to update.
        """
        if not self.update_data:
            return None

        if not self.conditions:
            raise ValueError(
                "Update query requires at least one condition to specify which records to update"
            )

        set_clause = ", ".join(
            [f"{key} = '{value}'" for key, value in self.update_data.items()]
        )
        conditions_str = " AND ".join(self.conditions)
        query = f"UPDATE {self.table_name} SET {set_clause} WHERE {conditions_str} RETURNING *"
        return query
