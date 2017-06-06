class FileOut():
    '''Provides a file exporting interface compatible with the pathlib.Path API 
    for any iterable object.'''
    def __init__(self, obj, path = None, *, mode = 'w', obj_iter = None):
        self.obj = obj
        self.path = path
        self.mode = mode
        try:
            self._iter = obj.__iter__
        except AttributeError:
            raise TypeError('The obj is not iterable.') from None
    def to_str(self):
        '''Export the object to a string.'''
        return '\n'.join(self._iter())
    def to_stream(self, fstream):
        '''Export the object to provided stream.'''
        fstream.write(self.to_str())
    def __enter__(self):
        try:
            # do not override an existing stream
            self.fstream
        except AttributeError:
            # convert self.path to str to allow for pathlib.Path objects
            self.fstream = open(str(self.path), mode = self.mode)
        return self
    def __exit__(self, exc_t, exc_v, tb):
        self.fstream.close()
        del self.fstream
    def to_file(self, path = None, mode = None):
        '''Export the object to a file at the path.
        
        Saves to the active stream if it exists.'''
        if mode is None:
            mode = self.mode
        try:
            fstream = self.fstream
        except AttributeError:
            if path is None:
                path = self.path
            # convert path to str to allow for pathlib.Path objects
            with open(str(path), mode = mode) as fstream:
                self.to_stream(fstream)
        else:
            if mode != fstream.mode:
                raise IOError('Ambiguous stream output mode: \
                            provided mode and fstream.mode conflict')
            if path is not None:
                raise IOError('Ambiguous output destination: \
                            a path was provided with an already active file stream.')
            self.to_stream(fstream)
