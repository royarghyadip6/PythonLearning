""" Learning Postgres with Python using psycopg2 library """
import psycopg2         # Import the psycopg2 library

# Connect to your postgres DB
conn = psycopg2.connect(dbname="test", user="postgres", password="Papai12#", host="localhost", port=5432)
# Open a cursor to perform database operations
cur = conn.cursor()
# Execute a query
cur.execute('select * from users')
# Retrieve all query results
records = cur.fetchall()
print("All data: ",records)

# Insert a new user
query = "INSERT INTO users (id, name, email) VALUES (6, 'Palash Giri', 'palashgiri@nokia.com')"
cur.execute(query)
# Commit the changes
conn.commit()

# Update user with ID 4
query: str = """
            UPDATE users
            SET name = 'Jane Doe'
            WHERE id = 4
            """
cur.execute(query)
conn.commit()

cur.execute("SELECT * FROM users WHERE ID = 4")
user = cur.fetchone()
print("4TH USER : ",user)

# Execute a query
cur.execute("select * from users")
# Retrieve all query results
records = cur.fetchmany(3)
print("Range data: ",records)

# Close communication with the database
cur.close()
conn.close()
