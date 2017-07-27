from ... import reg
from .any import A1, E1
from . import L3
from . import soil
from . import pipe

linedef_reg = reg.CidRegistry()

for name, obj in (  ('A1', A1),
                    ('E1', E1),
                    ('A2', L3.A2),
                    ('C1', L3.C1),
                    ('C2', L3.C2),
                    ('C3', L3.C3),
                    ('C3L', L3.C3), #  for last entry
                    ('C4', L3.C4),
                    ('C4L', L3.C4), #  for last entry
                    ('C5', L3.C5),
                    ('C5L', L3.C5), #  for last entry
                    ('D1', soil.D1),
                    ('D1L', soil.D1), #  for last entry
                    ('D2Isotropic', soil.D2Isotropic),
                    ('D2Orthotropic', soil.D2Orthotropic),
                    ('D2Duncan', soil.D2Duncan),
                    ('D3Duncan', soil.D3Duncan),
                    ('D4Duncan', soil.D4Duncan),
                    ('D2Over', soil.D2Over),
                    ('D2Hardin', soil.D2Hardin),
                    ('D2HardinTRIA', soil.D2HardinTRIA),
                    ('D2Interface', soil.D2Interface),
                    ('D2Composite', soil.D2Composite),
                    ('D2MohrCoulomb', soil.D2MohrCoulomb),
                    ('B1Alum', pipe.alum.B1Alum),
                    ('B2AlumA', pipe.alum.B2AlumA),
                    ('B2AlumDWSD', pipe.alum.B2AlumDWSD),
                    ('B2AlumDLRFD', pipe.alum.B2AlumDLRFD),
                    ('B3AlumADLRFD', pipe.alum.B3AlumADLRFD),
                    ('B2Plastic', pipe.plastic.B2Plastic),
                    ('B3PlasticAGeneral', pipe.plastic.B3PlasticAGeneral),
                    ('B3PlasticASmooth', pipe.plastic.B3PlasticASmooth),
                    ('B3PlasticAProfile', pipe.plastic.B3PlasticAProfile),
                    ('B3bPlasticAProfile', pipe.plastic.B3bPlasticAProfile),
                    ('B3PlasticDWSD', pipe.plastic.B3PlasticDWSD),
                    ('B3PlasticDLRFD', pipe.plastic.B3PlasticDLRFD),
                    ('B4Plastic', pipe.plastic.B4Plastic),
                    ('B1Steel', pipe.steel.B1Steel),
                    ('B2SteelA', pipe.steel.B2SteelA),
                    ('B2SteelDWSD', pipe.steel.B2SteelDWSD),
                    ('B2SteelDLRFD', pipe.steel.B2SteelDLRFD),
                    ('B2bSteel', pipe.steel.B2bSteel),
                    ('B2cSteel', pipe.steel.B2cSteel),
                    ('B2dSteel', pipe.steel.B2dSteel),
                    ('B3SteelADLRFD', pipe.steel.B3SteelADLRFD),
                    ):
    linedef_reg[name] = obj
