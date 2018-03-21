from elo import expected
from elo import elo
import csv
import sys

class Player:
    name = ""  # Nickname assigned in
    ELO = 1200
    expected = 0
    result = 0
    wins = 0
    losses = 0
    games = 0

def OpenData():
    '''
    Opens the CSV file detailing matches and their results
    '''
    global csvfile
    csvfile = open(sys.argv[1])
    global readCSV  # TODO: change this to not make use of a global
    readCSV = csv.reader(csvfile, delimiter=',')

def ResetCSV():
    '''
    Resets the file seek on the input CSV back to the start of data, skipping the header
    '''
    csvfile.seek(0)
    next(readCSV)

def GetPlayers():
    '''
    Populates the list of players from the input CSV
    '''
    # Get unique array of player names
    playernames = set()
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
    '''
    Calculates the K value to be used for that player

    Called in UpdateELO()

    Parameters
    ----------
    player : object of player class
        The player to get the correct K value for

    Returns
    -------
    int
        The K value to be used when calucating the new ELO value
    '''
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
    '''
    Updates the ELO value for the specified player

    Called in GetStats()

    Parameters
    ----------
    player : object of player class
        The player to update the ELO value for
    '''
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
        challenger.losses += 1
        defendant.result = 1
        defendant.wins += 1
    # Increment number of games played
    challenger.games += 1
    defendant.games += 1
    # Set new ELO ratings
    UpdateELO(challenger)
    UpdateELO(defendant)

def UpdateELO(player):
    '''
    Updates the ELO value for the specified player

    Called in match()

    Parameters
    ----------
    player : object of player class
        The player to update the ELO value for
    '''
    player.ELO = elo(player.ELO, player.expected, player.result, GetK(player))

def GetStats():
    '''
    Loops through each match that took place in the input CSV, running match() on each one to update the player's stats
    '''
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
    '''
    Loops through each player, writing their stats to the output CSV
    '''
    with open(sys.argv[2], "wb") as elofile:
        elowriter = csv.writer(elofile, delimiter=',', quotechar="'", quoting=csv.QUOTE_MINIMAL)
        elowriter.writerow(["Player", "ELO", "Games", "Wins", "Losses"])  # Header row
        for i in players:
            elowriter.writerow([i.name, i.ELO, i.games, i.wins, i.losses])
        #elowriter.writerow([jodgers.name, jodgers.ELO])
        #elowriter.writerow([rory.name, rory.ELO])
        elofile.flush()  # Write data to file
    elofile.close()

def CloseData():
    '''
    Closes the opened input CSV
    '''
    csvfile.close()

def main():
    global players
    players = []  # TODO: move these
    #playernames = set()
    OpenData()
    GetPlayers()
    GetStats()
    WriteCSV()
    CloseData()

if __name__ == "__main__":
    main()
