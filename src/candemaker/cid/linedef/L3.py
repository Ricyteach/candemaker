from mytools.blank import BlankInt, BlankFloat
from . import format_specs as fs, cid_line


A2 = cid_line(
                # ALUMINUM, BASIC, CONCRETE, PLASTIC, STEEL, CONRIB, CONTUBE
                Type = (fs.s10, 'NO_DEFAULT'),
                Num = (fs.d5, 0)
                )

C1 = cid_line(
                Prep = (fs.s5, 'PREP'),
                Title = (fs.s68, '')
                )

C2 = cid_line(
                Steps = (fs.d5, 1),
                # 1: control data, 2: input data,
                # 3: created data, 4: maximum
                MeshOutput = (fs.d5, 3),
                Check = (fs.d5, 1),  # 0: run, 1: check
                PlotControl = (fs.d5, 3),  # always 3
                # 0: minimal, 1: standard, 2: plus Duncan,
                # 3: plus interface, 4: plus Mohr Coulomb
                ResponseOutput = (fs.d5, 0),
                Nodes = (fs.d5, 0),
                Elements = (fs.d5, 0),
                Boundaries = (fs.d5, 0),
                SoilMaterials = (fs.d5, 0),
                InterfMaterials = (fs.d5, 0),
                # 0: none, 1: minimize, 2: minimize and print
                Bandwidth = (fs.d5, 1)
                )

C3 = cid_line(
                Limit = (fs.s1, ' '),
                Num = (fs.d4, 0),
                SpecialReferenceCode = (fs.d3, 0),
                SpecialGenerationCode = (fs.d1, 0),
                BasicGenerationCode = (fs.d1, BlankInt()),
                X = (fs.f10, 0),
                Y = (fs.f10, 0),
                Increment = (fs.d5, BlankInt()),
                Spacing = (fs.f10, BlankFloat()),
                Radius = (fs.f10, BlankFloat())
                )

C4 = cid_line(
                Limit = (fs.s1, ' '),
                Num = (fs.d4, 0),
                I = (fs.d5, 0),
                J = (fs.d5, 0),
                K = (fs.d5, 0),
                L = (fs.d5, 0),
                Mat = (fs.d5, 0),
                Step = (fs.d5, 0),
                # 0 for normal, 1 for interface,
                # 8 for link element fixed, 9 for link element pinned
                InterfLink = (fs.d5, BlankInt()),
                IncrementAdded = (fs.d5, BlankInt()),
                RowsAdded = (fs.d5, BlankInt()),
                IncrementBetween = (fs.d5, BlankInt()),
                Death = (fs.d5, BlankInt())
                )

C5 = cid_line(
                Limit = (fs.s1, ' '),
                Node = (fs.d4, 0),
                Xcode = (fs.d5, 0),
                Xvalue = (fs.f10, 0),
                Ycode = (fs.d5, 0),
                Yvalue = (fs.f10, 0),
                Angle = (fs.f10, 0),
                Step = (fs.d5, 0),
                EndNode = (fs.d5, BlankInt()),
                Increment = (fs.d5, BlankInt()),
                Pressure1 = (fs.f10, BlankFloat()),
                Pressure2 = (fs.f10, BlankFloat())
                )
