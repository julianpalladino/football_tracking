import os
import pytest
import config
from object_tracker import MultiObjectTracker
from pdb import set_trace as st
import warnings

MINIMUM_SUCCESS_RATE = 70 # %70

test_filenames = ['messi1', 'messi2', 'messi3', 'maradona_1986']


@pytest.mark.parametrize('filename', test_filenames)
@pytest.mark.parametrize('tracking_method', config.TRACKER_METHODS)
def test01_all_methods_should_reach_minimum_success_rate(filename, tracking_method):
    object_tracker = MultiObjectTracker(
        os.path.join('data', filename + '.mp4'),
        os.path.join('data', filename + '_initial_conditions.json'),
        tracking_method,
        os.path.join('test_output', filename, '{}.mp4'.format(tracking_method)))
    success_rates = object_tracker.run_tracking()
    if not all([a_success_rate  > MINIMUM_SUCCESS_RATE for a_success_rate in success_rates]):
        warnings.warn(UserWarning(
            'For file {} and method {} success rates are {}. '.format(
                filename, tracking_method, success_rates) + \
            ' But the minimum is {}'.format(MINIMUM_SUCCESS_RATE)))
