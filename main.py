#-------------------------------------------------------------------------------
# Name:        main
# Purpose:     Runs Prisoner's Dilemma
#
# Author:      David
#
# Created:     06/05/2013
#-------------------------------------------------------------------------------
from random import *

BOTH_EXPLOIT=3
BOTH_COOPERATE=7
OPP_EXPLOIT=1
OPP_COOPERATE=11

class Player(object):
    """Base class for the two players"""
    def __init__(self, id):
        self.points=0
        self.id=id
        self.roundsPlayed = 0
        self.pointsPerRound = 0.0

    def __repr__(self):
        return  type(self).__name__ + " " + str(self.id)

    def reset(self, id):
        self.points=0
        self.roundsPlayed=0
        self.pointsPerRound=0.0
        self.id = 0

    def calcPointsPerRound(self):
        self.pointsPerRound = float(self.points)/float(self.roundsPlayed)

class PermenantRetaliation(Player):
    """Permenant Retaliation player"""
    def __init__(self, id):
        super(PermenantRetaliation, self).__init__(id)
        self.beenExploited=[]

    def play(self, id):
        """plays a round against a player of id"""
        if(id in self.beenExploited):
            return True #Once exploited, returns true
        else:
            return False #Returns false until exploited

    def addExploited(self, id):
        """plays a round against a player of id"""
        if (id not in self.beenExploited):
            self.beenExploited.append(id)

    def reset(self, id):
        super().reset(id)
        self.beenExploited=[]

class AlwaysExploit(Player):
    def __init__(self, id):
        super(AlwaysExploit, self).__init__(id)

    def play(self, id):
        return True #Always returns true

def scheduleMatches(players):
    schedule=[]
    for i in range(0, len(players)):
        for j in range(i+1, len(players)):
            schedule.append([players[i],players[j]])
    return schedule

def playRound(schedule, w):
    for match in schedule:
        playGame(match[0], match[1], w)

def playGame(player1, player2, w):
    rand = 100
    w = w*100
    while(rand>w):
        playTurn(player1, player2)
        rand = randint(1, 10000) % 100

def playTurn(player1, player2):
    p1 = player1.play(player2.id)
    p2 = player2.play(player1.id)
    #both exploit
    if (p1 and p2):
        player1.points += BOTH_EXPLOIT
        player2.points += BOTH_EXPLOIT
    #both cooperate
    elif((not p1) and (not p2)):
        player1.points += BOTH_COOPERATE
        player2.points += BOTH_COOPERATE
    #p1 exploit, p2 coop
    elif(p1 and (not p2)):
        player1.points += OPP_COOPERATE
        player2.points += OPP_EXPLOIT
        player2.addExploited(player1.id)
    #p2 exploit, p1 coop
    else:
        player1.points += OPP_EXPLOIT
        player2.points += OPP_COOPERATE
        player1.addExploited(player2.id)
    #increment the number of rounds played
    player1.roundsPlayed += 1
    player2.roundsPlayed += 1
    player1.calcPointsPerRound()
    player2.calcPointsPerRound()

def getNumPR(players):
    numPR=0
    for player in players:
        if type(player).__name__ == "PermenantRetaliation":
            numPR+=1
    return numPR

def getAvgPPR(players):
    sum=0
    for player in players:
        sum += player.pointsPerRound
    return sum/float(len(players))

def getStdDeviation(players, avg):
    sum=0
    for player in players:
        sum += (float(avg)-float(player.pointsPerRound))**2
    return (sum/float(len(players)))**(0.5)

def main():
    #Constants definining what happens after a single round

    numPlayers=input("Input the number of players: ")
    numPlayers=int(numPlayers)
    print(numPlayers)
    fractionPR=input("Input the % of players playing PR: ")
    fractionPR=float(fractionPR)
    print(fractionPR)
    w=input("What is the probability of another round occuring: ")
    w=float(w)
    print(w)

    players=[]

    numPR = int(float(numPlayers)*float(fractionPR))

    #Initialize Players
    for i in range(0, numPlayers):
        if i<numPR:
            players.append(PermenantRetaliation(i))
        else:
            players.append(AlwaysExploit(i))

    #Round robin scheduling
    schedule = scheduleMatches(players)

    #Play rounds
    rounds=0
    nextRound='y'
    #while(nextRound == 'y' or nextRound =='Y'):
    for x in range(1,10000):
        pass
        playRound(schedule, w)
        print("##############################")
        print("Round " + str(rounds) + " stats")
        print("##############################")
        avgPPR = getAvgPPR(players)
        print("\tNumber of Players: " + str(numPlayers))
        print("\tNumber playing PR: " + str(getNumPR(players)))
        print("\tAverage points per round: " + str(avgPPR))
        #nextRound=input("Should there be a new round? (y/n): ")
        if(nextRound == 'y' or nextRound == 'Y'):
            players = sorted(players, key=lambda player: player.pointsPerRound)
            stdDev = getStdDeviation(players, avgPPR)
            i=0
            #prune below std. deviation
            while(players[i].pointsPerRound + stdDev <= avgPPR):
                i+=1
            belowStdDev=i
            #copy above std. deviation
            while(players[i].pointsPerRound - stdDev > avgPPR):
                i+=1
            aboveStdDev=players[i:]
            for j in range(0,belowStdDev):
                temp = aboveStdDev[(len(aboveStdDev)-(j+1))]
                if type(temp).__name__ == "PermenantRetaliation":
                    players[i] = PermenantRetaliation(i)
                elif type(temp).__name__ == "AlwaysExploit":
                    players[i] = AlwaysExploit(i)
            i=0
            for player in players:
                player.reset(i)
                i+=1
            print("Next generation...")
            print()
        rounds+=1

    print()
    print("##############################")
    print("######   Final Stats    ######")
    print("##############################")
    print("\tNumber of rounds: " + str(rounds))
    print("\tNumber of Players: " + str(numPlayers))
    print("\tNumber remaining PR: " + str(getNumPR(players)))

if __name__ == '__main__':
    main()