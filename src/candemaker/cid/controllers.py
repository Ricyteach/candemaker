import logging
from mytools.utilities import copymembers, getfields

logging = logging.getLogger(__name__)

class ControlError(Exception):
    pass

class CommandError(Exception):
    pass

class ListComplete(Exception):
    pass

class MergeError(Exception):
    pass

def merge_lower(from_obj, to_obj):
    '''Copies all members from one object to another
    in lowercase form.'''
    logging.debug('Merging from\n{}: {}\n<---------to--------->\n{}: {}.'
                  ''.format(type(from_obj).__name__, from_obj,
                            type(to_obj).__name__, to_obj))
    fields = ((f, f.lower()) for f in from_obj._fields)
    try:
        copymembers(from_obj, to_obj, fields, suppress_err=False)
    except AttributeError as e:
        raise MergeError('Failed to merge from_obj into to_obj.',
                          from_obj, to_obj) from e


def top_level_merge(top_obj):
    '''Pulls sent objects into top object model.'''
    try:
        logging.debug('top_level_merge started')
        obj = yield
        logging.debug('top_level_merge received {}'
                      ''.format(obj))
        merge_lower(obj, top_obj)
        logging.debug('top_level_merge finished')
    except GeneratorExit:
        logging.debug('top_level_merge exited')
        raise



def list_merge(xlist):
    '''Appends sent objects to the list.'''
    try:
        logging.debug('list_merge started')
        obj = yield
        logging.debug('appending {}: {}'
                      ''.format(type(obj).__name__, obj))
        xlist.append(obj)
        logging.debug('list_merge finished')
    except GeneratorExit:
        logging.debug('list_merge exited')
        raise


def list_merge_last(xlist):
    '''Appends sent object to the list and raises
    an exception to signal the list is complete.'''
    try:
        logging.debug('list_merge_last started')
        obj = yield
        logging.debug('appending {}: {}'
                      ''.format(type(obj).__name__, obj))
        xlist.append(obj)
        logging.debug('list_merge_last finished')
        raise ListComplete()
    except GeneratorExit:
        logging.debug('list_merge_last exited')
        raise


def flatten_merge(top_obj):
    '''Pulls multiple objects into object model.'''
    logging.debug('flatten_merge started')
    try:
        while True:
            yield from top_level_merge(top_obj)
            logging.debug('continuing flatten_merge')
    except GeneratorExit:
        logging.debug('flatten_merge exited')
        raise


def mult_list_merge(xlist):
    '''Appends multiple objects to the list.'''
    logging.debug('mult_list_merge started')
    try:
        while True:
            yield from list_merge(xlist)
            logging.debug('continuing mult_list_merge')
    except GeneratorExit:
        logging.debug('mult_list_merge exited')
        raise


def flat_list_merge(xlist):
    '''Flattens multiple sent objects and appends
    flattened object to the list.'''
    logging.debug('flat_list_merge started')
    try:
        obj = yield
        logging.debug('appending {}: {}'
                      ''.format(type(obj).__name__, obj))
        xlist.append(obj)
        yield from flatten_merge(obj)
        logging.debug('flat_list_merge finished')
    except GeneratorExit:
        logging.debug('mult_list_merge exited')
        raise


def control_director(dispatch):
    '''Dispatches control to generator from sent command
    and generator args.'''
    logging.debug('control_director started for dispatch:\n'
                  'Dispatch = {!r}'.format(dispatch.keys()))
    args = yield
    logging.debug('control_director received args of type {}'
                  ''.format(type(args).__name__))
    command, *args = getfields(args)
    logging.debug('control_director split args into:'
                  '\n\tcommand: {}\n\targs: {}'
                  ''.format(command, args))
    try:
        next_gen = dispatch[command]
        try:
            logging.debug('control_director dispatching to {}'
                          ''.format(next_gen.__name__))
        except AttributeError:
            raise TypeError('The chosen dispatcher is not a valid '
                            'dispatching type (i.e, a generator)')
        yield from next_gen(*args)
        logging.debug('control_director succeeded')
    except KeyError as err:
        logging.debug('control_director failed')
        raise ControlError('The dispatch control command is not valid.',
                           command, *args) from err
    except MergeError as err:
        logging.debug('Received a merge error:\n{}\nThe original '
                      'received command was {!r}.'.format(err, command))
        err.args = err.args + (command,)
        raise


def controller(dispatch, default=None):
    '''Manages generator dispatch.
    
    The dispatch argument is a mapping of commands to
    dispatch generators.
    
    The default argument is the generator to be used when
    there is an invalid key.
    '''
    logging.debug('controller started for dispatch')
    try:
        while True:
            try:
                yield from control_director(dispatch)
                logging.debug('continuing controller dispatch')
            except ControlError as err:
                logging.debug('controller dispatch to control_director failed')
                msg, args = err.args[:1], err.args[1:]
                if default:
                    yield from default(*args)
                    logging.debug('controller dispatch to default succeeded')
                    continue
                else:
                    logging.debug('no default - controller dispatch failed')
                    raise ControlError(msg)
    except GeneratorExit:
        logging.debug('controller dispatch exited')
        raise
