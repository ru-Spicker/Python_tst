import psycopg2
import time
conn = psycopg2.connect(host='192.168.1.164', user='adi_admin', password='12345', dbname='postgres')
cursor = conn.cursor()
cursor.execute("SELECT now();")
for row in cursor:
    print(row)

cursor.execute("COMMIT;")

cursor.execute("CREATE DATABASE adi_test;")
cursor.execute("GRANT ALL privileges ON DATABASE adi_test TO adi_admin;")
cursor.close()
conn.close()

conn = psycopg2.connect(host='192.168.1.164', user='adi_admin', password='12345', dbname='adi_test')
cursor = conn.cursor()

cursor.execute("CREATE TABLE ne (ne_id INTEGER PRIMARY KEY, ne_name VARCHAR);")
cursor.execute("select table_name, column_name from information_schema.columns where table_schema='public';")
for row in cursor:
    print(row)

cursor.execute("INSERT INTO ne (ne_id, ne_name) VALUES (12345, 'Tupoleva');")
cursor.execute("SELECT * FROM ne;")
try:
    data = cursor.fetchall()
    for row in data:
        print(row)
except psycopg2.ProgrammingError:
    print("No data to out")

cursor.close()
conn.close()


conn = psycopg2.connect(host='192.168.1.164', user='adi_admin', password='12345', dbname='postgres')
cursor = conn.cursor()
cursor.execute("COMMIT;")
cursor.execute("DROP DATABASE adi_test;")
try:
    data = cursor.fetchall()
    for row in data:
        print(row)
except psycopg2.ProgrammingError:
    print("No data to out")
cursor.close()
conn.close()
