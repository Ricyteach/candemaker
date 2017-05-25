from candemaker.mshmaker import CountLine, NodeLine, ElementLine, BoundaryLine    
import pytest

def test_Count():
    assert CountLine.format(**dict(Num=35)) == '35'
    
def test_NodeLine():
    assert NodeLine
    
def test_ElementLine():
    assert ElementLine
    
def test_BoundaryLine():
    assert BoundaryLine