import cv2
import numpy as np
import pandas as pd
from ultralytics import YOLO,solutions
from lane_change import LaneChange
import os
import ipdb
import json
import multiprocessing

def load_polygon(json_file):
  
  line_pts_dict = {}
  with open(json_file, 'r') as file:
    
    data = json.load(file)
    
    regions = data['shapes'] 
    
    for areas in regions:
      line_pts_dict[areas['label']] = [(round(x),round(y)) for (x,y) in areas['points']]
  return line_pts_dict
  


# def detect_change(self, im0, tracks,big_car_threhsold=(120,200),time):


def process_video(video_path, ip_dir, root, mp4_file, savedir, model, line_pts_dict):
    
    
    cap = cv2.VideoCapture(video_path)
    w, h, fps = (int(cap.get(x)) for x in (
    cv2.CAP_PROP_FRAME_WIDTH, 
    cv2.CAP_PROP_FRAME_HEIGHT, 
    cv2.CAP_PROP_FPS))
    print('video path:',video_path)
    print('fps is:', fps)
    exit()
    video_writer = cv2.VideoWriter(
    os.path.join(savedir,ip_dir,f'{mp4_file.replace("mp4","")}-lane_change.avi'),
    cv2.VideoWriter_fourcc(*"mp4v"),
    fps, (w, h))
    
    
    # line_pts = [(120, 200), (420, 200)]  first row
    # line_pts = [(120, 300), (560, 300)]  center row
    # line_pts = [(420, 400), (640, 400)]  argent row
    print("*"*60)
    print("initializing the speed estimator")
    print("*"*60)
    lane_obj = LaneChange(reg_pts=line_pts_dict,
                          names=names,
                          view_img=False, # True,
                          spdl_dist_thresh=5)
                                          
    frame_count = 0    
      
    
    while cap.isOpened():
      success, im0 = cap.read()
      if not success:        
        break
      
      
      timestamp = frame_count / fps
      
      print("*"*60)
      print(f"Tracking")
      print("*"*60)
      
      tracks = model.track(im0, persist=True, show=False)
      
      print("*"*60)
      print(f"Calculate speed")
      print("*"*60)
    
      im0 = lane_obj.detect_change( im0, 
                                    tracks,
                                    timestamp = timestamp
                                    )
      
      print("*"*60)
      print(f"Writing to output")
      print("*"*60)
      
      video_writer.write(im0)
      
      
      
      
        
      frame_count += 1
      # debug
      # if frame_count > 5:
         # break
          
    cap.release()
    video_writer.release()
    cv2.destroyAllWindows()
    
    
    lane_track_info = lane_obj.lane_change_info
    
    print("*"*60)
    print(f"Save to output")
    print("*"*60)
      
    # lane_track_info_inv = {idx: [time[idx] for idx in time] for time in lane_track_info.keys()}
    print(f"track_info:\n{lane_track_info}")
    
    df = pd.DataFrame.from_dict(lane_track_info,orient='index')
    
    df.to_csv(os.path.join(savedir,ip_dir,f'{mp4_file.replace("mp4","")}-lane_change.csv'))

    print("*"*60)
    print(f"processing the {video_path} DONE")
    print("*"*60)
  

   
if __name__ == '__main__':
    root = './data'
    savedir = "./processed-lane-multi2-debug"
    os.makedirs(savedir, exist_ok=True)
    
    model = YOLO("yolov8n.pt")
    names = model.model.names
    
    # 
    pool = multiprocessing.Pool(processes=os.cpu_count())  # 
    
    # 
    tasks = []
    for ip_dir in os.listdir(root):
        if not os.path.isdir(os.path.join(root, ip_dir)):
            continue
        os.makedirs(os.path.join(savedir, ip_dir), exist_ok=True)
        
        # if ip_dir != "32.31.250.107": continue
        
        line_pts_dict = load_polygon(os.path.join(root, ip_dir, f"{ip_dir}-lane_change.json"))
        
        for mp4_file in os.listdir(os.path.join(root, ip_dir)):
            if 'mp4' not in mp4_file:
                continue
            # if mp4_file != "20240501_20240501125647_20240501140806_125649.mp4": continue
            
            video_path = os.path.join(root, ip_dir, mp4_file)
            task = (video_path, ip_dir, root, mp4_file, savedir, model, line_pts_dict)
            tasks.append(task)
    
    # 
    pool.starmap(process_video, tasks)
    
    # 
    pool.close()
    pool.join()
