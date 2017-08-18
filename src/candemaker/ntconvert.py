import logging
from enum import Enum
from .cid.registry import CidTagReg

logging = logging.getLogger(__name__)


def NTtoLowerCaseObj(name, bases=(), ns={}):
    '''Factory for converting a namedtuple class with capital letters in
    its member names into a regular mutable class with the fields as all
    lower case attribute names. The default argument values are considered.
    '''
    ntbases = tuple(b for b in bases if issubclass(b, tuple)
                                        and hasattr(b, '_fields'))
    bases = tuple(b for b in bases if b not in ntbases)
    basenames = tuple(b.__name__ for b in bases)
    if len(set(basenames)) != len(bases):
        raise ValueError('Duplicate parent class names detected')
    if any(not n.isidentifier() for n in basenames):
        raise ValueError('Invalid parent class name detected')
    for bn, b in zip(basenames, bases):
        exec(f'{bn} = b')
    bases_str = ', '.join(bn for bn in basenames)
    args = []
    args_dict = {}
    for base in reversed(ntbases):
        defaults = base.__new__.__defaults__
        fields = tuple(f.lower() for f in base._fields)
        args_rev = reversed(fields)
        defaults_rev = reversed(defaults if defaults is not None else ())
        # defaults_rev comes first in zip so it will be consumed first
        def_args_rev = zip(defaults_rev, args_rev)
        def_args = list(reversed(list(def_args_rev)))
        defaultnames = [f'_{n}' for _,n in def_args]
        for dn, d in zip(reversed(defaultnames), reversed(defaults)):
            exec(f'{dn} = d')
        # remaining args without defaults goes to args
        args.extend(list(reversed(list(args_rev))))
        def_args_dict = dict((k, f'{v!r}')
                              for (v,k),_
                              in zip(def_args, defaultnames))
        args_dict.update(def_args_dict)
    args_str = ', '.join(['self'] + args)
    kwargs_str = ', '.join(f'{k} = {v}' for k,v in args_dict.items())
    signature_str = args_str + (', ' if args_str and kwargs_str 
                                     else '') + kwargs_str
    init_str = '\n        '.join(f'self.{n} = {n}' for n in fields)
    
    code = f'''
class {name}({bases_str}):
    def __init__({signature_str}):
        {init_str}
    '''
    exec(code)
    result = eval(f'{name}')
    logging.debug(f'New class {name!r} created:\n{code}')
    return result


def NTtoLowerCaseObjFactory(name):
    '''Creates LowerCaseObj classes for members of CidTagReg.'''
    tag, NT = name, CidTagReg[name]
    return NTtoLowerCaseObj(name=tag, bases=(NT,))
