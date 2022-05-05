# read verbs from Zero-shot NLVL's input
import json
import csv
file = open('charades_train_pseudo_supervision_TEP_PS.json')
data = json.load(file)
file.close()
with open('verbs_psvl.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for row in data:
        a = [row['vid']]
        a.extend(row['tokens'][0:3])
        csvwriter.writerow(a)