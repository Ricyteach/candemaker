from mytools import update_special
from mytools.validdict import ValidKeyDict
import logging
from .cid.enum import CidEnum, ObjEnum
from types import ModuleType


class RegistryError(Exception):
    pass


class CidRegistry(ValidKeyDict):
    '''A ValidKeyDict which validates keys against CidEnum member names
    '''
    _valid_keys = CidEnum._member_names_


class ObjRegistry(ValidKeyDict):
    '''A ValidKeyDict which validates keys against ObjEnum member names
    '''
    _valid_keys = ObjEnum._member_names_


# unformatter = CidRegistry()
# cidobj_reg = ObjRegistry()


'''
# Not using right now - may delete
def register(*modules, registry, names):
    '''#Register objects in modules corresponding to CidEnum member names
'''
    for module in modules:
        temp_reg = {}
        logging.info('Begin registration of {} module'
                    ''.format(module.__name__))
        try:
            for mod_oname in vars(module):
                if mod_oname in names:
                    update_special(temp_reg, {mod_oname : vars(module)[mod_oname]})
                    logging.debug('Registered {} object'
                                 ''.format(mod_oname))
        except KeyError as err1:
            err2 = RegistryError('{} module missing {!r} object'
                                ''.format(module.__name__, mod_oname))
            logging.exception(err2)
            raise err2 from err1
        else:
            try:
                update_special(registry, temp_reg)
            except ValueError as err1:
                err2 = RegistryError('The same object name used in multiple registered modules')
                logging.exception(err2)
                raise err2 from err1
            logging.info('Registered {:d} objects in {} module'
                        ''.format(len(temp_reg), module.__name__))
    logging.info('\n'.join(('registration completed for {!r} modules:'.format(len(modules)),
                            '{}'.format(', '.join((m.__name__ for m in modules))))))


    def register_all():
        from . import cid
        modules = cid, cid.L3, cid.soil, *(getattr(cid.pipe, item) for item in vars(cid.pipe) if isinstance(getattr(cid.pipe, item), ModuleType))
        logging.info('cid generator registration starting')
        register(*modules, registry=cidgen)
        logging.info('cid generator registration complete')


        from .cid import linedef as ld_mod
        modules = ld_mod, ld_mod.L3, ld_mod.soil, *(getattr(ld_mod.pipe, item) for item in vars(ld_mod.pipe) if isinstance(getattr(ld_mod.pipe, item), ModuleType))
        logging.info('cid generator registration starting')
        register(*modules, registry=linedef)
        logging.info('cid definition registration complete')


    from .cid import cidparmatters
    modules = XXX, XXX, *(getattr(XXX, item) for item in vars(XXX) if isinstance(getattr(XXX, item), ModuleType))
    logging.info('cid unformatter registration starting')
    register(*modules, registry=unformatter)
    logging.info('cid unformatter registration complete')
    '''
