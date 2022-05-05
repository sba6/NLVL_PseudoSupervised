import csv
import json
from math import floor

def main():
    temporal_predictions = []
    bad = []
    vids = []

    with open("charades_annotations.json", newline="") as framefile:
        charades_annots = json.load(framefile)

    with open("Charades_results_11_17.csv") as csvfile:
        lines = [line.rstrip() for line in csvfile]
        columns = ['','frame-init', 'frame-end', 'video-frames', 'time-init', 'time-end', 'video-seconds', 'score', 'name']
        with open("Charades_temporal_predictions_updated_4_17.csv", 'w', newline='') as writefile:
            writer = csv.writer(writefile)
            writer.writerow(columns)
            for l in range(1,len(lines)):
                line = lines[l].split(",")
                line[1] = floor(float(line[1]))
                line[2] = floor(float(line[2]))
                line[4] = floor(float(line[4]))
                if float(line[1]) > float(line[2]):
                    bad.append(line)
                    continue
                if float(line[2]) > float(line[4]):
                    line[2] = line[4]
                    if float(line[1])>float(line[2]):
                        bad.append(line)
                        continue
                fps = charades_annots[line[5]]['fps']
                start_seconds = line[1] / fps
                end_seconds = line[2] / fps
                total_seconds = line[4] / fps
                row = [line[0],line[1],line[2],line[4],"{:.2f}".format(start_seconds),
                       "{:.2f}".format(end_seconds),"{:.2f}".format(total_seconds),line[3],line[5]]
                if line[5] not in vids:
                    vids.append(line[5])
                writer.writerow(row)
            print(len(bad)) #315,315 entries
            print(len(vids))

if __name__ == '__main__':
    main()

