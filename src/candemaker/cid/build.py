import pdb
import logging
from .controllers import merge_lower, controller, top_level_merge, flatten_merge, flat_list_merge, list_merge, list_merge_last, ListComplete, ControlError, MergeError, CommandError
from .. import reg

logging = logging.getLogger(__name__)

cidbuild_reg = reg.CidRegistry(
                            A1 = flatten_merge,
                            C1 = flatten_merge,
                            C2 = flatten_merge,
                            A2 = flat_list_merge,
                            D1Soil = flat_list_merge,
                            D1Interf = flat_list_merge,
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
    def check_active(self):
        if self.cande is None:
            raise ControlError('Use the DispatchController only in a context manager.')
    def send(self, member_name, cande_obj):
        logging.debug('DispatchController.send:\n\tmember_name: {}\n\t'
                      'cande_obj type: {}\n\tcande_obj: {}'
                      ''.format(member_name, type(cande_obj).__name__, cande_obj))
        # each of these can mean the end of a previous sub-section
        if member_name in 'A2 C1 D1 STOP'.split():
            self.reset()
        try:
            self.send_control_command(member_name, cande_obj)
        except CommandError:
            pass
        self.send_cande_obj(cande_obj)
    def send_control_command(self, member_name, cande_obj):
        self.check_active()
        try:
            to_send = member_name, self.cande.candeattr_reg[member_name]
        except KeyError as err:
            raise CommandError(member_name, cande_obj) from err
        self.controller.send(to_send)
    def send_cande_obj(self, cande_obj):
        self.check_active()
        try:
            logging.debug('Initial attempt to send cande_obj received from {}: {} '
                          'type cande_obj'.format(type(self.cande).__name__, 
                                                  type(cande_obj).__name__))
            self.controller.send(cande_obj)
            logging.debug('Initial attempt to send cande_obj succeeded.')
        except ListComplete:
            logging.debug('Initial attempt to send cande_obj succeeded. '
                          'Received signal to reset the list.')
            self.reset()
        except MergeError as merge_err:
            # The intial attempt may fail because the namedtuple object is trying
            # to be merged into a top_level object that is itself simply some
            # namedtuple; the two namedtuples need to be merged into a new top_level
            logging.debug('Initial attempt to send cande_obj failed. '
                          'Getting new object...')
            second, first, member_name = merge_err.args[1:]
            logging.debug('Constructing new object from {} and {}'
                          ''.format(*(type(o).__name__ for o in (first, second))))
            self.reset()
            new_obj = type(type(first).__name__+'Object', (), {})()
            logging.debug('Merging first into new object: {}'.format(type(new_obj).__name__))
            merge_lower(first, new_obj)
            self.send_control_command(member_name, new_obj)
            logging.debug('Sending second object: {}'.format(type(second).__name__))
            self.send_cande_obj(second)
            logging.debug('Handling of MergeError complete.')
        except Exception:
            logging.debug('Initial attempt to send cande_obj failed. Need new object?')
            raise
