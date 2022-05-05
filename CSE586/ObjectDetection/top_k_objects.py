import csv
from heapq import *

def find_min_distances(target_box, values, k):
    target_x_mid = (target_box[2]+target_box[0])/2
    target_y_mid = (target_box[3]+target_box[1])/2
    closest = []
    for val in range(len(values)):
        v_x = (values[val][2]+values[val][0])/2
        v_y = (values[val][3]+values[val][1])/2
        distance = ((v_x-target_x_mid)**2 + (v_y-target_y_mid)**2)**0.5
        heappush(closest, (distance, val))
    indices = []
    while k>0 and closest:
        k-=1
        popped = heappop(closest)
        indices.append(popped[1])
    return indices

def main():
    k = 10 # objects other than person
    to_write = []
    with open('../ActionRecognition/detections_train.csv') as csv_file:
        reader = csv.reader(csv_file)
        vids = 0
        for line in reader:
            if vids == 0:
                vids += 1
                continue
            video_name = line[0]
            # len(line) = 2 + 5 * num_objects
            objects, boxes = [], []
            for x in range(2, len(line), 5):
                #only take first person object found
                if ('person' in objects and line[x] == 'person') or (line[x] in objects): continue
                objects.append(line[x])
                boxes.append((int(line[x+1]), int(line[x+2]), int(line[x+3]), int(line[x+4])))
            if 'person' not in objects: continue #only keep if has a person
            person_index = -1
            for x in range(len(objects)):
                if objects[x] == 'person':
                    person_index = x
                    break
            person_box = boxes[person_index]
            values = objects[:person_index] + objects[person_index+1:]
            value_boxes = boxes[:person_index] + boxes[person_index+1:]
            if not value_boxes: continue
            top_values = find_min_distances(person_box, value_boxes, k)
            # print(values, value_boxes, video_name)
            # print(top_values, person_box)
            writel = line[:2]
            writel.append('person')
            for x in person_box:
                writel.append(x)
            for x in range(len(top_values)):
                writel.append(values[top_values[x]])
                for y in range(4):
                    writel.append(value_boxes[top_values[x]][y])
            to_write.append(writel)
    with open('../ActionRecognition/detections_train_10.csv', 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        columns = ['name', 'frame',
                   'object1', 'xmin1', 'ymin1', 'xmax1', 'ymax1',
                   'object2', 'xmin2', 'ymin2', 'xmax2', 'ymax2',
                   'object3', 'xmin3', 'ymin3', 'xmax3', 'ymax3']
        writer.writerow(columns)
        for line in to_write:
            print(line)
            writer.writerow(line)

if __name__ == '__main__':
    #print(calculate_iou((5,10),(5,10)))
    main()