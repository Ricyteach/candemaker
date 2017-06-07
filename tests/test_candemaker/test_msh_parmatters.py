from pathlib import Path
from candemaker.msh_parmatters import CountLine, NodeLine, ElementLine, BoundaryLine
import pytest

@pytest.fixture(scope='module')
def msh_lines():
    path=Path('tests\\test_candemaker\\test_mesh.msh')
    with open(path) as f:
        lines=f.readlines()
    return lines

@pytest.mark.parametrize('i, value',
                            [  
                            (0, 641),
                            (642, 588),
                            (1232, 156),
                            ],
                            ids=['Nodes','Elements','Boundaries'])
def test_CountLine(i, value, msh_lines):
    test=CountLine.unformat(msh_lines[i]).fixed[0]
    assert test==value
        
@pytest.mark.parametrize('i',
                            [  
                            1,
                            2,
                            102,
                            ],
                            ids=['Node1','Node2','Node3'])
def test_NodeLine(i, msh_lines):
    test=tuple(NodeLine.unformat(msh_lines[i]).fixed)
    n,x,y=test
    value = int(n), float(x), float(y)
    assert test==value

@pytest.mark.parametrize('i',
                            [  
                            644,
                            645,
                            646,
                            ],
                            ids=['Element1','Element2','Element3'])
def test_ElementLine(i, msh_lines):
    test=tuple(ElementLine.unformat(msh_lines[i]).fixed)
    n,i,j,k,l=test
    value = tuple(int(v) for v in (n,i,j,k,l))
    assert test==value

@pytest.mark.parametrize('i',
                            [  
                            1233,
                            1234,
                            1235,
                            ],
                            ids=['Boundary1','Boundary2','Boundary3'])
def test_BoundaryLine(i, msh_lines):
    test=tuple(BoundaryLine.unformat(msh_lines[i]).fixed)
    n,b=test
    value = tuple(int(v) for v in (n,b))
    assert test==value
