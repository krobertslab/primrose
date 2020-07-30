import csv

tsv_file = open("train_dev.tsv")
read_tsv = csv.reader(tsv_file, delimiter="\t")

labels = []
for row in read_tsv:
	if row[1] not in labels:
		labels.append(row[1])

print(labels)
