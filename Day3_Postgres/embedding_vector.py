"""Sample code to a PostgreSQL database and creates a table for storing embedding vectors."""
import psycopg2 as pg

connection = pg.connect("postgresql://postgres:Papai12#@localhost:5432/test")
print("Successfully connected to the database" if connection else "Connection failed")
cur = connection.cursor()

cur.execute("SELECT * FROM pg_extension WHERE extname = 'vector';")
extension = cur.fetchone()
if not extension:
    cur.execute("CREATE EXTENSION vector;")
    connection.commit()
    print("pgvector extension created.")
else:
    print("pgvector extension already exists.")

CREATE_TABLE_QUERY = '''CREATE TABLE IF NOT EXISTS test_vectors
                        (id SERIAL PRIMARY KEY,
                        text_data TEXT NOT NULL,
                        embedding vector(3) NOT NULL);'''
cur.execute(CREATE_TABLE_QUERY)

QUERY1 = """
INSERT INTO test_vectors (text_data, embedding) VALUES
('PostgreSQL database',        '[0.10, 0.20, 0.30]'),
('Relational database system', '[0.12, 0.22, 0.32]'),
('Java programming language',  '[0.90, 0.10, 0.20]'),
('Spring Boot framework',      '[0.88, 0.12, 0.18]'),
('GenAI and LLM models',       '[0.40, 0.80, 0.90]'),
('Artificial intelligence',   '[0.42, 0.78, 0.88]'),
('Semantic search',            '[0.25, 0.60, 0.70]'),
('pgvector extension',         '[0.20, 0.55, 0.65]'),
('RAG architecture',           '[0.30, 0.65, 0.75]'),
('Machine learning concepts', '[0.45, 0.85, 0.95]')
"""
cur.execute(QUERY1)
connection.commit()

QUERY2 = "SELECT * FROM test_vectors;"
cur.execute(QUERY2)
all_rows = cur.fetchall()
print(all_rows)

QUERY3 = """
SELECT id, text_data, embedding <-> '[0.11, 0.21, 0.31]' AS distance
FROM test_vectors
ORDER BY embedding <-> '[0.11, 0.21, 0.31]'
LIMIT 3;
"""
cur.execute(QUERY3)
closest_rows = cur.fetchall()
print("3 Closest Vectors: ", closest_rows)
