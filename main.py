from elo import expected
from elo import elo
import csv

# Define player class
class Player:
    name = ""
    ELO = 1200
    expected = 0
    result = 0
    wins = 0
    losses = 0
    games = 0

def OpenData():
    global csvfile
    csvfile = open('Stats Log - Battlelog.csv')
    global readCSV  # TODO: change this to not make use of a global
    readCSV = csv.reader(csvfile, delimiter=',')

def ResetCSV():
    csvfile.seek(0)
    next(readCSV)

# Define player objects
def GetPlayers():
    # Get unique array of player names
    playernames = set()
    '''
    with open('Stats Log - Battlelog.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        '''
    ResetCSV()
    # Loop through the challenger and defendant columns to populate player list
    for row in readCSV:
        challenger = row[2]
        playernames.add(challenger)
    ResetCSV()
    for row in readCSV:
        defendant = row[3]
        playernames.add(defendant)
    #print(len(playernames))
    # Populate player list
    for i in playernames:
        x = Player()
        x.name = i
        players.append(x)
        #print(x.name)

def GetK(player):
    newPlayerGames = 5
    newPlayerK = 40
    midPlayerK = 20
    topPlayerELO = 1400
    topPlayerK = 10
    if player.games > newPlayerGames:
        return newPlayerK
    elif player.ELO > topPlayerELO:
        return topPlayerK
    else:
        return midPlayerK

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
    challenger.ELO = elo(challenger.ELO, challenger.expected, challenger.result, GetK(challenger))
    defendant.ELO = elo(defendant.ELO, defendant.expected, defendant.result, GetK(defendant))

def CalculateELO():
    ResetCSV()
    for row in readCSV:
        challenger = row[2]
        defendant = row[3]
        winner = row[4]
        #print([challenger, defendant, winner])
        for i in players:
            if i.name == challenger:
                challenger = i
            if i.name == defendant:
                defendant = i
            if i.name == winner:
                winner = i
        #print([isinstance(challenger, Player), isinstance(defendant, Player), isinstance(winner, Player)])
        #print([challenger.name, defendant.name, winner.name])
        #print([challenger.ELO, defendant.ELO, winner.ELO])
        match(challenger, defendant, winner)

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
    csvfile.close()

def main():
    global players
    players = []  # TODO: move these
    #playernames = set()
    OpenData()
    GetPlayers()
    CalculateELO()
    WriteCSV()
    CloseData()

if __name__ == "__main__":
    main()
