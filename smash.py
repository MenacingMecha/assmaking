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

def OpenData():
    csvfile = open('Stats Log - Battlelog.csv')
    global readCSV  # TODO: change this to not make use of a global
    readCSV = csv.reader(csvfile, delimiter=',')

# Define player objects
def GetPlayers():
    # Get unique array of player names
    '''
    with open('Stats Log - Battlelog.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        '''
    for row in readCSV:
        name = row[2]
        # TODO: This is innefecient to check every time
        if name != "Challenger":
            playernames.add(name)
    #print(len(playernames))
    # Populate player list
    for i in playernames:
        x = Player()
        x.name = i
        players.append(x)
        #print(x.name)

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
    else:  # winner == defendant
        challenger.result = 0
        challenger.losses = 0
        defendant.result = 1
        defendant.losses += 1
    # Increment number of games played
    challenger.games += 1
    defendant.games += 1
    # Set new ELO ratings
    challenger.ELO = elo(challenger.ELO, challenger.expected, challenger.result, k=challenger.k)
    defendant.ELO = elo(defendant.ELO, defendant.expected, defendant.result, k=defendant.k)

def WriteCSV():
    with open("elo.csv", "wb") as elofile:
        elowriter = csv.writer(elofile, delimiter=',', quotechar="'", quoting=csv.QUOTE_MINIMAL)
        elowriter.writerow(["Player", "ELO"])  # Header row
        for i in players:
            elowriter.writerow([i.name, i.ELO])
        #elowriter.writerow([jodgers.name, jodgers.ELO])
        #elowriter.writerow([rory.name, rory.ELO])
        elofile.flush()  # Write data to file
    elofile.close()

def CloseData():
    readCSV.close()

def main():
    players = []  # TODO: move these
    playernames = set()
    OpenData()
    GetPlayers()
    WriteCSV()
    CloseData()
