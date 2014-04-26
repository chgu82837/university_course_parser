from nchu import dept, general


def correct_json():
    with open('nchu.json', 'r') as f:
        raw = f.readline()
    with open('nchu.json', 'w') as f:
        f.write('[' + raw[:-1] + ']')


def connect(year, debug=False):
    dept.connect(debug)
    general.connect(debug)


if __name__ == '__main__':
    connect('1022', debug=True)
    correct_json()
