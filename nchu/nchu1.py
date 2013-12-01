# -*- coding: utf-8 -*-
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
        raw_data["time"] += raw_data["prac_time"]
        raw_data["hours"] += raw_data["prac_hours"]
        raw_data["professor"] += raw_data["prac_professor"]
        raw_data["location"] += raw_data["prac_location"]
        raw_data["grade"] = raw_data["code"][0]

        if os.path.exists("nchu.json"):
            formatFile = open("nchu.json", "r")
            raw = formatFile.read()
            formatFile.close()

            formatFile = open("nchu.json", "w")
            if raw[0] != "[":
                raw = "[" + raw
            if raw[-1] == "]":
                raw = raw[:-1]
            formatFile.write(raw)
            formatFile.close()

        json_data = json.dumps(raw_data, ensure_ascii=False)
        f = codecs.open("nchu.json", "a", encoding='utf-8')
        f.write("%s, ]" % (json_data))
        f.close()


v = {"year":  0, "career": 1, "dept":  3,
     "level": 3, "text":   4, "teach": 5,
     "week":  6, "mtg":    7, "lang":  8}

t = ["title", ""]

t = ["obligatory", "code", "title", "previous", "year", "credits",
     "hours", "prac_hours", "time", "prac_time", "location",
     "prac_location", "professor", "prac_professor", "department",
     "number", "number_selected", "number_outter_dept", "number_available",
     "language", "note"]

url = "https://onepiece.nchu.edu.tw/cofsys/plsql/crseqry_gene"
br = mechanize.Browser()
br.open(url)

forms = [c for c in br.forms()]
contents = forms[2].controls[v["dept"]].get_items()

depts = {}
for i in range(1, len(contents) - 1):
    depts[contents[i].attrs["value"]] = contents[i].attrs["contents"]

for deptCode in depts.keys():
    forms[2]["v_group"] = [deptCode]
    br.form = forms[2]
    response = br.submit()
    soup = BeautifulSoup(response.read())
    td = soup.find_all("td")[105:-5]

    result = []
    for i in range(len(td) / 21 - 1):
        if i == len(td) / 21 - 1:
            result.append(td[-21:])
            break
        else:
            p = 21 * i
            result.append(td[p + 1:p + 22])

    logToJson(result)
