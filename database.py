import sqlite3

conn = sqlite3.connect("diet.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS progress (
    day INTEGER,
    weight REAL,
    calories REAL
)
""")

conn.commit()
conn.close()

print("Database created!")