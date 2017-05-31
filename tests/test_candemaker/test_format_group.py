from candemaker.format_group import FormatGroup as LineMaker
import pytest
from collections import namedtuple as nt

def test_LineMaker():
    assert LineMaker('EmptyLineDef')
    
def test_basic_LineMaker():
    assert LineMaker('BasicLineDef', a='{: >5s}')
    
@pytest.fixture
def ALineDefClass():
    '''For testing the LineMaker object.'''
    ALineDef = LineMaker('ALineDef', a = '{: >5d}', b = ('{: >10f}', 0), c = ('{: >2s}', ''), d = '{}')
    return ALineDef
    
@pytest.fixture
def ALineDefClassWithSep():
    '''For testing the LineMaker object with separators.'''
    ALineDefWithSep = LineMaker('ALineDefWithSep', a = '{: >5d}', b = ('{: >10f}', 0), c = ('{: >2s}', ''), d = '{}', sep = ',')
    return ALineDefWithSep
    
@pytest.fixture()
def ALineDefMembers(ALineDefClass, scope='function'):
    '''For testing the LineMaker object.'''
    return list(ALineDefClass)
    
@pytest.fixture()
def ABCD_namedtuple(scope='function'):
    '''Helper tuple for testing ALineDefClass'''
    ABCD = nt('ABC', 'a b c d')
    return ABCD
    
def test_init(ALineDefClass):
    a,b,c,d=ALineDefClass
    assert a._format_str == '{: >5d}'
    assert b._format_str == '{: >10f}'
    assert c._format_str == '{: >2s}'
    assert d._format_str == '{}'
    assert ALineDefClass._prefix == ''
    assert ALineDefClass._sep == ''
    
def test_member_format(ALineDefMembers):
    a,b,c,d = ALineDefMembers
    assert a.format(1) == '    1'
    with pytest.raises(IndexError):
        a.format()
    with pytest.raises(ValueError):
        a.format('')
    assert b.format(3) == '  3.000000'
    assert b.format() == '  0.000000'
    assert c.format('c') == ' c'
    assert c.format() == '  '
    assert d.format(3) == '3'
    with pytest.raises(IndexError):
        d.format()
        
def test_class_format_tuple(ALineDefClass, ALineDefMembers, ABCD_namedtuple):
    a,b,c,d = ALineDefMembers
    abcd = ABCD_namedtuple(1,2,'x','foo')
    assert ALineDefClass.format(abcd) == '    1  2.000000 xfoo'
    
def test_class_format_dict(ALineDefClass, ALineDefMembers):
    assert ALineDefClass.format(dict(a=1, d='d')) == '    1  0.000000  d'
    with pytest.raises(IndexError):
        ALineDefClass.format(dict(a=1))

def test_class_format_mixture(ALineDefClass, ALineDefMembers, ABCD_namedtuple):
    a,b,c,d = ALineDefMembers
    a_nt = nt('A', 'a')(1)
    assert ALineDefClass.format(a_nt, dict(d='d')) == '    1  0.000000  d'
    with pytest.raises(IndexError):
        ALineDefClass.format(a_nt, dict(b=3))
    assert ALineDefClass.format(a_nt, dict(c = 'xx', d='bar')) == '    1  0.000000xxbar'
    
def test_class_format_name_conflicts(ALineDefClass, ALineDefMembers, ABCD_namedtuple):
    abcd = ABCD_namedtuple(1,2,3,4)
    with pytest.raises(ValueError):
        ALineDefClass.format(abcd, dict(b=331))
    with pytest.raises(ValueError):
        ALineDefClass.format(abcd, **dict(b=331))
        
@pytest.mark.skip(reason="haven't decided whether/how to disallow overflow of width for fields")
def test_class_format_field_overflow(ALineDefClass, ALineDefMembers, ABCD_namedtuple):
    with pytest.raises(ValueError):
        ALineDefClass.format(dict(a=123456, d='d'))

def test_LineMakerFactory_basic():
    LineDef = LineMaker('LineDef', a = '{}')
    assert LineDef.format(dict(a=1)) == '1'
    assert LineDef.format(dict(a='string')) == 'string'
    
def test_LineMakerFactory_prefix():
    LineDef = LineMaker('LineDef', a = '{}', b = '{: >5d}', c = '{}', prefix = '          LALALA')
    assert LineDef.format(dict(a=1, b=1, c='')) == '          LALALA1    1'
    
def test_LineMakerMeta_prefix_set():
    LineDef = LineMaker('LineDef', a = '{}', b = '{: >5d}', c = ('{}',''), prefix = '          LALALA')
    LineDef._prefix = ''
    assert LineDef.format(dict(a=1, b=1)) == '1    1'
    
@pytest.mark.skip(reason="haven't decided whether/how to implement this")
@pytest.mark.parametrize('string, values',[
                    ('    3    -3.012 x', (3, float(-3.012), 'x')),
                    ('    3    -3.012 xlala', (3, float(-3.012), 'x', 'lala')),
                    ])
def test_LineDefClass_parse(ALineDefClass, string, values):
    result = dict(zip(ALineDefClass, values))#{a:A, b:B, c:C}
    test = ALineDefClass.parse(string)
    assert test == result

@pytest.mark.skip(reason="haven't decided whether/how to implement this")
@pytest.mark.parametrize('string, values',[
                    ('    3,    -3.012, x', (3, float(-3.012), 'x')),
                    ('    3,    -3.012, x,lala', (3, float(-3.012), 'x', 'lala')),
                    ])
def test_LineDefClass_parse_with_sep(ALineDefClassWithSep, string, values):
    result = dict(zip(ALineDefClassWithSep, values))#{a:A, b:B, c:C}
    test = ALineDefClassWithSep.parse(string)
    assert test == result