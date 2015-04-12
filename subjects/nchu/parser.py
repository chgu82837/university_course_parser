# coding=utf-8

import json,re,sys,pyprind,requests,urllib,traceback
from pyquery import PyQuery as pq

head_start_value = ["必選別"]
row_start_value = ["必修","選修"]
col_name2key = {
    "※上課時間":"time",
    "上課教室":"location",
    "上課教師":"professor",
    "上課時數":"hours",
    "備註":"note",
    "先修科目":"previous",
    "全/半年":"year",
    "學分數":"credits",
    "實習教室":"location",
    "實習教師":"professor",
    "實習時數":"hours",
    "實習時間":"time",
    "必選別":'obligatory',
    "科目名稱":"title",
    "語言":"language",
    "選課號碼":"code",
    "開課人數":"number",
    "開課單位":"department",
    "for_dept":"for_dept",
    "class":"class",
}
obligatory2tf = {
    "必修":True,
    "選修":False
}
required_key = {"obligatory","code","title","time","department","credits","professor"}
int_field = ["number","hours","credits"]

def get_nchu_course(url, payload):
    response = requests.post(url, data=payload)
    datas = []
    for table in re.findall(r'<TABLE.*?</TABLE>', response.text, re.S):
        data = {}
        table = table.replace("</BR>","`").replace("\u3000",'')
        with open('debug.html', 'w') as fdebug:
            fdebug.write(table)
        d = pq('<div>'+table+'</div>')
        table_title = d('strong:contains("系所名稱")').text()
        if table_title == '':
            continue
        match = re.fullmatch(r'系所名稱:(.*?) 年級:(.*?) 班別:(.*?)', table_title)
        data['for_dept'], data['class'] = match.group(1), match.group(2)+match.group(3)
        thead = []
        for tr in d('tr'):
            row = [ str(pq(i).text().strip()) for i in pq(tr).find('td') ]
            if len(thead) == 0:
                thead = row
            else:
                row = dict(zip(thead, row))
                row.update(data)
                datas.append(row)
    return datas

def parse_time(t_str):
    # print(t_str)
    return [{"day":int(d[0]),"time":[int(h,16) for h in list(d[1:]) if h in "123456789ABCD" ]} for d in t_str.split(",") if (len(d) and d[0] in "1234567")]

def parse_title(t_str):
    title_splited = [i.strip() for i in t_str.split('`')]
    if len(title_splited) == 1:
        return {'zh_TW': title_splited[0]}
    else:
        return {'zh_TW': title_splited[0], 'en_US': title_splited[1]}
    raise Exception('parse_title error: '+t_str)

def parse(data):
    r_data = {}
    required_key_cnt = 0
    for k in data.keys():
        if k in col_name2key:
            col_key = col_name2key[k]
            if col_key not in r_data or len(data[k]) > len(r_data[col_key]):
                r_data[col_key] = data[k]
            if col_key == "obligatory":
                r_data["obligatory_tf"] = obligatory2tf[r_data[col_key]]
            elif col_key == "time":
                r_data["time_parsed"] = parse_time(r_data[col_key])
            elif col_key == "title":
                r_data['title_parsed'] = parse_title(r_data[col_key])
            elif col_key in int_field:
                r_data[col_key + "_parsed"] = int(r_data[col_key]) if len(r_data[col_key]) else 0
    for k in required_key:
        if len(r_data.get(k, '')) == 0:
            raise Exception(k+' is required in '+str(r_data))
    return r_data

def to_json(json_path,arr,notFirst = False):
    # print(arr)
    with open(json_path, 'a') as json_file:
        for d in arr:
            json_str = json.dumps(d, ensure_ascii=False)
            json_file.write('{}{}'.format((',' if notFirst else ''), json_str))
            notFirst = True

def start_json_arr(json_path,name,notFirst = False):
    with open(json_path, 'a') as json_file:
        json_file.write('%s"%s":[' % ((',' if notFirst else ''), name))

def end_json_arr(json_path):
    with open(json_path, 'a') as json_file:
        json_file.write(']')

def start_json(json_path):
    with open(json_path, 'w') as json_file:
        json_file.truncate()
        json_file.write('{')

def end_json(json_path):
    with open(json_path, 'a') as json_file:
        json_file.write('}')

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage:\n\tpython[3] "+sys.argv[0]+" <url> <json_output> dept_id1 [dept_id2 [dept_id3 ...]]")
        print("\n\n\t URL can be:https://onepiece.nchu.edu.tw/cofsys/plsql/crseqry_home");
        print("\t URL can be:https://onepiece.nchu.edu.tw/cofsys/plsql/crseqry_gene");
        sys.exit(1)

    jpath = sys.argv[2]
    url = sys.argv[1]
    url = "https://onepiece.nchu.edu.tw/cofsys/plsql/crseqry_home"

    err = []

    dept_id = sys.argv[3:]
    print(dept_id)
    my_prbar = pyprind.ProgBar(len(dept_id),title = "共 %d 個系要處理" % len(dept_id))
    notFirst1 = False
    try:
        start_json(jpath)
        start_json_arr(jpath,"course",notFirst1)
        notFirst1 = True
        notFirst2 = False

        for ID in dept_id:
            raw = get_nchu_course(url,{'v_dept': ID})
            data = []

            for r in raw:
                try:
                    data.append(parse(r))
                except Exception as e:
                    err.append([r,str(e)+str(traceback.format_exc())])
            # print(data)
            to_json(jpath,data,notFirst2)
            notFirst2 = True
            my_prbar.update(1,item_id = ID)

        end_json_arr(jpath)
        end_json(jpath)
    except Exception as e:
        print("================ ERR ================")
        print(e)
        print(traceback.format_exc())

    print("================ WARN ================")
    print(err)
