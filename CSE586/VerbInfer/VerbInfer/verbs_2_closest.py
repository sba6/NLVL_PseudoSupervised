# read nouns for 2 closest objects condition
import csv
file = open("nouns_2.csv")
csvreader = csv.reader(file)
header = next(csvreader)
rows = []
nouns = []
for row in csvreader:
    rows.append(row)
for row in rows:
    ls = [];
    for sub in row:
        if (row.index(sub)%5 == 2 and sub != 'person'):
            if (sub == 'tvmonitor'):
                sub = 'tv'
            ls.append(sub)
    if (len(ls) != 0):
        tmp = [row[0]]
        tmp.extend(ls)
        nouns.append(tmp)
file.close()

nouns_del = []
for i in nouns:
    if i not in nouns_del:
        nouns_del.append(i)
for i in nouns_del:
    i.append(nouns.count(i))

# perform MLM on fine-tuned Distilbert
import torch
from transformers import AutoTokenizer, AutoModelForMaskedLM

tokenizer = AutoTokenizer.from_pretrained("huggingface-course/distilbert-base-uncased-finetuned-imdb")

model = AutoModelForMaskedLM.from_pretrained("huggingface-course/distilbert-base-uncased-finetuned-imdb")

n = 3
with open('verbs_2.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for row in nouns_del:
        tmp = [row[0],row[-1]]
        for obj in row[1:-1]:
            text = "A person will [MASK] the "+obj+"."
            inputs = tokenizer(text, return_tensors="pt")
            token_logits = model(**inputs).logits
            # Find the location of [MASK] and extract its logits
            mask_token_index = torch.where(inputs["input_ids"] == tokenizer.mask_token_id)[1]
            mask_token_logits = token_logits[0, mask_token_index, :]
            # Pick the [MASK] candidates with the highest logits
            top_n_tokens = torch.topk(mask_token_logits, n, dim=1).indices[0].tolist()
            for token in top_n_tokens:
                tmp.append(tokenizer.decode([token]))
        csvwriter.writerow(tmp)

