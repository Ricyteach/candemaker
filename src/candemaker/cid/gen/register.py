from ... import reg
from .cid import A1, E1
from . import L3
from . import soil

cidgen_reg = reg.CidRegistry()

for name, obj in (  ('A1', A1),
                    ('E1', E1),
                    ('A2', L3.A2),
                    ('C1', L3.C1),
                    ('C2', L3.C2),
                    ('C3', L3.C3),
                    ('C4', L3.C4),
                    ('C5', L3.C5),
                    ('D1', soil.D1),
                    ):
    cidgen_reg[name] = obj
