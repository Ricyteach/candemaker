from .. import format_specs as fs, cid_line


B1Alum = cid_line(
                    Modulus = (fs.f10, 10E6), # psi
                    Poissons = (fs.f10, 0.33),
                    Yield = (fs.f10, 24E3), # psi
                    Seam = (fs.f10, 24E3), # psi
                    Density = (fs.f10, 0), # pci
                    UpperModulus = (fs.f10, 0.05*10E6), # psi
                    Behavior = (fs.d5, 2), # Linear: 1, Bilinear: 2
                    # Small Deformation: 0, Large Deformation: 1, Plus Buckling: 2
                    Mode = (fs.d5, 0)
                    )


B2AlumA = cid_line(
                    # for ANALYS mode only
                    Area = (fs.f10, 0), # in2/in
                    I = (fs.f10, 0), # in4/in
                    S = (fs.f10, 0) # in3/in
                    )


B2AlumDWSD = cid_line(
                        # for DESIGN mode only and no LRFD only
                        YieldFS = (fs.f10, 3),
                        BucklingFS = (fs.f10, 2),
                        SeamFS = (fs.f10, 2),
                        PlasticFS = (fs.f10, 4),
                        Deflection = (fs.f10, 5) # percent
                        )


B2AlumDLRFD = cid_line(
                        # for DESIGN mode and LRFD mode only
                        Yield = (fs.f10, 1),
                        Buckling = (fs.f10, 1),
                        Seam = (fs.f10, 1),
                        Plastic = (fs.f10, 1),
                        Deflection = (fs.f10, 1)
                        )


B3AlumADLRFD = cid_line(
                        # LRFD only
                        Yieldϕ = (fs.f10, 1),
                        Bucklingϕ = (fs.f10, 1),
                        Seamϕ = (fs.f10, 0.67),
                        Plasticϕ = (fs.f10, 0.85),
                        Deflection = (fs.f10, 5) # percent
                        )
