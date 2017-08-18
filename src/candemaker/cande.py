import logging
from mytools.utilities import copymembers, not_str
from enum import Enum, auto
from collections.abc import Sequence, Mapping
from collections import namedtuple as nt
from .cid.validdict import CidRegistry
from .cid.registry import CidUnformatterReg, CidNtReg
from .candehandler import CandeHandler
from .ntconvert import NTtoLowerCaseObjFactory

logging = logging.getLogger(__name__)


def flatten(obj):
    '''Yield name, value pairs for items in a hierarchical structure.'''
    try:
        if isinstance(obj, Sequence):
            result = ((f, getattr(seq, f)) for seq in obj
                                           for f in seq._fields)
        elif isinstance(obj, Mapping):
            result = ((k, v) for d in obj for k,v in d.items())
        else:
            raise TypeError('Flattening of {!r} is not supported. '
                            ''.format(type(obj).__name__))
    except AttributeError as err:
        raise TypeError('The obj must be a Sequence of namedtuples '
                        'or a Mapping of Mappings.') from err
    yield from result


CandeNTBase = nt('CandeNTBase', '{} groups nodes elements boundaries'
                                'materials factors'.format(
                                                    ' '.join(f.lower()
                                                    for mem in (CidNtReg['Master'],
                                                               CidNtReg['Info'],
                                                               CidNtReg['Control'],
                                                               )
                                                    for f in mem._fields
                                                    )
                                                    )
                )
CandeNTBase.__new__.__defaults__ = (None,) * (len(CandeNTBase._fields))

class CandeNT(CandeNTBase):
    '''Fully defined Cande Level 3 cid object'''
    __slots__ = ()
    def __new__(cls, *args, **kwargs):
        defaults = dict((f.lower(), v) for f,v in flatten((CidNtReg['Master'](),
                                                           CidNtReg['Info'](),
                                                           CidNtReg['Control'](),
                                                           ))
                       )
        for field in ('groups nodes elements boundaries '
                      'materials factors').split():
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
    # catalog of members that are atomic
    _fields = tuple(f.lower() for f in CidNtReg['Master']._fields +
                                       CidNtReg['Info']._fields +
                                       CidNtReg['Control']._fields)
    # catalog of members that are collections
    _lists = ('groups nodes elements boundaries '
             'materials factors').split()
    # for initializing empty collection members
    groups = ObjListDesc('_groups')
    A2 = groups
    nodes = ObjListDesc('_nodes')
    C3 = nodes
    elements = ObjListDesc('_elements')
    C4 = elements
    boundaries = ObjListDesc('_boundaries')
    C5 = boundaries
    materials = ObjListDesc('_materials')
    D1Soil = materials
    D1Interf = materials
    factors = ObjListDesc('_factors')
    E1 = factors
    def __init__(self, cande_obj=None, **kwargs):
        if cande_obj is None:
            cande_obj = CandeObj(CandeNT())
        try:
            from_kwargs = CandeNT(**kwargs)
        except TypeError as e:
            raise TypeError('Invalid kwargs to create CandeObj') from e
        copymembers(cande_obj, self, CandeNT._fields, suppress_err=False)
        copymembers(from_kwargs, self, kwargs, suppress_err=False)
    @classmethod
    def empty(cls):
        obj = cls.__new__(cls)
        return obj
    @classmethod
    def from_cid(cls, lines, start='A1'):
        '''Construct an instance using a file-like sequence'''
        not_str(lines)
        obj = cls.empty()
        with obj.builder(start) as build_process:
            logging.debug('***CANDE_OBJ BUILD BEGUN***')
            import pdb;pdb.set_trace()
            next_tag = build_process.send(None)
            for line in lines:
                tag, next_tag = next_tag, None
                logging.debug('***BEGINNING OF SECTION {} HANDLING***'
                              ''.format(tag))
                cid_obj = obj.unformat(line, tag)
                next_tag = build_process.send(cid_obj)
                logging.debug('***ENDING OF SECTION {} HANDLING***'
                              ''.format(tag))
            logging.debug('***CANDE_OBJ BUILD COMPLETE***')
        return obj
    def builder(self, cidmember='A1'):
        try:
            if self._builder.start != cidmember:
                raise AttributeError()
        except AttributeError:
            self._builder = CandeHandler(self)(cidmember)
        return self._builder
    @staticmethod
    def unformatter(cidmember):
        '''The corresponding unformatter for the member'''
        return CidUnformatterReg[cidmember]
    @classmethod
    def unformat(cls, cidline, cidmember):
        '''Parse a CID file line into a cid object'''
        unformatter = cls.unformatter(cidmember)
        ObjType = CandeObjReg[cidmember]
        logging.debug('Unformatting {} to a {}'
                      ''.format(cidmember, ObjType.__name__))
        return ObjType(*unformatter.unformat(cidline))
    def __repr__(self):
        repgen = ('{}={!r}'.format(f, getattr(self, f, None))
                    for f in self._fields)
        return 'CandeObj({})'.format(', '.join(repgen))

CandeObjReg = CidRegistry(
    {k:NTtoLowerCaseObjFactory(k) for k in (
    # any
    'A1',
    'E1',
    # L3 Only
    'A2',
    'C1',
    'C2',
    'C3',
    # 'C3L',
    'C4',
    # 'C4L',
    'C5',
    # 'C5L',
    # soil
    'D1',
    # 'D1L',
    # 'D1Soil',
    # 'D1SoilL',
    # 'D1Interf',
    # 'D1InterfL',
    # 'D2Orthotropic',
    # 'D2Over',
    # 'D2Hardin',
    # 'D2HardinTRIA',
    # 'D2Composite',
    # 'D2MohrCoulomb',
    # 'D2Isotropic',
    # 'D2Duncan',
    # 'D3Duncan',
    # 'D4Duncan',
    # 'D2Interface',
    # 'alum
    # 'B1Alum',
    # 'B2AlumA',
    # 'B2AlumDWSD',
    # 'B2AlumDLRFD',
    # 'B3AlumADLRFD',
    # 'plastic
    # 'B1Plastic',
    # 'B2Plastic',
    # 'B3PlasticAGeneral',
    # 'B3PlasticASmooth',
    # 'B3PlasticDWSD',
    # 'B3PlasticDLRFD',
    # 'B3PlasticAProfile',
    # 'B3bPlasticAProfile',
    # 'B4Plastic',
    # 'steel
    # 'B1Steel',
    # 'B2SteelA',
    # 'B2SteelDWSD',
    # 'B2SteelDLRFD',
    # 'B2bSteel',
    # 'B2cSteel',
    # 'B2dSteel',
    # 'B3SteelADLRFD',
    )}
    )
