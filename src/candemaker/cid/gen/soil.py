from .. import exceptions as exc
from . import gen_line

__all__ = 'D1 D2Isotropic D2Duncan D2Interface D2MohrCoulomb'.split()


def D1(cid):
    for n_objs, nxt, name in ((cid.nsoil_materials, D1Soil, 'soil material'),
                              (cid.ninterf_materials, D1Interf, 'interf material')):
        for cid_obj_num in range(1, n_objs + 1):
            try:
                yield from nxt(cid, cid_obj_num)
            except StopIteration:
                raise
            except Exception as e:
                raise exc.CIDError('cid D1 failed at {} #'
                               '{:d}'.format(name, cid_obj_num)) from e
        cid.listener.throw(exc.SequenceComplete, ('{}s completed'.format(name), len(cid.materials)))


def D1Soil(cid, material_num):
    if cid.ninterf_materials == 0 and material_num == cid.nsoil_materials:
        yield from gen_line('D1L')
    else:
        yield from gen_line('D1Soil')
    material = cid.soil_materials[material_num-1]
    if material.model not in range(1, 9):
        raise exc.CIDError('Invalid model number {:d} for material #{:d}'
                           ''.format(material.model, material.id))
    if material.model in (7, 8): #  Interface or Composite
        raise exc.CIDError('Interface or composite model number'
                           'found in soil material #{:d}'.format(material.id))
    D_nxts[material.model](material)
    cid.listener.throw(exc.ObjectComplete)


def D1Interf(cid, material_num):
    if material_num == cid.ninterf_materials:
        yield from gen_line('D1L')
    else:
        yield from gen_line('D1Interf')
    material = cid.interf_materials[material_num-1]
    if material.model == 8:
        return NotImplemented
    if material.model not in range(7, 8):
        raise exc.CIDError('Non-interface or -composite model number ({:d})'
                       'found in interf material #{:d}'
                       ''.format(material.model, material.id))
    D2Interface(material)
    cid.listener.throw(exc.ObjectComplete)


# probably don't ever need these models
D2Orthotropic = None
D2Overburden = None
D2Hardin = None
D2HardinTRIA = None
D2Composite = None


def D2MohrCoulomb(material):
    if material.model != 8:
        raise exc.CIDError('Model #{:d} invalid for mohr/coulomb'
                       ''.format(material.model))
    yield from gen_line('D2MohrCoulomb')


def D2Isotropic(material):
    if material.model != 1:
        raise exc.CIDError('Model #{:d} invalid for isotropic'
                       ''.format(material.model))
    yield from gen_line('D2Isotropic')


def D2Duncan(material):
    if material.model != 3:
        raise exc.CIDError('Model #{:d} invalid for duncan'
                       ''.format(material.model))
    duncan_models = ('CA105 CA95 CA90 SM100 SM90 SM85'
                     'SC100 SC90 SC85 CL100 CL90 CL85').split()
    selig_models = ('SW100 SW95 SW90 SW85 SW80'
                    'ML95 ML90 ML85 ML80 ML50'
                    'CL95 CL90 CL85 CL80').split()

    yield from gen_line('D2Duncan')
    if material.name == 'USER':
        yield from gen_line('D3Duncan')
        yield from gen_line('D4Duncan')
    elif material.name not in duncan_models + selig_models:
        raise exc.CIDError('Invalid Duncan material name for '
                       '#{}'.format(material.id))


def D2Interface(material):
    if material.model != 6:
        raise exc.CIDError('Model #{:d} invalid for interface material'
                       ''.format(material.model))
    yield from gen_line('D2Interface')

D_nxts = (None, D2Isotropic, D2Orthotropic, D2Duncan, 
          D2Overburden, D2Hardin, D2HardinTRIA, D2Interface, 
          D2Composite, D2MohrCoulomb)
