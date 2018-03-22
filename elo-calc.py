from elo import expected
from elo import elo
import csv
import sys

class Player:
    '''
    Stores the stat values for each player
    '''
    def __init__(self):
        self.name = ""  # Nickname assigned in match log
        self.ELO = 1200
        self.expected = None
        self.result = None
        self.wins = 0
        self.losses = 0
        self.games = 0

class InputCSV:
    def __init__(self, pathtofile):
        '''
        Parameters
        ----------
        pathtofile : string
            The path to the input file
        '''
        self.inputFile = open(pathtofile)
        self.read = csv.reader(self.inputFile, delimiter=',')

    def ResetCSV(self):
        '''
        Resets the file seek on the input CSV back to the start of data, skipping the header
        '''
        self.inputFile.seek(0)
        next(self.read)

    def CloseData(self):
        '''
        Closes the opened input CSV
        '''
        self.inputFile.close()

def GetPlayers(inputfile):
    '''
    Populates the list of players from the input CSV

    Parameters
    ----------
    inputfile : object of the InputCSV class
        The match log to get list of players from
    '''
    # Get unique array of player names
    playernames = set()
    inputfile.ResetCSV()
    # Loop through the challenger and defendant columns to populate player list
    for row in inputfile.read:
        challenger = row[2]
        playernames.add(challenger)
    inputfile.ResetCSV()
    for row in inputfile.read:  # TODO: why loop here twice?
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

def GetStats(inputfile):
    '''
    Loops through each match that took place in the input CSV, running match() on each one to update the player's stats

    Parameters
    ----------
    inputfile : object of the InputCSV class
        The match log to get list of players from
    '''
    inputfile.ResetCSV()
    for row in inputfile.read:
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

def WriteCSV(pathtofile):
    '''
    Loops through each player, writing their stats to the output CSV

    Parameters
    ----------
    pathtofile : string
        The path to the input file
    '''
    with open(pathtofile, "wb") as elofile:
        elowriter = csv.writer(elofile, delimiter=',', quotechar="'", quoting=csv.QUOTE_MINIMAL)
        elowriter.writerow(["Player", "ELO", "Games", "Wins", "Losses"])  # Header row
        for i in players:
            elowriter.writerow([i.name, i.ELO, i.games, i.wins, i.losses])
        elofile.flush()  # Write data to file

def main():
    global players
    players = []  # TODO: move these
    matchlog = InputCSV(sys.argv[1])
    GetPlayers(matchlog)
    GetStats(matchlog)
    WriteCSV(sys.argv[2])
    matchlog.CloseData()

if __name__ == "__main__":
    main()
