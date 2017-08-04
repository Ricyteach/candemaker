from candemaker.msh import read as read_msh
from pathlib import Path
import pytest

def test_read_msh():
    path = Path(r'tests\test_candemaker\test_mesh.msh').resolve()
    mesh=read_msh(path)
    assert tuple(len(member) for member in mesh) == (641, 588, 156)
    with pytest.raises(ValueError):
        read_msh(path,validate=True)
