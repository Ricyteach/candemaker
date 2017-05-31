from candemaker.utilities import update_special, set_item_if, args_kwargs_from_args
from candemaker.parmatters import VersatileParmatter
from collections import OrderedDict as od

import sys
assert (sys.version_info)>(3,6)

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
    def format(cls, *args, _asdict=True, _popmappings=True, **unified_namespace):
        '''Return a combiend formatted string using joined formatter members.
        
        Mapping objects can represent individual member argslists/namespaces and the values 
        will be appended to the args of the member name matching the key.
        
        Additional keyword arguments are passed to all formatteras as a "universal namespace".
        
        _popmappings:
            If True any Mapping object at the end of the args list is a member namespace. It will
            be spun out as the args via the name of that member or method as a key.
        _asdict:
            If True any object in args list that includes an .asdict or ._asdict attribute will 
            be treated as a Mapping object via the name of that member or method as a key.'''
        # optionally remove any mappings from the args list
        if _popmappings:
            # the slice of args in which to look for mappings (end to beginning) 
            slc=slice(-1,None,-1)
            # spin out any Mapping (or optionally .asdict/._asdict) objects starting from the end of args
            args, kwargs_from_args = args_kwargs_from_args(args, slc=slc, asdict=_asdict, ignore_conflicts=True, terminate_on_failure=True)
        else:
            args, kwargs_from_args = args, {}
        # argslist to be passed to each formatter member on a per-member basis
        try:
            # use unpacking to disallow multiple argslists to same member name
            format_args = od(**kwargs_from_args, **od((k,a) for k,a in zip(cls._formatters, args)))
        except TypeError as exc:
            if 'multiple values for keyword argument' in str(exc):
                key_conflict = next(k for k,_ in zip(cls._formatters, args) if k in kwargs_from_args)
                raise TypeError('Multiple argument sets provided under member name: {}.'.format(key_conflict)) from None
            else:
                raise
        # convert any single namespace arguments to an args list
        format_args = od((k,(a if not isinstance(a,str) and hasattr(a, '__iter__') else [a])) for k,a in format_args.items())
        return cls._prefix + cls._sep.join(formatter.format(*format_args.get(member,[]), **unified_namespace) for member,formatter in cls._formatters.items())
    def __iter__(cls):
        yield from cls._formatters.values()
        
def FormatGroup(name, meta=FormatGroupMeta, formatter_type=VersatileParmatter, *, prefix = '', sep = '', **kwargs):
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