import psycopg2
import sys
import argparse

def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', nargs='?')
    parser.add_argument('--user', nargs='?')
    parser.add_argument('--password', nargs='?')
    parser.add_argument('--path', nargs='?')

    return parser


if __name__ == '__main__':
    parser = createParser()
    namespace = parser.parse_args()

print(namespace)


conn = psycopg2.connect(host=namespace.host, user=namespace.user, password=namespace.password, dbname='postgres')
cursor = conn.cursor()
cursor.execute("SELECT now();")
for row in cursor:
    print(row)

cursor.execute("COMMIT;")
