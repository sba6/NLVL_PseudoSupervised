import csv

# read verbs for 2 closest objects
file = open('verbs_2.csv')
csvreader = csv.reader(file)
first_line = next(csvreader)
del first_line[1]
verbs_mlm = [first_line]
i = 0
for row in csvreader:
    tmp = verbs_mlm[i]
    if row[0] in tmp:
        for j in range(2,len(row)):
            if row[j] not in tmp:
                tmp.append(row[j])
        verbs_mlm[-1] = tmp
    else:
        del row[1]
        verbs_mlm.append(row) 
        i += 1
file.close()

# read ground truth verbs
file = open('verb_list.csv')
csvreader = csv.reader(file)
first_line = next(csvreader)
rel = []
for row in csvreader:
    rel.append(row)
file.close()
file = open('verbs_gt.csv')
csvreader = csv.reader(file)
first_line = next(csvreader)
verbs_gt = [first_line]
i = 0
for row in csvreader:
    tmp = verbs_gt[i]
    if row[0] in tmp:
        for j in range(1,len(row)):
            if row[j] not in tmp:
                tmp.append(row[j])
        verbs_gt[-1] = tmp
    else:
        verbs_gt.append(row) 
        i += 1
file.close()
verbs_gt_1 = []
for row in verbs_gt:
    for line in verbs_mlm:
        if row[0] in line:
            verbs_gt_1.append(row)
            break
    if len(verbs_gt_1)>0:
        tmp = verbs_gt_1[-1]
        tmp_1 = [tmp[0]]
        for i in range(1,len(tmp)):
            if tmp[i] not in tmp_1:
                tmp_1.append(tmp[i])
        verbs_gt_1[-1] = tmp_1
verbs_gt_2 = []
for row in verbs_gt_1:
    tmp = [row[0]]
    for i in range(1,len(row)):
        for j in range(len(rel)):
            if row[i] in rel[j]:
                tmp.extend(rel[j][1:])
                break
    verbs_gt_2.append(tmp)
    if len(verbs_gt_2)>0:
        tmp_2 = verbs_gt_2[-1]
        tmp_1 = [tmp_2[0]]
        for i in range(1,len(tmp_2)):
            if tmp_2[i] not in tmp_1:
                tmp_1.append(tmp_2[i])
        verbs_gt_2[-1] = tmp_1

# read VerbBERT generated verbs
file = open('verbs_psvl.csv')
csvreader = csv.reader(file)
first_line = next(csvreader)
verbs_psvl = [first_line]
i = 0
for row in csvreader:
    tmp = verbs_psvl[i]
    if row[0] in tmp:
        for j in range(1,len(row)):
            if row[j] not in tmp:
                tmp.append(row[j])
        verbs_psvl[-1] = tmp
    else:
        verbs_psvl.append(row) 
        i += 1
file.close()
verbs_psvl_1 = []
for row in verbs_psvl:
    for line in verbs_mlm:
        if row[0] in line:
            verbs_psvl_1.append(row)
            break

# read verbs for 3 closest objects
file = open('verbs_3.csv')
csvreader = csv.reader(file)
first_line = next(csvreader)
del first_line[1]
verbs_mlm_3 = [first_line]
i = 0
for row in csvreader:
    tmp = verbs_mlm_3[i]
    if row[0] in tmp:
        for j in range(2,len(row)):
            if row[j] not in tmp:
                tmp.append(row[j])
        verbs_mlm_3[-1] = tmp
    else:
        del row[1]
        verbs_mlm_3.append(row) 
        i += 1
file.close()

# read verbs for all objects
file = open('verbs_all.csv')
csvreader = csv.reader(file)
first_line = next(csvreader)
del first_line[1]
verbs_mlm_all = [first_line]
i = 0
for row in csvreader:
    tmp = verbs_mlm_all[i]
    if row[0] in tmp:
        for j in range(2,len(row)):
            if row[j] not in tmp:
                tmp.append(row[j])
        verbs_mlm_all[-1] = tmp
    else:
        del row[1]
        verbs_mlm_all.append(row) 
        i += 1
file.close()

# read verbs for orignal DistilBERT
file = open('verbs_ori.csv')
csvreader = csv.reader(file)
first_line = next(csvreader)
del first_line[1]
verbs_dis = [first_line]
i = 0
for row in csvreader:
    tmp = verbs_dis[i]
    if row[0] in tmp:
        for j in range(2,len(row)):
            if row[j] not in tmp:
                tmp.append(row[j])
        verbs_dis[-1] = tmp
    else:
        del row[1]
        verbs_dis.append(row) 
        i += 1
file.close()

# function to compute metrics
def compute_metrics(verbs,verbs_gt,verbs_psvl):
    mIoU = 0;
    recall_1 = 0;
    recall_2 = 0;
    recall_3 = 0;
    for row1 in verbs_psvl:
        for row in verbs:
            if row1[0] == row[0]:
                for line in verbs_gt:
                    if row[0] == line[0]:
                        a = 0
                        b = len(line)-1
                        for i in range(1,len(row)):
                            if row[i] in line:
                                a += 1
                            else:
                                b += 1
                        mIoU += a/b*100
                        if a/b >= 0.15:
                            recall_1 += 1
                        if a/b >= 0.25:
                            recall_2 += 1  
                        if a/b >= 0.35:
                            recall_3 += 1  
                        break
                break
    mIoU /= len(verbs_psvl)
    recall_1 /= 0.01*len(verbs_psvl)
    recall_2 /= 0.01*len(verbs_psvl)
    recall_3 /= 0.01*len(verbs_psvl)
    return recall_1,recall_2,recall_3,mIoU
# compute metrics for 2 closest objects case
r1_mlm,r2_mlm,r3_mlm,mIoU_mlm = compute_metrics(verbs_mlm,verbs_gt_2,verbs_psvl_1)
print('2 closest objects\' verb Recall@0.15: '+str(r1_mlm))
print('2 closest objects\' verb Recall@0.25: '+str(r2_mlm))
print('2 closest objects\' verb Recall@0.35: '+str(r3_mlm))
print('2 closest objects\' verb meanIoU: '+str(mIoU_mlm))

# compute metrics for 3 closest objects case
r1_mlm_3,r2_mlm_3,r3_mlm_3,mIoU_mlm_3 = compute_metrics(verbs_mlm_3,verbs_gt_2,verbs_psvl_1)
print('3 closest objects\' verb Recall@0.15: '+str(r1_mlm_3))
print('3 closest objects\' verb Recall@0.25: '+str(r2_mlm_3))
print('3 closest objects\' verb Recall@0.35: '+str(r3_mlm_3))
print('3 closest objects\' verb meanIoU: '+str(mIoU_mlm_3))

# compute metrics for all objects case
r1_mlm_all,r2_mlm_all,r3_mlm_all,mIoU_mlm_all = compute_metrics(verbs_mlm_all,verbs_gt_2,verbs_psvl_1)
print('all objects\' verb Recall@0.15: '+str(r1_mlm_all))
print('all objects\' verb Recall@0.25: '+str(r2_mlm_all))
print('all objects\' verb Recall@0.35: '+str(r3_mlm_all))
print('all objects\' verb meanIoU: '+str(mIoU_mlm_all))

# compute metrics for 2 close objects case without fine-tuning
r1_dis,r2_dis,r3_dis,mIoU_dis = compute_metrics(verbs_dis,verbs_gt_2,verbs_psvl_1)
print('2 closest objects\' verb w/o fine-tuning Recall@0.15: '+str(r1_dis))
print('2 closest objects\' verb w/o fine-tuning Recall@0.25: '+str(r2_dis))
print('2 closest objects\' verb w/o fine-tuning Recall@0.35: '+str(r3_dis))
print('2 closest objects\' verb w/o fine-tuning meanIoU: '+str(mIoU_dis))

# compute metrics for VerbBERT case
r1_psvl,r2_psvl,r3_psvl,mIoU_psvl = compute_metrics(verbs_psvl_1,verbs_gt_2,verbs_psvl_1)
print('VerbBERT\'s verb Recall@0.15: '+str(r1_psvl))
print('VerbBERT\'s verb Recall@0.25: '+str(r2_psvl))
print('VerbBERT\'s verb Recall@0.35: '+str(r3_psvl))
print('VerbBERT\'s verb meanIoU: '+str(mIoU_psvl))
