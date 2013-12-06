# -*- coding utf-8 -*-
from bs4 import BeautifulSoup
import mechanize
import json
import codecs
import unicodedata
import os


def normalizeTime(raw_time):
    words = {5: "N", 10: "A", 11: "B", 12: "C", 13: "D"}
    times = {"N": 5, "A": 10, "B": 11, "C": 12, "D": 13}
    if not raw_time:
        return ""

    N = ""
    if raw_time.rfind("[") > 0:
        raw_time = raw_time.split("[")
        tmp_time = ["", "", ""]
        for j in range(1, 3):
            if raw_time[j].find("~") >= 0:
                p = raw_time[j].find("~")
                if raw_time[j][p - 1] in words.values():
                    if raw_time[j][p - 1] == "N":
                        N = "N"
                    start = times[raw_time[p - 1]]
                else:
                    start = int(raw_time[j][p - 1])
                if raw_time[j][p + 1] in words.values():
                    end = times[raw_time[p + 1]] + 1
                else:
                    end = int(raw_time[j][p + 1]) + 1
                for k in range(start, end):
                    if k >= 10:
                        tmp_time[j] += words[k]
                    else:
                        tmp_time[j] += str(k)
                tmp_time[j] = raw_time[j][0] + N + tmp_time[j]
            else:
                tmp_time[j] = raw_time[j][0] + raw_time[j][2:]
        return "%s,%s" % (tmp_time[1], tmp_time[2])
    else:
        p = raw_time.find("~")
        if p >= 0:
            tmp_time = ""
            if raw_time[p - 1] in words.values():
                if raw_time[p - 1] == "N":
                    N = "N"
                start = times[raw_time[p - 1]]
            else:
                start = int(raw_time[p - 1])
            if raw_time[p + 1] in words.values():
                end = times[raw_time[p + 1]] + 1
            else:
                end = int(raw_time[p + 1]) + 1
            for k in range(start, end):
                if k >= 10:
                    tmp_time += words[k]
                else:
                    tmp_time += str(k)
            tmp_time = raw_time[1] + N + tmp_time
        else:
            tmp_time = raw_time[1] + raw_time[3:]

        return tmp_time


def logToJson(result):
    raw_data = {}
    for r in result:
        for i in range(len(r)):
            raw_data[t[i]] = r[i].text.replace(" ", "")

        raw_data["code"] = "%s-%s %s" % (raw_data["dept_code"], raw_data["serial"], raw_data["code"])

        raw_time = unicodedata.normalize("NFD", raw_data["time"]).encode("ascii", "ignore")
        if raw_data["code"] == "I2-156 I231420":
            raw_data["time"] = "31234N5678"
            continue
        raw_data["time"] = normalizeTime(raw_time)

        del raw_data["dept_code"]
        del raw_data["serial"]
        del raw_data["class_code"]
        del raw_data["field"]
        del raw_data["number_selected"]
        del raw_data["crossfield"]
        del raw_data["property"]
        del raw_data["experts"]

        """
        if os.path.exists("ncku.json"):
            formatFile = open("ncku.json", "r")
            raw = formatFile.read()
            formatFile.close()

            formatFile = open("ncku.json", "w")
            if raw[0] != "[":
                raw = "[" + raw
            if raw[-1] == "]":
                raw = raw[:-1]
            formatFile.write(raw)
            formatFile.close()
        """

        json_data = json.dumps(raw_data, ensure_ascii=False)
        f = codecs.open("ncku_t.json", "a", encoding='utf-8')
        f.write("%s," % (json_data))
        f.close()


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

t = ["department", "dept_code", "serial", "code", "class_code",
     "class", "grade", "field", "language", "title", "obligatory",
     "credits", "professor", "number_selected", "time", "location", "note",
     "previous", "experts", "property", "crossfield"]

br = mechanize.Browser()

for dept in d:
    url = "http://course-query.acad.ncku.edu.tw/qry/qry001.php?dept_no=%s" % dept
    br.open(url)

    html = br.response().get_data()
    soup = BeautifulSoup(html)
    td = soup.find_all("td")

    result = []
    for i in range(len(td) / 21 - 1):
        if i == len(td) / 21 - 1:
            result.append(td[-21:])
            break
        else:
            p = 21 * i
            result.append(td[p:p + 21])

    logToJson(result)
