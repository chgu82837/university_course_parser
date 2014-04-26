import nchu, ncku, ntnu

YEAR = '1022'
u = ['nchu', 'ncku', 'ntnu']

for name in u:
    print(name.upper() + '...')
    exec(name + '.parser.connect(' + YEAR + ')')
    exec(name + '.parser.correct_json()')
