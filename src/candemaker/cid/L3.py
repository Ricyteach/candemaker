from . import CIDError, E1, pipe, soil, gen_line, CidEnum


reg_dict = {}

def A2(cid, group_num):
    yield from gen_line(cid, 'A2')
    group = cid.groups[group_num-1]
    try:
        typ = group.Type
        gen = pipe.lookup[typ]
        yield from gen(cid, group)
    except Exception as e:
        raise CIDError('cid section B failed for '
                       '{}'.format(group)) from e

reg_dict.update({CidEnum.A2 : A2})


def C1(cid):
    yield from 'C1'

reg_dict.update({CidEnum.C1 : C1})


def C2(cid):
    yield from gen_line(cid, 'C2')
    for n_objs, gen, name in ((cid.nnodes, C3, 'node'),
                              (cid.nelements, C4, 'element'),
                              (cid.nbounds, C5, 'boundary'),
                              (cid.nsoil_materials, soil.D1Soil, 'soil material'),
                              (cid.ninterf_materials, soil.D1Interf, 'interf material')):
        for cid_obj_num in range(1, n_objs + 1):
            try:
                yield from gen(cid, cid_obj_num)
            except Exception as e:
                raise CIDError('cid L3.C2 failed at {} #'
                               '{:d}'.format(name, cid_obj_num)) from e
    if cid.method == 1: #  LRFD
        for step_num, _ in enumerate(range(cid.nsteps), 1):
            yield from E1(cid)

reg_dict.update({CidEnum.C2 : C2})


def C3(cid, node_num):
    if node_num == cid.nnodes: 
        yield from gen_line(cid, 'C3L')
    else:
        yield from gen_line(cid,  'C3')

reg_dict.update({CidEnum.C3 : C3})


def C4(cid, element_num):
    if element_num == cid.nelements: 
        yield from gen_line(cid, 'C4L')
    else:
        yield from gen_line(cid,  'C4')


reg_dict.update({CidEnum.C4 : C4})


def C5(cid, bound_num):
    if bound_num == cid.nbounds: 
        yield from gen_line(cid, 'C5L')
    else:
        yield from gen_line(cid,  'C5')


reg_dict.update({CidEnum.C5 : C5})
