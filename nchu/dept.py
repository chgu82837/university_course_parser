import json
import requests
from bs4 import BeautifulSoup


def to_json(subjects, debug=False):
    items = ['obligatory', 'code', 'title', 'previous', 'year', 'credits',
             'hours', 'prac_hours', 'time', 'prac_time', 'location',
             'prac_location', 'professor', 'prac_professor', 'department',
             'number', 'number_outer_dept', 'number_available', 'language',
             'note']

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
        data['time'] += data['prac_time']
        data['professor'] += data['prac_professor']
        data['location'] += data['prac_location']
        data['grade'] = data['code'][0]

        # Remove useless data
        useless = ['prac_time', 'hours', 'prac_hours',
                   'prac_professor', 'prac_location',
                   'number', 'number_outer_dept', 'number_available']
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
    url = 'https://onepiece.nchu.edu.tw/cofsys/plsql/crseqry_home'
    html = requests.get(url)
    soup = BeautifulSoup(html.text)

    deptNames = soup.findAll('select', attrs={'name': 'v_dept'})
    regDeptNames = str(deptNames[0]).split('>')
    deptID = [name[0:4].strip() for name in regDeptNames[2:48]]

    for ID in deptID:
        payload = {'v_dept': ID}
        response = requests.post(url, data=payload)
        soup = BeautifulSoup(response.text)
        td = soup.findAll('td')[106:-5]

        if debug is True:
            # Print the length of courses
            print(ID, len(td) // 20)

        subjects = []
        for i in range(len(td) // 20):
            if i == len(td) // 20:
                subjects.append(td[-20:])
                break
            else:
                p = 20 * i
                subjects.append(td[p + 1:p + 21])

        to_json(subjects, debug)

if __name__ == '__main__':
    connect(debug=True)
    correct_json()
