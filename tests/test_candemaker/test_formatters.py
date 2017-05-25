from candemaker.formatters import StaticFormatter, DefaultFormatter, AttrFormatter, PositionalDefaultFormatter, KeywordFormatter, VersatileFormatter
import pytest

def test_StaticFormatter():
    f=StaticFormatter('{: >5d}')
    assert f.format(1) == '    1'
    with pytest.raises(IndexError):
        f.format()
    with pytest.raises(ValueError):
        f.format('')
    f=StaticFormatter('{a: >5d}')
    with pytest.raises(KeyError):
        f.format()
    with pytest.raises(ValueError):
        f.format(a='')
    
def test_DefaultFormatter():
    f=DefaultFormatter({0: 1})
    assert f.format('{: >5d}') == '    1'
    with pytest.raises(IndexError):
        f.format('{: >5d}{: >5d}')
    with pytest.raises(ValueError):
        f.format('{: >5s}')
    f=DefaultFormatter(dict(a=1,b=2,c=3))
    assert f.format('{a: >5d}{b: >5d}') == '    1    2'
    with pytest.raises(KeyError) as exc:
        f.format('{a: >5d}{d: >5d}')
    assert "key = 'd'" in str(exc.value)
    with pytest.raises(ValueError) as exc:
        f.format('{a: >5s}')
    assert "format code 's'" in str(exc.value)
        
def test_AttrFormatter():
    f=AttrFormatter()
    assert f.format('{a: >5d}', a=1) == '    1'
    class C(): pass
    c=C()
    setattr(c,'a',1)
    assert f.format('{a: >5d}', c) == '    1'
    with pytest.raises(ValueError):
        f.format('{a: >5d}', c, a=1) == '    1'
    assert f.format('{a: >5d}{b: >5d}', c, b=2) == '    1    2'
    
def test_PositionalDefaultFormatter():
    f=PositionalDefaultFormatter(1,2,3)
    assert f.format('{: >5d}{: >5d}') == '    1    2'
    with pytest.raises(KeyError):
        f.format('{: >5d}{b: >5d}') == '    1    2'
        
def test_KeywordFormatter():
    f=KeywordFormatter('{a: >5d}{b: >5d}', dict(a=1,b=2,c=3))
    assert f.format() == '    1    2'
    
def test_VersatileFormatter():
    f=VersatileFormatter('{: >5d}{: >5d}', 1,2,3)
    assert f.format() == '    1    2'
    f=VersatileFormatter('{: >5d}{: >5d}{: >5d}', 1,2,3)
    assert f.format() == '    1    2    3'
    f=VersatileFormatter('{: >5d}{: >5d}{a: >5d}{: >5d}', 1,2,3, default_namespace=dict(a=4))
    assert f.format() == '    1    2    4    3'
    f=VersatileFormatter('{: >5d}{: >5d}{a: >5d}{: >5d}')
    with pytest.raises((IndexError, KeyError)) as exc:
        f.format()
    with pytest.raises(ValueError):
        f.format('{: >5s}')
