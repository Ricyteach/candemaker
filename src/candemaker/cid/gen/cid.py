from .. import exceptions as exc
from ..enum import CidEnum

__all__ = 'A1 E1'.split()


class Generator():
    '''Generator wrapper.'''
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.start()
    def __next__(self):
        n = self.send(None)
        return n
    def __iter__(self):
        yield from self._gen
    def start(self):
        self._gen = self._func(*self.args, **self.kwargs)
    def send(self, *args, **kwargs):
        n = self._gen.send(*args, **kwargs)
        return n
    def throw(self, *args, **kwargs):
        self._gen.throw(*args, **kwargs)
    def close(self):
        self._gen.close()

def GeneratorObj(some_func):
    '''Makes a regular generator function into a
    Generator object. Example usage:
    
        @GeneratorDesc
        def f():
            yield
    '''
    cls = type(some_func.__name__, (Generator,), {})
    cls._func = staticmethod(some_func)
    return cls



def gen_line(tag):
    '''Validate the CID tag'''
    yield CidEnum[tag].name # execution pauses here

#@GeneratorObj
def A1(cid):
    yield from gen_line('A1')
    if cid.level == 3:
        from .L3 import L3
        yield from L3(cid)
    else:
        raise exc.CIDError('L1 and L2 not yet implemented')
    if cid.method == 1: #  LRFD
        for step_num, _ in enumerate(range(cid.nsteps), 1):
            yield from E1(cid)
        cid.listener.throw(exc.SequenceComplete, ('Factors completed', len(cid.factors)))

#@GeneratorObj
def E1(cid):
    yield from gen_line('E1')
