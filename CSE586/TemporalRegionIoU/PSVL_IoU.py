import csv
import json
from heapq import *
'''video-name,t-init,t-end,f-init,f-end,video-duration,frame-rate,video-frames,label-idx'''

def calculate_iou(prediction, ground_truth):
    if prediction[1] < ground_truth[0] or ground_truth[1] < prediction[0]:
        return 0
    int_start = max(prediction[0], ground_truth[0])
    int_end = min(prediction[1], ground_truth[1])
    union_start = min(prediction[0], ground_truth[0])
    union_end = max(prediction[1], ground_truth[1])

    return (int_end-int_start)/(union_end-union_start)


def main():
    columns = ['video-name','t-init','t-end','f-init','f-end','video-duration','frame-rate','video-frames','label-idx']
    ground_truth = {}
    with open('charades_ground_truth.csv') as csv_file:
        reader = csv.reader(csv_file)
        vids = 0
        for action in reader:
            if vids==0:
                vids+=1
                continue
            video_name = action[0]
            if video_name not in ground_truth:
                ground_truth[video_name] = []
            ground_truth[video_name].append((float(action[1]),float(action[2])))
    print(len(ground_truth))
    predictions = {}
    with open('../ObjectDetection/charades_train_pseudo_supervision_TEP_PS.json') as json_file:
        pred_dict = json.load(json_file)
        for x in pred_dict:
            if x['vid'] not in predictions:
                predictions[x['vid']] = []
            newstamp = x['timestamp']
            seconds = x['duration']
            newstamp[0] *= seconds
            newstamp[1] *= seconds
            if newstamp not in predictions[x['vid']]:
                predictions[x['vid']].append(newstamp)
    print(len(predictions))
    ''' 
    Take average of top 3 temporal predictions matched with closest action in ground truth
    (can be less than 3 if fewer than 3 actions)
    '''
    iou_scores = {}
    count = 0
    tot = 0
    score = 0
    for vid in predictions:
        if vid not in ground_truth:
            iou_scores[vid] = -1
            continue
        preds = predictions[vid]
        GT = ground_truth[vid]
        #print(vid, preds)
        #print(GT)
        max_iou = []
        for pred in preds:
            for gt in GT:
                heappush(max_iou, -calculate_iou(pred, gt))
        num_samples = min(min(len(preds), len(GT)),3)
        count += 1
        tot+=num_samples
        tmp = 0
        iou_sum = 0
        while tmp<num_samples and max_iou:
            iou_sum -= heappop(max_iou)
            tmp+=1
        #print(iou_sum, num_samples)
        iou_scores[vid] = iou_sum / num_samples
        score += iou_sum / num_samples
    print(iou_scores)
    s = 0
    for x in iou_scores:
        s += iou_scores[x]
    print("AVG IOU ", s / len(iou_scores))
    thresh = [0.30, 0.50, 0.70]
    total = 0
    thresh_cnt = [0] * 3
    for x in iou_scores:
        total += 1
        for t in range(len(thresh)):
            if iou_scores[x] > thresh[t]:
                thresh_cnt[t] += 1
    for t in range(len(thresh_cnt)):
        thresh_cnt[t] /= total
    print("""
        IOU: recall
        """)
    for x in thresh_cnt:
        print(x)
    with open('charades_PSVL_iou.json', 'w', encoding='utf8') as json_file:
        json.dump(iou_scores, json_file)
    print('average segment predictions / video: {}'.format(tot/count))
    print('average segment iou: {}'.format(score/count))

if __name__ == '__main__':
    #print(calculate_iou((5,10),(5,10)))
    main()