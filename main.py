from functools import total_ordering
from sre_constants import SUCCESS
import cv2
import os
import ffmpeg
from pdb import set_trace as st # For debugging
import config
import json
from tqdm import tqdm
from colors import COLORS
import random

def convert_all_data_from_mkv_to_mp4(data_folder):
    print('Converting all files at {} from mkv to mp4'.format(data_folder))
    for path, folder, files in os.walk(data_folder):
        for file in files:
            if file.endswith('.mkv'):
                print("Found file: %s" % file)
                convert_from_mkv_to_mp4(os.path.join(data_folder, file))

def convert_from_mkv_to_mp4(mkv_filepath):
    name, ext = os.path.splitext(mkv_filepath)
    out_name = name + ".mp4"
    ffmpeg.input(mkv_filepath).output(out_name).run()
    print("Finished converting {}".format(mkv_filepath))

class TrackedObject():
    def __init__(self, name, id, coords, color):
        self.name = name
        self.id = id
        self.bbox = tuple(coords)
        print('Using tracker {}'.format(config.TRACKER))
        if config.TRACKER == 'medianflow':
            self.tracker = cv2.TrackerMedianFlow.create()
        elif config.TRACKER == 'mosse':
            self.tracker = cv2.TrackerMOSSE.create()
        elif config.TRACKER == 'boosting':
            self.tracker = cv2.TrackerBoosting.create()
        elif config.TRACKER == 'mil':
            self.tracker = cv2.TrackerMIL.create()
        elif config.TRACKER == 'CSRT':
            self.tracker = cv2.TrackerCSRT.create()
        else:
            raise RuntimeError('Tracker {} not recognized. Options: {}'.format(
                config.POSSIBLE_TRACKERS
            ))
        self.total_frames = 0
        self.successful_tracked_frames = 0
        self.color = color
    
    def initialize_tracker(self, frame):
        if not self.tracker.init(frame, self.bbox):
            raise RuntimeError('Tracker for object {} {} could not initialize'.format(
                self.name, self.id))
    
    def update_tracker(self, frame, frame_number):
        success, bbox = self.tracker.update(frame)
        self.total_frames +=1
        if success:
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(frame, p1, p2, self.color, 2, 1)
            self.successful_tracked_frames += 1
        else:
            if config.VERBOSE:
                print('Could not track at frame #{}'.format(frame_number))
        return frame
    
    def print_report(self):
        print('===== Tracked object {} #{} ===='.format(
            self.name, self.id))
        print('Successful tracked frames: {}/{} (%{})'.format(
            self.successful_tracked_frames, self.total_frames,
            round(self.successful_tracked_frames / self.total_frames * 100, 3)))

def parse_json_to_list(json_filepath):
    '''
    Parses a json of initial conditions into a list of tracked objects.
    The json is expected to be a list of elements with the following attributes:
    * Name: String. Name of the object to track. i.e 'player'
    * Id: Int. Id of the object to track.
    * Coords: List of 4 ints: x, y, width, height
    '''
    with open(json_filepath, 'r') as f:
        list_of_dicts = list(json.load(f))

    list_of_tracked_objects = []
    assert len(list_of_dicts) < len(COLORS), \
        'Insufficient number of colors for the objects to track'

    for a_dict, a_color in zip(list_of_dicts, COLORS):
        assert len(a_dict['object']) > 0, "Object's name shouldn't be empty"
        assert type(a_dict['id']) == int, 'Object ID should be an int'
        assert type(a_dict['coordinates']) == list, 'Object coordinates should be a list'
        assert all(type(elem) == int for elem in a_dict['coordinates']), \
            "All elems in object's coordinates should be ints"
        list_of_tracked_objects.append(
            TrackedObject(
                name = a_dict['object'],
                id = a_dict['id'],
                coords = a_dict['coordinates'],
                color = a_color))
    # TODO: Check that there are no two objects with the same name and id
    return list_of_tracked_objects
            

def main():
    # input_filepath = os.path.join('data', 'messi.mp4')
    # input_bbox_filepath = os.path.join('data', 'messi_initial_conditions.json')
    # input_filepath = os.path.join('data', 'maradona_1986.mp4')
    # input_bbox_filepath = os.path.join('data', 'maradona_1986_initial_conditions.json')
    input_filepath = os.path.join('data', 'messi2.mp4')
    input_bbox_filepath = os.path.join('data', 'messi2_initial_conditions.json')
    # input_filepath = os.path.join('data', 'messi3.mp4')
    # input_bbox_filepath = os.path.join('data', 'messi3_initial_conditions.json')
    tracked_objects = parse_json_to_list(input_bbox_filepath)

    cap = cv2.VideoCapture(input_filepath)
    object_detector = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=40)

    # Create VideoWriter
    frame_width  = cap.get(3)
    frame_height = cap.get(4)
    cap_fps = cap.get(cv2.CAP_PROP_FPS)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('out.mp4', fourcc, cap_fps,(frame_width,frame_height))

    # Initialize trackers
    ret, init_frame = cap.read()
    bbox = [711,
            311,
            80,
            210]
    p1 = (int(bbox[0]), int(bbox[1]))
    p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
    cv2.rectangle(init_frame, p1, p2, (255,0,0), 2, 1)
    cv2.imwrite('init_frame.png', init_frame)
    number_of_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    for a_tracked_object in tracked_objects:
        a_tracked_object.initialize_tracker(init_frame)

    for frame_number in tqdm(range(number_of_frames)):
        ret, frame = cap.read()
        mask = object_detector.apply(frame)

        for a_tracked_object in tracked_objects:
            a_tracked_object.update_tracker(frame, frame_number)
        
        out.write(frame)
        
    cap.release()
    out.release()

    print_final_report(tracked_objects)

def print_final_report(tracked_objects):
    for a_tracked_object in tracked_objects:
        a_tracked_object.print_report()

if __name__ == '__main__':
    # convert_all_data_from_mkv_to_mp4('data')
    main()