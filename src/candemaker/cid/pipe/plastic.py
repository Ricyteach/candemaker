from .. import CIDError, gen_line, CidEnum

reg_dict = {}

def B1Plastic(cid, group):
    yield from gen_line(cid, 'B1Plastic')
    yield from B2Plastic(cid, group)

reg_dict.update({CidEnum.B1Plastic : B1Plastic})

def B2Plastic(cid, group):
    yield from gen_line(cid, 'B2Plastic')
    yield from B3_dict[group.WallType](cid)
    if cid.method == 1:  # LRFD
        yield from B4Plastic(cid)

reg_dict.update({CidEnum.B2Plastic : B2Plastic})


def B3PlasticGeneral(cid):
    if cid.mode != 'ANALYS':
        raise CIDError('General plastic pipe type for ANALYS mode only')
    yield from gen_line(cid, 'B3PlasticAGeneral')

# reg_dict.update({CidEnum.B3PlasticGeneral : B3PlasticGeneral})


def B3PlasticSmooth(cid):
    if cid.mode == 'ANALYS':
        yield from gen_line(cid, 'B3PlasticASmooth')
    elif cid.mode == 'DESIGN':
        if cid.method == 0:  # WSD
            yield from gen_line(cid, 'B3PlasticDWSD')
        elif cid.method == 1:  # LRFD
            yield from gen_line(cid, 'B3PlasticDLRFD')

# reg_dict.update({CidEnum.B3PlasticSmooth : B3PlasticSmooth})


def B3PlasticProfile(cid):
    if cid.mode != 'ANALYS':
        raise CIDError('Profile plastic pipe type for ANALYS mode only')
    yield from gen_line(cid, 'B3PlasticAProfile')
    yield from gen_line(cid, 'B3bPlasticAProfile')

# reg_dict.update({CidEnum.B3PlasticProfile : B3PlasticProfile})


def B4Plastic(cid):        
        yield from gen_line(cid, 'B4Plastic')

# reg_dict.update({CidEnum.B4Plastic : B4Plastic})


B3_dict = dict(
                GENERAL=B3PlasticGeneral,
                SMOOTH=B3PlasticSmooth,
                PROFILE=B3PlasticProfile
                )
