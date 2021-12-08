# -*- coding: utf-8 -*-
"""
Spencer Kirin

pythagPoints
"""

import json
import operator
import math
import csv

def main():
    with open("stats.json", "r") as fp:
        dicto = json.load(fp)
        
        #Variables to decide how many points in a row will be classified 
        #as a run, and the exponent we will use for the pythagorean equation
        run = 6
        x = 3
    
        #Array of every team in NBA to loop through
        teamArr = ['BKN','HOU','DEN','NOP','POR','LAC','MIA','UTA','TOR','GSW',
                   'CHA','IND','BOS','CHI','SAC','DET','OKC','MIL','SAS','DAL',
                   'MEM','NYK','LAL','PHI','PHX','MIN','ORL','ATL','CLE','WAS']
        
        #Dictionary to keep track of stats so we can sort at the end
        teamDict = {}
        
        #Array to store pythagorean win perc of every team
        pythWin = []
        
        for team in teamArr:
            #Arrays to keep track of # of runs in each game for team and opponent
            pgTeamArr = []
            pgOppArr = []
            
            #Loop through each play in dicto
            for game_id in dicto:
                #Counters for stats we want
                strk = 0
                strksTeam = 0
                strksOpp = 0
                #Boolean to keep track of team we are looking at
                boolTEAM = False
                #Keeps track of team that made previous shot for streaks
                prevMade = ''
                #Keep track of quarter
                prevQuart = 1
                
                for our_id in dicto[game_id]:
                    
                    #Set boolTEAM to true when we know TEAM played in this game
                    if dicto[game_id][our_id][1] == team:
                        boolTEAM = True
                        
                    #Reset counters at start of new quarter
                    if dicto[game_id][our_id][4] != prevQuart:
                        strk = 0
                        prevQuart = dicto[game_id][our_id][4]
                      
                    #Only count runs in certain quarter
                    if dicto[game_id][our_id][4] == 1:
                        #Add to streak if team that made this shot also made previous
                        if dicto[game_id][our_id][1] == prevMade:
                            strk = strk + dicto[game_id][our_id][2]
                            
                        #When streak ends, if long enough, add to per game counter
                        else:
                            if strk >= run:
                                #Certain runs are so long they count as multiple runs
                                mult = math.floor(strk / run)
                                if prevMade == team:
                                    strksTeam = strksTeam + mult
                                else:
                                    strksOpp = strksOpp + mult
                            #Reset streak counter and prevMade when streak ends
                            strk = dicto[game_id][our_id][2]
                            prevMade = dicto[game_id][our_id][1]
                            
                    #Check for quarter ending streak
                    elif dicto[game_id][our_id][4] == 2 and prevQuart == 1:
                        if strk >= run:
                            #Certain runs are so long they count as multiple runs
                            mult = math.floor(strk / run)
                            if prevMade == team:
                                strksTeam = strksTeam + mult
                            else:
                                strksOpp = strksOpp + mult
                                
                    prevQuart == dicto[game_id][our_id][4]
                
                '''
                #Check for a game ending streak
                if strk >= run:
                    #Certain runs are so long they count as multiple runs
                    mult = math.floor(strk / run)
                    if prevMade == team:
                        strksTeam = strksTeam + mult
                    else:
                        strksOpp = strksOpp + mult
                '''
                    
                #Gather stats for game and reset counters
                #Use bool to only gather stats for games TEAM played in
                if boolTEAM == True:
                    pgTeamArr.append(strksTeam)
                    pgOppArr.append(strksOpp)
                
            #Calculate average number of streaks per game for team and opponent
            totalTeam = 0
            for i in pgTeamArr:
                totalTeam = totalTeam + i
            pgTeamAvg = totalTeam / len(pgTeamArr)
            
            totalOpp = 0
            for j in pgOppArr:
                totalOpp = totalOpp + j
            pgOppAvg = totalOpp / len(pgOppArr)
            
            #Calculate pythagorean winning percentage for each team
            winPerc = (totalTeam**x) / ((totalTeam**x) + (totalOpp**x))
            
            #Calclate teams expected recorded using pythagorean winning percentage
            wins = round(82 * winPerc)
            losses = 82 - wins
            predRecord = str(wins) + '-' + str(losses)
            
            #Store results in teamDict
            teamDict[team] = (round(winPerc*100,2), predRecord,
                    round(pgTeamAvg,2), round(pgOppAvg,2))
            
            #Store win perc in array of arrays to be written to csv later
            pythWin.append([team, winPerc])
        
        #Print results
        print('Team: (Pythagorean Winnning %, Runs PG, Runs Allowed PG)')
        results = dict(sorted(teamDict.items(), key=operator.itemgetter(1),reverse=True))
        for t in results:
            print(t + ': ' + str(results[t]))
            
        #Write results to csv file
        with open("pythagWinPerc.csv", "w") as fp:
            writer = csv.writer(fp)
            writer.writerows(pythWin)
    

main()
