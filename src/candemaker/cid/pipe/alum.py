from .. import gen_line, CidEnum

reg_dict = {}

def B1Alum(cid, group):
    yield from gen_line(cid, 'B1Alum')
    if cid.mode == 'ANALYS':
        yield from gen_line(cid, 'B2AlumA')
    elif cid.mode == 'DESIGN':
        if cid.method == 0: #  WSD
            yield from gen_line(cid, 'B2AlumDWSD')
        if cid.method == 1: #  LRFD
            yield from gen_line(cid, 'B2AlumDLRFD')
    if cid.method == 1: #  LRFD
        yield from gen_line(cid, 'B3AlumADLRFD')

reg_dict.update({CidEnum.B1Alum : B1Alum})
