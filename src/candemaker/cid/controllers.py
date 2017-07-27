import logging
from mytools.utilities import copymembers, getfields

logging = logging.getLogger(__name__)

class ControlError(Exception):
    pass

class ListComplete(Exception):
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
        raise TypeError('Failed to merge {} into {}.'
                        'The from_obj requires a ._fields attribute.'
                        ''.format(from_obj, to_obj)) from e

def top_level_merge(top_obj):
    '''Pulls sent objects into top object model.'''
    logging.debug('top_level_merge started')
    obj = yield
    logging.debug('top_level_merge received {}'
                  ''.format(obj))
    merge_lower(obj, top_obj)
    logging.debug('top_level_merge finished')


def list_merge(xlist):
    '''Appends sent objects to the list.'''
    logging.debug('list_merge started')
    obj = yield
    logging.debug('appending {}: {}'
                  ''.format(type(obj).__name__, obj))
    xlist.append(obj)
    logging.debug('list_merge finished')


def list_merge_last(xlist):
    '''Appends sent object to the list and raises
    an exception to signal the list is complete.'''
    logging.debug('list_merge_last started')
    obj = yield
    logging.debug('appending {}: {}'
                  ''.format(type(obj).__name__, obj))
    xlist.append(obj)
    logging.debug('list_merge_last finished')
    raise ListComplete()


def flatten_merge(top_obj):
    '''Pulls multiple objects into object model.'''
    logging.debug('flatten_merge started')
    try:
        while True:
            yield from top_level_merge(top_obj)
            logging.debug('continuing flatten_merge')
    except GeneratorExit:
        logging.debug('flatten_merge finished')
        raise


def mult_list_merge(xlist):
    '''Appends multiple objects to the list.'''
    logging.debug('mult_list_merge started')
    try:
        while True:
            yield from list_merge(xlist)
            logging.debug('continuing mult_list_merge')
    except GeneratorExit:
        logging.debug('mult_list_merge finished')
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
    except GeneratorExit:
        logging.debug('mult_list_merge finished')
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
    logging.debug('control_director split args into:\n'
                  'command: {}\nargs: {}'
                  ''.format(command, args))
    try:
        yield from dispatch[command](*args)
        logging.debug('control_director succeeded')
    except KeyError as err:
        logging.debug('control_director failed')
        raise ControlError('The dispatch control command '
                           '{!r} is not valid.'
                           ''.format(command), *args) from err


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
        logging.debug('controller dispatch finished')
        raise
