from collections import namedtuple as nt
from .. import format_specs as fs

Field = nt('Field', 'name spec default')

def line(**field_defs):
    '''Return a cid file line definition composed of a tuple of fields'''
    return tuple(Field(n, s, d) for n, (s, d) in field_defs.items())

A1 = line(
            # ANALYS or DESIGN
            Mode = (fs.s8, 'ANALYS'),
            # 1, 2, or 3
            Level = (fs.d2, 3),
            Method = (fs.d2, 1),
            NGroups = (fs.d3, 1),
            Heading = (fs.s60, 'CID from candemaker: Rick Teachey, rickteachey@cbceng.com'),
            Iterations = (fs.d5, -99),
            CulvertID = (fs.d5, 0),
            ProcessID = (fs.d5, 0),
            SubdomainID = (fs.d5, 0)
            )

E1 = line(
            Start = (fs.d5, 0),
            Last = (fs.d5, 0),
            Factor = (fs.f10, 1),
            Comment = (fs.s40, '')
            )
