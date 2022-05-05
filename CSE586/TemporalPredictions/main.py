import csv
import json

'''
Charades
{id: {"duration_second": length, "duration_frame": 25*duration_length,
"annotations": [{"segment": [start,end], "label": class}], "feature_frame": frames, "dataset": train/val} }
'''

def main():
    code_to_class = {}
    with open("Charades_v1_classes.txt") as classfile:
        lines = [line.rstrip() for line in classfile]
        for l in lines:
            line = l.split(" ")
            code_to_class[line[0]] = " ".join(line[1:])

    with open("charades_frames.json", newline="") as framefile:
        frame_dict = json.load(framefile)

    json_dict= {}
    with open("Charades_v1_train.csv", newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        cnt = 0
        print(cnt)
        for row in reader:
            cnt+=1
            if cnt==1:continue

            mini_dict = {}
            mini_dict["duration_second"] = float(row[10])
            mini_dict["fps"] = int(frame_dict[row[0]]) / mini_dict["duration_second"]
            mini_dict["duration_frame"] = mini_dict["fps"]*float(row[10])
            mini_dict["annotations"] = []
            mini_dict["feature_frame"] = (mini_dict["fps"]-1)*float(row[10])
            mini_dict["dataset"] = "training"

            annots = [x.split(" ") for x in row[9].split(";")]
            for a in annots:
                if len(a)<2: continue
                mini_dict["annotations"].append({"segment":[float(a[1]),float(a[2])], "label":code_to_class[a[0]]})

            json_dict[row[0]] = mini_dict

    with open("Charades_v1_test.csv", newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        cnt = 0
        print(cnt)
        for row in reader:
            cnt += 1
            if cnt == 1: continue

            mini_dict = {}
            mini_dict["duration_second"] = float(row[10])
            mini_dict["fps"] = int(frame_dict[row[0]]) / mini_dict["duration_second"]
            mini_dict["duration_frame"] = mini_dict["fps"] * float(row[10])
            mini_dict["annotations"] = []
            mini_dict["feature_frame"] = (mini_dict["fps"]-1) * float(row[10])
            mini_dict["dataset"] = "validation"

            annots = [x.split(" ") for x in row[9].split(";")]
            for a in annots:
                if len(a) < 2: continue
                mini_dict["annotations"].append({"segment": [float(a[1]), float(a[2])], "label": code_to_class[a[0]]})

            json_dict[row[0]] = mini_dict

    print(json_dict)
    with open('charades_annotations.json', 'w', encoding='utf8') as jsonfile:
        json.dump(json_dict, jsonfile, ensure_ascii=True)


if __name__ == '__main__':
    main()

