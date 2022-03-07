import argparse

import pytest

import config
from object_tracker import MultiObjectTracker


def main():
    parser = argparse.ArgumentParser(description='Track football players')
    parser.add_argument('-test', action='store_true',
        help='Run pytest with all available input videos and methods')
    parser.add_argument('-input_path', action='store',
                        type=str, help='Input video filepath')
    parser.add_argument('-input_bbox_path', action='store',
                        type=str, help='Input bbox json filepath')
    parser.add_argument('-output_path', action='store',
                        type=str, help='Output video filepath')
    parser.add_argument('-method', action='store', type=str,
                        help='Tracking method. Can be one of the following: {}'.format(config.TRACKER_METHODS))
    parser.set_defaults(feature=True)
    args = parser.parse_args()

    if args.test:
        pytest.main(['-s', '/app/'])
    else:
        assert args.input_path != None, 'input_path parameter should not be None'
        assert args.input_bbox_path != None, 'input_bbox_path parameter should not be None'
        assert args.method != None, 'method parameter should not be None'
        assert args.output_path != None, 'output_path parameter should not be None'
        object_tracker = MultiObjectTracker(
            args.input_path,
            args.input_bbox_path,
            args.method,
            args.output_path)
        object_tracker.run_tracking()


if __name__ == '__main__':
    main()
