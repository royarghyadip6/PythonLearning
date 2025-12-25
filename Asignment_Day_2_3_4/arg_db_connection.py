"""DbConnection Module"""
import psycopg2 as pg

def get_db_connection():
    """DbConnection"""
    username = "postgres"
    password = "Papai12#"
    host = "localhost"
    port = "5432"
    database = "postgres"

    # connection = pg.connect(user=username, password=password, host=host, port=port, database=database)
    connection = pg.connect(
        "postgresql://"+ username +":"+ password +"@"+host+":"+port+"/"+database
    )
    if connection is not None:
        print("DB Connected successfully.")
        return connection
    else:
        print("DB Connection failed.")
        return None

def close_db_cursor_connection(cursor, connection):
    """Close Cursor and DbConnection"""
    if cursor is not None:
        cursor.close()
    if connection is not None:
        connection.close()
    print("PostgreSQL connection is closed")
    return None