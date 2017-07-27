from collections import namedtuple as nt
from mytools import getfields, InvalidField
from . import reg

# import all line definition sequences from cid.linedef modules
from .cid.linedef import *
from .cid.linedef.L3 import *
from .cid.linedef.soil import *
from .cid.linedef.pipe.alum import *
from .cid.linedef.pipe.basic import *
from .cid.linedef.pipe.concrete import *
from .cid.linedef.pipe.plastic import *
from .cid.linedef.pipe.steel import *


__all__ = ('Factor Master PipeGroup Info Control '
'Node Element TriaElement QuadElement SoilElement BeamElement '
'InterfElement Bound ForceBound SideBound BotBound CornerBound '
'Material SoilMaterial InterfMaterial Isotropic Orthotropic '
'Duncan2 Duncan3 Duncan4 Overburden Hardin HardinTRIA Interface Composite MohrCoulomb '
'Alum1 Alum2A Alum2DWSD Alum2DLRFD Alum3ADLRFD '
'Steel1 Steel2A Steel2DWSD Steel2DLRFD Steel2b Steel2c Steel2d Steel3ADLRFD '
'Plastic1 Plastic2 Plastic3AGeneral '
'Plastic3ASmooth Plastic3AProfile Plastic3bAProfile Plastic3DWSD Plastic3DLRFD Plastic4').split()


obj_reg = reg.CidRegistry()
cidname_reg = reg.ObjRegistry()

def defaults(linedef):
    '''Generate the defaults from a line definition sequence'''
    try:
        yield from (field.default for field in linedef)
    except AttributeError as e:
        raise TypeError('The lindef argument did not contain '
                        'valid fields') from e

def names(linedef):
    '''Generate the names from a line definition sequence'''
    try:
        yield from (field.name for field in linedef)
    except AttributeError as e:
        raise TypeError('The lindef argument did not contain '
                        'valid fields') from e

##    Not done yet
def cidnt(name, linedef, *fields, **def_values):
    '''Factory to create a special CID named tuple
    Created from a line definition sequenceusing its
    default values'''
    linenames = tuple(names(linedef))
    linedefaults = tuple(defaults(linedef))
    invalid_defaults = [k for k in def_values.keys() if k not in linenames]
    if invalid_defaults:
        raise ValueError('One or more supplied default value names '
                         'do not appear in the linedef:\n'
                         '{!r}'.format(invalid_defaults))
    defaults_dict = {n: def_values.get(n, d)
                    for n, d in zip(linenames, linedefaults)}
    if fields:
        validator = lambda f: f in linenames
        try:
            fieldseq = tuple(getfields(*fields, validator=validator))
        except InvalidField as e:
            raise ValueError('One or more field names does not appear '
                             'in the linedef:\n{!r}'
                             ''.format(linedef)) from e
    else:
        fieldseq = linenames

    NT = nt(name, fieldseq)
    new_defaults = (defaults_dict[fieldname] for fieldname in fieldseq)
    NT.__new__.__defaults__ = tuple(new_defaults)
    return NT

# any

Master = cidnt('Master', A1)
Factor = cidnt('Factor', E1)

# L3

PipeGroup = cidnt('PipeGroup', A2)
Info = cidnt('Info', C1, ['Title'])
Control = cidnt('Control', C2, 'NSteps Check NNodes NElements NBoundaries '
                                   'NSoilMaterials NInterfMaterials Bandwidth')
Node = cidnt('Node', C3, 'Num X Y')
# NodeLast = cidnt('NodeLast', C3, 'Limit', Limit='L')
Element = cidnt('Element', C4, 'Num I J K L Mat Step InterfLink')
TriaElement = cidnt('TriaElement', C4, 'Num I J K')
QuadElement = cidnt('QuadElement', C4, 'Num I J K L')
SoilElement = cidnt('SoilElement', C4, 'Num I J K L')
BeamElement = cidnt('BeamElement', C4, 'Num I J')
InterfElement = cidnt('InterfElement', C4, 'Num I J K InterfLink', InterfLink=1)
# ElementLast = cidnt('ElementLast', C4, 'Limit', Limit='L')
Bound = cidnt('Bound', C5, 'Node Xcode Xvalue Ycode Yvalue Angle Step')
ForceBound = cidnt('ForceBound', C5, 'Node Xvalue Yvalue')
SideBound = cidnt('SideBound', C5, 'Node Xcode', Xcode=1)
BotBound = cidnt('BotBound', C5, 'Node Ycode', Ycode=1)
CornerBound = cidnt('CornerBound', C5, 'Node Xcode Ycode', Xcode=1, Ycode=1)
# BoundLast = cidnt('BoundLast', C5, 'Limit', Limit='L')

#soil

Material = cidnt('Material', D1, 'ID Model Density Name Layers')
# MaterialLast = cidnt('MaterialLast', D1, 'Limit', Limit='L')
SoilMaterial = cidnt('SoilMaterial', D1, 'ID Model Density Name')
InterfMaterial = cidnt('InterfMaterial', D1, 'ID Name Model', Model=6)
OverMaterial = cidnt('OverMaterial', D1, 
                     'ID Density Name Layers Model', Layers=1, Model=4)
Isotropic = cidnt('Isotropic', D2Isotropic)
Orthotropic = cidnt('Orthotropic', D2Orthotropic)
Duncan2 = cidnt('Duncan2', D2Duncan)
Duncan3 = cidnt('Duncan3', D3Duncan)
Duncan4 = cidnt('Duncan4', D4Duncan)
Overburden = cidnt('Overburden', D2Over)
Hardin = cidnt('Hardin', D2Hardin)
HardinTRIA = cidnt('HardinTRIA', D2HardinTRIA)
Interface = cidnt('Interface', D2Interface)
Composite = cidnt('Composite', D2Composite)
MohrCoulomb = cidnt('MohrCoulomb', D2MohrCoulomb)

# alum

Alum1 = cidnt('Alum1', B1Alum)
Alum2A = cidnt('Alum2A', B2AlumA)
Alum2DWSD = cidnt('Alum2DWSD', B2AlumDWSD)
Alum2DLRFD = cidnt('Alum2DLRFD', B2AlumDLRFD)
Alum3ADLRFD = cidnt('Alum3ADLRFD', B3AlumADLRFD)

# steel

Steel1 = cidnt('Steel1', B1Steel)
Steel2A = cidnt('Steel2A', B2SteelA)
Steel2DWSD = cidnt('Steel2DWSD', B2SteelDWSD)
Steel2DLRFD = cidnt('Steel2DLRFD', B2SteelDLRFD)
Steel2b = cidnt('Steel2b', B2bSteel)
Steel2c = cidnt('Steel2c', B2cSteel, ' '.join('Element{}'.format(i)
                                              for i in range(1,16)))
Steel2d = cidnt('Steel2d', B2dSteel, ' '.join('LengthRatio{}'.format(i)
                                              for i in range(1,16)))
Steel3ADLRFD = cidnt('Steel3ADLRFD', B3SteelADLRFD)

# plastic

Plastic1 = cidnt('Plastic1', B1Plastic)
Plastic2 = cidnt('Plastic2', B2Plastic)
Plastic3AGeneral = cidnt('Plastic3AGeneral', B3PlasticAGeneral)
Plastic3ASmooth = cidnt('Plastic3ASmooth', B3PlasticASmooth)
Plastic3AProfile = cidnt('Plastic3AProfile', B3PlasticAProfile)
Plastic3bAProfile = cidnt('Plastic3bAProfile', B3bPlasticAProfile)
Plastic3DWSD = cidnt('Plastic3DWSD', B3PlasticDWSD)
Plastic3DLRFD = cidnt('Plastic3DLRFD', B3PlasticDLRFD)
Plastic4 = cidnt('Plastic4', B4Plastic)


for name, obj in (
                    ('A1', Master),
                    ('E1', Factor),

                    # L3
                    ('A2', PipeGroup),
                    ('C1', Info),
                    ('C2', Control),
                    ('C3', Node),
                    ('C3L', Node),
                    ('C4', Element),
                    ('C4L', Element),
                    # ('C4', TriaElement),
                    # ('C4', QuadElement),
                    # ('C4', SoilElement),
                    # ('C4', BeamElement),
                    # ('C4', InterfElement),
                    ('C5', Bound),
                    ('C5L', Bound),
                    # ('C5', ForceBound),
                    # ('C5', SideBound),
                    # ('C5', BotBound),
                    # ('C5', CornerBound),

                    #soil
                    ('D1', Material),
                    ('D1L', Material),
                    # ('D1', SoilMaterial),
                    # ('D1', InterfMaterial),
                    # ('D1', OverMaterial),
                    ('D2Isotropic', Isotropic),
                    ('D2Orthotropic', Orthotropic),
                    ('D2Duncan', Duncan2),
                    ('D3Duncan', Duncan3),
                    ('D4Duncan', Duncan4),
                    ('D2Over', Overburden),
                    ('D2Hardin', Hardin),
                    ('D2HardinTRIA', HardinTRIA),
                    ('D2Interface', Interface),
                    ('D2Composite', Composite),
                    ('D2MohrCoulomb', MohrCoulomb),

                    # alum
                    ('B1Alum', Alum1),
                    ('B2AlumA', Alum2A),
                    ('B2AlumDWSD', Alum2DWSD),
                    ('B2AlumDLRFD', Alum2DLRFD),
                    ('B3AlumADLRFD', Alum3ADLRFD),

                    # steel
                    ('B1Steel', Steel1),
                    ('B2SteelA', Steel2A),
                    ('B2SteelDWSD', Steel2DWSD),
                    ('B2SteelDLRFD', Steel2DLRFD),
                    ('B2bSteel', Steel2b),
                    ('B2cSteel', Steel2c),
                    ('B2dSteel', Steel2d),
                    ('B3SteelADLRFD', Steel3ADLRFD),

                    # plastic
                    ('B1Plastic', Plastic1),
                    ('B2Plastic', Plastic2),
                    ('B3PlasticAGeneral', Plastic3AGeneral),
                    ('B3PlasticASmooth', Plastic3ASmooth),
                    ('B3PlasticAProfile', Plastic3AProfile),
                    ('B3bPlasticAProfile', Plastic3bAProfile),
                    ('B3PlasticDWSD', Plastic3DWSD),
                    ('B3PlasticDLRFD', Plastic3DLRFD),
                    ('B4Plastic', Plastic4),
                ):
    obj_reg[name] = obj


for name, obj in (
                    (Master.__name__, 'A1'),
                    (Factor.__name__, 'E1'),

                    # L3
                    (PipeGroup.__name__, 'A2'),
                    (Info.__name__, 'C1'),
                    (Control.__name__, 'C2'),
                    (Node.__name__, 'C3'),
                    (Element.__name__, 'C4'),
                    (TriaElement.__name__, 'C4'),
                    (QuadElement.__name__, 'C4'),
                    (SoilElement.__name__, 'C4'),
                    (BeamElement.__name__, 'C4'),
                    (InterfElement.__name__, 'C4'),
                    (Bound.__name__, 'C5'),
                    (ForceBound.__name__, 'C5'),
                    (SideBound.__name__, 'C5'),
                    (BotBound.__name__, 'C5'),
                    (CornerBound.__name__, 'C5'),

                    #soil
                    (Material.__name__, 'D1'),
                    (SoilMaterial.__name__, 'D1'),
                    (InterfMaterial.__name__, 'D1'),
                    (OverMaterial.__name__, 'D1'),
                    (Isotropic.__name__, 'D2Isotropic'),
                    (Orthotropic.__name__, 'D2Orthotropic'),
                    (Duncan2.__name__, 'D2Duncan'),
                    (Duncan3.__name__, 'D3Duncan'),
                    (Duncan4.__name__, 'D4Duncan'),
                    (Overburden.__name__, 'D2Over'),
                    (Hardin.__name__, 'D2Hardin'),
                    (HardinTRIA.__name__, 'D2HardinTRIA'),
                    (Interface.__name__, 'D2Interface'),
                    (Composite.__name__, 'D2Composite'),
                    (MohrCoulomb.__name__, 'D2MohrCoulomb'),

                    # alum
                    (Alum1.__name__, 'B1Alum'),
                    (Alum2A.__name__, 'B2AlumA'),
                    (Alum2DWSD.__name__, 'B2AlumDWSD'),
                    (Alum2DLRFD.__name__, 'B2AlumDLRFD'),
                    (Alum3ADLRFD.__name__, 'B3AlumADLRFD'),

                    # steel
                    (Steel1.__name__, 'B1Steel'),
                    (Steel2A.__name__, 'B2SteelA'),
                    (Steel2DWSD.__name__, 'B2SteelDWSD'),
                    (Steel2DLRFD.__name__, 'B2SteelDLRFD'),
                    (Steel2b.__name__, 'B2bSteel'),
                    (Steel2c.__name__, 'B2cSteel'),
                    (Steel2d.__name__, 'B2dSteel'),
                    (Steel3ADLRFD.__name__, 'B3SteelADLRFD'),

                    # plastic
                    (Plastic1.__name__, 'B1Plastic'),
                    (Plastic2.__name__, 'B2Plastic'),
                    (Plastic3AGeneral.__name__, 'B3PlasticAGeneral'),
                    (Plastic3ASmooth.__name__, 'B3PlasticASmooth'),
                    (Plastic3AProfile.__name__, 'B3PlasticAProfile'),
                    (Plastic3bAProfile.__name__, 'B3bPlasticAProfile'),
                    (Plastic3DWSD.__name__, 'B3PlasticDWSD'),
                    (Plastic3DLRFD.__name__, 'B3PlasticDLRFD'),
                    (Plastic4.__name__, 'B4Plastic'),
                ):
    cidname_reg[name] = obj
