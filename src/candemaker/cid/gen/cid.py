from ..enum import CidEnum

__all__ = 'A1 E1'.split()

class CIDError(Exception):
    pass

class Complete(CIDError):
    pass

class SectionComplete(Complete):
    pass

class ObjectComplete(Complete):
    pass

'''
def gen_line(receiver, tag):
    while True:
        try:
            # Validate the CID tag
            receiver.send(CidEnum[tag].name)
            yield
        except Complete as err:
            receiver.throw(err)
'''

def A1(cid):
    from .L3 import A2
    cid.listener.send('A1')
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
    cid.listener.send('E1')
    cid.listener.throw(SectionComplete)
