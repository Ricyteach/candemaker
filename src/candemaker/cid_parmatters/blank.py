class Blank():
    def __new__(cls, value=0):
        try:
            obj = super().__new__(cls, value)
            return obj
        except ValueError:
            if value == '' or value == ' ':
                return super().__new__(cls, 0.0)
            else:
                raise
    def __str__(self):
        return '' if self==0 else super().__str__()
    def __format__(self, spec):
        if (spec.endswith('d') or spec.endswith('f') or spec.endswith('n')) and self==0:
            spec = spec[:-1]+'s'
            return format('',spec)
        else:
            return super().__format__(spec)

class BlankInt(Blank, int):
    '''An int that prints blank when zero.'''
    pass
        
class BlankFloat(Blank, float):
    '''A float that prints blank when zero.'''
    pass