import os
import csv
import json

def main():
    columns = ['video','numFrame','seconds','fps','rfps','subset','featureFrame']
    print(columns)
    json_file_path = "charades_annotations.json"
    with open(json_file_path) as json_file:
        json_file = json.load(json_file)
        #print(json_file)
        video_names = json_file.keys()
        csv_file_path = "charades_video_info.csv"
        #print(csv_file_path)
        with open(csv_file_path,'w',newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(columns)
            for video in video_names:
                frames = json_file[video]['duration_frame']
                seconds = json_file[video]['duration_second']
                feature_frames = json_file[video]['feature_frame']
                fps =  json_file[video]['fps']
                train_val = json_file[video]['dataset']
                row = [video, frames, seconds, fps, fps, train_val, feature_frames]
                writer.writerow(row)

if __name__ == '__main__':
    main()