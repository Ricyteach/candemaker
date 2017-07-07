def Alum_gen(cid, struct, group):
    yield Alum1
    if cid.mode == 'ANALYS':
        yield Alum2A
    elif cid.mode == 'DESIGN':
        if cid.method == 0: #  WSD
            yield Alum2DWSD
        if cid.method == 1: #  LRFD
            yield Alum2DLRFD
    if cid.method == 1: #  LRFD
        yield Alum3ADLRFD

def register_objects():
    from collections import namedtuple as nt
    from ... import format_specs as fs
    from ...cid import register
    from ..general import ObjDef, add_specs_defaults_to_nts

    reg_list = []

    alum1_dict = dict(
                     Modulus = ObjDef(fs.f10, 10E6), # psi
                     Poissons = ObjDef(fs.f10, 0.33),
                     Yield = ObjDef(fs.f10, 24E3), # psi
                     Seam = ObjDef(fs.f10, 24E3), # psi
                     Density = ObjDef(fs.f10, 0), # pci
                     UpperModulus = ObjDef(fs.f10, 0.05*10E6), # psi
                     Behavior = ObjDef(fs.d5, 2), # Linear: 1, Bilinear: 2
                     # Small Deformation: 0, Large Deformation: 1, Plus Buckling: 2
                     Mode = ObjDef(fs.d5, 0)
                     )

    Alum1 = nt('Alum1', alum1_dict.keys())
    Alum1._prefix = 'B-1.Alum'
    Alum1._name = 'B1Alum'
    reg_list.append((Alum1, alum1_dict, Alum_gen))


    alum2A_dict = dict(
                      # for ANALYS mode only
                      Area = ObjDef(fs.f10, 0), # in2/in
                      I = ObjDef(fs.f10, 0), # in4/in
                      S = ObjDef(fs.f10, 0) # in3/in
                      )

    Alum2A = nt('Alum2A', alum2A_dict.keys())
    Alum2A._prefix = 'B-2.Alum.A'
    Alum2A._name = 'B2AlumA'
    reg_list.append((Alum2A, alum2A_dict, Alum_gen))


    alum2DWSD_dict = dict(
                         # for DESIGN mode only and no LRFD only
                         YieldFS = ObjDef(fs.f10, 3),
                         BucklingFS = ObjDef(fs.f10, 2),
                         SeamFS = ObjDef(fs.f10, 2),
                         PlasticFS = ObjDef(fs.f10, 4),
                         Deflection = ObjDef(fs.f10, 5) # percent
                         )

    Alum2DWSD = nt('Alum2DWSD', alum2DWSD_dict.keys())
    Alum2DWSD._prefix = 'B-2.Alum.D.WSD'
    Alum2DWSD._name = 'B2AlumDWSD'
    reg_list.append((Alum2DWSD, alum2DWSD_dict, Alum_gen))


    alum2DLRFD_dict = dict(
                          # for DESIGN mode and LRFD mode only
                          Yield = ObjDef(fs.f10, 1),
                          Buckling = ObjDef(fs.f10, 1),
                          Seam = ObjDef(fs.f10, 1),
                          Plastic = ObjDef(fs.f10, 1),
                          Deflection = ObjDef(fs.f10, 1)
                          )

    Alum2DLRFD = nt('Alum2DLRFD', alum2DLRFD_dict.keys())
    Alum2DLRFD._prefix = 'B-2.Alum.D.LRFD'
    Alum2DLRFD._name = 'B2AlumDLRFD'
    reg_list.append((Alum2DLRFD, alum2DLRFD_dict, Alum_gen))


    alum3ADLRFD_dict = dict(
                            # LRFD only
                            Yieldϕ = ObjDef(fs.f10, 1),
                            Bucklingϕ = ObjDef(fs.f10, 1),
                            Seamϕ = ObjDef(fs.f10, 0.67),
                            Plasticϕ = ObjDef(fs.f10, 0.85),
                            Deflection = ObjDef(fs.f10, 5) # percent
                            )

    Alum3ADLRFD = nt('Alum3ADLRFD', alum3ADLRFD_dict.keys())
    Alum3ADLRFD._prefix = 'B-3.Alum.AD.LRFD'
    Alum3ADLRFD._name = 'B3AlumADLRFD'
    reg_list.append((Alum3ADLRFD, alum3ADLRFD_dict, Alum_gen))


    for obj, d, gen in reg_list:
        add_specs_defaults_to_nts(obj, d)
        register(obj, d, gen)
        yield obj

for obj in register_objects():
    exec('{} = obj'.format(obj.__name__))

del register_objects
del obj
