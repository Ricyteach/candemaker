from mytools.validdict import ValidKeyDict, ValidKeys
from .enum import CidEnum, ObjEnum

class CidRegistry(ValidKeyDict):
    '''Member names validated against CidEnum.'''
    valid_keys = ValidKeys(*CidEnum._member_map_)


class ObjRegistry(ValidKeyDict):
    '''Member names validated against ObjEnum.'''
    valid_keys = ValidKeys(*ObjEnum._member_map_)


