# Ultralytics YOLO 🚀, AGPL-3.0 license

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
    
    
class SpeedEstimator:
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
        self.reg_pts = reg_pts if reg_pts is not None else [(20, 400), (1260, 400)]

        self.names = names  # Classes names

        # Tracking information
        self.trk_history = defaultdict(list)
        self.trk_bot_history = defaultdict(list) # bottom line
        self.view_img = view_img  # bool for displaying inference
        self.tf = line_thickness  # line thickness for annotator
        self.spd = defaultdict(dict)  # set for speed data
        # self.trkd_ids = []  # list for already speed_estimated and tracked ID's
        self.spdl = spdl_dist_thresh  # Speed line distance threshold
        self.trk_pt = {}  # set for tracks previous time
        self.trk_pp = {}  # set for tracks previous point
        self.big_car = defaultdict(dict)
        self.box_width = defaultdict(dict)
        # Check if the environment supports imshow
        self.env_check = False # check_imshow(warn=True)

    def estimate_speed(self, im0, tracks,timestamp,big_car_threhsold=(120,200)):
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
        annotator.draw_region(reg_pts=self.reg_pts, color=(255, 0, 255), thickness=self.tf * 2)
        print("the number of boxes:", len(boxes))
        
        
        
        self.spd[timestamp] = {}
        self.box_width[timestamp] = {}
        self.big_car[timestamp] = {}
        for box, t_id, cls in zip(boxes, t_ids, clss):
            track = self.trk_history[t_id]
            
            track_bot = self.trk_bot_history[t_id]
            
            bbox_center = (float((box[0] + box[2]) / 2), float((box[1] + box[3]) / 2))
            bbox_bottom = (float((box[0] + box[2]) / 2), max(float(box[1]),float(box[3])))
            
            track.append(bbox_center)
            # track_bot.append(bbox_bottom)
            track_bot.append(bbox_bottom)
            if len(track) > 30:
                track.pop(0)
            
            if len(track_bot) > 30:
                track_bot.pop(0)
                
            # trk_pts = np.hstack(track).astype(np.int32).reshape((-1, 1, 2))
            
            trk_bot_pts = np.hstack(track_bot).astype(np.int32).reshape((-1, 1, 2))
            
            if t_id not in self.trk_pt:
                self.trk_pt[t_id] = 0
            
            
                
            
            # Calculation of object speed
            
            if is_point_in_polygon(self.reg_pts, track_bot[-1]):
              direction = "known"
            else:
              direction = "unknown"
              
            if self.trk_pt.get(t_id) != 0 and direction != "unknown":
                
                time_difference = timestamp - self.trk_pt[t_id]
                
                self.spd[timestamp][t_id] = (np.abs(track_bot[-1][1] - self.trk_pp[t_id][1])**2 + np.abs(track_bot[-1][0] - self.trk_pp[t_id][0])**2)**0.5 / time_difference
                # big car
                self.box_width[timestamp][t_id] = np.abs(box[0] - box[2])
                if (np.abs(track_bot[-1][1]-track[-1][1]) >= big_car_threhsold[0] and np.abs(track_bot[-1][1]-track[-1][1]) <= big_car_threhsold[1] ) or cls in ['truck','bus','van']:
                    self.big_car[timestamp][t_id] = 1
                else:
                    self.big_car[timestamp][t_id] = 0
                    
                speed_label = f"{int(self.spd[timestamp][t_id])} v_virtual-{t_id}" if t_id in self.spd[timestamp] else f"{self.names[int(cls)]}-{t_id}"
                bbox_color = colors(int(t_id), True)
    
                annotator.box_label(box, speed_label, bbox_color)
                # cv2.polylines(im0, [trk_pts], isClosed=False, color=bbox_color, thickness=self.tf)
                cv2.polylines(im0, [trk_bot_pts], isClosed=False, color=bbox_color, thickness=self.tf)
                
                # cv2.circle(im0, (int(track[-1][0]), int(track[-1][1])), self.tf * 2, bbox_color, -1)
                cv2.circle(im0, (int(track_bot[-1][0]), int(track_bot[-1][1])), self.tf * 2, bbox_color, -1)
                      
            self.trk_pt[t_id] = timestamp # start_point
            # self.trk_pp[t_id] = track[-1]
            self.trk_pp[t_id] = track_bot[-1]
        if self.view_img and self.env_check:
            cv2.imshow("Ultralytics Speed Estimation", im0)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                return

        return im0


if __name__ == "__main__":
    names = {0: "person", 1: "car"}  # example class names
    speed_estimator = SpeedEstimator(names)
