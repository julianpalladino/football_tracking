import os
import shutil

def pytest_configure(config):
    '''
    We set up the output folder so old files don't get mixed with new ones
    '''
    if os.path.exists('test_output'):
        shutil.rmtree('test_output')
    return 'test_output'