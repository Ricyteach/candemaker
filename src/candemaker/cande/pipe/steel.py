def Steel_gen(cid, struct, group):
    yield Steel1
    if cid.mode == 'ANALYS':
        yield Steel2A
    elif cid.mode == 'DESIGN':
        if cid.method == 0: #  WSD
            yield Steel2DWSD
        if cid.method == 1: #  LRFD
            yield Steel2DLRFD
    if group.JointSlip: #  Slotted Joints
        yield Steel2b
        if cid.level > 1:
            yield Steel2c
            if group.VaryTravel: # Model of "Half Joints"
                yield Steel2d
    if cid.method == 1: #  LRFD
        yield Steel3ADLRFD

def register_objects():
    from collections import namedtuple as nt
    from ... import format_specs as fs
    from ...cid import register
    from ..general import ObjDef, add_specs_defaults_to_nts

    reg_list = []


    steel1_dict = dict(
                        Modulus = ObjDef(fs.f10, 29E6), # psi
                        Poissons = ObjDef(fs.f10, 0.3),
                        Yield = ObjDef(fs.f10, 33E3), # psi
                        Seam = ObjDef(fs.f10, 33E3), # psi
                        Density = ObjDef(fs.f10, 0), # pci
                        UpperModulus = ObjDef(fs.f10, 0), # psi
                        # None: 0, Yes: 1, Yes, print trace: 2
                        JointSlip = ObjDef(fs.d5, 0),
                        Behavior = ObjDef(fs.d5, 2), # Linear: 1, Bilinear: 2
                        # Small Deformation AASHTO Buckling: 0
                        # Large Deformation AASHTO Buckling: 1
                        # Large Deformation CANDE Buckling:  2
                        # Small Deformation Deep Corrugation Buckling: 3
                        # Large Deformation Deep Corrugation Buckling: 4
                        Mode = ObjDef(fs.d5, 0)
                        )
        
    Steel1 = nt('Steel1', steel1_dict.keys())
    Steel1._prefix = 'B-1.Steel'
    Steel1._name = 'B1Steel'
    reg_list.append((Steel1, steel1_dict, Steel_gen))

    steel2A_dict = dict(
                        # for ANALYS only
                        Area = ObjDef(fs.f10, 0), # in2/in
                        I = ObjDef(fs.f10, 0), # in4/in
                        S = ObjDef(fs.f10, 0), # in3/in
                        Z = ObjDef(fs.f10, 0) # in3/in
                        )

    Steel2A = nt('Steel2A', steel2A_dict.keys())
    Steel2A._prefix = 'B-2.Steel.A'
    Steel2A._name = 'B2SteelA'
    reg_list.append((Steel2A, steel2A_dict, Steel_gen))


    steel2DWSD_dict = dict(
                        # for DESIGN only
                        # Non LRFD only
                        YieldFS = ObjDef(fs.f10, 2),
                        BucklingFS = ObjDef(fs.f10, 2),
                        SeamFS = ObjDef(fs.f10, 2),
                        PlasticFS = ObjDef(fs.f10, 3),
                        Deflection = ObjDef(fs.f10, 5) # percent
                        )

    Steel2DWSD = nt('Steel2DWSD', steel2DWSD_dict.keys())
    Steel2DWSD._prefix = 'B-2.Steel.D.WSD'
    Steel2DWSD._name = 'B2SteelDWSD'
    reg_list.append((Steel2DWSD, steel2DWSD_dict, Steel_gen))


    steel2DLRFD_dict = dict(
                            # for DESIGN only
                            # LRFD only
                            Yield = ObjDef(fs.f10, 1),
                            Buckling = ObjDef(fs.f10, 1),
                            Seam = ObjDef(fs.f10, 1),
                            Plastic = ObjDef(fs.f10, 1),
                            Deflection = ObjDef(fs.f10, 1)
                            )

    Steel2DLRFD = nt('Steel2DLRFD', steel2DLRFD_dict.keys())
    Steel2DLRFD._prefix = 'B-2.Steel.D.LRFD'
    Steel2DLRFD._name = 'B2SteelDLRFD'
    reg_list.append((Steel2DLRFD, steel2DLRFD_dict, Steel_gen))


    steel2b_dict = dict(
                        # use if JointSlip>0
                        Slip = ObjDef(fs.f10, 4950), # psi
                        Yield = ObjDef(fs.f10, 33E3), # psi
                        SlipRatio = ObjDef(fs.f10, 0.0003),
                        PostSlipRatio = ObjDef(fs.f10, 0.5),
                        YieldRatio = ObjDef(fs.f10, 0),
                        Travel = ObjDef(fs.f10, 1), # in
                        NumJoints = ObjDef(fs.d5, 1), # max 15
                        # Same lengths: 0; Different: 1
                        VaryTravel = ObjDef(fs.d5, 0)
                        )

    Steel2b = nt('Steel2b', steel2b_dict.keys())
    Steel2b._prefix = 'B-2b.Steel'
    Steel2b._name = 'B2bSteel'
    reg_list.append((Steel2b, steel2b_dict, Steel_gen))


    steel2c_dict = dict(
                        # Level 2 or 3 only
                        # use if JointSlip>0
                        # up to 15 fields of d4 integers
                        (('Element{}'.format(i), ObjDef(fs.d4, 0)) for i in range(1, 16))
                        )

    Steel2c = nt('Steel2c', ' '.join('Element{}'.format(i) for i in range(1,16)))
    Steel2c._prefix = 'B-2c.Steel'
    Steel2c._name = 'B2cSteel'
    reg_list.append((Steel2c, steel2c_dict, Steel_gen))


    steel2d_dict = dict(
                        # Level 2 or 3 only
                        # use if JointSlip>0
                        # up to 15 fields of f4 floats
                        (('LengthRatio{}'.format(i), ObjDef(fs.d4, 0)) for i in range(1, 16))
                        )
        

    Steel2d = nt('Steel2d', ' '.join('LengthRatio{}'.format(i) for i in range(1,16)))
    Steel2d._prefix = 'B-2d.Steel'
    Steel2d._name = 'B2dSteel'
    reg_list.append((Steel2d, steel2d_dict, Steel_gen))


    steel3ADLRFD_dict = dict(
                            # LRFD only
                            Yieldϕ = ObjDef(fs.f10, 1),
                            Bucklingϕ = ObjDef(fs.f10, 1),
                            Seamϕ = ObjDef(fs.f10, 1),
                            Plasticϕ = ObjDef(fs.f10, 0.9),
                            Deflection = ObjDef(fs.f10, 5), # percent
                            Combined = ObjDef(fs.f10, 0.9) # deep corrug only
                            )

    Steel3ADLRFD = nt('Steel3ADLRFD', steel3ADLRFD_dict.keys())
    Steel3ADLRFD._prefix = 'B-2.Steel.AD.LRFD'
    Steel3ADLRFD._name = 'B3SteelADLRFD'
    reg_list.append((Steel3ADLRFD, steel3ADLRFD_dict, Steel_gen))

    for obj, d, gen in reg_list:
        add_specs_defaults_to_nts(obj, d)
        register(obj, d, gen)
        yield obj

for obj in register_objects():
    exec('{} = obj'.format(obj.__name__))

del register_objects
del obj
