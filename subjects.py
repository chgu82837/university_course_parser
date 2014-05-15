import nchu, ncku, ntnu

YEAR = '1022'
u = ['nchu', 'ncku', 'ntnu']

for name in u:
    print(name.upper() + '...')
    exec(name + '.parser.parse(' + YEAR + ')')

print('Done')
