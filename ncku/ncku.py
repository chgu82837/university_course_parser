import json
import requests
from bs4 import BeautifulSoup


def normalizeTime(raw):
    try:
        int(raw)
        if not(raw):
            return ""
    except ValueError:
        return ""

    words = {5: "N", 10: "A", 11: "B", 12: "C", 13: "D"}
    times = {"N": 5, "A": 10, "B": 11, "C": 12, "D": 13}

    N = ""
    if raw.count("[") > 1:
        raw = raw.split("[")
        tmp = ["", "", ""]
        for i in range(1, 3):
            if raw[i].find("~") >= 0:
                p = raw[i].find("~")
                if raw[i][p - 1] in words.values():
                    if raw[i][p - 1] == "N":
                        N = "N"
                    start = times[raw[p - 1]]
                else:
                    start = int(raw[i][p - 1])
                if raw[i][p + 1] in words.values():
                    end = times[raw[p + 1]] + 1
                else:
                    end = int(raw[i][p + 1]) + 1
                for k in range(start, end):
                    if k >= 10:
                        tmp[i] += words[k]
                    else:
                        tmp[i] += str(k)
                tmp[i] = raw[i][0] + N + tmp[i]
            else:
                tmp[i] = raw[i][0] + raw[i][2:]
        return "{0},{1}".format(tmp[1], tmp[2])
    else:
        p = raw.find("~")
        if p >= 0:
            tmp = ""
            if raw[p - 1] in words.values():
                if raw[p - 1] == "N":
                    N = "N"
                start = times[raw[p - 1]]
            else:
                start = int(raw[p - 1])
            if raw[p + 1] in words.values():
                end = times[raw[p + 1]] + 1
            else:
                end = int(raw[p + 1]) + 1
            for k in range(start, end):
                if k >= 10:
                    tmp += words[k]
                else:
                    tmp += str(k)
            tmp = raw[1] + N + tmp
        else:
            tmp = raw[1] + raw[3:]

        return tmp


def logToJson(subjects):
    data = {}
    for r in subjects:
        # Remove spaces
        for i in range(len(r)):
            data[t[i]] = r[i].text.replace(" ", "")

        # Normalize particular data
        data["code"] = "{0}-{1} {2}".format(data["dept_code"], data["serial"], data["code"])
        data["time"] = normalizeTime(data["time"])
        if data["code"] == "I2-156 I231420":
            data["time"] = "31234N5678"

        # Remove useless data
        useless = ["dept_code", "serial", "class_code",
                   "field", "number_selected", "crossfield",
                   "property", "experts"]
        for item in useless:
            data.pop(item)

        json_data = json.dumps(data, ensure_ascii=False)
        with open("ncku.json", "a") as f:
            f.write("{0},".format(json_data))


t = ["department", "dept_code", "serial", "code", "class_code",
     "class", "grade", "field", "language", "title", "obligatory",
     "credits", "professor", "number_selected", "number_left", "time",
     "location", "note", "previous", "experts", "property", "crossfield"]

d = ["A2", "A3", "A4", "A5", "A6", "AA", "AH", "AN", "C0", "XZ", "A1",
     "A7", "A8", "A9", "AG", "B1", "K1", "B2", "K2", "B3", "K3", "B5",
     "K5", "K4", "C1", "L1", "C2", "L2", "C3", "L3", "C4", "L4", "F8",
     "L7", "LA", "VF", "E0", "E1", "N1", "E3", "N3", "E4", "N4", "E5",
     "N5", "E6", "N6", "E8", "N8", "E9", "N9", "F0", "F1", "P1", "F4",
     "P4", "F5", "P5", "F6", "P6", "F9", "P8", "N0", "NA", "NB", "NC",
     "Q4", "H1", "R1", "H2", "R2", "H3", "R3", "H4", "R4", "H5", "R5",
     "R0", "R6", "R7", "R8", "R9", "RB", "RD", "RZ", "I2", "T2", "I3",
     "T3", "I5", "I6", "T6", "I7", "T7", "I8", "S0", "S1", "S2", "S3",
     "S4", "S5", "S6", "S7", "S8", "S9", "SA", "T1", "T4", "T8", "T9",
     "TA", "TB", "TC", "D2", "U2", "U6", "D4", "D5", "U5", "D8", "U7",
     "U1", "U3", "E2", "N2", "F7", "P7", "ND", "P9", "Q1", "Q1", "Q3",
     "Q5", "Q6", "Q7", "V6", "V8", "V9", "VA", "VB", "VC", "VD", "VE",
     "VG", "VH", "VJ", "VK", "E7", "N7", "F2", "P2", "F3", "P3", "PA",
     "C5", "L5", "L6", "L8", "Z0" "Z1", "Z2", "Z3"]

for dept in d:
    url = "http://course-query.acad.ncku.edu.tw/qry/qry001.php?dept_no={0}".format(dept)
    html = requests.get(url)
    html.encoding = 'utf-8'
    soup = BeautifulSoup(html.text)
    td = soup.find_all("td")

    subjects = []
    for i in range(len(td) // 22 - 1):
        if i == len(td) // 22 - 1:
            subjects.append(td[-22:])
            break
        else:
            p = 22 * i
            subjects.append(td[p:p + 22])

    logToJson(subjects)
