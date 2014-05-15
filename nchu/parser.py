import json
import requests
from bs4 import BeautifulSoup


class department():
    def __init__(self):
        self.items = ['obligatory', 'code', 'title', 'previous', 'year', 'credits',
                      'hours', 'prac_hours', 'time', 'prac_time', 'location',
                      'prac_location', 'professor', 'prac_professor', 'department',
                      'number', 'number_outer_dept', 'number_available', 'language',
                      'note']

        self.useless = ['prac_time', 'hours', 'prac_hours',
                        'prac_professor', 'prac_location',
                        'number', 'number_outer_dept', 'number_available']

    def _to_json(self, subjects):
        data = {}
        for sub in subjects:
            for i in range(len(sub)):
                data[self.items[i]] = sub[i].text.strip()

            # Normalize particular data
            if data['obligatory'] == '必選別':
                data = {}
                continue
            print(data['obligatory'])
            data['time'] += data['prac_time']
            data['professor'] += data['prac_professor']
            data['location'] += data['prac_location']
            data['grade'] = data['code'][0]

            # Remove useless data
            for item in self.useless:
                data.pop(item)

            json_data = json.dumps(data, ensure_ascii=False)
            with open('nchu.json', 'a') as json_file:
                json_file.write('{},'.format(json_data))

            data = {}

    def _correct_json(self):
        with open('nchu.json', 'r') as json_file:
            raw = json_file.readline()
        with open('nchu.json', 'w') as json_file:
            json_file.write('[' + raw[:-1] + ']')

    def _connect(self):
        url = 'https://onepiece.nchu.edu.tw/cofsys/plsql/crseqry_home'
        html = requests.get(url)
        soup = BeautifulSoup(html.text)

        dept_names = soup.findAll('select', attrs={'name': 'v_dept'})
        reg_dept_names = str(dept_names[0]).split('>')
        dept_id = [name[0:4].strip() for name in reg_dept_names[2:48]]

        for ID in dept_id:
            payload = {'v_dept': ID}
            response = requests.post(url, data=payload)
            soup = BeautifulSoup(response.text)
            td = soup.findAll('td')[106:-5]

            subjects = []
            for i in range(len(td) // 20):
                if i == len(td) // 20:
                    subjects.append(td[-20:])
                    break
                else:
                    p = 20 * i
                    subjects.append(td[p + 1:p + 21])

            self._to_json(subjects)

    def parse(self):
        self._connect()
        self._correct_json()


class general():
    def __init__(self):
        self.items = ['obligatory', 'code', 'title', 'trash1', 'year', 'credits',
                      'hours', 'trash2', 'time', 'trash3', 'location', 'trash4',
                      'professor', 'trash5', 'department', 'number', 'number_selected',
                      'trash6', 'number_available', 'language', 'note']

        self.useless = ['number_selected', 'number_available',
                        'trash1', 'trash2', 'trash3', 'trash4',
                        'trash5', 'trash6']

    def _to_json(self, subjects):
        data = {}
        for sub in subjects:
            for i in range(len(sub)):
                if sub[i].text.strip() == '必選別':
                    break
                data[self.items[i]] = sub[i].text.strip()

            # Normalize particular data
            data['grade'] = data['code'][0]

            # Remove useless data
            for item in self.useless:
                data.pop(item)

            json_data = json.dumps(data, ensure_ascii=False)
            with open('nchu.json', 'a') as f:
                f.write('{},'.format(json_data))

    def _correct_json(self):
        with open('nchu.json', 'r') as f:
            raw = f.readline()
        with open('nchu.json', 'w') as f:
            f.write('[' + raw[:-1] + ']')

    def _connect(self):
        url = 'https://onepiece.nchu.edu.tw/cofsys/plsql/crseqry_gene'
        html = requests.get(url)
        soup = BeautifulSoup(html.text)

        form = soup.findAll('select', attrs={'name': 'v_group'})
        reg_form = str(form[0]).split('value="')
        dept_id = [name[0:4].strip() for name in reg_form[2:]]

        for ID in dept_id:
            payload = {'v_group': ID}
            response = requests.post(url, data=payload)
            soup = BeautifulSoup(response.text)
            td = soup.findAll('td')[105:-2]

            subjects = []
            for i in range(len(td) // 21):
                if i == len(td) // 21:
                    subjects.append(td[-21:])
                    break
                else:
                    p = 21 * i
                    subjects.append(td[p + 1:p + 22])

            self._to_json(subjects)

    def parse(self):
        self._connect()
        self._correct_json()


def parse(year):
    d = department()
    d.parse()
    g = general()
    g.parse()

if __name__ == '__main__':
    parse(1022)
