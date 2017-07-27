from candemaker.cid_parmatters import A1, D1


def test_A1():
    assert A1.format() == '                      A-1!!ANALYS   3 1  1                                                              -99    0    0    0'
                                                                                                                            
def test_D1():
    assert D1.format() == '                      D-1!!    0    1    0.0000                     0'