from candemaker.cid.unformatter import UnformatterReg


def test_A1():
    assert UnformatterReg['A1'].value.format() == '                      A-1!!ANALYS   3 1  1                                                              -99    0    0    0'

def test_D1():
    assert UnformatterReg['D1'].value.format() == '                      D-1!!    0    1    0.0000                     0'
