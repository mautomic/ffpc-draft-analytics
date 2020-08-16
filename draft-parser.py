import csv

read = []

with open('drafts/draftresults-0.csv', 'r') as csvfile:
	reader = csv.reader(csvfile, delimiter=',')
	for row in reader:
		read.append(row)

for i in read:
	print(i)