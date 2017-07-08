def register_objects():
    from collections import namedtuple as nt
    from ... import format_specs as fs
    from ...cid import register
    from ..general import ObjDef, add_specs_defaults_to_nts

    reg_list = []

    plastic1_dict = dict(
                        # GENERAL, SMOOTH, PROFILE
                        WallType = ObjDef(fs.s10, 'GENERAL'),
                        # HDPE, PVC, PP, OTHER
                        PipeType = ObjDef(fs.s10, 'HDPE'),
                        # 1: Short term, 2: Long term
                        Duration = ObjDef(fs.d5, 1),
                        # Small Deformation: 0, Large Deformation: 1, Plus Buckling: 2
                        Mode = ObjDef(fs.d5, 0)
                        )

    Plastic1 = nt('Plastic1', plastic1_dict.keys())
    Plastic1._prefix = 'B-1.Plastic'
    Plastic1._name = 'B1Plastic'
    reg_list.append((Plastic1, plastic1_dict, Plastic_gen))

    plastic2_dict = dict(
                        ShortModulus = ObjDef(fs.f10, 0), # psi
                        ShortStrength = ObjDef(fs.f10, 0), # psi
                        LongModulus = ObjDef(fs.f10, 0), # psi
                        LongStrength = ObjDef(fs.f10, 0), # psi
                        Poissons = ObjDef(fs.f10, 0.3),
                        Density = ObjDef(fs.f10, 0) # pci
                        )
        
    Plastic2 = nt('Plastic2', plastic2_dict.keys())
    Plastic2._prefix = 'B-2.Plastic'
    Plastic2._name = 'B2Plastic'
    reg_list.append((Plastic2, plastic2_dict, Plastic2_gen))

    plastic3AGeneral_dict = dict(
                                # for ANALYS only
                                # WallType = GENERAL
                                Height = ObjDef(fs.f10, 0) # in
                                )

    Plastic3AGeneral = nt('Plastic3AGeneral', plastic3AGeneral_dict.keys())
    Plastic3AGeneral._prefix = 'B-3.Plastic.A.General'
    Plastic3AGeneral._name = 'B3PlasticAGeneral'
    reg_list.append((Plastic3AGeneral, plastic3AGeneral_dict, PlasticGeneral_gen))
    
    plastic3ASmooth_dict = dict(
                                # for ANALYS only
                                # WallType = SMOOTH
                                Height = ObjDef(fs.f10, 0), # in
                                Area = ObjDef(fs.f10, 0), # in2/in
                                I = ObjDef(fs.f10, 0), # in4/in
                                Centroid = ObjDef(fs.f10, 0) # in
                                )
        
    Plastic3ASmooth = nt('Plastic3ASmooth', plastic3ASmooth_dict.keys())
    Plastic3ASmooth._prefix = 'B-3.Plastic.A.Smooth'
    Plastic3ASmooth._name = 'B3PlasticASmooth'
    reg_list.append((Plastic3ASmooth, plastic3ASmooth_dict, PlasticSmooth_gen))
    
    plastic3AProfile_dict = dict(
                                # for ANALYS only
                                # WallType = PROFILE
                                # repeatable (multiple properties in one pipe group)
                                Period = ObjDef(fs.f10, 0), # in
                                Height = ObjDef(fs.f10, 0), # in
                                WebAngle = ObjDef(fs.f10, 90), # degrees
                                WebThickness = ObjDef(fs.f10, 0), # in
                                WebK = ObjDef(fs.f10, 4),
                                # 0 to 4
                                NumHorizontal = ObjDef(fs.d5, 0),
                                # 1: include, -1: ignore
                                Buckling = ObjDef(fs.d5, 1),
                                First = ObjDef(fs.d5, 0),
                                Last = ObjDef(fs.d5, 1)
                                )

    Plastic3AProfile = nt('Plastic3AProfile', plastic3AProfile_dict.keys())
    Plastic3AProfile._prefix = 'B-3.Plastic.A.Profile'
    Plastic3AProfile._name = 'B3PlasticAProfile'
    reg_list.append((Plastic3AProfile, plastic3AProfile_dict, PlasticProfile_gen))

    plastic3bAProfile_dict = dict(
                                  # for ANALYS only
                                  # WallType = PROFILE
                                  # Required for each NumHorizontal elements
                                  # 1: inner valley, 2: inner liner, 3: outer crest, 4: outer link
                                  Identifier = ObjDef(fs.d5, 0),
                                  Length = ObjDef(fs.f10, 0), # in
                                  Thickness = ObjDef(fs.f10, 0), # in
                                  SupportK = ObjDef(fs.f10, 4)
                                  )

    Plastic3bAProfile = nt('Plastic3bAProfile', plastic3bAProfile_dict.keys())
    Plastic3bAProfile._prefix = 'B-3b.Plastic.A.Profile'
    Plastic3bAProfile._name = 'B3bPlasticAProfile'
    reg_list.append((Plastic3bAProfile, plastic3bAProfile_dict, PlasticProfile_gen))
    
    plastic3DWSD_dict = dict(
                            # for DESIGN only
                            # WallType = SMOOTH
                            # Non LRFD only
                            YieldFS = ObjDef(fs.f10, 2),
                            BucklingFS = ObjDef(fs.f10, 3),
                            StrainFS = ObjDef(fs.f10, 2),
                            Deflection = ObjDef(fs.f10, 5), # percent
                            Tension = ObjDef(fs.f10, 0.05) # in/in
                            )

    Plastic3DWSD = nt('Plastic3DWSD', plastic3DWSD_dict.keys())
    Plastic3DWSD._prefix = 'B-3.Plastic.D.WSD'
    Plastic3DWSD._name = 'B3PlasticDWSD'
    reg_list.append((Plastic3DWSD, plastic3DWSD_dict, PlasticSmooth_gen))

    plastic3DLRFD_dict = dict(
                             # for DESIGN only
                             # WallType = SMOOTH
                             # LRFD only
                             Yield = ObjDef(fs.f10, 1),
                             Buckling = ObjDef(fs.f10, 1),
                             Strain = ObjDef(fs.f10, 1),
                             Deflection = ObjDef(fs.f10, 1),
                             Tension = ObjDef(fs.f10, 1)
                             )

    Plastic3DLRFD = nt('Plastic3DLRFD', plastic3DLRFD_dict.keys())
    Plastic3DLRFD._prefix = 'B-3.Plastic.D.LRFD'
    Plastic3DLRFD._name = 'B3PlasticDLRFD'
    reg_list.append((Plastic3DLRFD, plastic3DLRFD_dict, PlasticSmooth_gen))

    plastic4_dict = dict(
                        # for DESIGN only
                        # WallType = SMOOTH
                        # LRFD only
                        Yieldϕ = ObjDef(fs.f10, 1),
                        Bucklingϕ = ObjDef(fs.f10, 1),
                        Strainϕ = ObjDef(fs.f10, 1),
                        Deflection = ObjDef(fs.f10, 5), # percent
                        Tension = ObjDef(fs.f10, 0.05) # in/in
                        )

    Plastic4 = nt('Plastic4', plastic4_dict.keys())
    Plastic4._prefix = 'B-4.Plastic'
    Plastic4._name = 'B4Plastic'
    reg_list.append((Plastic4, plastic4_dict, Plastic4_gen))

    for obj, d, gen in reg_list:
        add_specs_defaults_to_nts(obj, d)
        register(obj, d, gen)
        yield obj

for obj in register_objects():
    exec('{} = obj'.format(obj.__name__))

del register_objects
del obj
