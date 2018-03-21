  -------------- -----------------------------------------------------------------------------------------------
   \                                                                                                 [index](.)\
   \               [/cygdrive/e/Documents/elo-calc/elo-calc.py](file:/cygdrive/e/Documents/elo-calc/elo-calc.py)
  **elo-calc**   
  -------------- -----------------------------------------------------------------------------------------------

 \
**Modules**

`      `

 

  ------------------ ------------------ -- --
  [csv](csv.html)\   [sys](sys.html)\      
  ------------------ ------------------ -- --

 \
**Classes**

`      `

 

[Player](elo-calc.html#Player)

 \
[class **Player**]{#Player}

`   `

 

Data and other attributes defined here:\

**ELO** = 1200

**expected** = 0

**games** = 0

**losses** = 0

**name** = \'\'

**result** = 0

**wins** = 0

 \
**Functions**

`      `

 

[**CloseData**]{#-CloseData}()
:   `Closes the opened input CSV`

<!-- -->

[**GetK**]{#-GetK}(player)
:   `Calculates the K value to be used for that player   Called in UpdateELO()   Parameters ---------- player : object of player class     The player to get the correct K value for   Returns ------- int     The K value to be used when calucating the new ELO value`

<!-- -->

[**GetPlayers**]{#-GetPlayers}()
:   `Populates the list of players from the input CSV`

<!-- -->

[**GetStats**]{#-GetStats}()
:   `Loops through each match that took place in the input CSV, running match() on each one to update the player's stats`

<!-- -->

[**OpenData**]{#-OpenData}()
:   `Opens the CSV file detailing matches and their results`

<!-- -->

[**ResetCSV**]{#-ResetCSV}()
:   `Resets the file seek on the input CSV back to the start of data, skipping the header`

<!-- -->

[**UpdateELO**]{#-UpdateELO}(player)
:   `Updates the ELO value for the specified player   Called in match()   Parameters ---------- player : object of player class     The player to update the ELO value for`

<!-- -->

[**WriteCSV**]{#-WriteCSV}()
:   `Loops through each player, writing their stats to the output CSV`

[**main**]{#-main}()

[**match**]{#-match}(challenger, defendant, winner)
:   `Updates the ELO value for the specified player   Called in GetStats()   Parameters ---------- player : object of player class     The player to update the ELO value for`
