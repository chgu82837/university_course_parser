import json
from xlrd import open_workbook

class Parser():
    def __init__(self):
        self.items = ['serial', 'code', 'department', 'team', 'grade',
                      'class', 'language', 'moocs', 'sex', 'title',
                      'eng_title', 'credits', 'obligatory', 'year',
                      'professor', 'location', 'number', 'number_selected',
                      'previous', 'note']

    def __to_num(self, s):
        return {'一': '1', '二': '2', '三': '3', '四': '4',
                '五': '5', '六': '6', '七': '7'}[s]

    def __to_word(self, n):
        return {1: '1', 2: '2', 3: '3', 4: '4', 5: 'N',
                6: '5', 7: '6', 8: '7', 9: '8', 10: '9',
                11: 'A', 12: 'B', 13: 'C', 14: 'D', 15: 'E'}[n]

    def format_time(self, raw_time):
        if raw_time == '':
            return ''

        times = raw_time.split(',')
        result = ''
        for time in times:
            if time == '':
                continue
            time = time.split(' ')
            fmt = self.__to_num(time[0])
            raw = time[1].split('-')
            start = int(raw[0])
            stop = int(raw[1]) if len(raw) > 1 else int(raw[0])
            for i in range(start, stop+1):
                fmt += self.__to_word(i+1 if i > 5 else i)
            result += fmt + ','

        return result[:len(result)-1]

    def filter(self, subject):
        data = {}
        for i in range(len(subject)):
            data[self.items[i]] = subject[i].strip()

        # Normalize particular data
        data['obligatory'] = '必修' if data['obligatory'] == '必' else '選修'
        data['code'] = '{0}-{1}'.format(data['code'], data['serial'])
        data['time'] = self.format_time(data['location'])

        # Remove useless data
        useless = ['team', 'moocs', 'sex', 'eng_title',
                   'number', 'number_selected']
        for item in useless:
            data.pop(item)

        self.__to_json(data)

    def __to_json(self, data):
        json_data = json.dumps(data, ensure_ascii=False)
        with open('ntnu.json', 'a') as json_file:
            json_file.write('{0},'.format(json_data))

    def __correct_json(self):
        with open('ntnu.json', 'r') as json_file:
            raw = json_file.readline()
        with open('ntnu.json', 'w') as json_file:
            json_file.write('[' + raw[:-1] + ']')

    def __open_excel(self, year):
        excel = open_workbook('{0}.xls'.format(year))
        table = excel.sheets()[0]

        nrows = table.nrows
        for i in range(1, nrows):
            subject = []
            colnames = table.row_values(i)
            for col in colnames:
                subject.append(col)

            self.filter(subject)

    def parse(self, year):
        self.__open_excel(year)
        self.__correct_json()
