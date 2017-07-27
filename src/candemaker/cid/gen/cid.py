from ..enum import CidEnum

__all__ = 'A1 E1'.split()

class CIDError(Exception):
    pass

def gen_line(tag):
    '''Validate the CID tag'''
    yield CidEnum[tag].name


def A1(cid):
    from .L3 import A2
    yield from gen_line('A1')
    if cid.level == 3:
        for group_num in range(1, cid.ngroups + 1):
            try:
                yield from A2(cid, group_num)
            except Exception as e:
                raise CIDError('cid failed at pipe group #'
                               '{:d}'.format(group_num)) from e
    else:
        return 'L1 and L2 not implemented'


def E1(cid):
    if cid.method == 0: #  WSD
        raise CIDError('E1 should only be applied to LRFD problems')
    yield from gen_line('E1')
