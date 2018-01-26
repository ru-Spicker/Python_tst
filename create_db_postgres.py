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


def insert_in_table(cursor: object, insert_list: list, start_str: str, pack_len: int):
    list_argument = []
    list_sub_arg = []
    for i in range(0, len(insert_list) - 1, pack_len):
        str_select = start_str
        for ii in range(i, ((i + pack_len) if (i + pack_len) < len(insert_list) else len(insert_list)), 1):
            if type(insert_list[ii]) == list:
                list_sub_arg = []
                for el in insert_list[ii]:
                    list_sub_arg.append(to_arg(el))
                list_argument.append(str(ii) + ", " + ", ".join(list_sub_arg))
            else:
                list_argument.append(str(ii) + ", " + to_arg(insert_list[ii]))
        str_select = str_select + "), (".join(list_argument) + ");"
        list_argument = []
        print(i, ii)
        print(str_select)
        cursor.execute(str_select)


def to_arg(arg: object):
    if type(arg) == int:
        result = str(arg)
    else:
        if type(arg) == str:
            result = "'" + arg + "'"
        else:
            if type(arg) == list:
                if len(arg) > 0:
                    result = "ARRAY["
                    for i in range(0, len(arg)-2):
                        result = result + to_arg(arg[i]) + ","
                    result = result + to_arg(arg[len(arg)-1]) + "]"
                else:
                    result = "'{}'"
            else:
                if arg is None:
                    result = "NULL"
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
cursor.execute(str_select)
str_select = "GRANT ALL privileges ON DATABASE {0} TO adi_admin;".format(db_file_list[0]['name'])
print(str_select)
cursor.execute(str_select)
cursor.close()
conn.close()

time.sleep(5)
conn = psycopg2.connect(host=namespace.host, user=namespace.user, password=namespace.password,
                        dbname=str(db_file_list[0]['name']).lower())
cursor = conn.cursor()

cursor.execute("COMMIT;")
cursor.execute("CREATE TABLE adi_ne (id INTEGER PRIMARY KEY, ne_name VARCHAR);")
cursor.execute("CREATE TABLE adi_port (id INTEGER PRIMARY KEY, port VARCHAR);")
cursor.execute("""CREATE TABLE adi_description (id INTEGER PRIMARY KEY, 
                                                ne_id INTEGER REFERENCES adi_ne,
                                                port_id INTEGER REFERENCES adi_port,
                                                description VARCHAR);""")
cursor.execute("""CREATE TABLE adi_tunnel (id INTEGER PRIMARY KEY,
                                            tunnel VARCHAR,
                                            tunnel_id VARCHAR,
                                            direction VARCHAR,
                                            src_ne_id INTEGER REFERENCES adi_ne,
                                            src_port_id INTEGER REFERENCES adi_port, 
                                            snk_ne_id INTEGER REFERENCES adi_ne,
                                            snk_port_id INTEGER REFERENCES adi_port, 
                                            transit_ne_id INTEGER[],
                                            transit_in_port_id INTEGER[], 
                                            transit_out_port_id INTEGER[] 
                                            );""")
cursor.execute("""CREATE TABLE adi_group (id INTEGER PRIMARY KEY,
                                            aps_name VARCHAR,
                                            src_ne_id INTEGER REFERENCES adi_ne,
                                            snk_ne_id INTEGER REFERENCES adi_ne,
                                            wrk_fwd_wrk INTEGER REFERENCES adi_tunnel,
                                            prt_fwd_prt INTEGER REFERENCES adi_tunnel,
                                            bwd_wrk INTEGER REFERENCES adi_tunnel,
                                            bwd_prt INTEGER REFERENCES adi_tunnel
                                            );""")
cursor.execute("""CREATE TABLE adi_pw (id INTEGER PRIMARY KEY, 
                                            right_ne_id INTEGER REFERENCES adi_ne,
                                            left_ne_id INTEGER REFERENCES adi_ne,
                                            pw_id VARCHAR,
                                            tunnels VARCHAR[]);""")
cursor.execute("""CREATE TABLE adi_eth (id INTEGER PRIMARY KEY, 
                                            name VARCHAR,
                                            service_id VARCHAR,
                                            protect_type1 INTEGER,
                                            protect_type2 INTEGER,
                                            src_ne_id INTEGER REFERENCES adi_ne,
                                            src_port_id INTEGER REFERENCES adi_port, 
                                            src_vlan VARCHAR,
                                            snk_ne_id INTEGER REFERENCES adi_ne,
                                            snk_port_id INTEGER REFERENCES adi_port, 
                                            snk_vlan VARCHAR,
                                            cust_srv_type VARCHAR,
                                            wrk_pw_id INTEGER[],
                                            prt_ne_id INTEGER REFERENCES adi_ne,
                                            prt_port_id INTEGER REFERENCES adi_port, 
                                            prt_vlan VARCHAR,
                                            prt_pw_id INTEGER[],
                                            dni_pw_id INTEGER[]);""")
cursor.execute("""CREATE TABLE adi_ces (id INTEGER PRIMARY KEY, 
                                            name VARCHAR,
                                            service_id VARCHAR,
                                            protect_type1 INTEGER,
                                            protect_type2 INTEGER,
                                            src_ne_id INTEGER REFERENCES adi_ne,
                                            src_port_id INTEGER REFERENCES adi_port, 
                                            src_high_path VARCHAR,
                                            src_low_path VARCHAR,
                                            snk_ne_id INTEGER REFERENCES adi_ne,
                                            snk_port_id INTEGER REFERENCES adi_port, 
                                            snk_high_path VARCHAR,
                                            snk_low_path VARCHAR,
                                            cust_srv_type VARCHAR,
                                            wrk_pw_id INTEGER[],
                                            prt_ne_id INTEGER REFERENCES adi_ne,
                                            prt_port_id INTEGER REFERENCES adi_port, 
                                            prt_high_path VARCHAR,
                                            prt_low_path VARCHAR,
                                            prt_pw_id INTEGER[],
                                            dni_pw_id INTEGER[]);""")
cursor.execute("COMMIT;")

print("len(list_Tunnel)", len(list_Tunnel))
print(list_Tunnel)

insert_in_table(cursor, list_NE, "INSERT INTO adi_ne (id , ne_name) VALUES (", db_packet_len)
insert_in_table(cursor, list_Port, "INSERT INTO adi_port (id , port) VALUES (", db_packet_len)
insert_in_table(cursor, list_Port_Description, """INSERT INTO adi_description (id, ne_id,
                                                                    port_id, description) VALUES (""", db_packet_len)
insert_in_table(cursor, list_Tunnel, """INSERT INTO adi_tunnel (id,
                                            tunnel,
                                            tunnel_id,
                                            direction,
                                            src_ne_id,
                                            src_port_id, 
                                            snk_ne_id,
                                            snk_port_id, 
                                            transit_ne_id,
                                            transit_in_port_id, 
                                            transit_out_port_id 
                                            ) VALUES (""", db_packet_len)
insert_in_table(cursor, list_TNL_GRP, """INSERT INTO adi_group (id,
                                            aps_name,
                                            src_ne_id,
                                            snk_ne_id,
                                            wrk_fwd_wrk,
                                            prt_fwd_prt,
                                            bwd_wrk,
                                            bwd_prt
                                            ) VALUES (""", db_packet_len)

insert_in_table(cursor, list_PW, """INSERT INTO adi_pw (id, right_ne_id,
                                                                    left_ne_id, pw_id, tunnels) VALUES (""", db_packet_len)

insert_in_table(cursor, list_ETH, """INSERT INTO adi_eth (id,
                                            name,
                                            service_id,
                                            protect_type1,
                                            protect_type2,
                                            src_ne_id,
                                            src_port_id, 
                                            src_vlan,
                                            snk_ne_id,
                                            snk_port_id, 
                                            snk_vlan,
                                            cust_srv_type,
                                            wrk_pw_id,
                                            prt_ne_id,
                                            prt_port_id, 
                                            prt_vlan,
                                            prt_pw_id,
                                            dni_pw_id) VALUES (""", db_packet_len)
insert_in_table(cursor, list_CES, """INSERT INTO adi_ces (id,
                                            name,
                                            service_id,
                                            protect_type1,
                                            protect_type2,
                                            src_ne_id,
                                            src_port_id, 
                                            src_high_path,
                                            src_low_path,
                                            snk_ne_id,
                                            snk_port_id, 
                                            snk_high_path,
                                            snk_low_path,
                                            cust_srv_type,
                                            wrk_pw_id,
                                            prt_ne_id,
                                            prt_port_id, 
                                            prt_high_path,
                                            prt_low_path,
                                            prt_pw_id,
                                            dni_pw_id) VALUES (""", db_packet_len)


cursor.execute("select * from adi_ces;")
try:
    data = cursor.fetchall()
    for row in data:
        print(row)
except psycopg2.ProgrammingError:
    print("No data to out")
print("len(list_TNL_GRP)", len(list_TNL_GRP))
print(list_TNL_GRP)


'''conn = psycopg2.connect(host=namespace.host, user=namespace.user, password=namespace.password, dbname='postgres')
cursor = conn.cursor()
cursor.execute("SELECT now();")
for row in cursor:
    print(row)

cursor.execute("COMMIT;")
'''
