from .. import exceptions as exc
from ..enum import CidEnum

__all__ = 'A1 E1'.split()


def gen_line(tag):
    '''Validate the CID tag'''
    yield CidEnum[tag].name # execution pauses here


def A1(cid):
    yield from gen_line('A1')
    if cid.level == 3:
        from .L3 import L3
        yield from L3(cid)
    else:
        raise exc.CIDError('L1 and L2 not yet implemented')
    if cid.method == 1: #  LRFD
        for step_num, _ in enumerate(range(cid.nsteps), 1):
            yield from E1(cid)
        cid.listener.throw(exc.SequenceComplete, ('Factors completed', len(cid.factors)))


def E1(cid):
    yield from gen_line('E1')
