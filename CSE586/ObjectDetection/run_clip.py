import json
import subprocess
import os
import argparse
import csv

parser = argparse.ArgumentParser()
parser.add_argument('--output', default = "detections", help='output csv file')
opt = parser.parse_args()
print(opt)

with open("../RTD-Action/BSN2/data/charades_annotations/charades_annotations.json") as json_file:
  annotations = json.load(json_file)

train_videos = []
with open("../ActionRecognition/Charades_v1_train.csv") as csv_file:
    reader = csv.reader(csv_file)
    for x in reader:
        print(x[0])
        if x[0] not in train_videos:
            train_videos.append(x[0])

charades_path = "../dataset/Charades_480/"
for video_path in os.listdir(charades_path):
  video_name = video_path.split("/")[-1][:-4]
  if video_name not in train_videos:
      continue
  path = charades_path+video_name+'.mp4'
  fps = str(int(annotations[video_name]["duration_frame"] // annotations[video_name]["duration_second"]))
  print(annotations[video_name]["duration_frame"], annotations[video_name]["duration_second"])
  print(path, fps)
  p = subprocess.call(['python', 'clip_object_tracker.py', '--weights', 'models/yolov5s.pt', \
                    '--detection-engine', 'yolov5','--source', path,\
                    '--frame-rate', fps, '--detection-output', opt.output])
  # while p.poll() is None:
  #   print(p.stdout.readline()[2:])
  # print(p.stdout.read())