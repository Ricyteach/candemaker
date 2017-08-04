import logging
from mytools.utilities import copymembers, getfields
from collections.abc import Sequence, Mapping
from collections import namedtuple as nt
from .cid.unformatter import unformatter_reg
from .cid.gen import cidgen_reg
from .cid.enum import CidEnum
from .cid.build import cidbuild_reg, DispatchController
from .obj import obj_reg, cidname_reg, Master, Info, Control
from . import reg

logging = logging.getLogger(__name__)


def flatten(obj):
    '''Yield name, value pairs for items in a hierarchical structure'''
    try:
        if isinstance(obj, Sequence):
            result = ((f, getattr(seq, f)) for seq in obj for f in seq._fields)
        elif isinstance(obj, Mapping):
            result = ((k, v) for d in obj for k,v in d.items())
        else:
            raise TypeError('Flattening of {!r} is not supported. '
                            ''.format(type(obj).__name__))
    except AttributeError as err:
        raise TypeError('The obj must be a Sequence of namedtuples '
                        'or a Mapping of Mappings.') from err
    yield from result


CandeNTBase = nt('CandeNTBase', '{} groups nodes elements boundaries materials factors'
                                ''.format(' '.join(f.lower()
                                                    for NT in (Master, Info, Control)
                                                    for f in NT._fields
                                                    )
                                            )
                )
CandeNTBase.__new__.__defaults__ = (None,) * (len(CandeNTBase._fields))

class CandeNT(CandeNTBase):
    '''Fully defined Cande Level 3 cid object'''
    __slots__ = ()
    def __new__(cls, *args, **kwargs):
        defaults = dict((f.lower(), v) for f,v in flatten((Master(), Info(), Control())))
        for field in 'groups nodes elements boundaries materials factors'.split():
            defaults[field] = []
        from_args = super().__new__(cls, *args, **kwargs)
        for field, value in from_args._asdict().items():
            if value is not None:
                del defaults[field]
        from_args = from_args._replace(**defaults)
        return from_args

class ObjListDesc():
    '''A class attribute that initializes as an empty list.'''
    def __init__(self, private_var):
        self.private_var = private_var
    def __get__(self, obj, owner=None):
        if obj is not None:
            try:
                x = getattr(obj, self.private_var)
            except:
                x = []
                setattr(obj, self.private_var, x)
            return x
        else:
            return self
    def __set__(self, obj, value):
        setattr(obj, self.private_var, value)


class GeneratorManager():
    '''A context manager that produces a generator.
    
    Example usage:
    
        with GeneratorManager(some_gen, arg) as g:
            yield from g
    '''
    def __init__(self, start, *args, **kwargs):
        self._generator = start(*args, **kwargs)
    def __enter__(self):
        return self._generator
    def __exit__(self, owner, value, tb):
        self._generator.close()
        del self._generator


class CandeObj():
    '''For working with Cande Level 3 problems'''
    _fields = tuple(f.lower() for f in Master._fields + Info._fields + Control._fields)
    _lists = 'groups nodes elements boundaries materials factors'.split()
    cid_builder = DispatchController(cidbuild_reg)
    groups = ObjListDesc('_groups')
    nodes = ObjListDesc('_nodes')
    elements = ObjListDesc('_elements')
    boundaries = ObjListDesc('_boundaries')
    materials = ObjListDesc('_materials')
    factors = ObjListDesc('_factors')
    def __init__(self, cande_obj=None, **kwargs):
        if cande_obj is None:
            cande_obj = CandeObj(CandeNT())
        try:
            from_kwargs = CandeNT(**kwargs)
        except TypeError as e:
            raise TypeError('Invalid kwargs to create CandeObj') from e
        copymembers(cande_obj, self, CandeNT._fields, suppress_err=False)
        copymembers(from_kwargs, self, kwargs, suppress_err=False)
        self._init_reg()
    def _init_reg(self):
        self.candeattr_reg = reg.CidRegistry(A1=self, A2=self.groups, C1=self, C2=self,
                                             C3=self.nodes, C4=self.elements,
                                             C5=self.boundaries, D1=self.materials,
                                             E1=self.factors)
    @classmethod
    def empty(cls):
        obj = cls.__new__(cls)
        obj._init_reg()
        return obj
    @classmethod
    def from_cid(cls, lines, start='A1'):
        '''Construct an instance using a file-like sequence'''
        try:
            lines + ''
        except TypeError:
            pass
        else:
            raise TypeError('A string was supplied; a file '
                            'line sequence is required.')
        obj = cls.empty()
        try:
            startmember = CidEnum[start].name
        except KeyError:
            raise ValueError('Invalid starting member name: '
                             '{!r}'.format(start)) from None
        with obj.cid_builder as builder, 
             obj.logic_gen(startmember) as logic_gen:
            logging.debug('***CANDE_OBJ BUILD BEGUN***')
            for line, label in zip(lines, logic_gen):
                logging.debug('***BEGINNING OF SECTION {} HANDLING***'
                              ''.format(label))
                cid_obj = obj.unformat(line, label)
                builder.send(label, cid_obj)
                logging.debug('***ENDING OF SECTION {} HANDLING***'
                              ''.format(label))
            logging.debug('***CANDE_OBJ BUILD COMPLETE***')
        return obj
    def logic_gen(self, cidmember='A1'):
        '''Get a logic generator object corresponding to the member'''
        start = cidgen_reg[cidmember]
        gen = GeneratorManager(start, self)
        return gen
    @staticmethod
    def unformatter(cidmember):
        '''The corresponding unformatter for the member'''
        return unformatter_reg[cidmember]
    @classmethod
    def unformat(cls, cidline, cidmember):
        '''Parse a CID file line into a cid object'''
        unformatter = cls.unformatter(cidmember)
        ObjType = obj_reg[cidmember]
        logging.debug('Unformatting {} to a {}'
                      ''.format(cidmember, ObjType.__name__))
        return ObjType(*unformatter.unformat(cidline))
    def pull(self, obj, name=None):
        '''Bring some object into the object model.'''
        try:
            name = obj.__name__ if name is None else name
        except AttributeError:
            pass
        if name in 'A1 C1 C2'.split():
            pass
        elif name in '':
            pass
        else:
            raise ValueError('Encountered invalid cid line name: {!r}'
                             ''.format(name))
    def __repr__(self):
        repgen = ('{}={!r}'.format(f, getattr(self, f, None))
                    for f in self._fields)
        return 'CandeObj({})'.format(', '.join(repgen))

    '''
    def __getattr__(self, attr):
        if attr in 'Master Control Info'.split():
            pass
        else:
            for member in (self.Master, self.Control, self.Info):
                try:
                    return getattr(member, attr)
                except AttributeError:
                    pass
    def __setattr__(self, attr, val):
        for cidnt_name in 'Master Control Info'.split():
            try:
                cidnt = getattr(self, cidnt_name)
                if attr in cidnt._fields:
                    setattr(self, cidnt_name, cidnt._replace(**{attr : val}))
                    break
            except AttributeError:
                continue
        else:
            super().__setattr__(attr, val)
    '''
