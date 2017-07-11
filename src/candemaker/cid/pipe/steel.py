from .. import gen_line, CidEnum

reg_dict = {}

def B1Steel(cid, struct, group):
    yield from gen_line(cid, 'B1Steel')
    if cid.mode == 'ANALYS':
        yield from gen_line(cid, 'B2SteelA')
    elif cid.mode == 'DESIGN':
        if cid.method == 0: #  WSD
            yield from gen_line(cid, 'B2SteelDWSD')
        if cid.method == 1: #  LRFD
            yield from gen_line(cid, 'B2SteelDLRFD')
    if group.JointSlip: #  Slotted Joints
        yield from gen_line(cid, 'B2bSteel')
        if cid.level > 1:
            yield from gen_line(cid, 'B2cSteel')
            if group.VaryTravel: # Model of "Half Joints"
                yield from gen_line(cid, 'B2dSteel')
    if cid.method == 1: #  LRFD
        yield from gen_line(cid, 'B3SteelADLRFD')

reg_dict.update({CidEnum.B1Steel : B1Steel})
