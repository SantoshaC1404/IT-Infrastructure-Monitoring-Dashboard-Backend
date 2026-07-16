import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    user="bel",
    password="bel@123",
    dbname="it_monitoring",
)

print("Connected!")
conn.close()
