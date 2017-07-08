reg_dict = {}

def B1Steel(cid, struct, group):
    yield 'B1Steel'
    if cid.mode == 'ANALYS':
        yield 'B2SteelA'
    elif cid.mode == 'DESIGN':
        if cid.method == 0: #  WSD
            yield 'B2SteelDWSD'
        if cid.method == 1: #  LRFD
            yield 'B2SteelDLRFD'
    if group.JointSlip: #  Slotted Joints
        yield 'B2bSteel'
        if cid.level > 1:
            yield 'B2cSteel'
            if group.VaryTravel: # Model of "Half Joints"
                yield 'B2dSteel'
    if cid.method == 1: #  LRFD
        yield 'B3SteelADLRFD'

reg_dict.update(B1Steel = B1Steel)
