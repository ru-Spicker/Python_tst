import time
from os import listdir

import psycopg2
import sys
import argparse
import json
from re import match

def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', nargs='?')
    parser.add_argument('--user', nargs='?')
    parser.add_argument('--password', nargs='?')
    parser.add_argument('--path', nargs='?')

    return parser

def to_arg(arg :object):
    if type(arg) == int:
        result = str(arg)
    else:
        if type(arg) == str:
            result = "'" + arg + "'"
        else:
            if type(arg) == "list":
                result = "["
                for i in range(len(arg)-2):
                    result = result + to_arg(arg[i]) + ","
                result = result + to_arg(arg[len(arg)-1]) + "]"
            else:
                print(type(arg))
                result = None
    return result



db_file_list = []
list_NE = []
list_Port = []
list_Port_Description = []
list_PW = []
list_ETH = []
list_CES = []
list_Tunnel = []
list_TNL_GRP = []
db_packet_len = 100
list_argument = []


if __name__ == '__main__':
    parser = createParser()
    namespace = parser.parse_args()

list_File = listdir(namespace.path)
print(list_File)

for f in list_File:
    rx = match(r'^(ADI_\d\d\d\d_\d\d_\d\d_\d\d_\d\d_\d\d)\.(ces|description|eth|group|node|port|pw|tunnel)$', f)
    if rx is None:
        # print('Not db file:', f)
        continue
    db_file_list.append({'name': rx.group(1), 'extension': rx.group(2)})

for db_file in db_file_list:
    if db_file['extension'] == 'node':
        print('Load list ne')
        list_NE = json.load(open(namespace.path + '\\' + db_file['name'] + '.' + db_file['extension'], 'r'))
    if db_file['extension'] == 'ces':
        print('Load list ces')
        list_CES = json.load(open(namespace.path + '\\' + db_file['name'] + '.' + db_file['extension'], 'r'))
    if db_file['extension'] == 'eth':
        print('Load list eth')
        list_ETH = json.load(open(namespace.path + '\\' + db_file['name'] + '.' + db_file['extension'], 'r'))
    if db_file['extension'] == 'description':
        print('Load list description')
        list_Port_Description = json.load(open(namespace.path + '\\' + db_file['name'] + '.' + db_file['extension'], 'r'))
    if db_file['extension'] == 'group':
        print('Load list group')
        list_TNL_GRP = json.load(open(namespace.path + '\\' + db_file['name'] + '.' + db_file['extension'], 'r'))
    if db_file['extension'] == 'port':
        print('Load list port')
        list_Port = json.load(open(namespace.path + '\\' + db_file['name'] + '.' + db_file['extension'], 'r'))
    if db_file['extension'] == 'pw':
        print('Load list pw')
        list_PW = json.load(open(namespace.path + '\\' + db_file['name'] + '.' + db_file['extension'], 'r'))
    if db_file['extension'] == 'tunnel':
        print('Load list tunnel')
        list_Tunnel = json.load(open(namespace.path + '\\' + db_file['name'] + '.' + db_file['extension'], 'r'))


conn = psycopg2.connect(host=namespace.host, user=namespace.user, password=namespace.password, dbname='postgres')
cursor = conn.cursor()
cursor.execute("COMMIT;")
str_select = "CREATE DATABASE {0};".format(db_file_list[0]['name'])
print(str_select)
try:
    data = cursor.fetchall()
    for row in data:
        print(row)
except psycopg2.ProgrammingError:
    print("No data to out")
cursor.execute(str_select)
str_select = "GRANT ALL privileges ON DATABASE {0} TO adi_admin;".format(db_file_list[0]['name'])
print(str_select)
try:
    data = cursor.fetchall()
    for row in data:
        print(row)
except psycopg2.ProgrammingError:
    print("No data to out")
cursor.execute(str_select)
cursor.close()
conn.close()

time.sleep(5)
conn = psycopg2.connect(host=namespace.host, user=namespace.user, password=namespace.password,
                        dbname=str(db_file_list[0]['name']).lower())
cursor = conn.cursor()

cursor.execute("COMMIT;")
cursor.execute("CREATE TABLE ne (id INTEGER PRIMARY KEY, ne_name VARCHAR);")
cursor.execute("COMMIT;")

for i in range(0, len(list_NE) - 1, db_packet_len):
    str_select = "INSERT INTO ne (id , ne_name) VALUES ("
    for ii in range(i, ((i + db_packet_len) if (i + db_packet_len) < len(list_NE) else len(list_NE) - 1), 1):
        # str_select = "INSERT INTO ne (id , ne_name) VALUES ({0}, '{1}');".format(i, list_NE[i])
        list_argument.append(str(ii) + ", " + to_arg(list_NE[ii]))

    str_select = str_select + "), (".join(list_argument) + ");"
    list_argument = []
    print(i, ii)
    print(str_select)
    cursor.execute(str_select)

cursor.execute("select * from ne;")
try:
    data = cursor.fetchall()
    for row in data:
        print(row)
except psycopg2.ProgrammingError:
    print("No data to out")


'''conn = psycopg2.connect(host=namespace.host, user=namespace.user, password=namespace.password, dbname='postgres')
cursor = conn.cursor()
cursor.execute("SELECT now();")
for row in cursor:
    print(row)

cursor.execute("COMMIT;")
'''
