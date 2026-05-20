import sqlite3
import pandas as pd

conn = sqlite3.connect("checkpoints.db")

# Show all tables
tables = pd.read_sql_query(
    "SELECT name FROM sqlite_master WHERE type='table';",
    conn
)

print(tables)

# View checkpoints table
df = pd.read_sql_query(
    "SELECT * FROM checkpoints",
    conn
)

print(df)

conn.close()