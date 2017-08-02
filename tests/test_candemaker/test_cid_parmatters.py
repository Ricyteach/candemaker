from candemaker.cid.unformatter import unformatter_reg


def test_A1():
    assert unformatter_reg['A1'].format() == '                      A-1!!ANALYS   3 1  1                                                              -99    0    0    0'

def test_D1():
    assert unformatter_reg['D1'].format() == '                      D-1!!    0    1    0.0000                     0'
