import csv
from heapq import *

def main():
    to_write = []
    with open('../ActionRecognition/detections_train_10.csv') as csv_file:
        reader = csv.reader(csv_file)
        vids = 0
        for line in reader:
            if vids == 0:
                vids += 1
                continue
            # len(line) = 2 + 5 * num_objects
            objects = []
            for x in range(2, len(line), 5):
                objects.append(line[x])
            writel = line[:2]
            for x in range(len(objects)):
                writel.append(objects[x])
            to_write.append(writel)
    with open('../ActionRecognition/detections_train_no_bb_10.csv', 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        columns = ['name', 'frame', 'object1', 'object2', 'object3']
        writer.writerow(columns)
        for line in to_write:
            print(line)
            writer.writerow(line)

if __name__ == '__main__':
    #print(calculate_iou((5,10),(5,10)))
    main()