import os
from tracked_object import TrackedObject
import json
from colors import COLORS
import cv2
from tqdm import tqdm


class MultiObjectTracker():
    '''
    Class which loads video, keeps track of all tracked objects, annotates
    the video and saves it

    Parameters
    ----------
    input_filepath: str, filepath for input mp4 video
    input_bbox_json_filepath: str, filepath for input json file with bbox data
    tracking_method: str, determines which tracker method to use. See config.py
        for all possible methods
    output_filepath: str, filepath for output annotated mp4 video
    verbose: bool, allows additional printing
    '''
    def __init__(self,
                 input_filepath,
                 input_bbox_json_filepath,
                 tracking_method,
                 output_filepath,
                 verbose=True):

        # Validation
        assert input_filepath[-3:] == 'mp4', 'Only mp4 format is accepted'

        # Initialization
        self.verbose = verbose
        self.tracking_method = tracking_method
        self.input_filepath = input_filepath
        self.output_filepath = output_filepath
        self.video_in = cv2.VideoCapture(input_filepath)

        self.tracked_objects = self.parse_hbox_json(input_bbox_json_filepath)
        self.print_initial_message()
        self.create_video_writer_for_output()
        self.initialize_trackers()

    def print_initial_message(self):
        '''
        Prints initial message if self.verbose is True
        '''
        self.print_if_verbose(
            'Loading MultiObjectTracker:\n' +
            '  > Input file: {}\n'.format(self.input_filepath) +
            '  > Output file: {}\n'.format(self.output_filepath) +
            '  > Tracking method: {}\n'.format(self.tracking_method) +
            '  > Number of objects: {}\n'.format(len(self.tracked_objects)))

    def create_video_writer_for_output(self):
        '''
        Creates VideoWriter object for output annotated video
        '''
        dir = os.path.dirname(self.output_filepath)
        if dir != '':
            os.makedirs(dir, exist_ok=True)
        cap_fps = self.video_in.get(cv2.CAP_PROP_FPS)
        frame_width, frame_height = self.get_frame_dimensions()
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.video_out = cv2.VideoWriter(
            self.output_filepath, fourcc, cap_fps, (frame_width, frame_height))

    def get_frame_dimensions(self):
        '''
        Gets the frame dimensions of the input video

        Returns
        -------
        Tuple of integers (frame_width, frame_height)
        '''
        frame_width = int(self.video_in.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(self.video_in.get(cv2.CAP_PROP_FRAME_HEIGHT))
        return frame_width, frame_height

    def initialize_trackers(self):
        '''
        Initializes all trackers for the given input video
        '''
        _, init_frame = self.video_in.read()
        self.number_of_frames = int(
            self.video_in.get(cv2.CAP_PROP_FRAME_COUNT))
        for a_tracked_object in self.tracked_objects:
            a_tracked_object.initialize_tracker(init_frame)
        cv2.imwrite('init_frame.png', init_frame)

    def parse_hbox_json(self, input_bbox_json_filepath):
        '''
        Parses a json of initial conditions into a list of tracked objects.
        The json is expected to be a list of dictionaries with the following keys:
        * Name: String. Name of the object to track. i.e 'player'
        * Id: Int. Id of the object to track.
        * Coords: List of 4 ints: x, y, width, height

        Returns
        -------
        A list of TracedObjects corresponding to the given bbox json filepath
        '''
        with open(input_bbox_json_filepath, 'r') as f:
            list_of_dicts = list(json.load(f))

        list_of_tracked_objects = []
        assert len(list_of_dicts) < len(COLORS), \
            'Insufficient number of colors for the objects to track'

        for a_bbox_dict, a_color in zip(list_of_dicts, COLORS):
            list_of_tracked_objects.append(
                TrackedObject(a_bbox_dict, a_color, self))

        return list_of_tracked_objects

    def run_tracking(self):
        '''
        Runs tracking for all TrackedObjects for all frames for the given input
        video filepath, saves annotated video in given output filepath

        Returns
        -------
        A list of success rates corresponding to the tracked objects
        '''
        if self.verbose:
            iterable_frames = tqdm(range(self.number_of_frames-5))
        else:
            iterable_frames = range(self.number_of_frames-5)

        for frame_number in iterable_frames:
            _, frame = self.video_in.read()

            for a_tracked_object in self.tracked_objects:
                a_tracked_object.update_tracker(frame)

            self.video_out.write(frame)

        self.video_in.release()
        self.video_out.release()

        if self.verbose:
            self.print_final_report()

        return [a_tracked_obj.get_success_rate()
                for a_tracked_obj in self.tracked_objects]

    def print_final_report(self):
        '''
        Prints tracking final report
        '''
        for a_tracked_object in self.tracked_objects:
            a_tracked_object.print_report()

    def print_if_verbose(self, text):
        '''
        Prints the given text if self.verbose is True
        '''
        if self.verbose:
            print(text)
