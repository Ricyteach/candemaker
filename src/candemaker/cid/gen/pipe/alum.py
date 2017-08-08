def B1Alum(cid, group):
    cid.listener.send('B1Alum')
    yield
    if cid.mode == 'ANALYS':
        cid.listener.send('B2AlumA')
        yield
    elif cid.mode == 'DESIGN':
        if cid.method == 0: #  WSD
            cid.listener.send('B2AlumDWSD')
            yield
        if cid.method == 1: #  LRFD
            cid.listener.send('B2AlumDLRFD')
            yield
    if cid.method == 1: #  LRFD
        cid.listener.send('B3AlumADLRFD')
        yield
