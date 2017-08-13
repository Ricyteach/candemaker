from mytools.resettable import Resettable
from .cid.controllers import CidBuildReg
from .cid.gen import CidGenReg
from .cid.enum import CidEnum, CidRegistry
from .cid.exceptions import ObjectComplete, SequenceComplete
from .cid import controllers as ctl

class CandeHandler():
    def __init__(self, candeobj):
        self.obj = candeobj
        '''
        self.candeattr_reg = CidRegistry(A1=candeobj, A2=candeobj.groups, C1=candeobj, C2=candeobj,
                                         C3=candeobj.nodes, C4=candeobj.elements,
                                         C5=candeobj.boundaries, D1Soil=candeobj.materials,
                                         D1Interf=candeobj.materials, E1=candeobj.factors)
        '''
        self.handlerargs_reg = CidRegistry('handlerargs_reg', 
                                            dict(
                                                    A1 = (candeobj, ),
                                                    C1 = (candeobj, ),
                                                    C2 = (candeobj, ),
                                                    A2 = (candeobj.groups, ),
                                                    D1Soil = (candeobj.materials, ),
                                                    D1Interf = (candeobj.materials, ),
                                                    C3 = (candeobj.nodes,),
                                                    C4 = (candeobj.elements,),
                                                    C5 = (candeobj.boundaries,),
                                                    E1 = (candeobj.factors,),
                                                )
                                           )
    def __enter__(self):
        exec_logic = self.exec_logic(self.start)
        try:
            self.logic = exec_logic(self.obj)
        except AttributeError:
            self.logic = exec_logic()
        return self.build()
    def __exit__(self, owner, value, tb):
        self.logic.close()
        del self.logic
    def __call__(self, start):
        self.start = self.valid_tag(start)
        return self
    @staticmethod
    def valid_tag(tag):
        try:
            return CidEnum[tag].name
        except KeyError:
            raise ValueError('Invalid tag: '
                             '{!r}'.format(tag)) from None
    def exec_logic(self, cidmember='A1'):
        '''Get a logic generator object corresponding to the member'''
        return getattr(CidGenReg,cidmember)
    def make_handler(self, tag):
        '''Get a generator that accepts objects to build the CID file 
        section corresponding to the tag.
        
        Example:
            h = ch.make_handler('A1')
            h.send(None)
            h.send(some_A1_obj)
        '''
        handler_func = Resettable(getattr(CidBuildReg,tag))
        # handler_args is unique for each CandeObj instance
        # because each instances has its own members to be
        # passed as args
        handler_args = self.handlerargs_reg[tag].value
        return handler_func(*handler_args)
    def get_handler(self, tag):
        '''Get a handler object that accepts objects to build the CID file 
        section corresponding to the tag. The handler object initializes
        itself it has been closed.
        
        Example:
            h = c.get_handler('A1')
            h.send(some_A1_obj)
        '''
        self._handler = self.make_handler(tag)
        self._handler.send(None)
        return self._handler
    def build(self):
        # NOTE TO SELF TO ASSIST WITH UNDERSTANDING:
        # + next() and .send() are "caught" by the yield keyword
        # + Execution happens like so:
        #       START:  x = yield 1 
        #               y = yield 2
        #               z = yield 3
        #   execution has been suspended at the first yield. the
        #   1 has already been yielded previously. upon a next()
        #   or .send(), the generator executes everything between
        #   the first and second yield. the value is sent into x
        #   first, then 2 is yield. 
        # + code BEFORE a yield is executed upon next()
        #   and execution paused at the yield.
        # + code AFTER a yield is executed upon a .send()
        #   and excution paused at the NEXT yield.
        # + the FIRST .send(None) initializes up to first yield, 
        #   BUT a line like this: `x = yield 1` will yield the 1
        #   upon the first .send() call - excution is paused at
        #   the yield as usual, and x gets the next .send() arg.
        try:
            logic = self.logic
            while True:
                try:
                    try:
                        # label sent by self.logic generator
                        label = next(logic)
                    except ObjectComplete as e:
                        # next triggered a completion signal from logic
                        obj_handler.throw(e) # closes current handler
                        obj_handler.send(None) # closes current handler
                        # did not delete handler because these flat_list_merge
                        # handlers, which receive completion signal of a pipe
                        # group or a material type, are assumed to be @Resettable
                        # so that the current sequence continues being appended to
                except SequenceComplete:
                    # next triggered completion signal
                    # (second or first) from logic
                    obj_handler.close()
                    del obj_handler # new sequence means new handler
                # transmit label to main loop
                # for making an obj from label
                # receive obj sent by main loop
                obj = yield label
                try:
                    # continue with same handler if it exists
                    obj_handler
                except NameError:
                    # lookup and init. a handler generator
                    obj_handler = self.get_handler(label)
                    # the above line really shouldn't cause any errors...
                    # if it does then i may not understand what my code
                    # is doing and that sucks.
                try:
                    obj_handler.send(obj) # success
                except ObjectComplete:
                    # got signal that section is complete
                    obj_handler.close()
                    del obj_handler
        except GeneratorExit:
            del self._handler
            raise

'''
        sections:
            A1:
                next(logic)
                # label sent by self.logic generator
                label = yield # A1
                # lookup and init. a handler generator
                obj_handler = self.get_handler(label) # top_level_merge_last(top_obj, merger=merge_default)
                # transmit label for making an obj from line
                yield label
                # obj sent by main from_cid loop
                obj = yield
                try:
                    obj_handler.send(obj) # success
                except Complete:
                    # got signal that section is complete
                    obj_handler.close()

            A2:
                next(logic)
                # label sent by self.logic generator
                label = yield # A2
                # lookup and init. a handler generator
                obj_handler = self.get_handler(label) # flat_list_merge(xlist, merger=merge_default)
                # transmit label for making an obj from line
                yield label
                # obj sent by main from_cid loop
                obj = yield
                obj_handler.send(obj) # success
            
            B1:
                next(logic)
                # label sent by self.logic generator
                label = yield # B1, first part
                try:
                    # lookup and init. a handler generator
                    obj_handler = self.get_handler(label) # no handler for B1
                except AttributeError:
                    pass # keep same handler as before
                # transmit label for making an obj from line
                yield label
                # obj sent by main from_cid loop
                obj = yield
                obj_handler.send(obj) # success
            
            B2:
                next(logic)
                # label sent by self.logic generator
                label = yield # B2, last part
                try:
                    # lookup and init. a handler generator
                    obj_handler = self.get_handler(label) # no handler for B2
                except AttributeError:
                    pass # keep same handler as before
                # transmit label for making an obj from line
                yield label
                # obj sent by main from_cid loop
                obj = yield
                obj_handler.send(obj) # success
            
            A2 #2:
                try:
                    next(logic)
                except Complete as e:
                    # next triggered a completion signal from logic
                    obj_handler.throw(e) # closes current handler
                    obj_handler.send(None)
                # label sent by self.logic generator
                label = yield # A2
                # lookup and init. a handler generator
                obj_handler = self.get_handler(label) # flat_list_merge(xlist, merger=merge_default)
                # transmit label for making an obj from line
                yield label
                # obj sent by main from_cid loop
                obj = yield
                obj_handler.send(obj) # success
        
            B1 #2:
                next(logic)
                # label sent by self.logic generator
                label = yield # B1, first part
                try:
                    # lookup and init. a handler generator
                    obj_handler = self.get_handler(label) # no handler for B1
                except AttributeError:
                    pass # keep same handler as before
                # transmit label for making an obj from line
                yield label
                # obj sent by main from_cid loop
                obj = yield
                obj_handler.send(obj) # success
                
                next(logic)
                # label sent by self.logic generator
                label = yield # B2, last part
                try:
                    # lookup and init. a handler generator
                    obj_handler = self.get_handler(label) # no handler for B2
                except AttributeError:
                    pass # keep same handler as before
                # transmit label for making an obj from line
                yield label
                # obj sent by main from_cid loop
                obj = yield
                obj_handler.send(obj) # success
        
            C1:
                try:
                    next(logic)
                except Complete as e:
                    # next triggered a completion signal from logic
                    obj_handler.throw(e) # closes current handler
                # label sent by self.logic generator
                label = yield # C1
                # lookup and init. a handler generator
                obj_handler = self.get_handler(label) # top_level_merge_last(top_obj, merger=merge_default)
                # transmit label for making an obj from line
                yield label
                # obj sent by main from_cid loop
                obj = yield
                obj_handler.send(obj) # success

            C2:
                try:
                    next(logic)
                except Complete as e:
                    # next triggered a completion signal from logic
                    obj_handler.throw(e) # closes current handler
                    obj_handler.send(None) # re-initializes handler
                # label sent by self.logic generator
                label = yield # C2
                # lookup and init. a handler generator
                obj_handler = self.get_handler(label) # top_level_merge_last(top_obj, merger=merge_default)
                # transmit label for making an obj from line
                yield label
                # obj sent by main from_cid loop
                obj = yield
                obj_handler.send(obj) # success
            
            C3,4,5 and E1 first and on:
                try:
                    next(logic)
                except Complete as e:
                    # next triggered a completion signal from logic
                    obj_handler.throw(e) # closes current handler
                    obj_handler.send(None) # re-initializes handler
                # label sent by self.logic generator
                label = yield # label is C3 or C4 or C5
                # transmit label for making an obj from line
                yield label
                # obj sent by main from_cid loop
                obj = yield
                obj_handler.send(obj) # success

'''