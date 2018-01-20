import json
import sys

import xlrd
from itertools import groupby
from os import listdir
from re import match

''' Опрделяем номера столбцов для нужных полей на листе PWE3 ETH'''


def get_columns_num(line, sheet_dict):
    for i in range(0, len(line), 1):
        if line[i] in sheet_dict:
            d2 = {line[i]: i}
            sheet_dict.update(d2)


'''Добавляем элемент в список проверкой дубликатов, возвращаем индекс'''


def add_list_with_check_of_double(list_to_add: list, element: object) -> object:
    try:
        return list_to_add.index(element)
    except ValueError:
        list_to_add.append(element)
        return len(list_to_add) - 1


def add_list_pw(line, column_list, list_pw, columns):
    service_pw_list = [str(line[columns.get(column_list[0])]).splitlines(),
                       str(line[columns.get(column_list[1])]).splitlines(),
                       str(line[columns.get(column_list[2])]).splitlines(),
                       str(line[columns.get(column_list[3])]).splitlines()]
    list_pw_index = []
    '''Проверяем количество туннелей в PW. Может быть два unidirectional'''
    for i in range(len(service_pw_list[0])):
        try:
            tmp_list = []

            if range(len(service_pw_list[3])) == range(len(service_pw_list[0]) * 2):
                tmp_list.extend([service_pw_list[3][i * 2], service_pw_list[3][i * 2 + 1]])
            else:
                if (len(service_pw_list[3])) != 0:
                    print('Некорректное количество туннелей в PW', len(list_pw), service_pw_list)
                    tmp_list.append(service_pw_list[3][i])
            list_pw.append([add_list_with_check_of_double(list_NE, service_pw_list[0][i]),
                            add_list_with_check_of_double(list_NE, service_pw_list[1][i]), service_pw_list[2][i],
                            [el for el, _ in groupby(tmp_list)]])
        except:
            print('Не удалось разобрать PW', len(list_pw), service_pw_list)
        list_pw_index.append(len(list_pw) - 1)
    return list_pw_index


'''
def add_list_pw_CES(line, column_list, list_PW):
    service_PW_list = [str(line[CES_columns.get(column_list[0])]).splitlines(),
                       str(line[CES_columns.get(column_list[1])]).splitlines(),
                       str(line[CES_columns.get(column_list[2])]).splitlines(),
                       [el for el, _ in groupby(str(line[CES_columns.get(column_list[3])]).splitlines())]]
    list_PW_index = []
    for i in range(len(service_PW_list[0])):
        list_PW.append([add_list_with_check_of_double(list_NE, service_PW_list[0][i]),
                        add_list_with_check_of_double(list_NE, service_PW_list[1][i]), service_PW_list[2][i],
                         service_PW_list[3][i]])
        list_PW_index.append(len(list_PW) - 1)
    return list_PW_index
'''


def show_eth_service(list_eth_service, list_eth_service_index):
    print(list_eth_service[list_eth_service_index][1], list_eth_service[list_eth_service_index][0],
          list_eth_service[list_eth_service_index][2], list_eth_service[list_eth_service_index][10])
    print(list_NE[list_eth_service[list_eth_service_index][4]], list_Port[list_eth_service[list_eth_service_index][5]],
          list_eth_service[list_eth_service_index][6])
    # Нужно вывести дескрипшен
    print(list_NE[list_eth_service[list_eth_service_index][7]], list_Port[list_eth_service[list_eth_service_index][8]],
          list_eth_service[list_eth_service_index][9])
    # Нужно вывести дескрипшен
    print('WRK PW')
    for el in list_eth_service[list_eth_service_index][11]:
        print('\t', el, list_NE[list_PW[el][0]], list_NE[list_PW[el][1]], list_PW[el][2], list_PW[el][3])
    if list_eth_service[list_eth_service_index][12] != '':
        print('PRT PW')
        print('\t', list_NE[list_eth_service[list_eth_service_index][12]],
              list_Port[list_eth_service[list_eth_service_index][13]],
              list_eth_service[list_eth_service_index][14])
        for el in list_eth_service[list_eth_service_index][15]:
            print('\t', el, list_NE[list_PW[el][0]], list_NE[list_PW[el][1]], list_PW[el][2], list_PW[el][3])
        print('DNI PW')
        for el in list_eth_service[list_eth_service_index][16]:
            print('\t', el, list_NE[list_PW[el][0]], list_NE[list_PW[el][1]], list_PW[el][2], list_PW[el][3])
    print()


def show_ces_service(list_ces_service, list_ces_service_index):
    print(list_ces_service[list_ces_service_index][1], list_ces_service[list_ces_service_index][0],
          list_ces_service[list_ces_service_index][2], list_ces_service[list_ces_service_index][10])
    print(list_NE[list_ces_service[list_ces_service_index][4]], list_Port[list_ces_service[list_ces_service_index][5]],
          list_ces_service[list_ces_service_index][6], list_ces_service[list_ces_service_index][7])
    # Нужно вывести дескрипшен
    print(list_NE[list_ces_service[list_ces_service_index][8]], list_Port[list_ces_service[list_ces_service_index][9]],
          list_ces_service[list_ces_service_index][10])
    # Нужно вывести дескрипшен
    print('WRK PW')
    for el in list_ces_service[list_ces_service_index][13]:
        print('\t', el, list_NE[list_PW[el][0]], list_NE[list_PW[el][1]], list_PW[el][2], list_PW[el][3])
    if list_ces_service[list_ces_service_index][18] != '':
        print('PRT PW')
        print('\t', list_NE[list_ces_service[list_ces_service_index][14]],
              list_Port[list_ces_service[list_ces_service_index][15]], list_ces_service[list_ces_service_index][16],
              list_ces_service[list_ces_service_index][17])
        for el in list_ces_service[list_ces_service_index][18]:
            print('\t', el, list_NE[list_PW[el][0]], list_NE[list_PW[el][1]], list_PW[el][2], list_PW[el][3])
        print('DNI PW')
        for el in list_ces_service[list_ces_service_index][19]:
            print('\t', el, list_NE[list_PW[el][0]], list_NE[list_PW[el][1]], list_PW[el][2], list_PW[el][3])
    print()


def search_in_list_tunnel(_list: list, tunnel: object) -> object:
    for elem in _list:
        if str(elem[0]) == str(tunnel):
            return _list.index(elem)
    return None


ETH_columns = dict.fromkeys(['ServiceName', 'ServiceID', 'ProtectType1', 'ProtectType2', 'SrcNe', 'SrcPort',
                             'srcPortDescribe', 'SrcVlan', 'SnkNe', 'SnkPort', 'snkPortDescribe', 'SnkVlan',
                             'CustomerSvrType', 'PwLeftNe', 'PwRightNe', 'PWID', 'Tunnel', 'ApsPwLeftNe',
                             'ApsPwRightNe', 'APSPWID', 'APSTunnel'], 0)

CES_columns = dict.fromkeys(['ServiceName', 'ServiceID', 'ProtectType1', 'ProtectType2', 'SrcNe', 'SrcPort',
                             'srcPortDescribe', 'SrcHighPath', 'SrcLowPath', 'SnkNe', 'SnkPort', 'snkPortDescribe',
                             'SnkHighPath', 'SnkLowPath', 'CustomerSvrType', 'PwLeftNe', 'PwRightNe', 'PWID', 'Tunnel',
                             'ApsPwLeftNe', 'ApsPwRightNe', 'APSPWID', 'APSTunnel'], 0)

TNL_columns = dict.fromkeys(['Tunnel', 'TunnelID', 'Direction', 'SrcNe', 'SrcPort', 'SnkNe', 'SnkPort', 'TransitNE',
                             'TransitInPort', 'TransitOutPort'], 0)

TNL_GRP_columns = dict.fromkeys(['ApsName', 'SrcNe', 'SnkNe', 'Role', 'Tunnel'], 0)

PRT_type1 = {'Protection-Free': 0, 'PW APS (single source and dual sink)': 1, 'PW APS (dual source and single sink)': 2,
             'PW backup': 3, 'PW APS (single source and single sink)': 4}

PRT_type2 = {'Working': 0, 'Protection': 1}

TNL_role = {'Working': 0, 'Protecting': 1, 'Forward Working': 0, 'Forward Protecting': 1, 'Backward Working': 2,
            'Backward Protecting': 3}

list_NE = []
list_Port = []
list_Port_Description = []
list_PW = []
list_ETH_Service = []
list_CES_Service = []
list_Tunnel = []
list_TNL_GRP = []
db_name = ""

if __name__ == "__main__":
    if len(sys.argv) > 1:
        db_path = sys.argv[1]
        print("DB path = ", db_path)
    else:
        db_path = ''
        exit("Missing param db path")

list_File = listdir(db_path)
print(list_File)

for f in list_File:

    db_date = match(r'(Tunnel_APS)_(\d\d\d\d_\d\d_\d\d_\d\d_\d\d_\d\d).*', f)
    if db_date is not None:
        db_name = 'ADI_'
        db_name = db_name + db_date.group(2)
        print('db_name = ' + db_name)
        break

for f in list_File:
    if match(r'^(Tunnel_APS|Pwe3Service)_(\d\d\d\d_\d\d_\d\d_\d\d_\d\d_\d\d)_(\d+)\.(xls)$', f) is None:
        print('Not .xls file:', f)
        continue
    print('Reading ', f)
    file_name = db_path + '\\' + f
    rb = xlrd.open_workbook(file_name)
    sheet = rb.sheet_by_name('PWE3 ETH')
    row = sheet.row_values(4)
    """ Опрделяем номера столбцов для нужных полей на листе PWE3 ETH"""
    get_columns_num(row, ETH_columns)

    '''Обрабатываем PWE3 ETH'''
    for rownum in range(8, sheet.nrows - 2, 2):
        row = sheet.row_values(rownum)
        row2 = sheet.row_values(rownum + 1)
        index_SrcPort = add_list_with_check_of_double(list_Port, str(row[ETH_columns.get('SrcPort')]))
        #    print('{0} - {1} - {2}'.format(index_SrcPort, list_Port[index_SrcPort], row[ETH_columns.get('SrcPort')]))
        index_SnkPort = add_list_with_check_of_double(list_Port, str(row[ETH_columns.get('SnkPort')]))

        '''Добавляем NE с проверкой дубликатов, получаем индекс'''
        index_SrcNE = add_list_with_check_of_double(list_NE, str(row[ETH_columns.get('SrcNe')]))
        index_SnkNE = add_list_with_check_of_double(list_NE, str(row[ETH_columns.get('SnkNe')]))

        '''Добавляем дескрипшены с проверкой дубликатов, получаем индекс'''
        if row[ETH_columns.get('srcPortDescribe')] != '':
            index_WRK_Src_port_desc = add_list_with_check_of_double(list_Port_Description,
                                                                    [index_SrcNE, index_SrcPort,
                                                                     str(row[ETH_columns.get('srcPortDescribe')])])
        if row[ETH_columns.get('snkPortDescribe')] != '':
            index_WRK_Snk_port_desc = add_list_with_check_of_double(list_Port_Description,
                                                                    [index_SnkNE, index_SnkPort,
                                                                     str(row[ETH_columns.get('snkPortDescribe')])])

        '''Добавляем PW, без проверки дубликатов, получаем индекс'''
        list_PW_index = add_list_pw(row, ['PwLeftNe', 'PwRightNe', 'PWID', 'Tunnel'], list_PW, ETH_columns)

        '''Добавляем сервис, вносим NE индекс, порт индекс и PW индекс'''
        list_ETH_Service.append([str(row[ETH_columns.get('ServiceName')]),
                                 str(row[ETH_columns.get('ServiceID')]),
                                 PRT_type1.get(str(row[ETH_columns.get('ProtectType1')])),
                                 PRT_type2.get(str(row[ETH_columns.get('ProtectType2')])),
                                 index_SrcNE,
                                 index_SrcPort,
                                 str(row[ETH_columns.get('SrcVlan')]),
                                 index_SnkNE,
                                 index_SnkPort,
                                 str(row[ETH_columns.get('SnkVlan')]),
                                 str(row[ETH_columns.get('CustomerSvrType')]),
                                 list_PW_index
                                 ])
        list_ETH_Service_index = len(list_ETH_Service) - 1
        #    print(list_ETH_Service[list_ETH_Service_index])

        '''Если сервис с защитой, добавляем PRT и DNI'''
        try:
            if list_ETH_Service[list_ETH_Service_index][2] > 0:
                '''PW APS (single source and dual sink)'''
                if list_ETH_Service[list_ETH_Service_index][2] == 1:
                    index_PRT_SnkPort = add_list_with_check_of_double(list_Port, str(row2[ETH_columns.get('SnkPort')]))
                    index_PRT_SnkNE = add_list_with_check_of_double(list_NE, str(row2[ETH_columns.get('SnkNe')]))
                    list_ETH_Service[list_ETH_Service_index].append(index_PRT_SnkNE)
                    list_ETH_Service[list_ETH_Service_index].append(index_PRT_SnkPort)
                    list_ETH_Service[list_ETH_Service_index].append(str(row[ETH_columns.get('SnkVlan')]))

                    if row2[ETH_columns.get('snkPortDescribe')] != '':
                        index_PRT_Snk_port_desc = add_list_with_check_of_double(list_Port_Description,
                                                                                [index_PRT_SnkNE, index_PRT_SnkPort,
                                                                                 str(row[ETH_columns.get(
                                                                                     'snkPortDescribe')])])
                if list_ETH_Service[list_ETH_Service_index][2] == 2:
                    index_PRT_SrcPort = add_list_with_check_of_double(list_Port, str(row2[ETH_columns.get('SrcPort')]))
                    index_PRT_SrcNE = add_list_with_check_of_double(list_NE, str(row2[ETH_columns.get('SrcNe')]))
                    list_ETH_Service[list_ETH_Service_index].append(index_PRT_SrcNE)
                    list_ETH_Service[list_ETH_Service_index].append(index_PRT_SrcPort)
                    list_ETH_Service[list_ETH_Service_index].append(str(row[ETH_columns.get('SrcVlan')]))
                    if row2[ETH_columns.get('srcPortDescribe')] != '':
                        index_PRT_Src_port_desc = add_list_with_check_of_double(list_Port_Description,
                                                                                [index_PRT_SrcNE, index_PRT_SrcPort,
                                                                                 str(row[ETH_columns.get(
                                                                                     'srcPortDescribe')])])

                if list_ETH_Service[list_ETH_Service_index][2] == 3:
                    print('Дописать обработчик PW backup', list_ETH_Service[list_ETH_Service_index])
                if list_ETH_Service[list_ETH_Service_index][2] == 4:
                    print('Дописать обработчик PW APS (single source and single sink)',
                          list_ETH_Service[list_ETH_Service_index])
                    print('Дописать обработчик PW APS (single source and single sink)',
                          list_ETH_Service[list_ETH_Service_index])
                '''Добавляем PW, без проверки дубликатов, получаем индекс'''
                list_PRT_PW_index = add_list_pw(row2, ['PwLeftNe', 'PwRightNe', 'PWID', 'Tunnel'], list_PW, ETH_columns)

                list_DNI_PW_index = add_list_pw(row2, ['ApsPwLeftNe', 'ApsPwRightNe', 'APSPWID', 'APSTunnel'], list_PW,
                                                ETH_columns)
                list_ETH_Service[list_ETH_Service_index].append(list_PRT_PW_index)
                list_ETH_Service[list_ETH_Service_index].append(list_DNI_PW_index)
            else:
                list_ETH_Service[list_ETH_Service_index].append('')
                list_ETH_Service[list_ETH_Service_index].append('')
                list_ETH_Service[list_ETH_Service_index].append('')
                list_ETH_Service[list_ETH_Service_index].append('')

        except:
            print('Необработанный тип сервиса', list_ETH_Service[list_ETH_Service_index])
    '''Вывод ETH сервиса'''

    sheet = rb.sheet_by_name('PWE3 CES')
    row = sheet.row_values(4)
    """ Опрделяем номера столбцов для нужных полей на листе PWE3 CES"""
    get_columns_num(row, CES_columns)

    '''Обрабатываем PWE3 CES'''
    for rownum in range(8, sheet.nrows - 2, 2):
        row = sheet.row_values(rownum)
        row2 = sheet.row_values(rownum + 1)
        index_SrcPort = add_list_with_check_of_double(list_Port, str(row[CES_columns.get('SrcPort')]))
        # print('{0} - {1} - {2}'.format(index_SrcPort, list_Port[index_SrcPort], row[CES_columns.get('SrcPort')]))
        index_SnkPort = add_list_with_check_of_double(list_Port, str(row[CES_columns.get('SnkPort')]))

        '''Добавляем NE с проверкой дубликатов, получаем индекс'''
        index_SrcNE = add_list_with_check_of_double(list_NE, str(row[CES_columns.get('SrcNe')]))
        index_SnkNE = add_list_with_check_of_double(list_NE, str(row[CES_columns.get('SnkNe')]))

        '''Добавляем дескрипшены с проверкой дубликатов, получаем индекс'''
        if row[CES_columns.get('srcPortDescribe')] != '':
            index_WRK_Src_port_desc = add_list_with_check_of_double(list_Port_Description,
                                                                    [index_SrcNE, index_SrcPort,
                                                                     str(row[CES_columns.get('srcPortDescribe')])])
        if row[CES_columns.get('snkPortDescribe')] != '':
            index_WRK_Snk_port_desc = add_list_with_check_of_double(list_Port_Description,
                                                                    [index_SnkNE, index_SnkPort,
                                                                     str(row[CES_columns.get('snkPortDescribe')])])

        '''Добавляем PW, без проверки дубликатов, получаем индекс'''
        list_PW_index = add_list_pw(row, ['PwLeftNe', 'PwRightNe', 'PWID', 'Tunnel'], list_PW, CES_columns)

        '''Добавляем сервис, вносим NE индекс, порт индекс и PW индекс'''
        list_CES_Service.append([str(row[CES_columns['ServiceName']]),
                                 str(row[CES_columns['ServiceID']]),
                                 PRT_type1.get(str(row[CES_columns['ProtectType1']])),
                                 PRT_type2.get(str(row[CES_columns['ProtectType2']])),
                                 index_SrcNE,
                                 index_SrcPort,
                                 str(row[CES_columns['SrcHighPath']]),
                                 str(row[CES_columns['SrcLowPath']]),
                                 index_SnkNE,
                                 index_SnkPort,
                                 str(row[CES_columns['SnkHighPath']]),
                                 str(row[CES_columns['SnkLowPath']]),
                                 str(row[CES_columns['CustomerSvrType']]),
                                 list_PW_index
                                 ])
        list_CES_Service_index = len(list_CES_Service) - 1
        #    print(list_CES_Service[list_CES_Service_index])

        '''Если сервис с защитой, добавляем PRT и DNI'''
        if list_CES_Service[list_CES_Service_index][2] > 0:
            '''PW APS (single source and dual sink)'''
            if list_CES_Service[list_CES_Service_index][2] == 1:
                index_PRT_SnkPort = add_list_with_check_of_double(list_Port, str(row2[CES_columns.get('SnkPort')]))
                index_PRT_SnkNE = add_list_with_check_of_double(list_NE, str(row2[CES_columns.get('SnkNe')]))
                list_CES_Service[list_CES_Service_index].append(index_PRT_SnkNE)
                list_CES_Service[list_CES_Service_index].append(index_PRT_SnkPort)
                list_CES_Service[list_CES_Service_index].append(str(row[CES_columns.get('SnkHighPath')]))
                list_CES_Service[list_CES_Service_index].append(str(row[CES_columns.get('SnkLowPath')]))

                if row2[CES_columns.get('snkPortDescribe')] != '':
                    index_PRT_Snk_port_desc = add_list_with_check_of_double(list_Port_Description,
                                                                            [index_PRT_SnkNE, index_PRT_SnkPort,
                                                                             str(row[CES_columns.get(
                                                                                 'snkPortDescribe')])])
            if list_CES_Service[list_CES_Service_index][2] == 2:
                index_PRT_SrcPort = add_list_with_check_of_double(list_Port, str(row2[CES_columns.get('SrcPort')]))
                index_PRT_SrcNE = add_list_with_check_of_double(list_NE, str(row2[CES_columns.get('SrcNe')]))
                list_CES_Service[list_CES_Service_index].append(index_PRT_SrcNE)
                list_CES_Service[list_CES_Service_index].append(index_PRT_SrcPort)
                list_CES_Service[list_CES_Service_index].append(str(row[CES_columns.get('SrcHighPath')]))
                list_CES_Service[list_CES_Service_index].append(str(row[CES_columns.get('SrcLowPath')]))
                if row2[CES_columns.get('srcPortDescribe')] != '':
                    index_PRT_Src_port_desc = add_list_with_check_of_double(list_Port_Description,
                                                                            [index_PRT_SrcNE, index_PRT_SrcPort,
                                                                             str(row[CES_columns.get
                                                                                                 ('srcPortDescribe')])])

            if list_CES_Service[list_CES_Service_index][2] == 3:
                print('Дописать обработчик PW backup')
            if list_CES_Service[list_CES_Service_index][2] == 4:
                print('Дописать обработчик PW APS (single source and single sink)')

            '''Добавляем PW, без проверки дубликатов, получаем индекс'''
            list_PRT_PW_index = add_list_pw(row2, ['PwLeftNe', 'PwRightNe', 'PWID', 'Tunnel'], list_PW, CES_columns)

            list_DNI_PW_index = add_list_pw(row2, ['ApsPwLeftNe', 'ApsPwRightNe', 'APSPWID', 'APSTunnel'], list_PW,
                                            CES_columns)
            list_CES_Service[list_CES_Service_index].append(list_PRT_PW_index)
            list_CES_Service[list_CES_Service_index].append(list_DNI_PW_index)

        else:
            list_CES_Service[list_CES_Service_index].append('')
            list_CES_Service[list_CES_Service_index].append('')
            list_CES_Service[list_CES_Service_index].append('')
            list_CES_Service[list_CES_Service_index].append('')
            list_CES_Service[list_CES_Service_index].append('')
            list_CES_Service[list_CES_Service_index].append('')

    sheet = rb.sheet_by_name('Static CR Tunnel')
    row = sheet.row_values(4)
    ''' Опрделяем номера столбцов для нужных полей на листе Static CR Tunnel'''
    get_columns_num(row, TNL_columns)

    '''Обрабатываем Static CR Tunnel'''
    for rownum in range(8, sheet.nrows - 3):
        row = sheet.row_values(rownum)
        index_SrcPort = add_list_with_check_of_double(list_Port, str(row[TNL_columns.get('SrcPort')]))
        # print('{0} - {1} - {2}'.format(index_SrcPort, list_Port[index_SrcPort], row[TNL_columns.get('SrcPort')]))
        index_SnkPort = add_list_with_check_of_double(list_Port, str(row[TNL_columns.get('SnkPort')]))

        '''Добавляем NE с проверкой дубликатов, получаем индекс'''
        index_SrcNE = add_list_with_check_of_double(list_NE, str(row[TNL_columns.get('SrcNe')]))
        index_SnkNE = add_list_with_check_of_double(list_NE, str(row[TNL_columns.get('SnkNe')]))

        list_Transit_NE = str(row[TNL_columns.get('TransitNE')]).splitlines()
        index_Transit_NE = []
        for el in list_Transit_NE:
            index_Transit_NE.append(add_list_with_check_of_double(list_NE, el))

        list_TransitInPort = str(row[TNL_columns.get('TransitInPort')]).splitlines()
        index_TransitInPort = []
        for el in list_TransitInPort:
            index_TransitInPort.append(add_list_with_check_of_double(list_NE, el))

        list_TransitOutPort = str(row[TNL_columns.get('TransitOutPort')]).splitlines()
        index_TransitOutPort = []
        for el in list_TransitOutPort:
            index_TransitOutPort.append(add_list_with_check_of_double(list_NE, el))

        list_Tunnel.append((str(row[TNL_columns.get('Tunnel')]),
                            str(row[TNL_columns.get('TunnelID')]),
                            str(row[TNL_columns.get('Direction')]),
                            index_SrcNE,
                            index_SrcPort,
                            index_SnkNE,
                            index_SnkPort,
                            index_Transit_NE,
                            index_TransitInPort,
                            index_TransitOutPort))

    sheet = rb.sheet_by_name('Tunnel Protection Group')
    row = sheet.row_values(4)
    """ Опрделяем номера столбцов для нужных полей на листе Tunnel Protection Group"""
    get_columns_num(row, TNL_GRP_columns)

    '''Обрабатываем Tunnel Protection Group'''
    for rownum in range(8, sheet.nrows - 3):
        row = sheet.row_values(rownum)
        index_SrcNE = []
        index_SnkNE = []
        index_list_Tunnel = []
        try:
            index_SrcNE = list_NE.index(row[TNL_GRP_columns.get('SrcNe')])
        except ValueError:
            print('\t\tОшибка! Нет NE')

        try:
            index_SnkNE = list_NE.index(row[TNL_GRP_columns.get('SnkNe')])
        except ValueError:
            print('\t\tОшибка! Нет NE')

        for el in str(row[TNL_GRP_columns.get('Tunnel')]).splitlines():
            try:
                index_list_Tunnel.append(search_in_list_tunnel(list_Tunnel, el))
            except ValueError:
                print('\t\tОшибка! Нет Tunnel')
                continue

        list_Role = str(row[TNL_GRP_columns.get('Role')]).splitlines()

        list_TNL_GRP.append([str(row[TNL_GRP_columns.get('ApsName')]),
                             index_SrcNE, index_SnkNE, '', '', '', ''])
        index_TNL_GRP = len(list_TNL_GRP) - 1

        for i in range(len(list_Role)):
            list_TNL_GRP[index_TNL_GRP][3 + TNL_role.get(str(list_Role[i]))] = index_list_Tunnel[i]

json.dump(list_NE, open(db_path + '\\' + db_name + '.node', 'w'))
json.dump(list_Port, open(db_path + '\\' + db_name + '.port', 'w'))
json.dump(list_Port_Description, open(db_path + '\\' + db_name + '.description', 'w'))
json.dump(list_PW, open(db_path + '\\' + db_name + '.pw', 'w'))
json.dump(list_ETH_Service, open(db_path + '\\' + db_name + '.eth', 'w'))
json.dump(list_CES_Service, open(db_path + '\\' + db_name + '.ces', 'w'))
json.dump(list_Tunnel, open(db_path + '\\' + db_name + '.tunnel', 'w'))
json.dump(list_TNL_GRP, open(db_path + '\\' + db_name + '.group', 'w'))


