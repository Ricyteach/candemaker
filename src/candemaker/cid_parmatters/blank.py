class BlankInt(int):
    '''An int that prints a blank when zero.'''
    def __str__(self):
        return '' if self==0 else super().__str__()