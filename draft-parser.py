import csv
import os

files = []

for file in os.listdir("drafts"):
    if file.endswith(".csv"):
        files.append(os.path.join("drafts", file))

print("Found " + str(len(files)) + " drafts to analyze")

for file in files:

	print()
	print("Beginning parsing of " + file)
	read = []

	with open(file, 'r') as csvfile:
		reader = csv.reader(csvfile, delimiter=',')
		for row in reader:
			read.append(row)

	for i in read:
		print(i)

print("Finished parsing all drafts")