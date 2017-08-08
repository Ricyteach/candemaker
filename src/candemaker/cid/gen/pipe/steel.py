def B1Steel(cid, group):
    cid.listener.send('B1Steel')
    yield
    if cid.mode == 'ANALYS':
        cid.listener.send('B2SteelA')
        yield
    elif cid.mode == 'DESIGN':
        if cid.method == 0: #  WSD
            cid.listener.send('B2SteelDWSD')
            yield
        if cid.method == 1: #  LRFD
            cid.listener.send('B2SteelDLRFD')
            yield
    import pdb;pdb.set_trace()
    if group.jointslip: #  Slotted Joints
        cid.listener.send('B2bSteel')
        yield
        if cid.level > 1:
            cid.listener.send('B2cSteel')
            yield
            if group.varytravel: # Model of "Half Joints"
                cid.listener.send('B2dSteel')
                yield
    if cid.method == 1: #  LRFD
        cid.listener.send('B3SteelADLRFD')
        yield
