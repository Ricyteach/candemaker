from . import CIDError
from ..cid import register


def D1Soil_gen(cid, struct, material_num):
    if cid.ninterf_materials == 0 and material_num == cid.nsoil_materials:
        yield SoilMaterialLast
    else:
        yield SoilMaterial
    material = cid.soil_materials[material_num-1]
    if material.Model not in range(1, 9):
        raise CIDError('Invalid model number {:d} for material #{:d}'
                       ''.format(material.Model, material.ID))
    if material.Model in (7, 8): #  Interface or Composite
        raise CIDError('Interface or composite model number'
                       'found in soil material #{:d}'.format(material.ID))
    yield from D_gens[material.Model](material)

def D1Interf_gen(cid, struct, material_num):
    if material_num == cid.ninterf_materials:
        yield InterfMaterialLast
    else:
        yield InterfMaterial
    material = cid.interf_materials[material_num-1]
    if material.Model == 8:
        return NotImplemented
    if material.Model not in range(7, 8):
        raise CIDError('Non-interface or -composite model number ({:d})'
                       'found in interf material #{:d}'
                       ''.format(material.Model, material.ID))
    yield from Interface_gen(material)


# probably don't ever need these models
(Orthotropic_gen, Overburden_gen, Hardin_gen,
HardinTRIA_gen, Composite_gen) = (None,)*5


def MohrCoulomb_gen(material):
    if material.Model != 8:
        raise CIDError('Model #{:d} invalid for mohr/coulomb'
                       ''.format(material.Model))
    yield MohrCoulomb

def Isotropic_gen(material):
    if material.Model != 1:
        raise CIDError('Model #{:d} invalid for isotropic'
                       ''.format(material.Model))
    yield Isotropic

def Duncan_gen(material):
    if material.Model != 3:
        raise CIDError('Model #{:d} invalid for duncan'
                       ''.format(material.Model))
    duncan_models = ('CA105 CA95 CA90 SM100 SM90 SM85'
                     'SC100 SC90 SC85 CL100 CL90 CL85').split()
    selig_models = ('SW100 SW95 SW90 SW85 SW80'
                    'ML95 ML90 ML85 ML80 ML50'
                    'CL95 CL90 CL85 CL80').split()

    yield Duncan2
    if material.Name == 'USER':
        yield Duncan3
        yield Duncan4
    elif material.Name not in duncan_models + selig_models:
        raise CIDError('Invalid Duncan material name for '
                       '#{}'.format(material.ID))

def Interface_gen(material):
    if material.Model != 6:
        raise CIDError('Model #{:d} invalid for interface material'
                       ''.format(material.Model))
    yield Interface

def register_objects():
    from collections import namedtuple as nt
    from .. import format_specs as fs
    from .general import ObjDef, add_specs_defaults_to_nts
    from mytools.blank import BlankInt

    # Section D1

    material_dict = dict(
                            Limit = ObjDef(fs.s1, ' '),
                            ID = ObjDef(fs.d4, 0),
                            # 1: isotropic, 2: orthotropic, 
                            # 3: Duncan/Selig, 4: Overburden,
                            # 5: Extended Hardin, 6: Interface, 
                            # 7: Composite Link, 8: Mohr/Coulomb
                            Model = ObjDef(fs.d5, 1),
                            Density = ObjDef(fs.f10, 0),
                            Name = ObjDef(fs.s20, ''),
                            # overburden model only
                            Layers = ObjDef(fs.d2, BlankInt())
                            )

    SoilMaterial = nt('SoilMaterial', 'ID Model Density Name Layers')
    SoilMaterialLast = nt('SoilMaterialLast', 'Limit ID Model Density Name Layers')
    InterfMaterial = nt('InterfMaterial', 'ID Model Density Name Layers')
    InterfMaterialLast = nt('InterfMaterialLast', 'Limit ID Model Density Name Layers')

    for NT in (SoilMaterial, SoilMaterialLast, InterfMaterial, InterfMaterialLast):
        NT._prefix = 'D-1'
        NT._name = 'D1'

    # Section D2 onward

    isotropic_dict = dict(
                            # only for Model = 1
                            Modulus = ObjDef(fs.f10, 0), # psi
                            Poissons = ObjDef(fs.f10, 0)
                            )

    Isotropic = nt('Isotropic', isotropic_dict.keys())
    Isotropic._prefix = 'D-2.Isotropic'
    Isotropic._name = 'D2Isotropic'

    orthotropic_dict = dict(
                            # only for Model = 2
                            ModulusX = ObjDef(fs.f10, 0), # psi
                            ModulusZ = ObjDef(fs.f10, 0), # psi
                            ModulusY = ObjDef(fs.f10, 0), # psi
                            ModulusG = ObjDef(fs.f10, 0), # psi
                            Angle = ObjDef(fs.f10, 0) # degrees
                            )

    Orthotropic = nt('Orthotropic', orthotropic_dict.keys())
    Orthotropic._prefix = 'D-2.Orthotropic'
    Orthotropic._name = 'D2Orthotropic'

    duncan2_dict = dict(
                        # only for Model = 3
                        LRFDControl = ObjDef(fs.d5, 0),
                        # 1.0 for in-situ materials
                        ModuliAveraging = ObjDef(fs.f10, 0.5),
                        # Duncan: 0, Dancan/Selig: 1
                        Model = ObjDef(fs.d5, 1),
                        # Original: 0, Unloading: 1
                        Unloading = ObjDef(fs.d5, 1)
                        )

    Duncan2 = nt('Duncan2', duncan2_dict.keys())
    Duncan2._prefix = 'D-2.Duncan'
    Duncan2._name = 'D2Duncan'

    duncan3_dict = dict(
                        # only for Model = 3
                        Cohesion = ObjDef(fs.f10, 0), # psi
                        Phi_i = ObjDef(fs.f10, 0), # degrees
                        Delta_Phi = ObjDef(fs.f10, 0), # degrees
                        Modulus_i = ObjDef(fs.f10, 0),
                        Modulus_n = ObjDef(fs.f10, 0),
                        Ratio = ObjDef(fs.f10, 0)
                        )
                        
    Duncan3 = nt('Duncan3', duncan3_dict.keys())
    Duncan3._prefix = 'D-3.Duncan'
    Duncan3._name = 'D3Duncan'

    duncan4_dict = dict(
                        # only for Model = 3
                        Bulk_i = ObjDef(fs.f10, 0),
                        Bulk_m = ObjDef(fs.f10, 0),
                        Poissons = ObjDef(fs.f10, 0)
                        )

    Duncan4 = nt('Duncan4', duncan4_dict.keys())
    Duncan4._prefix = 'D-4.Duncan'
    Duncan4._name = 'D4Duncan'

    overburden_dict = dict(
                            # only for Model = 4
                            # repeatable
                            Limit = ObjDef(fs.s1, ' '),
                            Pressure = ObjDef(fs.f9, 0),
                            Modulus = ObjDef(fs.f10, 0), # psi
                            # granular: 0.3-0.35, mixed: 0.3-0.4,
                            # cohesive: 0.33-0.4
                            Poissons = ObjDef(fs.f10, 0),
                            # End to indicate last entry of table
                            End = ObjDef(fs.s3, '   ')
                            )

    Overburden = nt('Overburden', overburden_dict.keys())
    Overburden._prefix = 'D-2.Over'
    Overburden._name = 'D2Over'

    hardin_dict = dict(
                        # only for Model = 5
                        PoissonsLow = ObjDef(fs.f10, 0.01),
                        PoissonsHigh = ObjDef(fs.f10, 0.49),
                        Shape = ObjDef(fs.f10, 0.26),
                        # GRAN: 0.60, MIXE: 0.5, COHE: 1.0
                        VoidRatio = ObjDef(fs.f10, 0.6),
                        # GRAN: 0, MIXE: 0.5, COHE: 0.9
                        Saturation = ObjDef(fs.f10, 0),
                        # GRAN: 0, MIXE: 0.05, COHE: 0.20
                        PI = ObjDef(fs.f10, 0),
                        Nonlinear = ObjDef(fs.d5, 0) # ignored
                        )

    Hardin = nt('Hardin', hardin_dict.keys())
    Hardin._prefix = 'D-2.Hardin'
    Hardin._name = 'D2Hardin'

    hardinTRIA_dict = dict(
                            # only for Model = 5
                            PoissonsLow = ObjDef(fs.f10, 0.01),
                            PoissonsHigh = ObjDef(fs.f10, 0.49),
                            Shape = ObjDef(fs.f10, 0.26),
                            S1 = ObjDef(fs.f10, 0),
                            C1 = ObjDef(fs.f10, 0),
                            A = ObjDef(fs.f10, 0),
                            Nonlinear = ObjDef(fs.d5, 0) # ignored
                            )

    HardinTRIA = nt('HardinTRIA', hardinTRIA_dict.keys())
    HardinTRIA._prefix = 'D-2.Hardin.TRIA'
    HardinTRIA._name = 'D2HardinTRIA'

    interface_dict = dict(
                            # only for Model = 6
                            Angle = ObjDef(fs.f10, 0), # degrees
                            Friction = ObjDef(fs.f10, 0),
                            Tensile = ObjDef(fs.f10, 1), # lbs/in
                            Gap = ObjDef(fs.f10, 0) # in
                            )

    Interface = nt('Interface', interface_dict.keys())
    Interface._prefix = 'D-2.Interface'
    Interface._name = 'D2Interface'

    composite_dict = dict(
                            # only for Model = 7
                            Group1 = ObjDef(fs.d5, 0),
                            Group2 = ObjDef(fs.d5, 0),
                            Fraction = ObjDef(fs.f10, 0)
                            )

    Composite = nt('Composite', composite_dict.keys())
    Composite._prefix = 'D-2.Composite'
    Composite._name = 'D2Composite'

    mohrcoulomb_dict = dict(
                            # only for Model = 8
                            Modulus = ObjDef(fs.f10, 0), # psi
                            Poissons = ObjDef(fs.f10, 0),
                            Cohesion = ObjDef(fs.f10, 0), # psi
                            Phi = ObjDef(fs.f10, 0) # degrees
                            )

    MohrCoulomb = nt('MohrCoulomb', mohrcoulomb_dict.keys())
    MohrCoulomb._prefix = 'D-2.MohrCoulomb'
    MohrCoulomb._name = 'D2MohrCoulomb'

    for obj, d, gen in ((SoilMaterial, material_dict, D1Soil_gen),
                        (SoilMaterialLast, material_dict, D1Soil_gen),
                        (InterfMaterial, material_dict, D1Interf_gen),
                        (InterfMaterialLast, material_dict, D1Interf_gen),
                        (Isotropic, isotropic_dict, Isotropic_gen),
                        (Orthotropic, orthotropic_dict, Orthotropic_gen),
                        (Duncan2, duncan2_dict, Duncan_gen),
                        (Duncan3, duncan3_dict, Duncan_gen),
                        (Duncan4, duncan4_dict, Duncan_gen),
                        (Overburden, overburden_dict, Overburden_gen),
                        (Hardin, hardin_dict, Hardin_gen),
                        (HardinTRIA, hardinTRIA_dict, HardinTRIA_gen),
                        (Interface, interface_dict, Interface_gen),
                        (Composite, composite_dict, Composite_gen),
                        (MohrCoulomb, mohrcoulomb_dict, MohrCoulomb_gen)
                        ):
        add_specs_defaults_to_nts(obj, d)
        register(obj, d, gen)
        yield obj

for obj in register_objects():
    exec('{} = obj'.format(obj.__name__))

D_gens = (None, Isotropic_gen, Orthotropic_gen, Duncan_gen, 
          Overburden_gen, Hardin_gen, HardinTRIA_gen, Interface_gen, 
          Composite_gen, MohrCoulomb_gen)
          
del register_objects
del register
del obj
del CIDError
