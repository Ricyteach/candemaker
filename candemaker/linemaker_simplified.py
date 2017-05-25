    import enum

    class LineMakerMeta(enum.EnumMeta):
        '''Metaclass to produce formattable LineMaker child classes.'''
        def _iter_format(cls):
            '''Iteratively generate formatters for the class members.'''
            for member in cls:
                yield member.formatter
        def __str__(cls):
            return cls.format()
        def format(cls, **kwargs):
            '''Create formatted version of the line populated by the kwargs members.'''
            # build resulting string by iterating through members
            result = ''
            for member in cls:
                # determine value to be injected into member
                try:
                    try:
                        value = kwargs[member]
                    except KeyError:
                        value = kwargs[member.name]
                except KeyError:
                    value = member.default
                value_str = member.populate(value)
                result = result + value_str
            return result
            
    class LineMakerBase(enum.Enum, metaclass=LineMakerMeta):
        '''A base class for creating Enum subclasses used for populating lines of a file.
        
        Usage:
        
        class LineMaker(LineMakerBase):
            a = 0,      dict(align='>', fill=' ', type='f'), 3.14
            b = 10,     dict(align='>', fill=' ', type='d'), 1
            b = 15,     dict(align='>', fill=' ', type='s'), 'foo'
            #   ^-start ^---spec dictionary                  ^--default
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
            '''Produces a formatter in form of '{0:<format>}' based on the member.spec dictionary.
            The member.spec dictionary makes use of these keys ONLY (see the string.format docs):
                fill align sign width grouping_option precision type'''
            try:
                # get cached value
                return '{{0:{}}}'.format(member._formatter)
            except AttributeError:
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
                        continue
                    else:
                        # add part
                        sub_formatter = '{!s}'.format(spec_value)
                        formatter = formatter + sub_formatter
                member._formatter = formatter
                return '{{0:{}}}'.format(formatter)
        def populate(member, value=None):
            '''Injects the value into the member's formatter and returns the formatted string.'''
            formatter = member.formatter
            if value is not None:
                value_str = formatter.format(value)
            else:
                value_str = formatter.format(member.default)
            if len(value_str) > len(member) and len(member) != 0:
                raise ValueError('Length of object string {} ({}) exceeds available field length for {} ({}).'.format(value_str, len(value_str), member.name, len(member)))
            return value_str
        @property
        def length(member):
            return len(member)
        def __len__(member):
            '''Returns the length of the member field. The last member has no length.
            Length are based on simple subtraction of starting positions.'''
            try:
                # get cached value
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
