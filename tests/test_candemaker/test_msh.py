from candemaker.msh import read as read_msh
from pathlib import Path
import pytest

path=Path('tests\\test_candemaker\\test_mesh.msh')

@pytest.mark.current
def test_read_msh():
    mesh=read_msh(path)
    assert tuple(len(member) for member in mesh) == (641, 588, 156)
    with pytest.raises(ValueError):
        read_msh(path,validate=True)