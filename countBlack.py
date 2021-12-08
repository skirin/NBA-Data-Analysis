# -*- coding: utf-8 -*-
"""
Spencer Kirin

countBlack
"""

import json
import operator

def main():
    with open("stats.json", "r") as fp:
        dicto = json.load(fp)
        
        #Array to keep track of black stat for each game
        blackArr = []
        
        #Dictionary to display results
        results = {}
        
        #Array of every team in NBA to loop through
        teamArr = ['BKN','HOU','DEN','NOP','POR','LAC','MIA','UTA','TOR','GSW',
                   'CHA','IND','BOS','CHI','SAC','DET','OKC','MIL','SAS','DAL',
                   'MEM','NYK','LAL','PHI','PHX','MIN','ORL','ATL','CLE','WAS']
        
        for team in teamArr:
            #Loop through each play in dicto
            for game_id in dicto:
                #Boolean to keep track of team we are looking at
                boolTEAM = False
                #Count total shots for each team
                shotsTeam = 0
                shotsOpp = 0
                #Store every made shot in array
                shots = []
                
                for our_id in dicto[game_id]:
                    #Add shot to counters
                    #Add 0 or 1 to shots array
                    if dicto[game_id][our_id][1] == team:
                        shotsTeam = shotsTeam + 1
                        shots.append(1)
                    else:
                        shotsOpp = shotsOpp + 1
                        shots.append(0)
                    
                    #Set boolTEAM to true when we know TEAM played in this game
                    if dicto[game_id][our_id][1] == team:
                        boolTEAM = True
                        
                        
                #Check that team played in this game
                if boolTEAM:
                    #Count total number of shots made in game
                    totalMade = shotsTeam + shotsOpp
                    #Calculate shots made fraction for team
                    fraction = shotsTeam / totalMade
                    
                    #Loop through array of made shots and calculate black stat
                    #Keep a running queue of 10 most recent made shots
                    queue = []
                    black = 0
                    for i in shots:
                        queue.append(i)
                        #Start at 10th made shot of game
                        if len(queue) == 10:
                            last = 0
                            #Sum of last 10 shots (1s and 0s)
                            for j in queue:
                                last = last + j
                            movingAvg = last / 10
                            black = black + abs((movingAvg - fraction))
                            queue.pop(0)
                    blackArr.append(black)
                
            #Calculate average black for a game for team
            total = 0
            for i in blackArr:
                total = total + abs(i)
            blackAvg = total / len(blackArr)
            #Store results in dict
            results[team] = blackAvg
                
        #Print results
        print('Team: (Avg black per game)')
        sortResults = dict(sorted(results.items(), key=operator.itemgetter(1),reverse=True))
        for t in sortResults:
            print(t + ': ' + str(sortResults[t]))
        
            
main()