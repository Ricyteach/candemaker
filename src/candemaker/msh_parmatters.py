from parmatter import FormatGroupMeta, VersatileParmatter
from collections import namedtuple as nt

# for parmatter definitions
Pardef = nt('Pardef', 'spec default')
ld = '{:<d}'
lf = '{:<f}'

class MSH_formatter(FormatGroupMeta):
    _formatter_type = VersatileParmatter
    _sep = ' '
    _prefix = ''

class CountLine(metaclass=MSH_formatter):
    Num = Pardef(ld, 0)
        
class NodeLine(metaclass=MSH_formatter):
    Num = Pardef(ld, 0)
    X = Pardef(lf, 0)
    Y = Pardef(lf, 0)
    
class ElementLine(metaclass=MSH_formatter):
    Num = Pardef(ld, 0)
    I = Pardef(ld, 0)
    J = Pardef(ld, 0)
    K = Pardef(ld, 0)
    L = Pardef(ld, 0)
    
class BoundaryLine(metaclass=MSH_formatter):
    Num = Pardef(ld, 0)
    Node = Pardef(ld, 0)
