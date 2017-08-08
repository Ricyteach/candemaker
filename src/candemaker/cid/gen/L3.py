from .. import exceptions as exc
from . import pipe, soil

__all__ = 'L3 A2 C1 C2 C3 C4 C5'.split()

def L3(cid):
    for group_num, _ in enumerate(range(cid.ngroups), 1):
        try:
            yield from A2(cid, group_num)
        except Exception as e:
            raise exc.CIDError('cid failed at pipe group #'
                               '{:d}'.format(group_num)) from e
    cid.listener.throw(exc.SequenceComplete, ('Groups completed', len(cid.groups)))
    yield from C1(cid)
    yield from C2(cid)
    yield from soil.D1(cid)


def A2(cid, group_num):
    cid.listener.send('A2')
    yield
    group = cid.groups[group_num-1]
    try:
        typ = group.type
        gen = pipe.lookup[typ]
        yield from gen(cid, group)
    except Exception as e:
        raise exc.CIDError('cid section B failed for '
                       '{}'.format(group)) from e
    cid.listener.throw(exc.ObjectComplete)


def C1(cid):
    cid.listener.send('C1')
    yield


def C2(cid):
    cid.listener.send('C2')
    yield
    for n_objs, gen, name, nplural in ((cid.nnodes, C3, 'node', 'nnodes'),
                              (cid.nelements, C4, 'element', 'nelements'),
                              (cid.nbounds, C5, 'boundary', 'nboundaries')):
        for cid_obj_num in range(1, n_objs + 1):
            try:
                gen(cid, cid_obj_num)
                yield
            except Exception as e:
                raise exc.CIDError('cid L3.{} failed at {} #'
                               '{:d}'.format(gen.__name__, name,
                                             cid_obj_num)) from e
        cid.listener.throw(exc.SequenceComplete, ('{}s completed'.format(name), getattr(cid, nplural)))


def C3(cid, node_num):
    if node_num == cid.nnodes: 
        cid.listener.send('C3L')
    else:
        cid.listener.send('C3')


def C4(cid, element_num):
    if element_num == cid.nelements: 
        cid.listener.send('C4L')
    else:
        cid.listener.send('C4')


def C5(cid, bound_num):
    if bound_num == cid.nbounds: 
        cid.listener.send('C5L')
    else:
        cid.listener.send('C5')
