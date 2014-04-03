import json
from xlrd import open_workbook

def to_json(subject):
    items = ['serial', 'code', 'department', 'team', 'grade',
             'class', 'language', 'moocs', 'sex', 'title',
             'eng_title', 'credits', 'obligatory', 'year',
             'professor', 'location', 'number', 'number_selected',
             'previous', 'note']

    data = {}
    for i in range(len(subject)):
        data[items[i]] = subject[i]

    # Remove useless data
    useless = ['team', 'moocs', 'sex', 'eng_title',
               'number', 'number_selected']
    for item in useless:
        data.pop(item)

    print(data)

    json_data = json.dumps(data, ensure_ascii=False)
    with open('ntnu.json', 'a') as f:
        f.write('{0},'.format(json_data))


def open_excel():
    excel = open_workbook('export.xls')
    table = excel.sheets()[0]

    nrows = table.nrows
    for i in range(nrows):
        subject = []
        colnames = table.row_values(i)
        for col in colnames:
            subject.append(col)

        to_json(subject)

if __name__ == '__main__':
    open_excel()
