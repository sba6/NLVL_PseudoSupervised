# read verbs from Charades ground truth
import csv
file = open("Charades_v1_train.csv")
csvreader = csv.reader(file)
header = next(csvreader)
a = []
for row in csvreader:
    b = [row[0]]
    tmp = row[9]
    for i in range(0,len(tmp)):
        if tmp[i] == 'c':
            b.append(tmp[i:i+4])
    a.append(b)
file.close()

file = open("Charades_v1_test.csv")
csvreader = csv.reader(file)
header = next(csvreader)
for row in csvreader:
    b = [row[0]]
    tmp = row[9]
    for i in range(0,len(tmp)):
        if tmp[i] == 'c':
            b.append(tmp[i:i+4])
    a.append(b)
file.close()

file = open("mapping.csv")
csvreader = csv.reader(file)
for row in csvreader:
    for i in range(0,len(a)):
        tmp = a[i]
        for j in range(0,len(tmp)):
            if a[i][j] == row[0]:
                a[i][j] = row[1]
with open('verbs_gt.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for row in a:
        csvwriter.writerow(row)