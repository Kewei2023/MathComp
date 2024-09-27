# Ultralytics YOLO 馃殌, AGPL-3.0 license

from collections import defaultdict
from time import time

import cv2
import numpy as np

from ultralytics.utils.checks import check_imshow
from ultralytics.utils.plotting import Annotator, colors

import matplotlib.path as mpath

def is_point_in_polygon(polygon, point):
    
    
    path = mpath.Path(polygon)
    
    
    return path.contains_point(point)
    
    
class LaneChange:
    """A class to estimate the speed of objects in a real-time video stream based on their tracks."""

    def __init__(self, names, reg_pts=None, view_img=False, line_thickness=2, spdl_dist_thresh=10):
        """
        Initializes the SpeedEstimator with the given parameters.

        Args:
            names (dict): Dictionary of class names.
            reg_pts (list, optional): List of region points for speed estimation. Defaults to [(20, 400), (1260, 400)].
            view_img (bool, optional): Whether to display the image with annotations. Defaults to False.
            line_thickness (int, optional): Thickness of the lines for drawing boxes and tracks. Defaults to 2.
            spdl_dist_thresh (int, optional): Distance threshold for speed calculation. Defaults to 10.
        """
        # Region information
        self.reg_pts = reg_pts if reg_pts is not None else {'row1': [(20, 400), (1260, 400)]} # dictionary

        self.names = names  # Classes names

        # Tracking information
        self.trk_history = defaultdict(list)
        self.trk_bot_history = defaultdict(list) # bottom line
        self.view_img = view_img  # bool for displaying inference
        self.tf = line_thickness  # line thickness for annotator
        self.spd = {}  # set for speed data
        self.trkd_ids = []  # list for already speed_estimated and tracked ID's
        self.spdl = spdl_dist_thresh  # Speed line distance threshold
        self.trk_pt = {}  # set for tracks previous time
        self.trk_pp = {}  # set for tracks previous point
        self.big_car = {}
        self.lane_change_info = defaultdict(dict)
        # Check if the environment supports imshow
        self.env_check = False # check_imshow(warn=True)

    def detect_change(self, im0, tracks,timestamp,big_car_threhsold=(120,200)):
        """
        Estimates the speed of objects based on tracking data.

        Args:
            im0 (ndarray): Image.
            tracks (list): List of tracks obtained from the object tracking process.

        Returns:
            (ndarray): The image with annotated boxes and tracks.
        """
        if tracks[0].boxes.id is None:
            return im0

        boxes = tracks[0].boxes.xyxy.cpu()
        clss = tracks[0].boxes.cls.cpu().tolist()
        t_ids = tracks[0].boxes.id.int().cpu().tolist()
        annotator = Annotator(im0, line_width=self.tf)
        
        for row_name in self.reg_pts: # dictionary
          annotator.draw_region(reg_pts=self.reg_pts[row_name], color=(255, 0, 255), thickness=self.tf * 2)
        
        self.lane_change_info[timestamp] = {}
        for box, t_id, cls in zip(boxes, t_ids, clss):
            # track = self.trk_history[t_id]
            
            track_bot = self.trk_bot_history[t_id]
            
            bbox_center = (float((box[0] + box[2]) / 2), float((box[1] + box[3]) / 2))
            bbox_bottom = (float((box[0] + box[2]) / 2), max(float(box[1]),float(box[3])))
            
            # track.append(bbox_center)
            track_bot.append(bbox_bottom)
            
            # if len(track) > 30:
            #     track.pop(0)
            
            if len(track_bot) > 30:
                track_bot.pop(0)
                
            # trk_pts = np.hstack(track).astype(np.int32).reshape((-1, 1, 2))
            
            trk_bot_pts = np.hstack(track_bot).astype(np.int32).reshape((-1, 1, 2))
            
            # if t_id not in self.trk_pt:
            #     self.trk_pt[t_id] = 0
            
            
                
            
            # Justify lane change
            flag = []
            
            for row_name in self.reg_pts:
              
              if is_point_in_polygon(self.reg_pts[row_name], track_bot[-1]):
                
                flag.append(row_name)
            
            if len(flag) > 2:
              
              self.lane_change_info[timestamp][t_id] = f"both occur in {','.join(flag)}"
            elif len(flag) == 1:
              self.lane_change_info[timestamp][t_id] = flag[0]
            else:
              self.lane_change_info[timestamp][t_id] = 'lose track'
            
            
            speed_label = f"{self.lane_change_info[timestamp][t_id]}-{t_id}" if self.lane_change_info[timestamp][t_id] != 'lose track' else f"{self.names[int(cls)]}-{t_id}"
            bbox_color = colors(int(t_id), True)

            annotator.box_label(box, speed_label, bbox_color)
            # cv2.polylines(im0, [trk_pts], isClosed=False, color=bbox_color, thickness=self.tf)
            cv2.polylines(im0, [trk_bot_pts], isClosed=False, color=bbox_color, thickness=self.tf)
            
            # cv2.circle(im0, (int(track[-1][0]), int(track[-1][1])), self.tf * 2, bbox_color, -1)
            cv2.circle(im0, (int(track_bot[-1][0]), int(track_bot[-1][1])), self.tf * 2, bbox_color, -1)
            
            
            self.trk_pt[t_id] = time()
            # self.trk_pp[t_id] = track[-1]
            self.trk_pp[t_id] = track_bot[-1]
        

        return im0


if __name__ == "__main__":
    names = {0: "person", 1: "car"}  # example class names
    speed_estimator = SpeedEstimator(names)
