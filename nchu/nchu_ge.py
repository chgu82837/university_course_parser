import json
import requests
from bs4 import BeautifulSoup

def logToJson(subjects):
    data = {}
    for sub in subjects:
        for i in range(len(sub)):
            data[t[i]] = sub[i].text

        # Normalize particular data
        data["time"] += data["prac_time"]
        data["professor"] += data["prac_professor"]
        data["location"] += data["prac_location"]
        data["grade"] = data["code"][0]

        # Remove useless data
        useless = ["prac_time", "hours", "prac_hours",
                    "prac_professor", "prac_location",
                    "number", "number_selected",
                    "number_outer_dept", "number_available"]

        for item in useless:
            data.pop(item)

        json_data = json.dumps(data, ensure_ascii=False)
        with open("nchu.json", "a") as f:
            f.write("{},".format(json_data))

t = ["obligatory", "code", "title", "previous", "year", "credits",
     "hours", "prac_hours", "time", "prac_time", "location",
     "prac_location", "professor", "prac_professor", "department",
     "number", "number_selected", "number_outer_dept", "number_available",
     "language", "note"]

url = "https://onepiece.nchu.edu.tw/cofsys/plsql/crseqry_gene"

html = requests.get(url)
soup = BeautifulSoup(html.text)

form = soup.findAll('form')[2]
deptName = form.text.split('\n')
deptID = []

for text in deptName:
    if len(text.split(' ')) == 2:
        deptID.append(text.split(' ')[0])

for ID in deptID:
    payload = {"v_dept": ID}
    response = requests.post(url, data=payload)
    soup = BeautifulSoup(response.text)
    td = soup.findAll("td")[105:-5]

    subjects = []
    for i in range(len(td) // 21):
        if i == len(td) // 21:
            subjects.append(td[-21:])
            break
        else:
            p = 21 * i
            subjects.append(td[p + 1:p + 22])

    logToJson(subjects)
