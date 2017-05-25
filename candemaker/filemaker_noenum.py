def auto_save_as(filepath, saveaspath = None, ext = None):
    '''Provides a path-like object for saving a filepath under a new path.
    
    Will use the provided ext for the new file extension.
    If no saveaspath is provided, the same input file name is used; the input file extension
    will also be used if one is not provided. 
    If saveaspath is provided with no extension, the saveaspath is assumed to be directory.'''
    
    if saveaspath is None:
        savedir = filepath.parent
        savename = filepath.stem
        if ext is None:
            ext = filepath.suffix
    else:
        if saveaspath.suffix == '':
            savedir = saveaspath
            savename = filepath.stem
            ext = saveaspath.suffix
        else:
            savedir = saveaspath.parent
            savename = saveaspath.stem
            if ext != saveaspath.suffix:
                raise ValueError('Cannot resolve conflicting save as extensions.')

    savefile = type(saveaspath)(savename).with_suffix(ext)
    return savedir/savefile
    
class FileOut():
    '''An object that provides a file exporting interface for any iterable object.'''
    def __init__(self, obj, path = None, *, mode = 'w', obj_iter = None):
        self.obj = obj
        self.path = path
        self.mode = mode
        if obj_iter is None:
            try:
                self.obj_iter = obj.__iter__
            except AttributeError:
                raise TypeError('The obj must be iterable, or an obj_iter method parameter must be provided.')
        else:
            self.obj_iter = obj_iter
    def to_str(self):
        return '\n'.join(self.obj_iter())
    def to_stream(self, fstream):
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
