import logging
from mytools.utilities import copymembers
from . import exceptions as exc

logging = logging.getLogger(__name__)

def merge_objs(from_obj, to_obj, members):
    '''Copies specified members from one object to another.'''
    logging.debug('Merging from\n{}: {}\n<---------to--------->\n{}: {}.'
                  ''.format(type(from_obj).__name__, from_obj,
                            type(to_obj).__name__, to_obj))
    try:
        copymembers(from_obj, to_obj, members, suppress_err=False)
    except AttributeError as e:
        raise exc.MergeError('Failed to merge from_obj into to_obj.',
                          from_obj, to_obj) from e


def merge_default(from_obj, to_obj):
    '''Copies all members from one object to another.'''
    fields = list(vars(from_obj))
    merge_objs(from_obj, to_obj, fields)

def merge_namedtuple(from_nt, to_obj):
    '''Copies all namedtuple fields from one object to another.'''
    fields = from_obj._fields
    merge_objs(from_obj, to_obj, fields)

def merge_namedtuple_lower(from_obj, to_obj):
    '''Copies all namedtuple fields from one object to another
    in lowercase form.
    '''
    fields = ((f, f.lower()) for f in from_obj._fields)
    merge_objs(from_obj, to_obj, fields)


def top_level_merge(top_obj, merger=merge_default):
    '''Pulls sent object into top object model using
    the specified merger.
    '''
    try:
        logging.debug('top_level_merge started')
        obj = yield
        logging.debug('top_level_merge received {}'
                      ''.format(obj))
        merger(obj, top_obj)
        logging.debug('top_level_merge finished')
    except GeneratorExit:
        logging.debug('top_level_merge exited')
        raise


def top_level_merge_last(top_obj, merger=merge_default):
    '''Pulls sent object into top object model using the
    specified merger and raises an exception to signal
    the object is complete.
    '''
    yield from top_level_merge(top_obj, merger)
    raise exc.ObjectComplete()


def list_merge(xlist):
    '''Appends sent object to the list.'''
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
    an exception to signal the list is complete.
    '''
    yield from list_merge(xlist)
    raise exc.SequenceComplete()


def flatten_merge(top_obj, merger=merge_default):
    '''Pulls multiple objects into top object model.'''
    logging.debug('flatten_merge started')
    try:
        while True:
            yield from top_level_merge(top_obj, merger)
            logging.debug('continuing flatten_merge')
    except exc.ObjectComplete:
        logging.debug('flatten_merge completed')
        raise
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
    except exc.SequenceComplete:
        logging.debug('mult_list_merge completed')
        raise
    except GeneratorExit:
        logging.debug('mult_list_merge exited')
        raise


def flat_list_merge(xlist, merger=merge_default):
    '''Flattens multiple sent objects and appends
    flattened object to the list.'''
    try:
        logging.debug('flat_list_merge started')
        obj = yield
        xlist.append(obj)
        obj_merge = flatten_merge(obj, merger)
        yield from obj_merge
    except exc.ObjectComplete:
        logging.debug('flat_list_merge finished')
        raise
    except GeneratorExit:
        logging.debug('flat_list_merge exited')
        raise

from .enum import CidRegistry

class CidBuildReg(CidRegistry):
    A1 = top_level_merge_last
    C1 = top_level_merge_last
    C2 = top_level_merge_last
    A2 = flat_list_merge
    D1Soil = flat_list_merge
    D1Interf = flat_list_merge
    C3 = mult_list_merge
    C4 = mult_list_merge
    C5 = mult_list_merge
    E1 = mult_list_merge
