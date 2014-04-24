import nchu_dept
import nchu_ge


def correct_json():
    with open('nchu.json', 'r') as f:
        raw = f.readline()
    with open('nchu.json', 'w') as f:
        f.write('[' + raw[:-1] + ']')

if __name__ == '__main__':
    nchu_dept.connect()
    nchu_ge.connect()
    correct_json()
