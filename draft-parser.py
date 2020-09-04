import csv
import os
import pandas as pd

def clean_data(picks):
    cleansed_picks = []
    for pick in picks:
        items = []
        items.append(pick[0].strip()) # absolute pick number
        items.append(pick[1].strip()) # round
        items.append(pick[2].strip()) # pick in round
        player_data = pick[-5:]
        items.append(player_data[1].strip() + " " + player_data[0].strip()) # first + last name
        items.append(player_data[2].strip()) # position
        items.append(player_data[3].strip()) # team
        items.append(player_data[4].strip()) # bye
        cleansed_picks.append(items)
    return cleansed_picks

# Read in all draft csvs
files = []
for file in os.listdir("new-drafts"):
    if file.endswith(".csv"):
        files.append(os.path.join("new-drafts", file))

print("Found " + str(len(files)) + " drafts to analyze")

# Create list of all drafts, 1 draft per file
drafts = []
for file in files:
    picks = []
    with open(file, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            if (row[0] == "Overall Pick"):
                continue
            picks.append(row)
    cleansed_picks = clean_data(picks)
    drafts.append(cleansed_picks)

print("Finished parsing all drafts")

# Find adps for every player
player_adp = {}

# Also store team and position for quick lookups
player_team = {}
player_pos = {}

for draft in drafts:
    for pick in draft:
        #if pick[4] == 'TE':
        player = pick[3]
        player_team[player] = pick[5]
        player_pos[player] = pick[4]

        # Keep a list of spots player has been picked in the dictionary
        if player in player_adp:
            player_pick_nums = player_adp[player]
            player_pick_nums.append(pick[0])
        else:
            player_pick_nums = [pick[0]]
            player_adp[player] = player_pick_nums

df = pd.DataFrame()
df['Player'] = []
df['Pick'] = []
df['Team'] = []
df['Position'] = []

# Key/Value is adp : player
players_sorted_adp = {}

count = 25
skip = 0
for player in player_adp.keys():
    count = count - 1
    skip = skip + 1
    if skip < 0:
        continue
    if count < 0:
        break
    player_picks = player_adp[player]
    player_picks = [int(x) for x in player_picks]
    avg_adp = sum(player_picks) / len(player_picks)

    # Avoid collisions/overwrites, by incrementing avg adp by a decimal if it already exists as a key
    if avg_adp in players_sorted_adp:
        avg_adp = avg_adp + 0.0001
    players_sorted_adp[avg_adp] = player

# Sort all adps, so keys are in order from lowest to highest adps
all_adps_sorted = sorted(players_sorted_adp.keys())

rank = 1

# Add player and all of their picked spots to a pandas dataframe
# Also print the position, team, and ranked adp
for adp in all_adps_sorted:
    player = players_sorted_adp[adp]
    player_picks = player_adp[player]

    team = player_team[player]
    pos = player_pos[player]

    size = len(player)
    string_player = player
    string_player += ' ' * (25 - size)

    print(str(rank) + ".\t" + string_player + "" + pos + "\t" + team + "\t" + str(round(adp, 4)))
    rank = rank + 1
    player_picks = [int(x) for x in player_picks]
    for pick in player_picks:
        df = df.append({'Player': player, 'Pick': pick}, ignore_index=True)