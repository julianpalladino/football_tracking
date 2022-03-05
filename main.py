import config
from object_tracker import MultiObjectTracker
import argparse


def main():
    parser = argparse.ArgumentParser(description='Track football players')
    parser.add_argument('input_path', action='store',
                        type=str, help='Input video filepath')
    parser.add_argument('input_bbox_path', action='store',
                        type=str, help='Input bbox json filepath')
    parser.add_argument('output_path', action='store',
                        type=str, help='Output video filepath')
    parser.add_argument('method', action='store', type=str,
                        help='Tracking method. Can be one of the following: {}'.format(config.TRACKER_METHODS))
    args = parser.parse_args()

    object_tracker = MultiObjectTracker(
        args.input_path,
        args.input_bbox_path,
        args.method,
        args.output_path)
    object_tracker.run_tracking()


if __name__ == '__main__':
    main()
