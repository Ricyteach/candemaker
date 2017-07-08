from . import CIDError, E1, pipe, soil

reg_dict = {}

def A2(cid, group_num):
    yield 'A2'
    group = cid.groups[group_num-1]
    try:
        typ = group.Type
        gen = pipe.lookup[typ]
        yield from gen(cid, group)
    except Exception as e:
        raise CIDError('cid section B failed for '
                       '{}'.format(group)) from e

reg_dict.update(A2 = A2)


def C1(cid):
    yield 'C1'

reg_dict.update(C1 = C1)


def C2(cid):
    yield 'C2'
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

reg_dict.update(C2 = C2)


def C3(cid, node_num):
    yield 'C3L' if node_num == cid.nnodes else 'C3'

reg_dict.update(C3 = C3)


def C4(cid, element_num):
    yield 'C4L' if element_num == cid.nelements else 'C4'

reg_dict.update(C4 = C4)


def C5(cid, bound_num):
    yield 'C5L' if bound_num == cid.nbounds else 'C5'

reg_dict.update(C5 = C5)
