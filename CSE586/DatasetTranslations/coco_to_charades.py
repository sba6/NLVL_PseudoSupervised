import csv
import json

def main():
    to_write = []
    with open('COCO_Charades.csv') as csv_file:
        reader = csv.reader(csv_file)
        vids = 0
        convMap = {}
        for line in reader:
            vids+=1
            if vids==1:
                continue
            for x in range(1, len(line)):
                key = ""
                if line[x]:
                    #print(line[x].split(" ")[1:])
                    for t in range(len(line[x].split(" ")[1:])):
                        key+=line[x].split(" ")[1:][t]
                        if t < len(line[x].split(" ")[1:])-1:
                            key+=" "
                    #print(key)
                    if not key: continue
                    if key not in convMap:
                        convMap[key] = []
                    convMap[key].append(line[0][5:])
        print(len(convMap))
        with open('COCO_to_Charades.json', 'w') as json_file:
            json.dump(convMap, json_file)

if __name__ == '__main__':
    #print(calculate_iou((5,10),(5,10)))
    main()