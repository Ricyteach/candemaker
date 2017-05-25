'''Create general fixtures for testing.'''

from pathlib import Path
import pytest 

temp_testing_dir = Path(r'C:\temp_tests')

@pytest.fixture(scope='function')
def temp_files(request):
    '''Create temporary files in the supplied directory using a sequence of paths.
    First argument [0] is a sequence of file paths, or a file path, to be created.
    If present, second argument [1] is a sequence of strings, or a string, representing the temporary file contents. 
    This fixture will attempt to clean up the temporary files when done and ignores FileNotFound errors.
    NOTE: if two strings supplied, both assumed to be temp file names (with no contents).'''
    # sentinel to detect if multiple parameters given AND first parameter is a sequence of PathLike objects
    param0_is_path_seq = None
    try:
        # will succeed if only a single PathLike object argument supplied
        temp_ps = (Path(request.param),)
    except TypeError:
        # parse multiple supplied arguments and detect of single argument is not PathLike
        try:
            params = (*request.param,)
            # check for two parameters supplied, which could mean ambiguous values (e.g., ['test_file', 'test_contents'])
            if len(params) == 2:
                try:
                    # succeed if all args are PathLike
                    *(Path(param) for param in params),
                except TypeError:
                    pass
                else:
                    # check if all same type -> 
                    if len(set(type(param) for param in params)) == 1:
                        # YES: assume all intended to be path-like objects
                        pass
                    else:
                        # NO: turn first, second args into sequences
                        # subsequent code will assume first intended to be path-like object, second intended to be contents
                        params = (params[0],),(params[1],)
        except TypeError:
            raise TypeError('Supplied argument is {}, not a valid PathLike object.'.format(type(request.param).__name__)) from None

    try:
        # will succeed if supplied a sequence of PathLike objects
        temp_ps = tuple(Path(param) for param in params)
    except NameError:
        # a single PathLike object was supplied
        pass
    except TypeError:
        # continue to parse assuming first argument is a sequence of PathLike objects or a single PathLike object
        param0 = params[0]
        try:
            # will succeed if supplied a single PathLike object as first argument
            temp_ps = Path(param0)
        except TypeError:
            try:
                # will succeed if supplied a sequence of PathLike objects
                temp_ps = tuple(Path(p) for p in param0)
                # mark first param exists and is as a sequence of PathLike objects
                param0_is_path_seq = object()
            except TypeError:
                # will fail if not supplied a sequence of PathLike objects, a sequence of PathLike object as first argument, a single PathLike object as first argument, or a single PathLike object
                raise TypeError('Supplied argument is not a valid PathLike object nor is it a sequence of PathLike objects.') from None

    try:
        # will succeed if second param exists
        param1 = params[1]
    except (NameError, IndexError):
        # no contents argument object was supplied
        temp_contents = None
    else:
        if param0_is_path_seq is None:
            # either params is not a sequence OR param0 is not a sequence of PathLike objects, therefore 
            # second param is not content or a content sequence
            temp_contents = None
        else:
            try:
                # will succeed if second param is a sequence
                temp_contents = *param1,
            except TypeError:
                temp_contents = (param1,)
            # confirm same number of temp files and file contents
            if len(temp_ps) != len(temp_contents):
                raise ValueError('Mismatched number of temporary files ({}) and temporary file contents ({}).'.format(len(temp_ps), len(temp_contents))) from None
    try:
        if temp_contents is None:
            for p in temp_ps:
                # create temporary file
                p.touch()
        else:
            for p,c in zip(temp_ps, temp_contents):
                # create temporary file with temp contents
                p.write_text(c)
    except:
        raise
    else:
        yield temp_ps
    finally:
        # remove temporary files when tests are finished
        '''
        for p in temp_ps:
            p.unlink()
        '''    
        for p in temp_ps:
            try:
                p.unlink()
            except FileNotFoundError:
                # file was already deleted; no problem
                continue
            except OSError:
                # problem with permissions? 
                raise

@pytest.fixture(scope='function')
def temp_dirs(request):
    '''Create temporary directories using a sequence of paths.
    First argument [0] is the is a sequence of directory paths to be created.
    Any tests utilizing this fixture should clean up temporary directory contents when done or it will raise OSError.'''
    try:
        # will succeed if only a single PathLike object argument supplied
        temp_ps = (Path(request.param),)
    except TypeError:
        try:
            # will succeed if supplied a sequence
            params = (*request.param,)
        except TypeError as exc:
            raise TypeError('Supplied argument must be a path-like object or a sequence of path-like objects, not {}.'.format(type(request.param).__name__)) from None
        else:
            try:
                # will succeed if supplied a sequence of PathLike objects
                temp_ps = tuple(Path(param) for param in params)
            except TypeError:
                raise TypeError('Supplied argument is not a valid PathLike object nor is it a sequence of PathLike objects.') from None
    try:
        for p in temp_ps:
            # create temporary dir
            p.mkdir()
    except:
        raise
    else:
        yield temp_ps
    finally:
        # remove temporary folders when tests are finished
        for p in temp_ps:
            try:
                p.rmdir()
            except FileNotFoundError:
                # directory was already deleted; no problem
                continue
            except OSError:
                # there is stuff in the directory that didn't get cleaned up
                # or there's a problem with permissions? 
                raise

@pytest.fixture(autouse = True, scope='session')
def testing_dir():
    '''Establish the file output directory location to be used for testing.'''
    try:
        p = temp_testing_dir
        p.mkdir()
        yield p
    finally:
        try:
            p.rmdir()
        except OSError as exc:
            print('\n!!!! Temporary testing directory was not removed successfully: {}'.format(exc.args[0]))

@pytest.fixture(scope='function')
def call_f(request):
    '''Call the function with the provided arguments and return the result.'''
    f, args = request.param[0], request.param[1:]
    return f(*args)
    
@pytest.fixture(scope='function')
def ecolibrium_path():
    from ecobase.parse_paths import ecolibrium_path as p
    yield p
    
@pytest.fixture(scope='function')
def work_order_path():
    from ecobase.parse_paths import work_order_path as p
    yield p
    
