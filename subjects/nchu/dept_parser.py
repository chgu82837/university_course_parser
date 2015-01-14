import json,re,sys,pyprind,requests

head_start_value = ["必選別"]

row_start_value = ["必修","選修"]

def get_nchu_course(url,payload):
    response = requests.post(url, data=payload)
    content = re.sub(r'<a[^>]*>([^<]+)</a>', r'\1', response.text).replace("</BR>"," ")
    match = re.findall(r'<TD[^>]*>([^<]+)</TD>',content)

    data = []
    state = 0 # 0 for none, 1 for in head, 2 for in row
    for cell in match:
        value = cell.strip()
        # print("> " + value)
        if value in head_start_value:
            state = 1
            col_name = []
        elif value in row_start_value:
            state = 2
            colcnt = 0
            r_data = {}

        if state is 1:
            col_name.append(value)
        elif state is 2:
            if(len(value)):
                r_data[col_name[colcnt]] = value
            colcnt += 1
            if colcnt is len(col_name):
                data.append(r_data)
                state = 0

    return data

def parse_time(t_str):
    # print(t_str)
    return [{"day":int(d[0]),"time":[int(h,16) for h in list(d[1:]) if h in "123456789ABCD" ]} for d in t_str.split(",") if d[0] in "1234567"]

col_name2key = {
    "必選別":'obligatory',
    "選課號碼":"code",
    "科目名稱":"title",
    "先修科目":"previous",
    "全/半年":"year",
    "學分數":"credits",
    "上課時數":"hours",
    "實習時數":"hours",
    "※上課時間":"time",
    "實習時間":"time",
    "上課教室":"location",
    "實習教室":"location",
    "上課教師":"professor",
    "實習教師":"professor",
    "開課單位":"department",
    "開課人數":"number",
    "語言":"language",
    "備註":"note",
}

obligatory2tf = {
    "必修":True,
    "選修":False
}

required_key = ["obligatory","code","title","time","department","location","credits","professor"]

int_field = ["number","hours","credits"]

def parse(data):
    r_data = {}
    required_key_cnt = 0
    for k in data.keys():
        if k in col_name2key:
            col_key = col_name2key[k]
            r_data[col_key] = data[k]
            if(col_key == "obligatory"):
                r_data["obligatory_tf"] = obligatory2tf[data[k]]
            elif(col_key == "time"):
                r_data["time_parsed"] = parse_time(data[k])
            elif col_key in int_field:
                r_data[col_key + "_parsed"] = int(data[k])
            if col_key in required_key:
                required_key_cnt += 1
    if(required_key_cnt is not len(required_key)):
        raise Exception("required_key not satisfied!")
    return r_data

def to_json(json_path,arr):
    # print(arr)
    with open(json_path, 'a') as json_file:
        for d in arr:
            json_str = json.dumps(d, ensure_ascii=False)
            json_file.write('{},'.format(json_str))

def start_json_arr(json_path,name):
    with open(json_path, 'a') as json_file:
        json_file.write('"%s":[' % name)

def end_json_arr(json_path):
    with open(json_path, 'a') as json_file:
        json_file.write('],')

def start_json(json_path):
    with open(sys.argv[1], 'w') as json_file:
        json_file.truncate()
        json_file.write('{')

def end_json(json_path):
    with open(json_path, 'a') as json_file:
        json_file.write('}')

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:\n\tpython[3] "+sys.argv[0]+" <json_output> dept_id1 [dept_id2 [dept_id3 ...]]")
        sys.exit(1)

    jpath = sys.argv[1]
    url = 'https://onepiece.nchu.edu.tw/cofsys/plsql/crseqry_home'
    
    err = []

    # dept_id = ["U56","U53B","U53A"] for WP_final_proj
    dept_id = sys.argv[2:]
    print(dept_id)
    my_prbar = pyprind.ProgBar(len(dept_id),title = "共 %d 個系要處理" % len(dept_id))
    try:
        start_json(jpath)
        start_json_arr(jpath,"course")

        for ID in dept_id:
            raw = get_nchu_course(url,{'v_dept': ID})
            data = []

            for r in raw:
                try:
                    data.append(parse(r))
                except Exception as e:
                    err.append([r,e])
            # print(data)
            to_json(jpath,data)
            my_prbar.update(1,item_id = ID)

        end_json_arr(jpath)
        end_json(jpath)
    except Exception as e:
        print("================ ERR ================")
        print(e)

    print("================ WARN ================")
    print(err)

