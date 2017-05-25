from candemaker.linemaker import LineMakerBase
import pytest
from collections import namedtuple as nt

@pytest.fixture
def ALineMakerClass(scope='function'):
    '''For testing the LineMakerBase object.'''
    class ALineMaker(LineMakerBase):
        a = 0, dict(align='>', fill=' ', type='d')
        b = 5, dict(align='>', fill=' ', type='f'), 0
        c = 15, dict(align='>', fill=' ', type='s'), ''
        d = 17
    return ALineMaker
    
@pytest.fixture
def ALineMakerClassWithSep(scope='function'):
    '''For testing the LineMakerBase object with a separator.'''
    class ALineMaker(LineMakerBase):
        __sep__ = (',', ', ')
        a = 0, dict(width = 5, align='>', fill=' ', type='d')
        b = 1, dict(width = 10, align='>', fill=' ', type='f'), 0
        c = 2, dict(width = 2, align='>', fill=' ', type='s'), ''
        d = 3
    return ALineMaker
    
@pytest.fixture(scope='function')
def ALineMakerMembers(ALineMakerClass, scope='function'):
    '''For testing the LineMakerBase object.'''
    return list(ALineMakerClass)
    
@pytest.fixture(scope='function')
def ABCD_namedtuple(scope='function'):
    '''Helper tuple for testing ALineMakerClass'''
    ABCD = nt('ABC', 'a b c d')
    return ABCD
    
def test_member_init(ALineMakerMembers):
    a,b,c,d = ALineMakerMembers
    assert (a.start, a.default) == (0,0)        
    assert (b.start, b.default) == (5,0)
    assert (c.start, c.default) == (15,'')
    assert (d.start, d.default) == (17, '')
    assert (d.spec) == {}
    
def test_member__call__(ALineMakerMembers):
    a,b,c,d = ALineMakerMembers
    assert a(1) == '    1'
    assert a() == '    0'
    with pytest.raises(ValueError):
        a('')
    assert b(3) == '  3.000000'
    assert b() == '  0.000000'
    assert c('c') == ' c'
    assert c() == '  '
    assert d(3) == '3'
    assert d() == ''

def test_member_length(ALineMakerMembers):
    a,b,c,d = ALineMakerMembers
    assert a.length == 5
    assert b.length == 10
    assert c.length == 2
    assert d.length == 0
    
def test_class_format_tuple(ALineMakerClass, ALineMakerMembers, ABCD_namedtuple):
    a,b,c,d = ALineMakerMembers
    abcd = ABCD_namedtuple(1,2,'x','foo')
    assert ALineMakerClass.format(abcd) == '    1  2.000000 xfoo'
    # this test MUST come after test above
    assert a.spec['width'] == 5
    assert b.spec['width'] == 10
    assert c.spec['width'] == 2
    assert d.spec['width'] == ''
    
def test_class_format_dict(ALineMakerClass, ALineMakerMembers):
    assert ALineMakerClass.format(**dict(a=1)) == '    1  0.000000  '
    assert ALineMakerClass.format(**dict(a=1, d='d')) == '    1  0.000000  d'
    # this test MUST come after test above
    a,b,c,d = ALineMakerMembers
    assert a.spec['width'] == 5
    assert b.spec['width'] == 10
    assert c.spec['width'] == 2
    assert d.spec['width'] == ''

def test_class_format_mixture(ALineMakerClass, ALineMakerMembers, ABCD_namedtuple):
    a,b,c,d = ALineMakerMembers
    a_nt = nt('A', 'a')(1)
    assert ALineMakerClass.format(a_nt, **dict(d='d')) == '    1  0.000000  d'
    
    # this test MUST come after test above
    assert a.spec['width'] == 5
    assert b.spec['width'] == 10
    assert c.spec['width'] == 2
    assert d.spec['width'] == ''

    assert ALineMakerClass.format(a_nt, **dict(b=3)) == '    1  3.000000  '
    assert ALineMakerClass.format(a_nt, **dict(c = 'xx', d='bar')) == '    1  0.000000xxbar'
    
def test_class_format_name_conflicts(ALineMakerClass, ALineMakerMembers, ABCD_namedtuple):
    abcd = ABCD_namedtuple(1,2,3,4)
    with pytest.raises(ValueError):
        ALineMakerClass.format(abcd, **dict(b=331))
        
def test_class_format_field_overflow(ALineMakerClass, ALineMakerMembers, ABCD_namedtuple):
    with pytest.raises(ValueError):
        ALineMakerClass.format(**dict(a=123456))

def test_LineMakerMeta_basic():
    class LineMaker(LineMakerBase):
        a = 0
    assert LineMaker.format(**dict(a=1)) == '1'
    
def test_LineMakerMeta_prefix():
    class LineMaker(LineMakerBase):
        __prefix__ = '          LALALA'
        a = 0
        b = 5, dict(fill=' ')
        c = 10
    assert LineMaker.format(**dict(a=1, b=1)) == '          LALALA1    1'
    
def test_LineMakerMeta_prefix_setter():
    class LineMaker(LineMakerBase):
        __prefix__ = '          LALALA'
        a = 0, dict(fill=' ')
        b = 5
        c = 10
    LineMaker.prefix = ''
    assert LineMaker.format(**dict(a=1, b=1)) == '    11'
    
@pytest.mark.parametrize('string, values',[
                    ('    3    -3.012 x', (3, float(-3.012), 'x')),
                    ('    3    -3.012 xlala', (3, float(-3.012), 'x', 'lala')),
                    ])
def test_LineMakerClass_parse(ALineMakerClass, string, values):
    result = dict(zip(ALineMakerClass, values))#{a:3, b:float(-3.012), c:x}
    test = ALineMakerClass.parse(string)
    assert test == result

@pytest.mark.parametrize('string, values',[
                    ('    3,    -3.012, x', (3, float(-3.012), 'x')),
                    ('    3,    -3.012, x,lala', (3, float(-3.012), 'x', 'lala')),
                    ])
def test_LineMakerClass_parse_with_sep(ALineMakerClassWithSep, string, values):
    result = dict(zip(ALineMakerClassWithSep, values))#{a:3, b:float(-3.012), c:x}
    test = ALineMakerClassWithSep.parse(string)
    assert test == result
