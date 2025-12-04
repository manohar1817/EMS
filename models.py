import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="your_username",
    password="your_password",
    database="testdb"
)

cursor = conn.cursor()

# Fetch all data
cursor.execute("SELECT * FROM users")

rows = cursor.fetchall()

for row in rows:
    print(row)

cursor.close()
conn.close()
