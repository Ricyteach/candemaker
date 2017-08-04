# cid field format specs

s1 = '{: >1s}'
s3 = '{: <3s}'
s5 = '{: <5s}'
s8 = '{: <8s}'
s10 = '{: <10s}'
s20 = '{: <20s}'
s40 = '{: <40s}'
s60 = '{: <60s}'
s68 = '{: <68s}'
d1 = '{: >1d}'
d2 = '{: >2d}'
d3 = '{: >3d}'
d4 = '{: >4d}'
d5 = '{: >5d}'
f4 = '{: >4.1fd}'
f9 = '{: >9.1fd}'
f10 = '{: >10.1fd}'

def blank(spec):
    '''Add  "blank" to the format spec.'''
    spec = spec[:-1] + 'blank' + spec[-1:]
    return spec
