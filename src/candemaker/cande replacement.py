from mytools.utilities import not_str
from . import exceptions as exc, reg
from .cid import controllers as ctl
from .cid.enum import CidEnum

class Builder():
    def __init__(self, obj):
        self.obj = obj
    def __enter__(self):
        self.obj.listener = self.build(self.obj)
        exec_logic = self.exec_logic
        try:
            self.logic = exec_logic(self.start)
        except AttributeError:
            self.logic = exec_logic()
        return self.obj.listener
    def __exit__(self, owner, value, tb):
        self.obj.listener.close()
        del self.obj.listener
        del self.logic
    def exec_logic(self, cidmember='A1'):
        '''Get a logic generator object corresponding to the member'''
        return cidgen_reg[cidmember]
    def build(self, obj):
        for _ in self.logic:
            try:
                # signal sent by self.logic generator
                signal = yield
                # lookup and init. a handler generator
                obj_handler = obj.get_handler(signal)
                # transmit signal for making an obj from line
                yield signal
                # new_obj sent by main from_cid loop
                new_obj = yield
                while True:
                    try:
                        obj_handler.send(new_obj)
                        next(self.logic)
                        signal = yield
                        yield signal
                        new_obj = yield
                    except exc.Complete as e:
                        obj_handler.throw(e)
                        break
            except exc.Complete:
                continue
            finally:
                obj_handler.close()
    @staticmethod
    def valid_tag(tag):
        try:
            return CidEnum[tag].name
        except KeyError:
            raise ValueError('Invalid tag: '
                             '{!r}'.format(tag)) from None
    def __call__(self, start):
        self.start = self.valid_tag(start)
        return self

class CandeObj():
    '''For working with Cande Level 3 problems'''
    # catalog of members that are atomic
    _fields = tuple(f.lower() for f in Master._fields + Info._fields + Control._fields)
    # catalog of members that are collections
    _lists = 'groups nodes elements boundaries materials factors'.split()
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
        self._init_reg()
    def _init_reg(self):
        self.candeattr_reg = reg.CidRegistry(A1=self, A2=self.groups, C1=self, C2=self,
                                             C3=self.nodes, C4=self.elements,
                                             C5=self.boundaries, D1Soil=self.materials,
                                             D1Interf=self.materials, E1=self.factors)
        self.handlerargs_reg = reg.CidRegistry(
                                            A1 = (self, ctl.merge_namedtuple_lower),
                                            C1 = (self, ctl.merge_namedtuple_lower),
                                            C2 = (self, ctl.merge_namedtuple_lower),
                                            A2 = (self.groups, ctl.merge_namedtuple_lower),
                                            D1Soil = (self.materials, ctl.merge_namedtuple_lower),
                                            D1Interf = (self.materials, ctl.merge_namedtuple_lower),
                                            C3 = (self.nodes,),
                                            C4 = (self.elements,),
                                            C5 = (self.boundaries,),
                                            E1 = (self.factors,),
                                            )
    @classmethod
    def empty(cls):
        obj = cls.__new__(cls)
        obj._init_reg()
        return obj
    @classmethod
    def from_cid(cls, lines, start='A1'):
        '''Construct an instance using a file-like sequence'''
        not_str(lines)
        obj = cls.empty()
        with obj.builder(start) as build_process:
            logging.debug('***CANDE_OBJ BUILD BEGUN***')
            for line, tag in zip(lines, build_process):
                logging.debug('***BEGINNING OF SECTION {} HANDLING***'
                              ''.format(tag))
                cid_obj = obj.unformat(line, tag)
                build_process.send(cid_obj)
                logging.debug('***ENDING OF SECTION {} HANDLING***'
                              ''.format(label))
            logging.debug('***CANDE_OBJ BUILD COMPLETE***')
        return obj
    def builder(self, cidmember='A1'):
        try:
            if self._builder.start != cidmember:
                raise AttributeError()
        except AttributeError:
            self._builder = Builder(self)(cidmember)
        return self._builder
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
    def __repr__(self):
        repgen = ('{}={!r}'.format(f, getattr(self, f, None))
                    for f in self._fields)
        return 'CandeObj({})'.format(', '.join(repgen))
