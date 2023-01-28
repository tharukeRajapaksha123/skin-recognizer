
import sqlite3

QUERY = """ CREATE TABLE items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(255) NOT NULL,
            image_url CHAR(1000) NOT NULL,
            color_code VARCHAR(25),
            description VARCHAR(1000),
            price REAL
        ); """

# Connecting to sqlite
# connection object
conn = sqlite3.connect('geek.db')

# cursor object
cursor = conn.cursor()

# Drop the GEEK table if already exists.
cursor.execute("DROP TABLE IF EXISTS GEEK")

# Creating table
table = QUERY

cursor.execute(table)

print("Table is Ready")

# Close the connection
conn.close()