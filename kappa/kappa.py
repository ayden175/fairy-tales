import csv
import os
import numpy as np
from sklearn.metrics import cohen_kappa_score

def import_csv(directory):
    anno = []
    for file in os.listdir(directory):
        with open(os.path.join(directory, file), 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if row != ['word', 'entity', 'name', 'alignment']:
                    anno.append(row)
    return np.array(anno)

anno_one = import_csv("first")
anno_two = import_csv("second")

kappas = []

for i in range(1, anno_one.shape[1]):
    kappas.append(cohen_kappa_score(anno_one[:, i], anno_two[:, i]))

print(kappas)