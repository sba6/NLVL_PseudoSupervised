import csv
import json
from math import floor
from heapq import *

def main():
    temporal_predictions = []
    bad = []
    vids = []

    with open("charades_annotations.json", newline="") as framefile:
        charades_annots = json.load(framefile)

    with open("Charades_temporal_predictions.csv") as csvfile:
        lines = [line.rstrip() for line in csvfile]
        columns = ['','frame-init', 'frame-end', 'video-frames', 'time-init', 'time-end', 'video-seconds', 'score', 'name']
        with open("Charades_top_3.csv", 'w', newline='') as writefile:
            writer = csv.writer(writefile)
            writer.writerow(columns)
            max_scores = []
            curr_vid = ""
            for l in range(1,len(lines)):
                line = lines[l].split(",")
                if line[8] not in vids:
                    vids.append(line[8])
                if curr_vid == "":
                    curr_vid = line[8]
                elif curr_vid == line[8]:
                    heappush(max_scores, [-float(line[7]), line])
                else:
                    #write top k rows,
                    #clear out vids and append current to max_scores
                    k = 3
                    while k>0 and max_scores:
                        k-=1
                        r = heappop(max_scores)
                        writer.writerow(r[1])
                    max_scores = []
                    heappush(max_scores, [-float(line[7]), line])
                    curr_vid = line[8]

            print(len(bad)) #315,315 entries
            print(len(vids))

if __name__ == '__main__':
    main()

