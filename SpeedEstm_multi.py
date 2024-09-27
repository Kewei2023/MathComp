import cv2
import numpy as np
import pandas as pd
from ultralytics import YOLO
from speed_estimation import SpeedEstimator
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
  
  
def process_video(video_path, ip_dir, root, mp4_file, savedir, model, line_pts_dict):
    
    speed_dict = {}
    cap = cv2.VideoCapture(video_path)
    w, h, fps = (int(cap.get(x)) for x in (
    cv2.CAP_PROP_FRAME_WIDTH, 
    cv2.CAP_PROP_FRAME_HEIGHT, 
    cv2.CAP_PROP_FPS))
    
    for row_name in line_pts_dict:
  
      print("*"*60)
      print(f"calculating the {row_name}")
      print("*"*60)
     
      video_writer = cv2.VideoWriter(
      os.path.join(savedir,ip_dir,f'{mp4_file.replace("mp4","")}-speed_estimation_{row_name}.avi'),
      cv2.VideoWriter_fourcc(*"mp4v"),
      fps, (w, h))
      
      line_pts = line_pts_dict[row_name]#[(0, 360), (1280, 360)]
      
      speed_dict[row_name] = {'time(s)':[],'all_speed':[],'all_box_width':[],'big_car_speed':[], 'all_count':[], 'big_car_count':[],'big_car_box_width':[]}
      
      # line_pts = [(120, 200), (420, 200)]  first row
      # line_pts = [(120, 300), (560, 300)]  center row
      # line_pts = [(420, 400), (640, 400)]  argent row
      print("*"*60)
      print("initializing the speed estimator")
      print("*"*60)
      speed_obj = SpeedEstimator(reg_pts=line_pts,
                                            names=names,
                                            view_img=False, # True,
                                            spdl_dist_thresh=5)
                                            
      frame_count = 0    
      
      previous_spd = {}
      # previous_count = []     
      previous_width = {}   
      
      previous_big_car_spd = {}
      # previous_big_car_count = []  
      previous_big_car_width = {}      
      
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
      
        im0 = speed_obj.estimate_speed( im0, 
                                        tracks,
                                        timestamp = timestamp
                                        )
        
        print("*"*60)
        print(f"Writing to output")
        print("*"*60)
        
        video_writer.write(im0)
        
        
        
        speed_dict[row_name]['time(s)'].append(timestamp)
        
        
        
        
        if len(speed_obj.spd[timestamp]) == 0:
          speed_dict[row_name]['all_speed'].append(0)
          speed_dict[row_name]['all_count'].append(0)
          speed_dict[row_name]['big_car_speed'].append(0)
          speed_dict[row_name]['big_car_count'].append(0)
          speed_dict[row_name]['all_box_width'].append(0)
          speed_dict[row_name]['big_car_box_width'].append(0)
          
        else:
          
          current_spd = sum(speed_obj.spd[timestamp].values())/len(speed_obj.spd[timestamp])
          current_width = sum(speed_obj.box_width[timestamp].values()).item()/len(speed_obj.box_width[timestamp])
        
          print("speed is: ",current_spd)
          
          speed_dict[row_name]['all_speed'].append(current_spd)
          speed_dict[row_name]['all_box_width'].append(current_width)
          speed_dict[row_name]['all_count'].append(len(speed_obj.spd[timestamp]))
          # ipdb.set_trace()
          
          # update big car speed
          is_big_car = speed_obj.big_car[timestamp] # is big car or not dict
          current_big_car_spd  = {idx:spd for (idx,is_big), (idx_,spd) in zip(is_big_car.items(),speed_obj.spd[timestamp].items()) if idx == idx_ and is_big == 1 }
          
          if len(current_big_car_spd) > 0:
            speed_dict[row_name]['big_car_speed'].append(sum(current_big_car_spd.values())/len(current_big_car_spd))
          else:
            speed_dict[row_name]['big_car_speed'].append(0)
            
          speed_dict[row_name]['big_car_count'].append(len(current_big_car_spd))
          
          
          # big_box_width
          
          current_big_car_width  = {idx:spd for (idx,is_big), (idx_,spd) in zip(is_big_car.items(),speed_obj.box_width[timestamp].items()) if idx == idx_ and is_big == 1 }
         
          if len(current_big_car_width) > 0:
            speed_dict[row_name]['big_car_box_width'].append(sum(current_big_car_width.values()).item()/len(current_big_car_width))
          else:
            speed_dict[row_name]['big_car_box_width'].append(0)
          
        frame_count += 1
        # debug
        # if frame_count > 200:
           # break
            
      cap.release()
      video_writer.release()
      cv2.destroyAllWindows()
      
      print("*"*60)
      print(f"Save to output")
      print("*"*60)
        
      df = pd.DataFrame(speed_dict[row_name])
      df.set_index('time(s)', inplace=True)
      df.to_csv(os.path.join(savedir,ip_dir,f'{mp4_file.replace("mp4","")}-{row_name}.csv'))

      print("*"*60)
      print(f"processing the {video_path} DONE")
      print("*"*60)
    

   
if __name__ == '__main__':
    root = './data'
    savedir = "./processed-speed-multi2"
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
        
        if ip_dir == '32.31.250.105': continue
        line_pts_dict = load_polygon(os.path.join(root, ip_dir, f"{ip_dir}-speed_estm.json"))
        
        for mp4_file in os.listdir(os.path.join(root, ip_dir)):
            if 'mp4' not in mp4_file:
                continue
            video_path = os.path.join(root, ip_dir, mp4_file)
            task = (video_path, ip_dir, root, mp4_file, savedir, model, line_pts_dict)
            tasks.append(task)
    
    # 
    pool.starmap(process_video, tasks)
    
    # 
    pool.close()
    pool.join()
