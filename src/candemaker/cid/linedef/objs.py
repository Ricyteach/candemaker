# any

Master = nt('Master', master_dict.keys())
Master._prefix = 'A-1'
Master._name = 'A1'

Factor = nt('Factor', factor_dict.keys())
Factor._prefix = 'E-1'
Factor._name = 'E1'

# L3

prefix_spec = '{}.L3!!' # overwrites prefix_spec from .format_specs

PipeGroup = nt('PipeGroup', pipe_group_dict.keys())
PipeGroup._prefix = prefix_spec.format('A-2')
PipeGroup._name = 'A2'

L3Info = nt('L3Info', ['Title'])
L3Info._prefix = prefix_spec.format('C-1')
L3Info._name = 'C1'

L3Control = nt('L3Control', 'Steps Check Nodes Elements Boundaries SoilMaterials InterfMaterials Bandwidth')
L3Control._prefix = prefix_spec.format('C-2')
L3Control._name = 'C2'

Node = nt('Node', 'Num X Y')
NodeLast = nt('NodeLast', 'Limit Num X Y')

for NT in (Node, NodeLast):
    NT._prefix = prefix_spec.format('C-3')
    NT._name = 'C3'

Element = nt('Element', 'Num I J K Mat Step InterfLink')
TriaElement = nt('TriaElement', 'Num I J K Mat Step')
QuadElement = nt('QuadElement', 'Num I J K L Mat Step')
SoilElement = nt('SoilElement', 'Num I J K L Mat Step')
BeamElement = nt('BeamElement', 'Num I J Mat Step')
InterfElement = nt('InterfElement', 'Num I J K Mat Step InterfLink')
ElementLast = nt('ElementLast', 'Limit Num I J K Mat Step InterfLink')

for NT in (Element, TriaElement, QuadElement, SoilElement, BeamElement, InterfElement, ElementLast):
    NT._prefix = prefix_spec.format('C-4')
    NT._name = 'C4'

Bound = nt('Bound', 'Node Xcode Xvalue Ycode Yvalue Angle Step')
ForceBound = nt('ForceBound', 'Node Xvalue Yvalue Step')
SideBound = nt('SideBound', 'Node Xcode Step')
BotBound = nt('BotBound', 'Node Ycode Step')
CornerBound = nt('CornerBound', 'Node Xcode Ycode Step')
BoundLast = nt('BoundLast', 'Limit Node Xcode Xvalue Ycode Yvalue Angle Step')

for NT in (Bound, ForceBound, SideBound, BotBound, CornerBound, BoundLast):
    NT._prefix = prefix_spec.format('C-5')
    NT._name = 'C5'

#soil

SoilMaterial = nt('SoilMaterial', 'ID Model Density Name Layers')
SoilMaterialLast = nt('SoilMaterialLast', 'Limit ID Model Density Name Layers')
InterfMaterial = nt('InterfMaterial', 'ID Model Density Name Layers')
InterfMaterialLast = nt('InterfMaterialLast', 'Limit ID Model Density Name Layers')

for NT in (SoilMaterial, SoilMaterialLast, InterfMaterial, InterfMaterialLast):
    NT._prefix = 'D-1'
    NT._name = 'D1'


Isotropic = nt('Isotropic', isotropic_dict.keys())
Isotropic._prefix = 'D-2.Isotropic'
Isotropic._name = 'D2Isotropic'

Orthotropic = nt('Orthotropic', orthotropic_dict.keys())
Orthotropic._prefix = 'D-2.Orthotropic'
Orthotropic._name = 'D2Orthotropic'

Duncan2 = nt('Duncan2', duncan2_dict.keys())
Duncan2._prefix = 'D-2.Duncan'
Duncan2._name = 'D2Duncan'

Duncan3 = nt('Duncan3', duncan3_dict.keys())
Duncan3._prefix = 'D-3.Duncan'
Duncan3._name = 'D3Duncan'

Duncan4 = nt('Duncan4', duncan4_dict.keys())
Duncan4._prefix = 'D-4.Duncan'
Duncan4._name = 'D4Duncan'

Overburden = nt('Overburden', overburden_dict.keys())
Overburden._prefix = 'D-2.Over'
Overburden._name = 'D2Over'

Hardin = nt('Hardin', hardin_dict.keys())
Hardin._prefix = 'D-2.Hardin'
Hardin._name = 'D2Hardin'

HardinTRIA = nt('HardinTRIA', hardinTRIA_dict.keys())
HardinTRIA._prefix = 'D-2.Hardin.TRIA'
HardinTRIA._name = 'D2HardinTRIA'

Interface = nt('Interface', interface_dict.keys())
Interface._prefix = 'D-2.Interface'
Interface._name = 'D2Interface'

Composite = nt('Composite', composite_dict.keys())
Composite._prefix = 'D-2.Composite'
Composite._name = 'D2Composite'

MohrCoulomb = nt('MohrCoulomb', mohrcoulomb_dict.keys())
MohrCoulomb._prefix = 'D-2.MohrCoulomb'
MohrCoulomb._name = 'D2MohrCoulomb'

# alum

reg_list = []

Alum1 = nt('Alum1', alum1_dict.keys())
Alum1._prefix = 'B-1.Alum'
Alum1._name = 'B1Alum'
reg_list.append((Alum1, alum1_dict, Alum_gen))

Alum2A = nt('Alum2A', alum2A_dict.keys())
Alum2A._prefix = 'B-2.Alum.A'
Alum2A._name = 'B2AlumA'
reg_list.append((Alum2A, alum2A_dict, Alum_gen))

Alum2DWSD = nt('Alum2DWSD', alum2DWSD_dict.keys())
Alum2DWSD._prefix = 'B-2.Alum.D.WSD'
Alum2DWSD._name = 'B2AlumDWSD'
reg_list.append((Alum2DWSD, alum2DWSD_dict, Alum_gen))

Alum2DLRFD = nt('Alum2DLRFD', alum2DLRFD_dict.keys())
Alum2DLRFD._prefix = 'B-2.Alum.D.LRFD'
Alum2DLRFD._name = 'B2AlumDLRFD'
reg_list.append((Alum2DLRFD, alum2DLRFD_dict, Alum_gen))

Alum3ADLRFD = nt('Alum3ADLRFD', alum3ADLRFD_dict.keys())
Alum3ADLRFD._prefix = 'B-3.Alum.AD.LRFD'
Alum3ADLRFD._name = 'B3AlumADLRFD'
reg_list.append((Alum3ADLRFD, alum3ADLRFD_dict, Alum_gen))

# steel

reg_list = []

Steel1 = nt('Steel1', steel1_dict.keys())
Steel1._prefix = 'B-1.Steel'
Steel1._name = 'B1Steel'
reg_list.append((Steel1, steel1_dict, Steel_gen))

Steel2A = nt('Steel2A', steel2A_dict.keys())
Steel2A._prefix = 'B-2.Steel.A'
Steel2A._name = 'B2SteelA'
reg_list.append((Steel2A, steel2A_dict, Steel_gen))

Steel2DWSD = nt('Steel2DWSD', steel2DWSD_dict.keys())
Steel2DWSD._prefix = 'B-2.Steel.D.WSD'
Steel2DWSD._name = 'B2SteelDWSD'
reg_list.append((Steel2DWSD, steel2DWSD_dict, Steel_gen))

Steel2DLRFD = nt('Steel2DLRFD', steel2DLRFD_dict.keys())
Steel2DLRFD._prefix = 'B-2.Steel.D.LRFD'
Steel2DLRFD._name = 'B2SteelDLRFD'
reg_list.append((Steel2DLRFD, steel2DLRFD_dict, Steel_gen))

Steel2b = nt('Steel2b', steel2b_dict.keys())
Steel2b._prefix = 'B-2b.Steel'
Steel2b._name = 'B2bSteel'
reg_list.append((Steel2b, steel2b_dict, Steel_gen))

Steel2c = nt('Steel2c', ' '.join('Element{}'.format(i) for i in range(1,16)))
Steel2c._prefix = 'B-2c.Steel'
Steel2c._name = 'B2cSteel'
reg_list.append((Steel2c, steel2c_dict, Steel_gen))

Steel2d = nt('Steel2d', ' '.join('LengthRatio{}'.format(i) for i in range(1,16)))
Steel2d._prefix = 'B-2d.Steel'
Steel2d._name = 'B2dSteel'
reg_list.append((Steel2d, steel2d_dict, Steel_gen))

Steel3ADLRFD = nt('Steel3ADLRFD', steel3ADLRFD_dict.keys())
Steel3ADLRFD._prefix = 'B-2.Steel.AD.LRFD'
Steel3ADLRFD._name = 'B3SteelADLRFD'
reg_list.append((Steel3ADLRFD, steel3ADLRFD_dict, Steel_gen))

# plastic

reg_list = []

Plastic1 = nt('Plastic1', plastic1_dict.keys())
Plastic1._prefix = 'B-1.Plastic'
Plastic1._name = 'B1Plastic'
reg_list.append((Plastic1, plastic1_dict, Plastic_gen))

Plastic2 = nt('Plastic2', plastic2_dict.keys())
Plastic2._prefix = 'B-2.Plastic'
Plastic2._name = 'B2Plastic'
reg_list.append((Plastic2, plastic2_dict, Plastic2_gen))

Plastic3AGeneral = nt('Plastic3AGeneral', plastic3AGeneral_dict.keys())
Plastic3AGeneral._prefix = 'B-3.Plastic.A.General'
Plastic3AGeneral._name = 'B3PlasticAGeneral'
reg_list.append((Plastic3AGeneral, plastic3AGeneral_dict, PlasticGeneral_gen))

Plastic3ASmooth = nt('Plastic3ASmooth', plastic3ASmooth_dict.keys())
Plastic3ASmooth._prefix = 'B-3.Plastic.A.Smooth'
Plastic3ASmooth._name = 'B3PlasticASmooth'
reg_list.append((Plastic3ASmooth, plastic3ASmooth_dict, PlasticSmooth_gen))

Plastic3AProfile = nt('Plastic3AProfile', plastic3AProfile_dict.keys())
Plastic3AProfile._prefix = 'B-3.Plastic.A.Profile'
Plastic3AProfile._name = 'B3PlasticAProfile'
reg_list.append((Plastic3AProfile, plastic3AProfile_dict, PlasticProfile_gen))

Plastic3bAProfile = nt('Plastic3bAProfile', plastic3bAProfile_dict.keys())
Plastic3bAProfile._prefix = 'B-3b.Plastic.A.Profile'
Plastic3bAProfile._name = 'B3bPlasticAProfile'
reg_list.append((Plastic3bAProfile, plastic3bAProfile_dict, PlasticProfile_gen))

Plastic3DWSD = nt('Plastic3DWSD', plastic3DWSD_dict.keys())
Plastic3DWSD._prefix = 'B-3.Plastic.D.WSD'
Plastic3DWSD._name = 'B3PlasticDWSD'
reg_list.append((Plastic3DWSD, plastic3DWSD_dict, PlasticSmooth_gen))

Plastic3DLRFD = nt('Plastic3DLRFD', plastic3DLRFD_dict.keys())
Plastic3DLRFD._prefix = 'B-3.Plastic.D.LRFD'
Plastic3DLRFD._name = 'B3PlasticDLRFD'
reg_list.append((Plastic3DLRFD, plastic3DLRFD_dict, PlasticSmooth_gen))

Plastic4 = nt('Plastic4', plastic4_dict.keys())
Plastic4._prefix = 'B-4.Plastic'
Plastic4._name = 'B4Plastic'
reg_list.append((Plastic4, plastic4_dict, Plastic4_gen))

for obj, d, gen in ((Master, master_dict, A1_gen),
                    (Factor, factor_dict, E1_gen)
                    ):
    add_specs_defaults_to_nts(obj, d)
    register(obj, d, gen)
    yield obj

for obj in register_objects():
    exec('{} = obj'.format(obj.__name__))

del register_objects
del obj
del nt
