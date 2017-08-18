from ... import format_specs as fs
from ..general import line


B1Plastic = line(
                    # GENERAL, SMOOTH, PROFILE
                    WallType = (fs.s10, 'GENERAL'),
                    # HDPE, PVC, PP, OTHER
                    PipeType = (fs.s10, 'HDPE'),
                    # 1: Short term, 2: Long term
                    Duration = (fs.d5, 1),
                    # Small Deformation: 0, Large Deformation: 1, Plus Buckling: 2
                    Mode = (fs.d5, 0)
                    )


B2Plastic = line(
                    ShortModulus = (fs.f10, 0), # psi
                    ShortStrength = (fs.f10, 0), # psi
                    LongModulus = (fs.f10, 0), # psi
                    LongStrength = (fs.f10, 0), # psi
                    Poissons = (fs.f10, 0.3),
                    Density = (fs.f10, 0) # pci
                    )


B3PlasticAGeneral = line(
                            # for ANALYS only
                            # WallType = GENERAL
                            Height = (fs.f10, 0) # in
                            )

B3PlasticASmooth = line(
                            # for ANALYS only
                            # WallType = SMOOTH
                            Height = (fs.f10, 0), # in
                            Area = (fs.f10, 0), # in2/in
                            I = (fs.f10, 0), # in4/in
                            Centroid = (fs.f10, 0) # in
                            )

B3PlasticAProfile = line(
                            # for ANALYS only
                            # WallType = PROFILE
                            # repeatable (multiple properties in one pipe group)
                            Period = (fs.f10, 0), # in
                            Height = (fs.f10, 0), # in
                            WebAngle = (fs.f10, 90), # degrees
                            WebThickness = (fs.f10, 0), # in
                            WebK = (fs.f10, 4),
                            # 0 to 4
                            NumHorizontal = (fs.d5, 0),
                            # 1: include, -1: ignore
                            Buckling = (fs.d5, 1),
                            First = (fs.d5, 0),
                            Last = (fs.d5, 1)
                            )

B3bPlasticAProfile = line(
                                # for ANALYS only
                                # WallType = PROFILE
                                # Required for each NumHorizontal elements
                                # 1: inner valley, 2: inner liner, 3: outer crest, 4: outer link
                                Identifier = (fs.d5, 0),
                                Length = (fs.f10, 0), # in
                                Thickness = (fs.f10, 0), # in
                                SupportK = (fs.f10, 4)
                                )

B3PlasticDWSD = line(
                        # for DESIGN only
                        # WallType = SMOOTH
                        # Non LRFD only
                        YieldFS = (fs.f10, 2),
                        BucklingFS = (fs.f10, 3),
                        StrainFS = (fs.f10, 2),
                        Deflection = (fs.f10, 5), # percent
                        Tensile = (fs.f10, 0.05) # in/in
                        )

B3PlasticDLRFD = line(
                         # for DESIGN only
                         # WallType = SMOOTH
                         # LRFD only
                         Yield = (fs.f10, 1),
                         Buckling = (fs.f10, 1),
                         Strain = (fs.f10, 1),
                         Deflection = (fs.f10, 1),
                         Tensile = (fs.f10, 1)
                         )

B4Plastic = line(
                    # for DESIGN only
                    # WallType = SMOOTH
                    # LRFD only
                    Yieldϕ = (fs.f10, 1),
                    Bucklingϕ = (fs.f10, 1),
                    Strainϕ = (fs.f10, 1),
                    DeflectionPercent = (fs.f10, 5), # percent
                    TensileService = (fs.f10, 0.05) # in/in
                    )
