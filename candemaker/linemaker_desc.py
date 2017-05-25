import enum
from collections.abc import Mapping
from functools import partial

class LineMakerDesc():
    '''Metaclass to produce formattable LineMaker child classes.
    Child classes can set a __prefix__ value to be printed at the beginning of the line.
    Child classes can set a __sep__ value to be printed between each member item.'''
    _conversion_dict = {'': str}
    _conversion_dict.update(dict(s = str, f = float, e = float, g = float, n = float, d = int, b = partial(int, base=2), c = ord, o = partial(int, base=8), x = partial(int, base=16), X = partial(int, base=16)))
    def __init__(cls, name, bases, mapping):
        cls.prefix = mapping.pop('__prefix__', '')
        cls.sep = mapping.pop('__sep__', None)
        super().__init__(name, bases, mapping)
    def _iter_format(cls):
        '''Iteratively generate formatters for the class members.'''
        for member in cls:
            yield member.formatter
    def __str__(cls):
        return cls.format()
        # return ''.join('{{0.{m.name}:{f}}}'.format(m=member, f=fmat) for member,fmat in zip(cls, cls._iter_format()))
    @property
    def prefix(cls):
        '''The prefix that will be printed at the beginning of every line.'''
        return cls._prefix
    @prefix.setter
    def prefix(cls, value):
        cls._prefix = '{!s}'.format(value)
    @property
    def sep(cls):
        '''Separator between member strings. 
        If not provided, member.start refers to the substring index in the parent string.
        If provided, member.start refers to the substring index in string.split(sep).'''
        return cls._sep
    @sep.setter
    def sep(cls, value):
        if value is None:
            value = [None]
        try:
            # check if string
            value.split()
        except AttributeError:
            # assume sequence
            sep, *other_seps = *value,
        else:
            # assume string
            sep = value
            other_seps = []
        cls._sep = '{!s}'.format(sep) if sep is not None else None
        cls._other_seps = ['{!s}'.format(other_sep) for other_sep in other_seps]
    @property
    def other_seps(cls):
        yield from cls._other_seps
    def format(cls, obj=None, **kwargs):
        '''Create formatted version of the line populated by the obj attributes and/or kwargs members.'''
        # check that user didn't forget to unpack a dict
        if isinstance(obj, Mapping):
            raise TypeError('Mapping object needs to be passed as keyword args, e.g. instance.format(**mapping)')

        # check for name conflicts
        try:
            kwarg = next(kwarg for kwarg in kwargs if hasattr(obj, kwarg))
        except StopIteration:
            pass
        else:
            raise ValueError("Key and attribute name conflict for '{}'. Cannot provide a keyword argument that has the same name as an attribute of obj.".format(kwarg))
            
        # build resulting string by iterating through members
        result = ''
        for member in cls:
            name = member.name
            # determine value to be inserted into member
            try:
                try:
                    value = kwargs[member]
                except KeyError:
                    try:
                        value = getattr(obj, name)
                    except AttributeError:
                        value = kwargs[name]
            except KeyError:
                value = member.default
            value_str = member(value)
            result = result + value_str
        if cls.sep is not None:
            result = result[:-len(cls.sep)]
        return cls.prefix + result
    def iparse(cls, s, *, prefix=True):
        '''Iteratively read a string the conforms to the LineMaker class definition.
        Returns a (member,value) tuple'''
        if prefix:
            s = s[len(cls.prefix):]
        if cls.sep is None:
            slices = (slice(member.start, (member.start + member.length) if member.length != 0 else None) for member in cls )
        else:
            for other_sep in cls.other_seps:
                s = s.replace(other_sep, cls.sep)
            s = s.split(cls.sep)
            slices = (member.start for member in cls if member.start<len(s))
        parts = (s[slc].strip() for slc in slices)
        for part,member in zip(parts, cls):
            conversion = cls._conversion_dict[member.spec.get('type', '')]
            if part == '':
                continue
            value = conversion(part)
            yield member, value
    def parse(cls,s, *, prefix=True):
        '''Read a string the conforms to the LineMaker class definition.
        Returns a dictionary of parsed values with the members as keys.'''
        return dict(list(cls.iparse(s, prefix = prefix)))
        
class LineMakerBase(metaclass=LineMakerMeta):
    '''A base class for creating Enum subclasses used for populating lines of a file.
    Child classes can set a __prefix__ value to be printed at the beginning of the line.
    Child classes can set a __sep__ value to be printed between each member item.
    
    Usage:
    
    class LineMaker(LineMakerBase):
        __prefix__ = 'my prefix'
        __sep__ = ', '
        a = 1,      dict(width='5', align='>', fill=' ', type='s'), 'foo'
        #   ^-start ^---spec dictionary                             ^--default
    '''
    def __init__(member, start, spec={}, default=None):
        member.start = start
        member.spec = spec
        if default is not None:
            member.default = default
        else:
            # assume value is numerical for all provided types other than 's' (string)
            default_or_set_type = member.spec.get('type','s')
            default = {'s': ''}.get(default_or_set_type, 0)
            member.default = default
    @property
    def formatter(member):
        '''Produces a formatter based on the member.spec dictionary.
        The member.spec dictionary will make use of these 
        keys (see the string.format docs):
            fill align sign width grouping_option precision type'''
        try:
            # get cached value
            return '{{0:{}}}'.format(member._formatter)
        except AttributeError:
            if type(member).sep is None:
                # add width to format spec if not there
                member.spec.setdefault('width', member.length if member.length != 0 else '')
            
            # build formatter using the available parts in the member.spec dictionary
            # any missing parts will simply not be present in the formatter
            formatter = ''
            for part in 'fill align sign width grouping_option precision type'.split():
                try:
                    spec_value = member.spec[part]
                except KeyError:
                    # missing part
                    pass
                else:
                    # add part
                    sub_formatter = '{!s}'.format(spec_value)
                    formatter = formatter + sub_formatter
            member._formatter = formatter
            return '{{0:{}}}'.format(formatter)
    def __call__(member, value=None):
        '''Injects the value into the member's formatter and returns the formatted string.'''
        formatter = member.formatter
        if value is not None:
            value_str = formatter.format(value) + (type(member).sep if type(member).sep is not None else '')
        else:
            value_str = formatter.format(member.default) + (type(member).sep if type(member).sep is not None else '')
        # For testing convenience later:
        # print('\n#####', 'Name: ', member.name, '\t\t\tValue: ',value, '\t\t\tFormatter: ',formatter, '\t\t\tType: ', member.spec.get('type', '<<NO TYPE>>'), '\t\t\tValue: ', "'{0!s}'".format(value_str))
        if len(value_str) > len(member) and len(member) != 0:
            raise ValueError('Length of object string {} ({}) exceeds available field length for {} ({}).'.format(value_str, len(value_str), member.name, len(member)))
        return value_str
    @property
    def length(member):
        return len(member)
    def __len__(member):
        '''Returns the length of the member field. The last member has no length.
        Length can be based on simple subtraction of starting positions. 
        When a there is a separator, designate field length using member.spec['width']. '''
        try:
            return member._length
        except AttributeError:
            # calculate member length
            if type(member).sep is None:
                # compare by member value because member could be an alias
                members = list(type(member))
                try:
                    next_index = next(i+1 for i,m in enumerate(type(member)) if m.value == member.value)
                except StopIteration:
                    raise TypeError('The member value {} was not located in the {}.'.format(member.value, type(member).__name__))
                try:
                    next_member = members[next_index]
                except IndexError:
                    # last member defaults to no length
                    length = 0
                else:
                    length = next_member.start - member.start
            # get designated length, or set to default length (zero)
            else:
                length = member.spec.get('width', 0)
            member._length = length
            return length
