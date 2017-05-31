import pytest

@pytest.mark.incremental
@pytest.mark.current
def test_import():
    import candemaker
    assert candemaker