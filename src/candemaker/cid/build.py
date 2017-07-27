import logging
from .controllers import controller, top_level_merge, flatten_merge, flat_list_merge, list_merge, list_merge_last, ListComplete, ControlError
from .. import reg

logging = logging.getLogger(__name__)

cidbuild_reg = reg.CidRegistry(
                            A1 = flatten_merge,
                            C1 = flatten_merge,
                            C2 = flatten_merge,
                            A2 = flat_list_merge,
                            D1 = flat_list_merge,
                            C3 = list_merge,
                            C4 = list_merge,
                            C5 = list_merge,
                            C3L = list_merge_last,
                            C4L = list_merge_last,
                            C5L = list_merge_last,
                            )


class DispatchController():
    def __init__(self, dispatch, default=top_level_merge):
        self.dispatch = dispatch
        self.default = default
        self.cande = None
    def __get__(self, obj, owner=None):
        if self.cande is not None:
            raise ControlError('The DispatchController is already in use.')
        logging.debug('DispatchController fetched from {}'
                      ''.format(type(obj).__name__))
        self.controller = controller(self.dispatch, self.default)
        self.controller.send(None)
        logging.debug('DispatchController initialized with None')
        self.cande = obj
        return self
    def __enter__(self):
        return self
    def __exit__(self, owner, value, tb):
        self.controller.close()
        self.cande = None
    def reset(self):
        logging.debug('DispatchController resetting')
        self.controller.close()
        self.controller = controller(self.dispatch, self.default)
        self.controller.send(None)
        logging.debug('DispatchController initialized with None')
        logging.debug('DispatchController reset complete')
    def send(self, member_name, cande_obj):
        if self.cande is None:
            raise ControlError('Use the DispatchController only in a context manager.')
        logging.debug('DispatchController.send:\n\tmember_name: {}\n\t'
                      'cande_obj type: {}\n\tcande_obj: {}'
                      ''.format(member_name, type(cande_obj).__name__, cande_obj))
        if member_name in 'A2 C1 D1 STOP'.split():
            self.reset()
        try:
            to_send = member_name, self.cande.candeattr_reg[member_name]
            self.controller.send(to_send)
        except KeyError:
            pass
        to_send = cande_obj
        try:
            self.controller.send(to_send)
        except ListComplete:
            self.reset()
