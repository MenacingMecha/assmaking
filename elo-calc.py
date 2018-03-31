from elo import expected
from elo import elo
import csv
import sys
import argparse

class Player:
    ''' Stores the stat values for each player '''
    def __init__(self):
        self.name = ""  # Nickname assigned in match log
        self.ELO = 1200
        self.ELOHighest = self.ELO
        self.ELOLowest = self.ELO
        self.expected = None
        self.result = None
        self.wins = 0
        self.losses = 0
        self.games = 0
        self.onWhitelist = None

    def GetK(self):
        '''
        Calculates the K value to be used for that player

        Called in UpdateELO()

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
        if self.games > newPlayerGames:
            return newPlayerK
        elif self.ELO > topPlayerELO:
            return topPlayerK
        else:
            return midPlayerK

    def UpdateELO(self):
        '''
        Updates the ELO value for the specified player

        Called in match()
        '''
        self.ELO = elo(self.ELO, self.expected, self.result, self.GetK())
        if self.ELO > self.ELOHighest:
            self.ELOHighest = self.ELO
        elif self.ELO < self.ELOLowest:
            self.ELOLowest = self.ELO

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
        ''' Resets the file seek on the input CSV back to the start of data, skipping the header '''
        self.inputFile.seek(0)
        next(self.read)

    def CloseData(self):
        ''' Closes the opened input CSV '''
        self.inputFile.close()

class ArgParse:
    '''Handles command line arguments'''
    def __init__(self):
        self.parser = argparse.ArgumentParser(version='2.1')
        self.results = None

    def parse(self):
        '''Parses arguments, storing the appropriate values'''
        self.parser.add_argument('input_file', action='store',
                help='Input CSV containing details of matches')
        self.parser.add_argument('-s', '--silent', action='store_true', default=False,
                dest="silent", help='Silences terminal output')
        self.parser.add_argument('-o', action='store', dest='output_file',
                help='Output CSV to write stats to')
        self.parser.add_argument('-w', action='store', dest='whitelist_file',
                help='Newline-seperated list of players to check optionally check against')
        self.parser.add_argument('--print-output', action='store_true', default=False,
                dest='print_output',
                help='Print stats to terminal (output is ugly, use for debugging!)')
        self.parser.add_argument('-x', action='store', dest='offset', type=int,
                default=0, help='How many columns to offset in the input CSV')
        self.results = self.parser.parse_args()

def GetPlayers(inputfile, whitelistfile, column_offset):
    '''
    Populates the list of players from the input CSV

    Parameters
    ----------
    inputfile : object of the InputCSV class
        The match log to get list of players from

    whitelistfile : string
        Path to whitelist file to check players against

    column_offset : int
        How many columns to offset in the input CSV

    Returns
    -------
    players : list
        List of objects of the Player() class
    '''
    # Get unique array of player names
    playernames = set()
    inputfile.ResetCSV()
    # Loop through the challenger and defendant columns to populate player list
    for row in inputfile.read:
        challenger = row[0 + column_offset]
        defendant = row[1 + column_offset]
        playernames.add(challenger)
        playernames.add(defendant)
    # Check if we're using a whitelist for players
    if whitelistfile != None:
        whitelistSupplied = True
        whitelist = GetWhitelist(whitelistfile)
    else:
        whitelistSupplied = False
    # Populate player list
    players = []
    for i in playernames:
        x = Player()
        x.name = i
        if whitelistSupplied:
            x.onWhitelist = CheckWhitelist(x.name, whitelist)
        else:  # If not using a whitelist, default to True
            x.onWhitelist = True
        players.append(x)
    #for i in players:
    #    print(i.name, i.onWhitelist)
    return players

def GetWhitelist(pathtofile):
    '''
    Returns an array of players from the supplied whitelist file

    Parameters
    ----------
    pathtofile : string
        The path to the input file

    Returns
    -------
    whitelist : list
        Whitelist array to check against in match()
    '''
    whitelist = []
    with open(pathtofile, "r") as whitelistFile:
        for line in whitelistFile:
            name = line.rstrip()
            whitelist.append(name)
    return whitelist

def CheckWhitelist(name, whitelist):
    '''
    Returns whether or not a player is on the whitelist

    Parameters
    ----------
    name : string
        The player name to check against whitelist entries

    Returns
    -------
    onWhitelist : boolean
        Whether or not the name was on the supplied whitelist
    '''
    for i in whitelist:
        if name == i:
            return True
    else:
        return False

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
    challenger.UpdateELO()
    defendant.UpdateELO()

def GetStats(inputfile, players, column_offset):
    '''
    Loops through each match that took place in the input CSV, running match() on each one to update the player's stats

    Parameters
    ----------
    inputfile : object of the InputCSV class
        The match log to get list of players from

    players : list
        List of player objects of the Player class

    column_offset : int
        How many columns to offset in the input CSV
    '''
    inputfile.ResetCSV()
    for row in inputfile.read:
        challenger = row[0 + column_offset]
        defendant = row[1 + column_offset]
        winner = row[2 + column_offset]
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
        if challenger.onWhitelist and defendant.onWhitelist:
            match(challenger, defendant, winner)

def WriteCSV(pathtofile, stats):
    '''
    Loops through stats list, writing each row to the output csv

    Parameters
    ----------
    pathtofile : string
        The path to the input file

    stats : list
        List of stats ready to be exported
    '''
    with open(pathtofile, "wb") as elofile:
        elowriter = csv.writer(elofile, delimiter=',', quotechar="'",
                quoting=csv.QUOTE_MINIMAL)
        for i in stats:
                elowriter.writerow(i)
        elofile.flush()  # Write data to file

def OutputStats(players, outputfile, silentoutput, printoutput):
    '''
    Loops through each player, writing their stats to the output CSV

    Parameters
    ----------
    players : list
        List of player objects of the Player class

    outputfile : string
        The path to the input file

    silentoutput : boolean
        Whether or not to print the output to the terminal

    printoutput : boolean
        Whether or not to print stats to the terminal
    '''
    headerRow = []  # Move headerRow section to own method?
    headerRow.append("Player")
    headerRow.append("Elo")
    headerRow.append("Games")
    headerRow.append("Wins")
    headerRow.append("Losses")
    headerRow.append("Winrate")
    headerRow.append("Highest Elo")
    headerRow.append("Lowest Elo")
    stats = []
    stats.append(headerRow)
    placementGames = 5
    for i in players:
        if i.onWhitelist:  # Only add to output if on the whitelist
            # Fudge ELO value for players with very few games
            if i.games <= placementGames:
                i.ELO = i.games
                i.ELOHighest = i.games
                i.ELOLowest = i.games
            dataRow = []  # Move this to it's own section?
            dataRow.append(i.name)
            dataRow.append(i.ELO)
            dataRow.append(i.games)
            dataRow.append(i.wins)
            dataRow.append(i.losses)
            dataRow.append(float(i.wins)/float(i.games))  # winrate
            dataRow.append(i.ELOHighest)
            dataRow.append(i.ELOLowest)
            stats.append(dataRow)
    if printoutput and silentoutput == False:
        for i in stats:
            print(i)
    if outputfile != None:
        WriteCSV(outputfile, stats)
        if silentoutput == False:
            print("Output stats to " + outputfile)

def main():
    arg = ArgParse()
    arg.parse()
    matchlog = InputCSV(arg.results.input_file)
    players = GetPlayers(matchlog, arg.results.whitelist_file, arg.results.offset)
    GetStats(matchlog, players, arg.results.offset)
    OutputStats(players, arg.results.output_file, arg.results.silent,
            arg.results.print_output)
    matchlog.CloseData()

if __name__ == "__main__":
    main()
