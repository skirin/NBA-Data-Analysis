# -*- coding: utf-8 -*-
"""
Spencer Kirin

writeStats
"""

import json

def main():
    with open("[03-05-2016]-[06-19-2016]-combined-stats.csv", "r") as f:
        
        #Dictionary to store info we need
        dicto = {}
        #Couner for our_id in dicto for each play
        our_id = 0
        
        for line in f:
            #Put all stats of play into an array
            play = line.split(",")
            
            #Last line of file is empty, will be of length 1
            if(len(play)) == 1:
                break
            
            #Exclude playoff games
            if play[0] < '41500000':
                #Create new key with game_id for start of each new game
                if play[19] == '1':
                    dicto[play[0]] = {}
                    #reset our_id at start of each new game
                    our_id = 0
                #Check if play is a made shot
                elif play[32] == '1' or play[32] == '2' or play[32] == '3':
                    #{"game_id": {"our_id": [play_id, team, points, time remaining, quarter]}}
                    dicto[play[0]][our_id] = (int(play[19]),play[20],int(play[32]),play[16],int(play[13]))
                    #Add 1 to counter after each recorded play
                    our_id = our_id + 1
                else:
                    #Do nothing if play is not a made shot
                    pass
        
    #Write dictionary to json file
    with open("stats.json", "w") as fp:
        json.dump(dicto, fp)


main()
