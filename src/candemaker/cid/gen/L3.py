from ..enum import CidEnum
from . import CIDError, pipe, soil, gen_line

__all__ = 'A2 C1 C2 C3 C4 C5'.split()

def A2(cid, group_num):
    yield from gen_line('A2')
    group = cid.groups[group_num-1]
    try:
        typ = group.Type
        gen = pipe.lookup[typ]
        yield from gen(cid, group)
    except Exception as e:
        raise CIDError('cid section B failed for '
                       '{}'.format(group)) from e
    yield from C1(cid)


def C1(cid):
    yield from gen_line('C1')
    yield from C2(cid)


def C2(cid):
    yield from gen_line('C2')
    for n_objs, gen, name in ((cid.nnodes, C3, 'node'),
                              (cid.nelements, C4, 'element'),
                              (cid.nbounds, C5, 'boundary')):
        for cid_obj_num in range(1, n_objs + 1):
            try:
                yield from gen(cid, cid_obj_num)
            except Exception as e:
                raise CIDError('cid L3.C2 failed at {} #'
                               '{:d}'.format(name, cid_obj_num)) from e
    


def C3(cid, node_num):
    if node_num == cid.nnodes: 
        yield from gen_line('C3L')
    else:
        yield from gen_line('C3')


def C4(cid, element_num):
    if element_num == cid.nelements: 
        yield from gen_line('C4L')
    else:
        yield from gen_line('C4')


def C5(cid, bound_num):
    if bound_num == cid.nbounds: 
        yield from gen_line('C5L')
    else:
        yield from gen_line('C5')
    yield from soil.D1(cid)
