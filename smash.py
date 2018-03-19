from elo import expected
from elo import elo
import csv

# Define player class
class Player:
    name = ""
    ELO = 1200
    expected = 0
    result = 0
    k = 32
    wins = 0
    losses = 0
    games = 0

# Define player objects
jodgers = Player()
jodgers.name = "Jodgers"
rory = Player()
rory.name = "Rory"

# Add players to array
players = []
players.append(jodgers)
players.append(rory)

def match(challenger, defendant, winner):
    # Calculate the expected score for both players
    challenger.expected = expected(challenger.ELO, defendant.ELO)
    defendant.expected = expected(defendant.ELO, challenger.ELO)
    # Set actual score based on the match winner
    if winner == challenger:
        challenger.result = 1
        challenger.wins += 1
        defendant.result = 0
        defendant.losses += 1
    else:
        challenger.result = 0
        challenger.losses = 0
        defendant.result = 1
        defendant.losses += 1
    challenger.games += 1
    defendant.games += 1
    # Set new ELO ratings
    # TODO: Change to do this at the end of the week, rather than at the end of the match?
    challenger.ELO = elo(challenger.ELO, challenger.expected, challenger.result, k=challenger.k)
    defendant.ELO = elo(defendant.ELO, defendant.expected, defendant.result, k=defendant.k)

# Example matches
# TODO: Read this from csv match log
match(jodgers, rory, jodgers)
match(jodgers, rory, jodgers)
match(jodgers, rory, rory)
match(jodgers, rory, jodgers)
match(jodgers, rory, rory)
match(jodgers, rory, rory)
match(jodgers, rory, jodgers)

# Print example ELO ratings after a match
'''
print("jodgers' ELO: " + str(jodgers.ELO))
print("rory's ELO: " + str(rory.ELO))
'''

'''
with open('Stats Log - Battlelog.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        print(row[0])
'''

with open("elo.csv", "wb") as elofile:
    elowriter = csv.writer(elofile, delimiter=',', quotechar="'", quoting=csv.QUOTE_MINIMAL)
    elowriter.writerow(["Player", "ELO"])  # Header row
    for i in players:
        elowriter.writerow([i.name, i.ELO])
    #elowriter.writerow([jodgers.name, jodgers.ELO])
    #elowriter.writerow([rory.name, rory.ELO])
    elofile.flush()  # Write data to file
elofile.close()
