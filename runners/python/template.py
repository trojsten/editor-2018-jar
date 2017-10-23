b1, b2, b3 = True, True, True
c1, c2, c3 = 'a', 'a', 'a'
d, e, f, g, h, i, j, k = 0, 0, 0, 0, 0, 0, 0, 0
p, q = 1.0, 1.0
r1, r2 = [True, False], [True, True]
s1, s2, s3 = 'a', 'a', 'a'
u1, u2, u3 = ['kon', 'pes'], ['pracka', 'rozok'], ['ryba', 'smrdi']
v1, v2, v3 = [-1, 1], [42, 47], [94, 49]
w1 = [0.1, 1.1]

# load
file_in = '%INFILE%'
try:
    file = open(file_in, 'r')
    vars = list(map(lambda x: x.strip(), file.readlines()))
    b1, b2, b3 = map(lambda x: True if x == '1' else False, vars[0:3])
    c1, c2, c3 = vars[3:6]
    d, e, f, g, h, i, j, k = map(int, vars[6:14])
    p, q = map(float, vars[14:16])
    r1, r2 = map(lambda x: list(map(lambda y: True if y == '1' else False, x.split('~'))), vars[16:18])
    s1, s2, s3 = vars[18:21]
    u1, u2, u3 = map(lambda x: x.split('~'), vars[21:24])
    v1, v2, v3 = map(lambda x: list(map(int, x.split('~'))), vars[24:27])
    w1 = list(map(float, vars[27].split('~')))
    file.close()
except:
    pass

# execute
%LINE%

# write
file_out = '%OUTFILE%'
file = open(file_out, 'w')
file.write('\n'.join(map(lambda x: str(1 if x else 0), [b1, b2, b3])) + '\n' +
           '\n'.join([c1, c2, c3]) + '\n' +
           '\n'.join(map(str, [d, e, f, g, h, i, j, k])) + '\n' +
           '\n'.join(map(str, [p, q])) + '\n' +
           '~'.join(map(lambda x: str(1 if x else 0), r1)) + '\n' +
           '~'.join(map(lambda x: str(1 if x else 0), r2)) + '\n' +
           '\n'.join([s1, s2, s3]) + '\n' +
           '~'.join(u1) + '\n' + '~'.join(u2) + '\n' + '~'.join(u3) + '\n' +
           '~'.join(map(str, v1)) + '\n' +
           '~'.join(map(str, v2)) + '\n' +
           '~'.join(map(str, v3)) + '\n' +
           '~'.join(map(str, w1)) + '\n')
file.close()
