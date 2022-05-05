import csv
import json

'''{"video_test_0000004": {"annotations": [{
                "class": "CricketBowling",
                "label": 23,
                "segment": [0.2, 1.1],
                "segment_frame": [6, 33]}],
        "duration_frame": 1012.0,
        "duration_second": 33.73,
        "feature_dim": 202,
        "fps": 30,
        "subset": "test"}}'''

def main():
    code_to_class = {}
    with open("Charades_v1_classes.txt") as classfile:
        lines = [line.rstrip() for line in classfile]
        for l in lines:
            line = l.split(" ")
            code_to_class[line[0]] = " ".join(line[1:])
    json_dict= {}

    with open("charades_frames.json", newline="") as framefile:
        frame_dict = json.load(framefile)

    with open("Charades_v1_train.csv", newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        cnt = 0
        print(cnt)
        for row in reader:
            cnt+=1
            if cnt==1:continue

            mini_dict = {}
            mini_dict["annotations"] = []
            mini_dict["duration_second"] = float(row[10])
            mini_dict["fps"] = int(frame_dict[row[0]]) / mini_dict["duration_second"]
            mini_dict["duration_frame"] = mini_dict["fps"]*float(row[10])
            mini_dict["feature_dim"] = 1
            mini_dict["subset"] = "train"

            annots = [x.split(" ") for x in row[9].split(";")]
            for a in annots:
                if len(a)<2: continue
                mini_dict["annotations"].append({"segment":[float(a[1]),float(a[2])],
                                                 "segment_frame":[float(a[1])*mini_dict["fps"],float(a[2])*mini_dict["fps"]],
                                                 "class":code_to_class[a[0]],
                                                 "label":-2})
            json_dict[row[0]] = mini_dict

    with open("Charades_v1_test.csv", newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        cnt = 0
        print(cnt)
        for row in reader:
            cnt += 1
            if cnt == 1: continue

            mini_dict = {}
            mini_dict["annotations"] = []
            mini_dict["duration_second"] = float(row[10])
            mini_dict["fps"] = int(frame_dict[row[0]]) / mini_dict["duration_second"]
            mini_dict["duration_frame"] = mini_dict["fps"] * float(row[10])
            mini_dict["feature_dim"] = 1
            mini_dict["subset"] = "test"

            annots = [x.split(" ") for x in row[9].split(";")]
            for a in annots:
                if len(a) < 2: continue
                mini_dict["annotations"].append({"segment": [float(a[1]), float(a[2])],
                                                 "segment_frame": [float(a[1]) * mini_dict["fps"], float(a[2]) * mini_dict["fps"]],
                                                 "class": code_to_class[a[0]],
                                                 "label": -2})
            json_dict[row[0]] = mini_dict

    print(json_dict)
    with open('RTD_charades_annotations.json', 'w', encoding='utf8') as jsonfile:
        json.dump(json_dict, jsonfile, ensure_ascii=True)


if __name__ == '__main__':
    main()