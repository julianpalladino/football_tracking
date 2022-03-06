import config
import cv2
import utils


class TrackedObject():
    '''
    Class for a single object to track in the video. Allows its tracking
    and annotation over a single frame.

    Parameters
    ----------
    a_bbox_dict: Dictionary taken from the bbox json file which describes this
    object. The dictionary is expected to have the following keys:
        * Name: String. Name of the object to track. i.e 'player'
        * Id: Int. Id of the object to track.
        * Coords: List of 4 ints: x, y, width, height
    a_color: RGB color to annotate this tracked object
    multi_object_tracker: MultiObjectTracker instance which is tracking this
    object
    '''
    def __init__(self, a_bbox_dict, a_color, multi_object_tracker):
        self.multi_object_tracker = multi_object_tracker
        self.name = a_bbox_dict['object']
        self.id = a_bbox_dict['id']
        self.set_bbox(a_bbox_dict)
        self.color = a_color

        if multi_object_tracker.tracking_method == 'medianflow':
            self.tracker = cv2.legacy.TrackerMedianFlow_create()
        elif multi_object_tracker.tracking_method == 'mosse':
            self.tracker = cv2.legacy.TrackerMOSSE_create()
        elif multi_object_tracker.tracking_method == 'boosting':
            self.tracker = cv2.legacy.TrackerBoosting_create()
        elif multi_object_tracker.tracking_method == 'mil':
            self.tracker = cv2.legacy.TrackerMIL_create()
        elif multi_object_tracker.tracking_method == 'csrt':
            self.tracker = cv2.legacy.TrackerCSRT_create()
        elif multi_object_tracker.tracking_method == 'goturn':
            self.tracker = cv2.TrackerGOTURN.create()
        elif multi_object_tracker.tracking_method == 'dasiamrpn':
            self.tracker = cv2.TrackerDaSiamRPN.create()
        elif multi_object_tracker.tracking_method == 'kcf':
            self.tracker = cv2.legacy.TrackerKCF_create()
        elif multi_object_tracker.tracking_method == 'tld':
            self.tracker = cv2.legacy.TrackerTLD_create()
        else:
            raise RuntimeError('Tracker {} not recognized. Options: {}'.format(
                multi_object_tracker.tracking_method, config.TRACKER_METHODS
            ))

    def set_bbox(self, a_bbox_dict):
        '''
        Sets the bbox of the tracked object based on the dictionary retrieved
        from the bbox json file. Validates the bbox and bounds it in case it
        exceeds the frame's resolution.

        Parameters
        ----------
        a_bbox_dict: dictionary, must have 'object' (str), 'id' (int) and
        'coordinates' (list of 4 ints [x, y, width, height] which determine the
        bbox).
        '''
        assert len(a_bbox_dict['object']
                   ) > 0, "Object's name shouldn't be empty"
        assert type(a_bbox_dict['id']) == int, 'Object ID should be an int'
        assert type(a_bbox_dict['coordinates']
                    ) == list, 'Object coordinates should be a list'
        assert all(type(elem) == int for elem in a_bbox_dict['coordinates']), \
            "All elems in object's coordinates should be ints"
        self.bbox = tuple(self.bound_bbox(a_bbox_dict['coordinates']))

    def bound_bbox(self, bbox):
        '''
        Bounds the given bbox according to the frame's resolution.

        Parameters
        ----------
        bbox: tuple of 4 elements (x, y, width, height)

        Returns
        -------
        Tuple of 4 elements bounded by the frame's resolution
        '''
        def bound_value(value, min_bound, max_bound):
            value = min(value, max_bound)
            value = max(value, min_bound)
            return value

        frame_width, frame_height = self.multi_object_tracker.get_frame_dimensions()

        # Limit bbox position
        bbox = [
            bound_value(bbox[0], 0, frame_width),
            bound_value(bbox[1], 0, frame_height),
            bbox[2],
            bbox[3]
        ]

        # Limit bbox dimensions
        bbox = [
            bbox[0],
            bbox[1],
            bound_value(bbox[0] + bbox[2] + 1, 0, frame_width) - bbox[0],
            bound_value(bbox[1] + bbox[3] + 1, 0, frame_height) - bbox[1]
        ]

        return tuple(bbox)

    def initialize_tracker(self, frame):
        '''
        Initializes tracker based on the frame

        Parameters
        ----------
        frame: First frame of the video
        '''
        self.total_frames = 0
        self.successfully_tracked_frames = 0
        self.annotate_frame(frame)
        self.tracker.init(frame, self.bbox)

    def annotate_frame(self, frame):
        '''
        Annotates a frame according to the current value of self.bbox,
        the tracked object's name, id and color

        Paramters
        ---------
        frame: Current video frame to annotate

        Returns
        -------
        The input frame but annotated with the new bbox
        '''
        p1 = (int(self.bbox[0]), int(self.bbox[1]))
        p2 = (int(self.bbox[0] + self.bbox[2]),
              int(self.bbox[1] + self.bbox[3]))
        cv2.rectangle(frame, p1, p2, self.color, 2, 1)
        utils.draw_text(
            frame,
            '{}  #{}'.format(self.name, self.id),
            (self.bbox[0], self.bbox[1]))
        return frame

    def update_tracker(self, frame):
        '''
        Updates tracker value based on a new frame and annotates it.

        Paramters
        ---------
        frame: Current video frame to annotate

        Returns
        -------
        The input frame but annotated with the new bbox
        '''
        success, self.bbox = self.tracker.update(frame)
        self.total_frames += 1

        if success:
            frame = self.annotate_frame(frame)
            self.successfully_tracked_frames += 1
        return frame

    def get_success_rate(self):
        '''
        Calcualtes the tracking success rate of this object.

        Returns
        -------
        A float between 0 and 100 determining the % of successfully
        tracked frames
        '''
        return self.successfully_tracked_frames / self.total_frames * 100

    def print_report(self):
        '''
        Prints tracking report of this object
        '''
        print('Tracked object {} #{} with success rate of {}/{} (%{})'.format(
            self.name, self.id,
            self.successfully_tracked_frames, self.total_frames,
            round(self.successfully_tracked_frames / self.total_frames * 100, 3)))
