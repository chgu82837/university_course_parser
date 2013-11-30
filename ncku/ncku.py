# -*- coding utf-8 -*-
from bs4 import BeautifulSoup
import mechanize
import json
import codecs
import os


def logToJson(result):
    raw_data = {}
    for r in result:
        for i in range(len(r)):
            raw_data[t[i]] = r[i].text

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

        json_data = json.dumps(raw_data, ensure_ascii=False)
        f = codecs.open("ncku.json", "a", encoding='utf-8')
        f.write("%s,\n" % (json_data))
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
     "credits", "professor", "member", "time", "location", "note",
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
