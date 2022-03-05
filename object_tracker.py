import os
from tracked_object import TrackedObject
import json
from colors import COLORS
import cv2
from tqdm import tqdm

class MultiObjectTracker():
    def __init__(self, input_filepath, input_bbox_json_filepath, output_filepath, verbose=False):
        self.verbose = verbose
        assert input_filepath[-3:] == 'mp4', 'Only mp4 format is accepted'
        os.makedirs(output_filepath, exist_ok=True)
        self.tracked_objects = self.parse_hbox_json(input_bbox_json_filepath)
        self.video_in = cv2.VideoCapture(input_filepath)

        # Create VideoWriter for output
        frame_width  = self.video_in.get(3)
        frame_height = self.video_in.get(4)
        cap_fps = self.video_in.get(cv2.CAP_PROP_FPS)
        frame_width = int(self.video_in.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(self.video_in.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.video_out = cv2.VideoWriter('out.mp4', fourcc, cap_fps,(frame_width,frame_height))

        # Initialize trackers
        _, init_frame = self.video_in.read()
        self.number_of_frames = int(self.video_in.get(cv2.CAP_PROP_FRAME_COUNT))
        for a_tracked_object in self.tracked_objects:
            a_tracked_object.initialize_tracker(init_frame)

    def parse_hbox_json(self, input_bbox_json_filepath):
        '''
        Parses a json of initial conditions into a list of tracked objects.
        The json is expected to be a list of elements with the following attributes:
        * Name: String. Name of the object to track. i.e 'player'
        * Id: Int. Id of the object to track.
        * Coords: List of 4 ints: x, y, width, height
        '''
        with open(input_bbox_json_filepath, 'r') as f:
            list_of_dicts = list(json.load(f))

        list_of_tracked_objects = []
        assert len(list_of_dicts) < len(COLORS), \
            'Insufficient number of colors for the objects to track'

        for a_bbox_dict, a_color in zip(list_of_dicts, COLORS):
            list_of_tracked_objects.append(TrackedObject(a_bbox_dict, a_color))
        # TODO: Check that there are no two objects with the same name and id
        return list_of_tracked_objects
    
    def run_tracking(self):
        if self.verbose:
            iterable_frames = tqdm(range(self.number_of_frames-5))
        else:
            iterable_frames = range(self.number_of_frames-5)

        for frame_number in iterable_frames:
            _, frame = self.video_in.read()

            for a_tracked_object in self.tracked_objects:
                a_tracked_object.update_tracker(frame, frame_number)
            
            self.video_out.write(frame)
                
        self.video_in.release()
        self.video_out.release()

        if self.verbose:
            self.print_final_report()

    def print_final_report(self, tracked_objects):
        for a_tracked_object in tracked_objects:
            a_tracked_object.print_report()