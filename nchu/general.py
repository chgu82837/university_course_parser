import json
import requests
from bs4 import BeautifulSoup


def to_json(subjects, debug=False):
    items = ['obligatory', 'code', 'title', 'trash1', 'year', 'credits',
             'hours', 'trash2', 'time', 'trash3', 'location', 'trash4',
             'professor', 'trash5', 'department', 'number', 'number_selected',
             'trash6', 'number_available', 'language', 'note']

    data = {}
    flag = False
    for sub in subjects:
        for i in range(len(sub)):
            if sub[i].text.strip() == '必選別':
                flag = True
                break
            data[items[i]] = sub[i].text.strip()

        if flag is True:
            flag = False
            continue

        # Normalize particular data
        data['grade'] = data['code'][0]

        # Remove useless data
        useless = ['number_selected', 'number_available',
                   'trash1', 'trash2', 'trash3', 'trash4',
                   'trash5', 'trash6']
        for item in useless:
            data.pop(item)

        if debug is True:
            print(data)

        json_data = json.dumps(data, ensure_ascii=False)
        with open('nchu.json', 'a') as f:
            f.write('{},'.format(json_data))


def correct_json():
    with open('nchu.json', 'r') as f:
        raw = f.readline()
    with open('nchu.json', 'w') as f:
        f.write('[' + raw[:-1] + ']')


def connect(debug=False):
    url = 'https://onepiece.nchu.edu.tw/cofsys/plsql/crseqry_gene'
    html = requests.get(url)
    soup = BeautifulSoup(html.text)

    form = soup.findAll('select', attrs={'name': 'v_group'})
    regForm = str(form[0]).split('value="')
    deptID = [name[0:4].strip() for name in regForm[2:]]

    for ID in deptID:
        payload = {'v_group': ID}
        response = requests.post(url, data=payload)
        soup = BeautifulSoup(response.text)
        td = soup.findAll('td')[105:-2]

        if debug is True:
            # Print the length of courses
            print(ID, len(td) // 20)

        subjects = []
        for i in range(len(td) // 21):
            if i == len(td) // 21:
                subjects.append(td[-21:])
                break
            else:
                p = 21 * i
                subjects.append(td[p + 1:p + 22])

        to_json(subjects)

if __name__ == '__main__':
    connect(debug=True)
    correct_json()
