from collections import namedtuple as nt
from . import format_specs as fs

CIDField = nt('CIDField', 'name spec default')

def cid_line(**field_defs):
    return tuple(CIDField(n, s, d) for n, (s, d) in field_defs.items())

A1 = cid_line(
                # ANALYS or DESIGN
                Mode = (fs.s8, 'ANALYS'),
                # 1, 2, or 3
                Level = (fs.d2, 3),
                Method = (fs.d2, 1),
                NGroups = (fs.d3, 1),
                Heading = (fs.s60, ''),
                Iterations = (fs.d5, -99),
                CulvertID = (fs.d5, 0),
                ProcessID = (fs.d5, 0),
                SubdomainID = (fs.d5, 0)
                )

E1 = cid_line(
                Start = (fs.d5, 0),
                Last = (fs.d5, 0),
                Factor = (fs.f10, 1),
                Comment = (fs.s40, '')
                )
