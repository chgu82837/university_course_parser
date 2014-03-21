import json
import requests
from bs4 import BeautifulSoup

def normalize(raw_time):
    times = raw_time.split('[')[1:]
    for i in range(len(times)):
        times[i] = times[i].replace(']', '')

    to_word = {1: '1', 2: '2', 3: '3', 4: '4', 5: 'N',
               6: '5', 7: '6', 8: '7', 9: '8', 10: '9',
               11: 'A', 12: 'B', 13: 'C', 14: 'D'}
    to_time = {'0': 1, '1': 1, '2': 2, '3': 3, '4': 4, 'N': 5,
               '5': 6, '6': 7, '7': 8, '8': 9, '9': 10,
               'A': 11, 'B': 12, 'C': 13, 'D': 14}

    result = ''
    for time in times:
        raw = time.split('~')
        result += raw[0][0]

        start = to_time[raw[0][-1]]
        end = to_time[raw[1]] if len(raw) > 1 else to_time[raw[0][-1]]
        for i in range(start, end + 1):
            result += to_word[i]

        result += ',' if times[-1] != time else ''

    return result


def to_json(subjects):
    items = ['department', 'dept_code', 'serial', 'code', 'class_code',
             'class', 'grade', 'field', 'team', 'language', 'title', 'obligatory',
             'credits', 'professor', 'number_selected', 'number_left', 'time',
             'location', 'note', 'previous', 'experts', 'property', 'crossfield']

    data = {}
    for sub in subjects:
        # Remove spaces
        for i in range(len(sub)):
            data[items[i]] = sub[i].text.replace(' ', '').strip()

        # Normalize particular data
        data['code'] = '{0}-{1} {2}'.format(data['dept_code'], data['serial'], data['code'])
        data['time'] = normalize(data['time'])

        # Remove useless data
        useless = ['dept_code', 'serial', 'class_code',
                   'field', 'number_selected', 'crossfield',
                   'property', 'experts']
        for item in useless:
            data.pop(item)

        print(data)

        json_data = json.dumps(data, ensure_ascii=False)
        with open('ncku.json', 'a') as f:
            f.write('{0},'.format(json_data))


def connect():
    depts = ['A2', 'A3', 'A4', 'A5', 'A6', 'AA', 'AH', 'AN', 'C0', 'XZ', 'A1',
             'A7', 'A8', 'A9', 'AG', 'B1', 'K1', 'B2', 'K2', 'B3', 'K3', 'B5',
             'K5', 'K4', 'C1', 'L1', 'C2', 'L2', 'C3', 'L3', 'C4', 'L4', 'F8',
             'L7', 'LA', 'VF', 'E0', 'E1', 'N1', 'E3', 'N3', 'E4', 'N4', 'E5',
             'N5', 'E6', 'N6', 'E8', 'N8', 'E9', 'N9', 'F0', 'F1', 'P1', 'F4',
             'P4', 'F5', 'P5', 'F6', 'P6', 'F9', 'P8', 'N0', 'NA', 'NB', 'NC',
             'Q4', 'H1', 'R1', 'H2', 'R2', 'H3', 'R3', 'H4', 'R4', 'H5', 'R5',
             'R0', 'R6', 'R7', 'R8', 'R9', 'RB', 'RD', 'RZ', 'I2', 'T2', 'I3',
             'T3', 'I5', 'I6', 'T6', 'I7', 'T7', 'I8', 'S0', 'S1', 'S2', 'S3',
             'S4', 'S5', 'S6', 'S7', 'S8', 'S9', 'SA', 'T1', 'T4', 'T8', 'T9',
             'TA', 'TB', 'TC', 'D2', 'U2', 'U6', 'D4', 'D5', 'U5', 'D8', 'U7',
             'U1', 'U3', 'E2', 'N2', 'F7', 'P7', 'ND', 'P9', 'Q1', 'Q1', 'Q3',
             'Q5', 'Q6', 'Q7', 'V6', 'V8', 'V9', 'VA', 'VB', 'VC', 'VD', 'VE',
             'VG', 'VH', 'VJ', 'VK', 'E7', 'N7', 'F2', 'P2', 'F3', 'P3', 'PA',
             'C5', 'L5', 'L6', 'L8', 'Z0' 'Z1', 'Z2', 'Z3']

    for dept in depts:
        url = 'http://course-query.acad.ncku.edu.tw/qry/qry001.php?dept_no={0}'.format(dept)
        html = requests.get(url)
        html.encoding = 'utf-8'
        soup = BeautifulSoup(html.text)
        td = soup.find_all('td')

        print(dept, len(td))
        subjects = []
        for i in range(len(td) // 23 - 1):
            if i == len(td) // 23 - 1:
                subjects.append(td[-23:])
                break
            else:
                p = 23 * i
                subjects.append(td[p:p + 23])

        to_json(subjects)

if __name__ == '__main__':
    connect()
