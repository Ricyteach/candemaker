import pytest
from pathlib import Path
from candemaker import *

@pytest.fixture
def cid_lines():
    return Path(r'tests\test_candemaker\test_input.cid').read_text().split('\n')

@pytest.mark.current
@pytest.mark.cande
def test_from_cid(cid_lines):
    CandeObj.from_cid(cid_lines)

@pytest.mark.cande
def test_CandeObj_empty():
    obj = CandeObj.empty()
