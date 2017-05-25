from string import Formatter

class DefaultFormatter(Formatter):
    '''A formatter with a default namespace.
    Should probably be the first parent class when 
    used in multiple inheritance.'''
    def __init__(self, default_namespace):
        self.default_namespace = default_namespace
    def get_value(self, key, args, kwargs):
        try:
            return super().get_value(key, args, kwargs)
        except KeyError:
            return self.default_namespace[key]
            
class AttrFormatter(Formatter):
    '''A Formatter that looks in args object attributes for values.
    The args are inspected in order. First one wins. 
    Callable attributes are ignored.'''
    def get_value(self, key, args, kwargs):
        # sentinel marks lookup failure
        sentinel = object()
        # get the normal value
        try:
            value_norm = super().get_value(key, args, kwargs)
        # no value; error stored to be raised later if no attribute value
        except KeyError as keyerror_exc:
            value_norm = sentinel
        # return result if the key can't be an attribute
        else:
            # docs say key is either str or int
            if isinstance(int, key):
                return value_norm
        # assume no attribute values
        value_attr = sentinel
        # look for attribute values
        for arg in args:
            # try to get the attribute value
            value_attr = getattr(arg, key, sentinel)
            # check if found one (no callables!)
            if not callable(value_attr) and value_attr is not sentinel:
                break
            else:
                # discard any methods
                value_attr = sentinel
                continue
        # if no value; raise error as usual
        if value_norm is value_attr is sentinel:
            raise keyerror_exc
        # if two values, there is an unresolvable name conflict
        if value_norm is not sentinel and value_attr is not sentinel:
            raise ValueError('The name {} is both an attribute of first argument {} object and a key in the keyword arguments. Cannot resolve.'.format(key, type(args[0]).__name__))
        return  {value_norm:value_attr,value_attr:value_norm}[sentinel]
        
class VersatileFormatter(DefaultFormatter,AttrFormatter):
    '''A formatter with a default namespace that looks in args object 
    attributes for values. The args are inspected in order. First one wins. 
    Callable attributes are ignored.'''
    pass
    
class SpecialAttrsMeta(type):
    '''A metaclass that removes special attribute names from the namespace
    prior to passing them for initialization.'''
    def __new__(mcls, name, bases, mapping):
        cls = super().__new__(mcls,name,bases,mapping)
        sentinel = object()
        reserved_mapping = {n:mapping.pop(n, sentinel) for n in mcls._special}
        for k,v in (k,v for k,v in reserved_mapping.items() if v is not sentinel):
            setattr(cls, k, v)
        return cls
        
class UniformFormatGroupMeta(SpecialAttrsMeta):
    '''A metaclass that produces classes defining lines composed of uniform formatting members 
    with optional line prefixes and separators between members.'''
    _special = '_prefix _sep _formattings _formatter_type'.split()
    def __init__(cls, name, bases, mapping):
        formatter_type = cls._formatter_type
        cls._formattings = {k:((v,formatter_type()) if isinstance(v,str) else (v[0],formatter_type(*v[1:]))) for k,v in mapping.items()}
    def format(cls, *args, **kwargs):
        for format_str,formatter in cls._formattings.values():
            return cls._sep.join(formatter.format(format_str, *args, **kwargs))

def special_attrs_check(obj, **kwargs):
    '''Check to make sure there are no conflicts with obj special attributes.'''
    special = obj._special
    # check for reserved names
    for n in special:
        try:
            raise ValueError('The attribute name "{}" is reserved.'.format(kwargs[n]))
        except KeyError:
            continue
            
def set_item_if(obj, name, value, test):
    '''Sets an item of obj to a value if test passes.
    The test signature must be of the form:
        test(obj,name,value)'''
    # allow for individual arguments or iterables
    try:
        names = [name] if isinstance(name, str) else *name,
    except TypeError:
        names = [name]
    try:
        values = [value] if isinstance(value, str) else *value,
    except TypeError:
        values = [value]
    # check that same number of names and values provided
    if len(names)!=len(values):
        raise ValueError('Unequal number of names ({}) and values ({}) provided.'.format(len(names), len(values)))
    # set items based on test result
    for name,value in zip(names, values):
        if test(obj,name,value):
            obj[name] = value

def UniformFormatGroup(name, formatter_type=Formatter, *, prefix = None, sep = None, **kwargs):
    '''Factory for producing classes that define lines composed of uniform formatting members 
    with optional line prefixes and separators between members.'''
    # check the namespace for special item conflicts
    special_attrs_check(UniformFormatGroupMeta, **kwargs)
    # add special items to the namespace
    specials = '_prefix, _sep _formatter_type'.split()
    set_item_if(kwargs, specials, (prefix, sep, formatter_type), lambda o,n,v: v is not None)
    return UniformFormatGroupMeta(name, (), **kwargs)
            
class LineMaker():
    '''A factory class for creating classes used for populating lines of a file.
    Classes can set a prefix value to be printed at the beginning of the line.
    Child classes can set a sep value to be printed between each member item.
    
    Usage:
    
    LineDef = LineMaker(a = ' 5>s', default = 'foo', prefix = 'my prefix', sep = ', ')
    '''
    
    def __new__(cls, *, prefix = None, sep = None, **kwargs):
        return super().__new__(cls)
        
def test_UniformFormatGroup():
    assert UniformFormatGroup('', formatter_type=Formatter, *, prefix = None, sep = None, **kwargs)
    
# from candemaker.linemaker_factory import LineMaker
import pytest
from collections import namedtuple as nt

@pytest.fixture
def ALineDefClass(scope='function'):
    '''For testing the LineMaker object.'''
    ALineDef = LineMaker(a = ' >5d', b = ' >10f' 0, c = ' >2s' '', d = '')
    return ALineDef
    
@pytest.fixture
def ALineDefClassWithSep(scope='function'):
    '''For testing the LineMaker object with separators.'''
    ALineDef = LineMaker(a = ' >5d', b = ' >10f' 0, c = ' >2s' '', d = '', sep = (',', ', '))
    return ALineDef
    
@pytest.fixture(scope='function')
def ALineDefMembers(ALineDefClass, scope='function'):
    '''For testing the LineMaker object.'''
    return list(ALineDefClass)
    
@pytest.fixture(scope='function')
def ABCD_namedtuple(scope='function'):
    '''Helper tuple for testing ALineDefClass'''
    ABCD = nt('ABC', 'a b c d')
    return ABCD
    
def test_init(ALineDefClass):
    assert ALineDefClass.prefix == None
    assert ALineDefClass.sep == None
    
def test_member_format(ALineDefMembers):
    a,b,c,d = ALineDefMembers
    assert a.format(1) == '    1'
    assert a.format() == '    0'
    with pytest.raises(ValueError):
        a.format('')
    assert b.format(3) == '  3.000000'
    assert b.format() == '  0.000000'
    assert c.format('c') == ' c'
    assert c.format() == '  '
    assert d.format(3) == '3'
    assert d.format() == ''

def test_class_format_tuple(ALineDefClass, ALineDefMembers, ABCD_namedtuple):
    a,b,c,d = ALineDefMembers
    abcd = ABCD_namedtuple(1,2,'x','foo')
    assert ALineDefClass.format(abcd) == '    1  2.000000 xfoo'
    
def test_class_format_dict(ALineDefClass, ALineDefMembers):
    assert ALineDefClass.format(**dict(a=1)) == '    1  0.000000  '
    assert ALineDefClass.format(**dict(a=1, d='d')) == '    1  0.000000  d'

def test_class_format_mixture(ALineDefClass, ALineDefMembers, ABCD_namedtuple):
    a,b,c,d = ALineDefMembers
    a_nt = nt('A', 'a')(1)
    assert ALineDefClass.format(a_nt, **dict(d='d')) == '    1  0.000000  d'
    assert ALineDefClass.format(a_nt, **dict(b=3)) == '    1  3.000000  '
    assert ALineDefClass.format(a_nt, **dict(c = 'xx', d='bar')) == '    1  0.000000xxbar'
    
def test_class_format_name_conflicts(ALineDefClass, ALineDefMembers, ABCD_namedtuple):
    abcd = ABCD_namedtuple(1,2,3,4)
    with pytest.raises(ValueError):
        ALineDefClass.format(abcd, **dict(b=331))
        
def test_class_format_field_overflow(ALineDefClass, ALineDefMembers, ABCD_namedtuple):
    with pytest.raises(ValueError):
        ALineDefClass.format(**dict(a=123456))

def test_LineMakerFactory_basic():
    LineDef = LineMaker(a = '')
    assert LineDef.format(**dict(a=1)) == '1'
    assert LineDef.format(**dict(a='string')) == 'string'
    
def test_LineMakerFactory_prefix():
    class LineDef = LineMaker(a = '', b = ' >5d', c = '', prefix = '          LALALA')
    assert LineMaker.format(**dict(a=1, b=1)) == '          LALALA1    1'
    
def test_LineMakerMeta_prefix_setter():
    class LineDef = LineMaker(a = '', b = ' >5d', c = '', prefix = '          LALALA')
    LineDef.prefix = ''
    assert LineMaker.format(**dict(a=1, b=1)) == '1    1'
    
@pytest.mark.parametrize('string, values',[
                    ('    3    -3.012 x', (3, float(-3.012), 'x')),
                    ('    3    -3.012 xlala', (3, float(-3.012), 'x', 'lala')),
                    ])
def test_LineDefClass_parse(ALineDefClass, string, values):
    result = dict(zip(ALineDefClass, values))#{a:A, b:B, c:C}
    test = ALineDefClass.parse(string)
    assert test == result

@pytest.mark.parametrize('string, values',[
                    ('    3,    -3.012, x', (3, float(-3.012), 'x')),
                    ('    3,    -3.012, x,lala', (3, float(-3.012), 'x', 'lala')),
                    ])
def test_LineDefClass_parse_with_sep(ALineDefClassWithSep, string, values):
    result = dict(zip(ALineDefClassWithSep, values))#{a:A, b:B, c:C}
    test = ALineDefClassWithSep.parse(string)
    assert test == result
