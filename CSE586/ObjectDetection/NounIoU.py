import csv
import json
import random

def main():
    with open ('../ActionRecognition/Charades_class_to_object.json') as json_file:
        class_to_object = json.load(json_file)
    with open ('../ActionRecognition/COCO_to_Charades.json') as json_file:
        coco_to_charades = json.load(json_file)
    print(class_to_object)
    print(coco_to_charades)

    obj_preds = {}
    with open('../ActionRecognition/detections_train_no_bb_2.csv') as detections:
        reader = csv.reader(detections)
        vid = 0
        for line in reader:
            vid += 1
            if vid == 1:
                continue
            if line[0] not in obj_preds:
                obj_preds[line[0]] = []
            for i in range(3, len(line)):
                if line[i] not in obj_preds[line[0]]:
                    obj_preds[line[0]].append(line[i])
    '''for x in obj_preds:
        print(x, obj_preds[x])
        to_reduce = obj_preds[x]
        if len(to_reduce) <= 2: continue
        obj_preds[x] = random.sample(to_reduce, 2)
        print(x, obj_preds[x])'''
    ground_truth = {}
    with open('../ActionRecognition/Charades_v1_train.csv') as gt:
        reader = csv.reader(gt)
        vid = 0
        for line in reader:
            vid+=1
            if vid==1:
                continue
            classes = line[-2].split(";")
            l = []
            for c in classes:
                l.append(c.split(" ")[0])
            ground_truth[line[0]] = []
            for c in l:
                if not c: break
                if class_to_object[c] not in ground_truth[line[0]]:
                    ground_truth[line[0]].append(class_to_object[c])

    noun_ious = {}
    print(coco_to_charades)
    for vid in obj_preds:
        if vid not in ground_truth: continue
        p, a = [], []
        unique = []
        both = []
        #print(vid)
        #print("predicted:",end=" ")
        for o in obj_preds[vid]:
            if o in coco_to_charades:
                val = coco_to_charades[o]
                print(val)
                print()
                for v in val:
                    #print(v)
                    if v == 'None': continue
                    p.append(v)
                    if v not in unique:
                        unique.append(v)
                #print(str(coco_to_charades[o])[2:-2],end=", ")
        #print()
        #print("actual:",end=" ")
        for o in ground_truth[vid]:
            if o == 'None': continue
            a.append(o)
            if o in p:
                both.append(o)
            if o not in unique:
                unique.append(o)
            #print(o,end=", ")
        #print()
        #print()
        #  iou equals num in both / num unique
        print(p)
        print(a)
        print(len(both),len(unique), both, unique)
        print()
        if unique:
            noun_ious[vid] = len(both) / len(unique)
    s = 0
    for x in noun_ious:
        s += noun_ious[x]
    print("AVG IOU ", s/len(noun_ious))
    thresh = [0.15, 0.25, 0.30, 0.35, 0.50, 0.60, 0.70]
    total = 0
    thresh_cnt = [0]*7
    for x in noun_ious:
        total += 1
        for t in range(len(thresh)):
            if noun_ious[x] > thresh[t]:
                thresh_cnt[t] += 1
    for t in range(len(thresh_cnt)):
        thresh_cnt[t] /= total
    print("""
    IOU: recall
    """)
    for x in thresh_cnt:
        print(x)

    return s/len(noun_ious)

if __name__ == '__main__':
    s = 0
    for x in range(1):
        s+=main()
    print("AVG IOU ", s/1)
    # 0.11678