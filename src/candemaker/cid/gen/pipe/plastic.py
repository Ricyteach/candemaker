from ... import exceptions as exc


def B1Plastic(cid, group):
    cid.listener.send('B1Plastic')
    yield
    yield from B2Plastic(cid, group)


def B2Plastic(cid, group):
    cid.listener.send('B2Plastic')
    yield
    yield from B3_dict[group.walltype](cid)
    if cid.method == 1:  # LRFD
        yield from B4Plastic(cid)


def B3PlasticGeneral(cid):
    if cid.mode != 'ANALYS':
        raise exc.CIDError('General plastic pipe type for ANALYS mode only')
    cid.listener.send('B3PlasticAGeneral')
    yield


def B3PlasticSmooth(cid):
    if cid.mode == 'ANALYS':
        cid.listener.send('B3PlasticASmooth')
        yield
    elif cid.mode == 'DESIGN':
        if cid.method == 0:  # WSD
            cid.listener.send('B3PlasticDWSD')
            yield
        elif cid.method == 1:  # LRFD
            cid.listener.send('B3PlasticDLRFD')
            yield


def B3PlasticProfile(cid):
    if cid.mode != 'ANALYS':
        raise exc.CIDError('Profile plastic pipe type for ANALYS mode only')
    cid.listener.send('B3PlasticAProfile')
    yield
    cid.listener.send('B3bPlasticAProfile')
    yield


def B4Plastic(cid):        
    cid.listener.send('B4Plastic')
    yield


B3_dict = dict(
                GENERAL=B3PlasticGeneral,
                SMOOTH=B3PlasticSmooth,
                PROFILE=B3PlasticProfile
                )
