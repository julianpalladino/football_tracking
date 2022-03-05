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
from tracked_object import TrackedObject
from object_tracker import MultiObjectTracker
           

def main():
    # input_filepath = os.path.join('data', 'messi.mp4')
    # input_bbox_json_filepath = os.path.join('data', 'messi1_initial_conditions.json')
    # input_filepath = os.path.join('data', 'maradona_1986.mp4')
    # input_bbox_json_filepath = os.path.join('data', 'maradona_1986_initial_conditions.json')
    input_filepath = os.path.join('data', 'messi2.mp4')
    input_bbox_json_filepath = os.path.join('data', 'messi2_initial_conditions.json')
    # input_filepath = os.path.join('data', 'messi3.mp4')
    # input_bbox_json_filepath = os.path.join('data', 'messi3_initial_conditions.json')

    object_tracker = MultiObjectTracker(input_filepath, input_bbox_json_filepath, 'output/out.mp4')
    object_tracker.run_tracking()


if __name__ == '__main__':
    # convert_all_data_from_mkv_to_mp4('data')
    main()