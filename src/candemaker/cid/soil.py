from . import CIDError, gen_line, CidEnum

reg_dict = {}

def D1Soil(cid, material_num):
    if cid.ninterf_materials == 0 and material_num == cid.nsoil_materials:
        yield from gen_line(cid, 'D1SoilL')
    else:
        yield from gen_line(cid, 'D1Soil')
    material = cid.soil_materials[material_num-1]
    if material.Model not in range(1, 9):
        raise CIDError('Invalid model number {:d} for material #{:d}'
                       ''.format(material.Model, material.ID))
    if material.Model in (7, 8): #  Interface or Composite
        raise CIDError('Interface or composite model number'
                       'found in soil material #{:d}'.format(material.ID))
    yield from D_gens[material.Model](material)

reg_dict.update({CidEnum.D1Soil : D1Soil})


def D1Interf(cid, material_num):
    if material_num == cid.ninterf_materials:
        yield from gen_line(cid, 'D1InterfL')
    else:
        yield from gen_line(cid, 'D1Interf')
    material = cid.interf_materials[material_num-1]
    if material.Model == 8:
        return NotImplemented
    if material.Model not in range(7, 8):
        raise CIDError('Non-interface or -composite model number ({:d})'
                       'found in interf material #{:d}'
                       ''.format(material.Model, material.ID))
    yield from D2Interface(material)

reg_dict.update({CidEnum.D1Interf : D1Interf})


# probably don't ever need these models
D2Orthotropic = None
D2Overburden = None
D2Hardin = None
D2HardinTRIA = None
D2Composite = None

reg_dict.update({CidEnum.D2Orthotropic : D2Orthotropic, CidEnum.D2Overburden : D2Overburden,
                CidEnum.D2Hardin : D2Hardin, CidEnum.D2HardinTRIA : D2HardinTRIA,
                CidEnum.D2Composite : D2Composite})


def D2MohrCoulomb(material):
    if material.Model != 8:
        raise CIDError('Model #{:d} invalid for mohr/coulomb'
                       ''.format(material.Model))
    yield from gen_line(cid, 'D2MohrCoulomb')

reg_dict.update({CidEnum.D2MohrCoulomb : D2MohrCoulomb})

def D2Isotropic(material):
    if material.Model != 1:
        raise CIDError('Model #{:d} invalid for isotropic'
                       ''.format(material.Model))
    yield from gen_line(cid, 'D2Isotropic')

reg_dict.update({CidEnum.D2Isotropic : D2Isotropic})


def D2Duncan(material):
    if material.Model != 3:
        raise CIDError('Model #{:d} invalid for duncan'
                       ''.format(material.Model))
    duncan_models = ('CA105 CA95 CA90 SM100 SM90 SM85'
                     'SC100 SC90 SC85 CL100 CL90 CL85').split()
    selig_models = ('SW100 SW95 SW90 SW85 SW80'
                    'ML95 ML90 ML85 ML80 ML50'
                    'CL95 CL90 CL85 CL80').split()

    yield from gen_line(cid, 'D2Duncan')
    if material.Name == 'USER':
        yield from gen_line(cid, 'D3Duncan')
        yield from gen_line(cid, 'D4Duncan')
    elif material.Name not in duncan_models + selig_models:
        raise CIDError('Invalid Duncan material name for '
                       '#{}'.format(material.ID))

reg_dict.update({CidEnum.D2Duncan : D2Duncan})


def D2Interface(material):
    if material.Model != 6:
        raise CIDError('Model #{:d} invalid for interface material'
                       ''.format(material.Model))
    yield from gen_line(cid, 'D2Interface')

reg_dict.update({CidEnum.D2Interface : D2Interface})


D_gens = (None, D2Isotropic, D2Orthotropic, D2Duncan, 
          D2Overburden, D2Hardin, D2HardinTRIA, D2Interface, 
          D2Composite, D2MohrCoulomb)
