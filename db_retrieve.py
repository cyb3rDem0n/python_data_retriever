import json
import os
import oracledb

class QueryResult:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

def load_config(config_file):
    """
    Loads the database configuration from a JSON file.

    :param config_file: Path to the configuration file
    :return: Configuration dictionary
    """
    if not os.path.exists(config_file):
        raise FileNotFoundError(f"Configuration file '{config_file}' not found.")
    with open(config_file, 'r') as file:
        return json.load(file)

def connect_and_query_oracle_db(config_file, query):
    """
    Connects to an Oracle database, executes a selection query, and maps the result to objects.

    :param config_file: Path to the configuration file
    :param query: SQL query to execute
    :return: Query results as a list of objects
    """
    try:
        # Load configuration
        config = load_config(config_file)

        # Establish the connection
        connection = oracledb.connect(
            user=config["user"],
            password=config["password"],
            dsn=config["dsn"]
        )
        cursor = connection.cursor()

        # Execute the query
        cursor.execute(query)
        columns = [col[0].lower() for col in cursor.description]  # Get column names
        results = [QueryResult(**dict(zip(columns, row))) for row in cursor.fetchall()]

        # Close the cursor and connection
        cursor.close()
        connection.close()

        return results
    except oracledb.DatabaseError as e:
        print(f"Database error occurred: {e}")
        return None

# Example usage:
if __name__ == "__main__":
    query = """
    SELECT ID_PROFILE, PROFILE_IDENTIFIER, DESCRIPTION, LAST_UPDATE_TS 
    FROM MDLR_CORE_PROFILE_INSTANCES mcpi 
    """
    try:
        results = connect_and_query_oracle_db("config.json", query)
        if results is not None:
            for obj in results:
                print(obj.__dict__)
        else:
            print("No results to display.")
    except Exception as e:
        print(f"Errore: {e}")