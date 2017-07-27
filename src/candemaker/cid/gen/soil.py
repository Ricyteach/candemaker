from . import CIDError, gen_line, E1

__all__ = 'D1 D2Isotropic D2Duncan D2Interface D2MohrCoulomb'.split()

def D1(cid):
    for n_objs, gen, name in ((cid.nsoil_materials, D1Soil, 'soil material'),
                              (cid.ninterf_materials, D1Interf, 'interf material')):
        for cid_obj_num in range(1, n_objs + 1):
            try:
                yield from gen(cid, cid_obj_num)
            except Exception as e:
                raise CIDError('cid D1 failed at {} #'
                               '{:d}'.format(name, cid_obj_num)) from e
    if cid.method == 1: #  LRFD
        for step_num, _ in enumerate(range(cid.nsteps), 1):
            yield from E1(cid)


def D1Soil(cid, material_num):
    if cid.ninterf_materials == 0 and material_num == cid.nsoil_materials:
        yield from gen_line('D1L')
    else:
        yield from gen_line('D1Soil')
    material = cid.soil_materials[material_num-1]
    if material.Model not in range(1, 9):
        raise CIDError('Invalid model number {:d} for material #{:d}'
                       ''.format(material.Model, material.ID))
    if material.Model in (7, 8): #  Interface or Composite
        raise CIDError('Interface or composite model number'
                       'found in soil material #{:d}'.format(material.ID))
    yield from D_gens[material.Model](material)


def D1Interf(cid, material_num):
    if material_num == cid.ninterf_materials:
        yield from gen_line('D1L')
    else:
        yield from gen_line('D1Interf')
    material = cid.interf_materials[material_num-1]
    if material.Model == 8:
        return NotImplemented
    if material.Model not in range(7, 8):
        raise CIDError('Non-interface or -composite model number ({:d})'
                       'found in interf material #{:d}'
                       ''.format(material.Model, material.ID))
    yield from D2Interface(material)


# probably don't ever need these models
D2Orthotropic = None
D2Overburden = None
D2Hardin = None
D2HardinTRIA = None
D2Composite = None


def D2MohrCoulomb(material):
    if material.Model != 8:
        raise CIDError('Model #{:d} invalid for mohr/coulomb'
                       ''.format(material.Model))
    yield from gen_line('D2MohrCoulomb')


def D2Isotropic(material):
    if material.Model != 1:
        raise CIDError('Model #{:d} invalid for isotropic'
                       ''.format(material.Model))
    yield from gen_line('D2Isotropic')


def D2Duncan(material):
    if material.Model != 3:
        raise CIDError('Model #{:d} invalid for duncan'
                       ''.format(material.Model))
    duncan_models = ('CA105 CA95 CA90 SM100 SM90 SM85'
                     'SC100 SC90 SC85 CL100 CL90 CL85').split()
    selig_models = ('SW100 SW95 SW90 SW85 SW80'
                    'ML95 ML90 ML85 ML80 ML50'
                    'CL95 CL90 CL85 CL80').split()

    yield from gen_line('D2Duncan')
    if material.Name == 'USER':
        yield from gen_line('D3Duncan')
        yield from gen_line('D4Duncan')
    elif material.Name not in duncan_models + selig_models:
        raise CIDError('Invalid Duncan material name for '
                       '#{}'.format(material.ID))


def D2Interface(material):
    if material.Model != 6:
        raise CIDError('Model #{:d} invalid for interface material'
                       ''.format(material.Model))
    yield from gen_line('D2Interface')


D_gens = (None, D2Isotropic, D2Orthotropic, D2Duncan, 
          D2Overburden, D2Hardin, D2HardinTRIA, D2Interface, 
          D2Composite, D2MohrCoulomb)
