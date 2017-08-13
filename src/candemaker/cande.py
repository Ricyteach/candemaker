import logging
from mytools.utilities import copymembers, not_str
from enum import Enum, auto
from collections.abc import Sequence, Mapping
from collections import namedtuple as nt
from .candehandler import CandeHandler
from .cid.registry import CidUnformatterReg, CidNtReg
from .cid.enum import CidRegistry
from .ntconvert import NTtoLowerCaseObjEnum

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
                                                    for mem in (CidNtReg.Master,
                                                               CidNtReg.Info,
                                                               CidNtReg.Control)
                                                    for f in mem.value._fields
                                                    )
                                                    )
                )
CandeNTBase.__new__.__defaults__ = (None,) * (len(CandeNTBase._fields))

class CandeNT(CandeNTBase):
    '''Fully defined Cande Level 3 cid object'''
    __slots__ = ()
    def __new__(cls, *args, **kwargs):
        defaults = dict((f.lower(), v) for f,v in flatten((CidNtReg.Master.value(),
                                                           CidNtReg.Info.value(),
                                                           CidNtReg.Control.value(),
                                                           )))
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
    _fields = tuple(f.lower() for f in CidNtReg.Master.value._fields +
                                       CidNtReg.Info.value._fields +
                                       CidNtReg.Control.value._fields)
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
        return CidUnformatterReg[cidmember].value
    @classmethod
    def unformat(cls, cidline, cidmember):
        '''Parse a CID file line into a cid object'''
        unformatter = cls.unformatter(cidmember)
        ObjType = CandeObjReg[cidmember].value
        logging.debug('Unformatting {} to a {}'
                      ''.format(cidmember, ObjType.__name__))
        return ObjType(*unformatter.unformat(cidline))
    def __repr__(self):
        repgen = ('{}={!r}'.format(f, getattr(self, f, None))
                    for f in self._fields)
        return 'CandeObj({})'.format(', '.join(repgen))

class CandeObjReg(NTtoLowerCaseObjEnum, CidRegistry):
    # any
    A1 = auto()
    E1 = auto()
    # L3 Only
    A2 = auto()
    C1 = auto()
    C2 = auto()
    C3 = auto()
    # C3L = auto()
    C4 = auto()
    # C4L = auto()
    C5 = auto()
    # C5L = auto()
    # soil
    D1 = auto()
    # D1L = auto()
    # D1Soil = auto()
    # D1SoilL = auto()
    # D1Interf = auto()
    # D1InterfL = auto()
    # D2Orthotropic = auto()
    # D2Over = auto()
    # D2Hardin = auto()
    # D2HardinTRIA = auto()
    # D2Composite = auto()
    # D2MohrCoulomb = auto()
    # D2Isotropic = auto()
    # D2Duncan = auto()
    # D3Duncan = auto()
    # D4Duncan = auto()
    # D2Interface = auto()
    # alum
    # B1Alum = auto()
    # B2AlumA = auto()
    # B2AlumDWSD = auto()
    # B2AlumDLRFD = auto()
    # B3AlumADLRFD = auto()
    # plastic
    # B1Plastic = auto()
    # B2Plastic = auto()
    # B3PlasticAGeneral = auto()
    # B3PlasticASmooth = auto()
    # B3PlasticDWSD = auto()
    # B3PlasticDLRFD = auto()
    # B3PlasticAProfile = auto()
    # B3bPlasticAProfile = auto()
    # B4Plastic = auto()
    # steel
    # B1Steel = auto()
    # B2SteelA = auto()
    # B2SteelDWSD = auto()
    # B2SteelDLRFD = auto()
    # B2bSteel = auto()
    # B2cSteel = auto()
    # B2dSteel = auto()
    # B3SteelADLRFD = auto()
