from .. import exceptions as exc

__all__ = 'A1 E1'.split()

def A1(cid):
    cid.listener.send('A1')
    yield
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
    cid.listener.send('E1')
    yield
