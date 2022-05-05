import csv
import json

'''video-name,t-init,t-end,f-init,f-end,video-duration,frame-rate,video-frames,label-idx'''

def main():
    columns = ['video-name','t-init','t-end','f-init','f-end','video-duration','frame-rate','video-frames','label-idx']
    json_path = 'RTD_charades_annotations.json'
    csv_path = 'charades_ground_truth.csv'
    with open(json_path) as json_file:
        json_dict = json.load(json_file)
        with open(csv_path, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(columns)
            for vid in json_dict:
                for annot in json_dict[vid]['annotations']:
                    vid_dict = json_dict[vid]
                    #print(vid_dict)
                    if 'duration_frame' not in vid_dict:
                        print(vid_dict)
                    row = [vid,annot['segment'][0],annot['segment'][1],annot['segment_frame'][0],annot['segment_frame'][1],
                           vid_dict['duration_second'],vid_dict['fps'],vid_dict['duration_frame'],annot['label']]
                    writer.writerow(row)


if __name__ == '__main__':
    main()