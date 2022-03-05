import config
import cv2

class TrackedObject():
    def __init__(self, a_bbox_dict, a_color):
        self.name = a_bbox_dict['object']
        self.id = a_bbox_dict['id']
        self.bbox = tuple(a_bbox_dict['coordinates'])
        self.color = a_color
        
        print('Using tracker {}'.format(config.TRACKER_METHOD))
        if config.TRACKER_METHOD == 'medianflow':
            self.tracker = cv2.legacy.TrackerMedianFlow_create()
        elif config.TRACKER_METHOD == 'mosse':
            self.tracker = cv2.legacy.TrackerMOSSE_create()
        elif config.TRACKER_METHOD == 'boosting':
            self.tracker = cv2.legacy.TrackerBoosting_create()
        elif config.TRACKER_METHOD == 'mil':
            self.tracker = cv2.legacy.TrackerMIL_create()
        elif config.TRACKER_METHOD == 'csrt':
            self.tracker = cv2.legacy.TrackerCSRT_create()
        elif config.TRACKER_METHOD == 'goturn':
            self.tracker = cv2.TrackerGOTURN.create()
        elif config.TRACKER_METHOD == 'dasiamrpn':
            self.tracker = cv2.TrackerDaSiamRPN.create()
        elif config.TRACKER_METHOD == 'kcf':
            self.tracker = cv2.legacy.TrackerKCF_create()
        elif config.TRACKER_METHOD == 'tld':
            self.tracker = cv2.legacy.TrackerTLD_create()
        else:
            raise RuntimeError('Tracker {} not recognized. Options: {}'.format(
                config.TRACKER_METHOD, config.POSSIBLE_TRACKERS
            ))
        self.total_frames = 0
        self.successful_tracked_frames = 0
    
    def validate_bbox(self, a_bbox_dict):
        assert len(a_bbox_dict['object']) > 0, "Object's name shouldn't be empty"
        assert type(a_bbox_dict['id']) == int, 'Object ID should be an int'
        assert type(a_bbox_dict['coordinates']) == list, 'Object coordinates should be a list'
        assert all(type(elem) == int for elem in a_bbox_dict['coordinates']), \
            "All elems in object's coordinates should be ints"

    def initialize_tracker(self, frame):
        self.tracker.init(frame, self.bbox)
    
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
        print('Successfully tracked frames: {}/{} (%{})'.format(
            self.successful_tracked_frames, self.total_frames,
            round(self.successful_tracked_frames / self.total_frames * 100, 3)))