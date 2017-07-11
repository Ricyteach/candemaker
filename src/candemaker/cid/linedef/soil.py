from mytools.blank import BlankInt
from . import format_specs as fs, cid_line


D1 = cid_line(
                Limit = (fs.s1, ' '),
                ID = (fs.d4, 0),
                # 1: isotropic, 2: orthotropic, 
                # 3: Duncan/Selig, 4: Overburden,
                # 5: Extended Hardin, 6: Interface, 
                # 7: Composite Link, 8: Mohr/Coulomb
                Model = (fs.d5, 1),
                Density = (fs.f10, 0),
                Name = (fs.s20, ''),
                # overburden model only
                Layers = (fs.d2, BlankInt())
                )

D2Isotropic = cid_line(
                        # only for Model = 1
                        Modulus = (fs.f10, 0), # psi
                        Poissons = (fs.f10, 0)
                        )

D2Orthotropic = cid_line(
                        # only for Model = 2
                        ModulusX = (fs.f10, 0), # psi
                        ModulusZ = (fs.f10, 0), # psi
                        ModulusY = (fs.f10, 0), # psi
                        ModulusG = (fs.f10, 0), # psi
                        Angle = (fs.f10, 0) # degrees
                        )

D2Duncan = cid_line(
                    # only for Model = 3
                    LRFDControl = (fs.d5, 0),
                    # 1.0 for in-situ materials
                    ModuliAveraging = (fs.f10, 0.5),
                    # Duncan: 0, Dancan/Selig: 1
                    Model = (fs.d5, 1),
                    # Original: 0, Unloading: 1
                    Unloading = (fs.d5, 1)
                    )

D3Duncan = cid_line(
                    # only for Model = 3
                    Cohesion = (fs.f10, 0), # psi
                    Phi_i = (fs.f10, 0), # degrees
                    Delta_Phi = (fs.f10, 0), # degrees
                    Modulus_i = (fs.f10, 0),
                    Modulus_n = (fs.f10, 0),
                    Ratio = (fs.f10, 0)
                    )
                    
D4Duncan = cid_line(
                    # only for Model = 3
                    Bulk_i = (fs.f10, 0),
                    Bulk_m = (fs.f10, 0),
                    Poissons = (fs.f10, 0)
                    )

D2Over = cid_line(
                    # only for Model = 4
                    # repeatable
                    Limit = (fs.s1, ' '),
                    Pressure = (fs.f9, 0),
                    Modulus = (fs.f10, 0), # psi
                    # granular: 0.3-0.35, mixed: 0.3-0.4,
                    # cohesive: 0.33-0.4
                    Poissons = (fs.f10, 0),
                    # End to indicate last entry of table
                    End = (fs.s3, '   ')
                    )

D2Hardin = cid_line(
                    # only for Model = 5
                    PoissonsLow = (fs.f10, 0.01),
                    PoissonsHigh = (fs.f10, 0.49),
                    Shape = (fs.f10, 0.26),
                    # GRAN: 0.60, MIXE: 0.5, COHE: 1.0
                    VoidRatio = (fs.f10, 0.6),
                    # GRAN: 0, MIXE: 0.5, COHE: 0.9
                    Saturation = (fs.f10, 0),
                    # GRAN: 0, MIXE: 0.05, COHE: 0.20
                    PI = (fs.f10, 0),
                    Nonlinear = (fs.d5, 0) # ignored
                    )

D2HardinTRIA = cid_line(
                        # only for Model = 5
                        PoissonsLow = (fs.f10, 0.01),
                        PoissonsHigh = (fs.f10, 0.49),
                        Shape = (fs.f10, 0.26),
                        S1 = (fs.f10, 0),
                        C1 = (fs.f10, 0),
                        A = (fs.f10, 0),
                        Nonlinear = (fs.d5, 0) # ignored
                        )

D2Interface = cid_line(
                        # only for Model = 6
                        Angle = (fs.f10, 0), # degrees
                        Friction = (fs.f10, 0),
                        Tensile = (fs.f10, 1), # lbs/in
                        Gap = (fs.f10, 0) # in
                        )

D2Composite = cid_line(
                        # only for Model = 7
                        Group1 = (fs.d5, 0),
                        Group2 = (fs.d5, 0),
                        Fraction = (fs.f10, 0)
                        )

D2MohrCoulomb = cid_line(
                        # only for Model = 8
                        Modulus = (fs.f10, 0), # psi
                        Poissons = (fs.f10, 0),
                        Cohesion = (fs.f10, 0), # psi
                        Phi = (fs.f10, 0) # degrees
                        )
