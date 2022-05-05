import csv
import json

def main():
    charades_classes = []
    with open ('Charades_class_to_object.json') as json_file:
        class_to_object = json.load(json_file)
    for x in class_to_object:
        if class_to_object[x] not in charades_classes and class_to_object[x]!='None':
            charades_classes.append(class_to_object[x])
    with open ('charades_train_pseudo_supervision_TEP_PS.json') as json_file:
        psvl_dict = json.load(json_file)
    psvl_nouns = {}
    for x in psvl_dict:
        #print(x['vid'],x['tokens'][-5:])
        psvl_nouns[x['vid']] = x['tokens'][-5:]
    print(psvl_nouns)

    ground_truth = {}
    with open('Charades_v1_train.csv') as gt:
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
    for vid in psvl_nouns:
        if vid not in ground_truth: continue
        p, a = [], []
        unique = []
        both = []
        for o in psvl_nouns[vid]:
            if o not in charades_classes: continue
            p.append(o)
            if o not in unique:
                unique.append(o)
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
    print("AVG IOU ", s / len(noun_ious))
    thresh = [0.15, 0.25, 0.30, 0.35, 0.50, 0.60, 0.70]
    total = 0
    thresh_cnt = [0] * 7
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

if __name__ == '__main__':

    main()