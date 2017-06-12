from parmatter import FormatGroupMeta, VersatileParmatter
from collections import namedtuple as nt

# for parmatter definitions
Pardef = nt('Pardef', 'spec default')
s1 = '{: >1s}'
s5 = '{: <5s}'
s10 = '{: <10s}'
s20 = '{: <20s}'
s60 = '{: <60s}'
d1 = '{: >1d}'
d2 = '{: >2d}'
d3 = '{: >3d}'
d4 = '{: >4d}'
d5 = '{: >5d}'
f10 = '{: >10.4f}'
prefix_spec = '{: >25s}!!'

class CANDE_formatter(FormatGroupMeta):
    _formatter_type = VersatileParmatter
    _sep = ''

class A1(metaclass=CANDE_formatter):
    _prefix = prefix_spec.format('A-1')
    # ANALYS or DESIGN
    Mode = Pardef('{: <8s}', 'ANALYS')
    Level = Pardef(d2, 3)
    Method = Pardef(d2, 1)
    Groups = Pardef(d3, 1)
    Heading = Pardef(s60, '')
    Iterations = Pardef(d5, -99)
    CulvertID = Pardef(d5, 0)
    ProcessID = Pardef(d5, 0)
    SubdomainID = Pardef(d5, 0)
    
class E1(metaclass=CANDE_formatter):
    _prefix = prefix_spec.format('E-1')
    Start = Pardef(d5, 0)
    Last = Pardef(d5, 0)
    Factor = Pardef(f10, 1)
    Comment = Pardef('{: <40s}', '')