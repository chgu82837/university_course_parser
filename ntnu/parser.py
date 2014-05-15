import json
from xlrd import open_workbook


def _normalize(raw_time):
    if raw_time == '':
        return ''

    times = raw_time.split(',')

    days = {'一': '1', '二': '2', '三': '3', '四': '4',
            '五': '5', '六': '6', '七': '7'}

    to_word = {1: '1', 2: '2', 3: '3', 4: '4', 5: 'N',
               6: '5', 7: '6', 8: '7', 9: '8', 10: '9',
               11: 'A', 12: 'B', 13: 'C', 14: 'D', 15: 'E'}

    for time in times:
        if time == '':
            continue
        time = time.split(' ')
        result = days[time[0]]
        raw = time[1].split('-')
        start = int(raw[0])
        stop = int(raw[1]) if len(raw) > 1 else int(raw[0])
        for i in range(start, stop+1):
            result += to_word[i+1]

    return result


def _to_json(subject, debug=False):
    items = ['serial', 'code', 'department', 'team', 'grade',
             'class', 'language', 'moocs', 'sex', 'title',
             'eng_title', 'credits', 'obligatory', 'year',
             'professor', 'location', 'number', 'number_selected',
             'previous', 'note']

    data = {}
    for i in range(len(subject)):
        data[items[i]] = subject[i].strip()

    # Normalize particular data
    data['obligatory'] = '必修' if data['obligatory'] == '必' else '選修'
    data['code'] = '{0}-{1}'.format(data['code'], data['serial'])
    data['time'] = _normalize(data['location'])

    # Remove useless data
    useless = ['team', 'moocs', 'sex', 'eng_title',
               'number', 'number_selected']
    for item in useless:
        data.pop(item)

    if debug is True:
        print(data)

    json_data = json.dumps(data, ensure_ascii=False)
    with open('ntnu.json', 'a') as json_file:
        json_file.write('{0},'.format(json_data))


def _correct_json():
    with open('ntnu.json', 'r') as json_file:
        raw = json_file.readline()
    with open('ntnu.json', 'w') as json_file:
        json_file.write('[' + raw[:-1] + ']')


def _open_excel(year, debug=False):
    excel = open_workbook('{0}.xls'.format(year))
    table = excel.sheets()[0]

    nrows = table.nrows
    for i in range(1, nrows):
        subject = []
        colnames = table.row_values(i)
        for col in colnames:
            subject.append(col)

        _to_json(subject, debug)


def parse(year, debug=False):
    _open_excel(year, debug)
    _correct_json()

if __name__ == '__main__':
    parse(1022, debug=True)
