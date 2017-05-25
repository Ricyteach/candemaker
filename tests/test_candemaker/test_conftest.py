'''Test general testing fixtures in  conftest.'''

import pytest
from conftest import temp_testing_dir

print('\n', '\n', r'##### test_candemaker\conftest.py fixture tests ########', '\n')

temp_paths = [temp_testing_dir/'file_{}'.format(i) for i in range(5)]
temp_contents = ['contents'] * len(temp_paths)

@pytest.mark.test_temp_files
@pytest.mark.parametrize('temp_files',
                            [
                            temp_paths[0],
                            temp_paths,
                            ((temp_paths[0],temp_contents[0])),
                            (temp_paths[0],temp_contents[0]),
                            ((temp_paths, temp_contents)),
                            ],
                            ids = [
                            'test single arg', 'test seq of paths', 'test (single path, single content)', 'test single path, single content', 'test path seq, content seq'
                            ],
                            indirect = ['temp_files']
)
def test_temp_files(temp_files, testing_dir):
    assert True

def test_output_path(testing_dir):
    assert testing_dir.exists()

@pytest.mark.parametrize('call_f, x', 
                            [((int, '1'),1), ((str, 2),'2'), ((range, 1, 10, 2), range(1,10,2))], 
                            ids = ['test int', 'test str', 'test range'],
                            indirect=['call_f'])
def test_call_f(call_f, x):
    assert call_f == x