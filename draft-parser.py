import csv
import os

def main():
	files = []

	for file in os.listdir("drafts"):
	    if file.endswith(".csv"):
	        files.append(os.path.join("drafts", file))

	print("Found " + str(len(files)) + " drafts to analyze")

	drafts = []

	for file in files:
		picks = []
		with open(file, 'r') as csvfile:
			reader = csv.reader(csvfile, delimiter=',')
			for row in reader:
				picks.append(row)

		cleansed_picks = clean_data(picks)
		for clp in cleansed_picks:
			print(clp)
		drafts.append(cleansed_picks)

	print("Finished parsing all drafts")

def clean_data(picks):
	cleansed_picks = []
	for pick in picks:
	 	items = []
	 	items.append(pick[0].strip()) # absolute pick number
	 	items.append(pick[1].strip()) # round
	 	items.append(pick[2].strip()) # pick in round
	 	player_data = pick[-5:]
	 	items.append(player_data[1].strip()) # first name
	 	items.append(player_data[0].strip()) # last name
	 	items.append(player_data[2].strip()) # positions
	 	items.append(player_data[3].strip()) # team
	 	items.append(player_data[4].strip()) # bye
	 	cleansed_picks.append(items)
	return cleansed_picks

if __name__ == '__main__':
    main()