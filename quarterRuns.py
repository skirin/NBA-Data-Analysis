# -*- coding: utf-8 -*-
"""
Spencer Kirin

quarterRuns
"""

import json
import operator
import math

def main():
    with open("stats.json", "r") as fp:
        dicto = json.load(fp)
        
        #Variable to decide how many points in a row will be classified as a run
        run = 6
    
        #Array of every team in NBA to loop through
        teamArr = ['BKN','HOU','DEN','NOP','POR','LAC','MIA','UTA','TOR','GSW',
                   'CHA','IND','BOS','CHI','SAC','DET','OKC','MIL','SAS','DAL',
                   'MEM','NYK','LAL','PHI','PHX','MIN','ORL','ATL','CLE','WAS']
        
        #Dictionary to keep track of stats so we can sort at the end
        teamDict = {}
        oppDict = {}
        totalDict = {}
        q3Dict = {}
        
        for team in teamArr:
            #Arrays to keep track of # of runs in each game for team and opponent
            pgTeamArr = [0,0,0,0]
            pgOppArr = [0,0,0,0]
            
            #Loop through each play in dicto
            for game_id in dicto:
                #Counters for stats we want
                strk = 0
                #Array for runs in each quarter, position in array corresponds to quarter
                strksTeam = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
                strksOpp = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
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
                        
                    #Add to streak if team that made this shot also made previous
                    if dicto[game_id][our_id][1] == prevMade:
                        strk = strk + dicto[game_id][our_id][2]
                        
                    #When streak ends, if long enough, add to per game counter
                    else:
                        if strk >= run:
                            #Certain runs are so long they count as multiple runs
                            mult = math.floor(strk / run)
                            if prevMade == team:
                                strksTeam[prevQuart-1] = strksTeam[prevQuart-1] + mult
                            else:
                                strksOpp[prevQuart-1] = strksOpp[prevQuart-1] + mult
                        #Reset streak counter and prevMade when streak ends
                        strk = dicto[game_id][our_id][2]
                        prevMade = dicto[game_id][our_id][1]
                
                #Check for a game ending streak
                if strk >= run:
                    #Certain runs are so long they count as multiple runs
                    mult = math.floor(strk / run)
                    if prevMade == team:
                        strksTeam[prevQuart-1] = strksTeam[prevQuart-1] + mult
                    else:
                        strksOpp[prevQuart-1] = strksOpp[prevQuart-1] + mult
                    
                #Gather stats for game and reset counters
                #Use bool to only gather stats for games TEAM played in
                if boolTEAM == True:
                    for i in range(0,4):
                        pgTeamArr[i] = pgTeamArr[i] + strksTeam[i]
                        pgOppArr[i] = pgOppArr[i] + strksOpp[i]
                
            #Calculate average number of streaks per game for team and opponent
            #82 IS STATIC, SO DATA MUST BE FROM AN 82 GAME REGULAR SEASON
            avgTeam = [0,0,0,0,0]
            totalTeam = 0
            for i in range(1,5):
                totalTeam = totalTeam + pgTeamArr[i-1] / 82
                avgTeam[i] = round(pgTeamArr[i-1] / 82, 2)
            avgTeam[0] = round(totalTeam, 2)
            
            avgOpp = [0,0,0,0,0]
            totalOpp = 0
            for j in range(1,5):
                totalOpp = totalOpp + pgOppArr[j-1] / 82
                avgOpp[j] = round(pgOppArr[j-1] / 82, 2)
            avgOpp[0] = round(totalOpp, 2)
            
            #Store results in dictionaries
            teamDict[team] = (avgTeam)
            oppDict[team] = (avgOpp)
            
            #Store total runs in each quarter
            tot = 0
            for k in pgTeamArr:
                tot = tot + k
            runsArr = [tot, pgTeamArr[0], pgTeamArr[1], pgTeamArr[2], pgTeamArr[3]]
            totalDict[team] = runsArr
            
            #Store just q3 runs so we can sort teams in order of q3 runs
            q3Dict[team] = pgTeamArr[0]
        
        #Print results
        '''
        print('Team: [Avg Runs Scored (Total PG, then by quarter)]')
        teamResults = dict(sorted(teamDict.items(), key=operator.itemgetter(1),reverse=True))
        for t in teamResults:
            print(t + ': ' + str(teamResults[t]))
        print('Team: [Avg Runs Allowed (Total PG, then by quarter)]')
        oppResults = dict(sorted(oppDict.items(), key=operator.itemgetter(1),reverse=True))
        for t in oppResults:
            print(t + ': ' + str(oppResults[t]))
        '''
        '''
        print('Team: Q3 Runs Scored')
        q3Runs = dict(sorted(q3Dict.items(), key=operator.itemgetter(1),reverse=True))
        leagTot = 0
        for t in q3Runs:
            leagTot = leagTot + q3Runs[t]
            print(t + ': ' + str(q3Runs[t]))
        print('League Average: ' + str(round(leagTot / 30)))
        '''
        for key in totalDict:
            print(str(key) + ': ' + str(totalDict[key]))
        
    

main()
