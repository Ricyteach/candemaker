from candemaker.utilities import args_kwargs_from_args
from string import Formatter
from abc import ABC

class ArgsParseMixin(ABC):
    '''A mixin for providing default arg parsing behavior.'''
    @staticmethod
    def args_parse(*args):
        return args, {}

class StaticFormatter(Formatter, ArgsParseMixin):
    '''A formatter with a designated format string.'''
    def __init__(self, format_str, *args, **kwargs):
        self._format_str = format_str
        super().__init__(*args, **kwargs)
    def format(self, *args, **kwargs):
        '''The format method has been overridden to change the signature.
        Formmatting logic should be handled using get_value, format_field, etc.'''
        return super().format(self._format_str, *args, **kwargs)

class DefaultFormatter(Formatter, ArgsParseMixin):
    '''A formatter with any default namespace.
    
    Use int for indexes of positional arguments, str
    for keys of a mapping.'''
    def __init__(self, default_namespace, *args, **kwargs):
        self.default_namespace = default_namespace
        super().__init__(*args, **kwargs)
    def get_value(self, key, args, kwargs):
        try:
            return super().get_value(key, args, kwargs)
        except (KeyError, IndexError) as normal_exc:
            try:
                return self.default_namespace[key]
            except KeyError:
                ExcType = type(normal_exc)
                lookup_type = {KeyError:'key', IndexError:'index'}[ExcType]
                raise ExcType('No default argument was provided for this formatter, {} = {}.'.format(lookup_type, repr(key))) from None
            
class AttrFormatter(Formatter, ArgsParseMixin):
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
        except (KeyError, IndexError) as exc:
            value_norm = sentinel
            normal_exc = exc
        # return result if the key can't be an attribute
        else:
            # docs say key is either str or int
            if isinstance(key, int):
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
            raise normal_exc
        # if two values, there is an unresolvable name conflict
        if value_norm is not sentinel and value_attr is not sentinel:
            raise ValueError('The name {} is both an attribute of first argument {} object and a key in the keyword arguments. Cannot resolve.'.format(key, type(args[0]).__name__))
        return  {value_norm:value_attr,value_attr:value_norm}[sentinel]
        
class PositionalDefaultFormatter(DefaultFormatter):
    '''A formatter with a default positional namespace.
    Should probably be the first parent class when 
    used in multiple inheritance.'''
    def __init__(self, *values, default_namespace={}, **kwargs):
        default_namespace.update({i:value for i,value in enumerate(values)})
        super().__init__(default_namespace, **kwargs)
    @staticmethod
    def args_parse(*args):
        '''Form an alternate argument order to create a formatter.
        
        args = '{}', 0,  {a=2, b=3}
        args, kwargs = PositionalDefaultFormatter.arg_parse(*args)
        f = PositionalDefaultFormatter(*args, **kwargs)
        '''
        namespace_slice = slice(-1,None,-1)
        args, kwargs = args_kwargs_from_args(args, slc=namespace_slice, asdict=True, ignore_conflicts=True, terminate_on_failure=True)
        kwargs = dict(default_namespace = kwargs)
        return args, kwargs
        
class KeywordFormatter(StaticFormatter,DefaultFormatter,AttrFormatter):
    '''A static formatter with a default keyword namespace that looks in args object 
    attributes for values. The args are inspected in order. First one wins. 
    Callable attributes are ignored.'''
    def __init__(self, format_str, default_namespace, *args, **kwargs):
        super().__init__(format_str, default_namespace, *args, **kwargs)
    
class VersatileFormatter(StaticFormatter,PositionalDefaultFormatter,AttrFormatter):
    '''A static formatter with a default positional namespace that looks in args object 
    attributes for values. The args are inspected in order. First one wins. 
    Callable attributes are ignored.'''
    def __init__(self, format_str, *values, default_namespace={}, **kwargs):
        super().__init__(format_str, *values, default_namespace=default_namespace, **kwargs)