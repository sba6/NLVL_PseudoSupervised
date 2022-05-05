import csv
import json

def main():
    class_to_object = {}
    with open('Charades_v1_mapping.txt') as csv_file:
        reader = csv.reader(csv_file)
        for line in reader:
            l = str(line)[2:-2].split(" ")
            class_to_object[l[0]] = l[1]
    #print(class_to_object)
    c20 = {}
    with open("Charades_v1_objectclasses.txt") as csv_file:
        reader = csv.reader(csv_file)
        for line in reader:
            l = str(line)[2:-2].split(" ")
            c20[l[0]] = l[1]
    #print(c20)
    res = {}
    for x in class_to_object:
        for y in c20:
            if class_to_object[x] == y:
                res[x] = c20[y]
    for x in res:
        print(x, res[x])
    with open('Charades_class_to_object.json', 'w') as json_file:
        json.dump(res, json_file)
if __name__ == '__main__':
    #print(calculate_iou((5,10),(5,10)))
    main()