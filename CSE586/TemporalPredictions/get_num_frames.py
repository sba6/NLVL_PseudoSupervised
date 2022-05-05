#make json for number of frames in each Charades video
import os
import json
import subprocess
from subprocess import check_output

def main():
    directory = "Charades_v1_480"
    json_path = "charades_frames.json"
    json_dict = {}
    for vid_file in os.listdir(directory):
        cmd = 'ffprobe -v error -select_streams v:0 -count_packets -show_entries ' \
              'stream=nb_read_packets -of csv=p=0 \"{}/{}\"'.format(directory,vid_file)
        frames = check_output(cmd, shell=True)
        frames = str(frames)[2:-3]
        json_dict[vid_file[:-4]] = frames
        print(vid_file, len(json_dict))
    with open(json_path, 'w', encoding='utf8') as json_file:
        json.dump(json_dict, json_file)

if __name__ == '__main__':
    main()
