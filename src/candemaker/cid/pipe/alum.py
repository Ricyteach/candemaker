reg_dict = {}

def B1Alum(cid, group):
    yield 'B1Alum'
    if cid.mode == 'ANALYS':
        yield 'B2AlumA'
    elif cid.mode == 'DESIGN':
        if cid.method == 0: #  WSD
            yield 'B2AlumDWSD'
        if cid.method == 1: #  LRFD
            yield 'B2AlumDLRFD'
    if cid.method == 1: #  LRFD
        yield 'B3AlumADLRFD'

reg_dict.update(B1Alum = B1Alum)