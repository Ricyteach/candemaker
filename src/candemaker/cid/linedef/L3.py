from .. import format_specs as fs
from .general import line

__all__ = 'A2 C1 C2 C3 C4 C5'.split()

A2 = line(
                # ALUMINUM, BASIC, CONCRETE, PLASTIC, STEEL, CONRIB, CONTUBE
                Type = (fs.s10, 'NO_DEFAULT'),
                Num = (fs.d5, 0)
                )

C1 = line(
                Prep = (fs.s5, 'PREP'),
                Title = (fs.s68, '')
                )

C2 = line(
                NSteps = (fs.d5, 1),
                # 1: control data, 2: input data,
                # 3: created data, 4: maximum
                MeshOutput = (fs.d5, 3),
                Check = (fs.d5, 1),  # 0: run, 1: check
                PlotControl = (fs.d5, 3),  # always 3
                # 0: minimal, 1: standard, 2: plus Duncan,
                # 3: plus interface, 4: plus Mohr Coulomb
                ResponseOutput = (fs.d5, 0),
                NNodes = (fs.d5, 0),
                NElements = (fs.d5, 0),
                NBoundaries = (fs.d5, 0),
                NSoilMaterials = (fs.d5, 0),
                NInterfMaterials = (fs.d5, 0),
                # 0: none, 1: minimize, 2: minimize and print
                Bandwidth = (fs.d5, 1)
                )

C3 = line(
                # Note: moved limit field to line _prefix
                # Limit = (fs.s1, ' '),
                Num = (fs.d4, 0),
                SpecialReferenceCode = (fs.d3, 0),
                SpecialGenerationCode = (fs.d1, 0),
                BasicGenerationCode = (fs.blank(fs.d1), 0),
                X = (fs.f10, 0),
                Y = (fs.f10, 0),
                Increment = (fs.blank(fs.d5), 0),
                Spacing = (fs.blank(fs.f10), 0),
                Radius = (fs.blank(fs.f10), 0)
                )

C4 = line(
                # Note: moved limit field to line _prefix
                # Limit = (fs.s1, ' '),
                Num = (fs.d4, 0),
                I = (fs.d5, 0),
                J = (fs.d5, 0),
                K = (fs.d5, 0),
                L = (fs.d5, 0),
                Mat = (fs.d5, 0),
                Step = (fs.d5, 0),
                # 0 for normal, 1 for interface,
                # 8 for link element fixed, 9 for link element pinned
                InterfLink = (fs.blank(fs.d5), 0),
                IncrementAdded = (fs.blank(fs.d5), 0),
                RowsAdded = (fs.blank(fs.d5), 0),
                IncrementBetween = (fs.blank(fs.d5), 0),
                Death = (fs.blank(fs.d5), 0)
                )

C5 = line(
                # Note: moved limit field to line _prefix
                # Limit = (fs.s1, ' '),
                Node = (fs.d4, 0),
                Xcode = (fs.d5, 0),
                Xvalue = (fs.f10, 0),
                Ycode = (fs.d5, 0),
                Yvalue = (fs.f10, 0),
                Angle = (fs.f10, 0),
                Step = (fs.d5, 0),
                EndNode = (fs.blank(fs.d5), 0),
                Increment = (fs.blank(fs.d5), 0),
                Pressure1 = (fs.blank(fs.f10), 0),
                Pressure2 = (fs.blank(fs.f10), 0)
                )
