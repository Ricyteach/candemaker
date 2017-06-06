from candemaker.L3_parmatters import C1, C2, C3, C4, C5
import pytest

def test_C1():
    assert C1.format() == '                   C-1.L3!!PREP                                                                    '
    
def test_C2():
    assert C2.format() == '                   C-2.L3!!    1    3    1    3    1    0    0    0    0    0    1'
    
def test_C3():
    assert C3.format() == '                   C-3.L3!!    0  000    0.0000    0.0000    0         0.0000    0.0000'
    
def test_C4():
    assert C4.format() == '                   C-4.L3!!    0    0    0    0    0    0    0    1    1    1    0  100'
    
def test_C5():
    assert C5.format() == '                   C-5.L3!!    0    0    0.0000    0    0.0000    0.0000    0    0    0    0.0000    0.0000'