from . import CidEnum

class CIDError(Exception):
    pass

reg_dict = {}

def gen_line(cid, tag):
    '''Generate the CID enum member from the tag'''
    yield CidEnum[tag]


def A1(cid):
    yield from gen_line(cid, 'A1')
    if cid.level == 3:
        from .L3 import A2
        for group_num in range(1, cid.ngroups + 1):
            try:
                yield from A2(cid, group_num)
            except Exception as e:
                raise CIDError('cid failed at pipe group #'
                               '{:d}'.format(group_num)) from e
    else:
        return 'L1 and L2 not implemented'

reg_dict.update({CidEnum.A1 : A1})

def E1(cid, struct):
    if cid.method == 0: #  WSD
        raise CIDError('E1 should only be applied to LRFD problems')
    yield gen_line(cid, 'E1')

reg_dict.update({CidEnum.E1 : E1})