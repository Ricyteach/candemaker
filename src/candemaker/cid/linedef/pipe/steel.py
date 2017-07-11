from .. import format_specs as fs, cid_line


B1Steel = cid_line(
                        Modulus = (fs.f10, 29E6), # psi
                        Poissons = (fs.f10, 0.3),
                        Yield = (fs.f10, 33E3), # psi
                        Seam = (fs.f10, 33E3), # psi
                        Density = (fs.f10, 0), # pci
                        UpperModulus = (fs.f10, 0), # psi
                        # None: 0, Yes: 1, Yes, print trace: 2
                        JointSlip = (fs.d5, 0),
                        Behavior = (fs.d5, 2), # Linear: 1, Bilinear: 2
                        # Small Deformation AASHTO Buckling: 0
                        # Large Deformation AASHTO Buckling: 1
                        # Large Deformation CANDE Buckling:  2
                        # Small Deformation Deep Corrugation Buckling: 3
                        # Large Deformation Deep Corrugation Buckling: 4
                        Mode = (fs.d5, 0)
                        )

B2SteelA = cid_line(
                    # for ANALYS only
                    Area = (fs.f10, 0), # in2/in
                    I = (fs.f10, 0), # in4/in
                    S = (fs.f10, 0), # in3/in
                    Z = (fs.f10, 0) # in3/in
                    )


B2SteelDWSD = cid_line(
                        # for DESIGN only
                        # Non LRFD only
                        YieldFS = (fs.f10, 2),
                        BucklingFS = (fs.f10, 2),
                        SeamFS = (fs.f10, 2),
                        PlasticFS = (fs.f10, 3),
                        Deflection = (fs.f10, 5) # percent
                        )


B2SteelDLRFD = cid_line(
                        # for DESIGN only
                        # LRFD only
                        Yield = (fs.f10, 1),
                        Buckling = (fs.f10, 1),
                        Seam = (fs.f10, 1),
                        Plastic = (fs.f10, 1),
                        Deflection = (fs.f10, 1)
                        )


B2bSteel = cid_line(
                    # use if JointSlip>0
                    Slip = (fs.f10, 4950), # psi
                    Yield = (fs.f10, 33E3), # psi
                    SlipRatio = (fs.f10, 0.0003),
                    PostSlipRatio = (fs.f10, 0.5),
                    YieldRatio = (fs.f10, 0),
                    Travel = (fs.f10, 1), # in
                    NumJoints = (fs.d5, 1), # max 15
                    # Same lengths: 0; Different: 1
                    VaryTravel = (fs.d5, 0)
                    )


B2cSteel = cid_line(
                    # Level 2 or 3 only
                    # use if JointSlip>0
                    # up to 15 fields of d4 integers
                    **dict(('Element{}'.format(i), (fs.d4, 0)) for i in range(1, 16))
                    )


B2dSteel = cid_line(
                    # Level 2 or 3 only
                    # use if JointSlip>0
                    # up to 15 fields of f4 floats
                    **dict(('LengthRatio{}'.format(i), (fs.d4, 0)) for i in range(1, 16))
                    )
    


B3SteelADLRFD = cid_line(
                        # LRFD only
                        Yieldϕ = (fs.f10, 1),
                        Bucklingϕ = (fs.f10, 1),
                        Seamϕ = (fs.f10, 1),
                        Plasticϕ = (fs.f10, 0.9),
                        Deflection = (fs.f10, 5), # percent
                        Combined = (fs.f10, 0.9) # deep corrug only
                        )
