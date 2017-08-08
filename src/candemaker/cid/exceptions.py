class CIDError(Exception):
    pass

class Complete(Exception):
    '''Signals completion of a context.'''
    pass

class SequenceComplete(Complete):
    '''Signals completion of current sequence.'''
    pass

class ObjectComplete(Complete):
    '''Signals completion of current object.'''
    pass

class MergeError(Exception):
    '''Failure to merge two objects.'''
    pass
