from candemaker.formatters import VersatileFormatter
from collections import OrderedDict as od

import sys
assert (sys.version_info)>(3,6)

def set_item_if(obj, name, value, test):
    '''Sets an item of obj to a value if test passes.
    The test signature must be of the form:
        test(obj,name,value)'''
    # allow for individual arguments or iterables
    try:
        names = [name] if isinstance(name, str) else (*name,)
    except TypeError:
        names = [name]
    try:
        values = [value] if isinstance(value, str) else (*value,)
    except TypeError:
        values = [value]
    # check that same number of names and values provided
    if len(names)!=len(values):
        raise ValueError('Unequal number of names ({}) and values ({}) provided.'.format(len(names), len(values)))
    # set items based on test result
    for name,value in zip(names, values):
        if test(obj,name,value):
            obj[name] = value

class SpecialAttrsMeta(type):
    '''A base metaclass that removes special attribute names from the namespace
    prior to passing them for initialization.
    Special attributes are designated by the attribute "_special".
    Any _special attributes not defined at runtime are ignored.'''
    def __new__(mcls, name, bases, mapping):
        cls = super().__new__(mcls,name,bases,mapping)
        sentinel = object()
        reserved_mapping = {n:mapping.pop(n, sentinel) for n in mcls._special}
        for k,v in ((k,v) for k,v in reserved_mapping.items() if v is not sentinel):
            setattr(cls, k, v)
        return cls
    @classmethod
    def special_check(meta, **kwargs):
        '''Check to make sure there are no conflicts with special attribute names.'''
        try:
            special = meta._special
            # check for reserved names
            for n in special:
                try:
                    raise ValueError('The attribute name "{}" is reserved.'.format(kwargs[n]))
                except KeyError:
                    continue
        # no special names
        except AttributeError:
            pass
            
class FormatGroupMeta(SpecialAttrsMeta):
    '''A metaclass that produces classes defining lines composed of  
    formatting members with optional line prefixes and separators between members.
    
    Formatter type must provide a static args_parse() method with a signature of: 
    
        args, kwargs = FormatterType.args_parse(*args)
        f = FormatterType(*args, **kwargs)
    
    Usage:
    
        class LineDef(metaclass=FormatGroupMeta):
            _formatter_type = CustomStaticFormatter
            _prefix = 'my prefix'
            _sep = ', '
            a = '{: 5>s}', 'foo'
            b = '{: 10>f}', 0
            c = '{}'
    '''
    _special = '_prefix _sep _formatter_type _formatters'.split()
    def __init__(cls, name, bases, mapping):
        formatter_type = cls._formatter_type
        formatter_defs = {k:v for k,v in mapping.items() if not k.startswith('_') and not callable(v)}
        formatter_args = {}
        formatter_kwargs = {}
        # build the formatter args, kwargs using formatter_type.args_parse
        for k,args in formatter_defs.items():
            args = [args] if isinstance(args, str) else args
            formatter_args[k], formatter_kwargs[k] = formatter_type.args_parse(*args)
        formatters = (formatter_type(*formatter_args[k], **formatter_kwargs[k]) for k in formatter_defs)
        # pass each set of args and kwargs to the formatter type
        cls._formatters = {k:formatter for k,formatter in zip(formatter_defs,formatters)}
        cls.__init__(name,bases,mapping)
    def format(cls, *args, **kwargs):
        '''Return formatted string using joined prefix, formatters, and separator.'''
        for formatter in cls:
            return cls._prefix + cls._sep.join(formatter.format(*args, **kwargs))
    def __iter__(cls):
        yield from cls._formatters.values()
        
def FormatGroup(name, meta=FormatGroupMeta, formatter_type=VersatileFormatter, *, prefix = '', sep = '', **kwargs):
    '''Factory for producing classes that define lines composed of formatting members 
    with optional line prefixes and separators between members. Formatter type must 
    provide a static args_parse() method with a signature of: 
    
        args, kwargs = FormatterType.args_parse(*args)
        f = FormatterType(*args, **kwargs)

    The meta can be a subclass of SpecialAttrsMeta.
    
    Usage:
    
        LineDef = FormatGroup('LineDef', a = '{: 5>s}', prefix = 'my prefix', sep = ', ')
        DefaultLineDef = FormatGroup('DefaultLineDef', a = ('{: 5>s}','foo'), prefix = 'my prefix', sep = ', ')
    '''
    # check the namespace for special item conflicts
    meta.special_check(**kwargs)
    # add special items to the namespace
    factory_specials = '_prefix _sep _formatter_type'.split()
    set_item_if(kwargs, factory_specials, (prefix, sep, formatter_type), lambda o,n,v: v is not None)
    return meta(name, (), kwargs)