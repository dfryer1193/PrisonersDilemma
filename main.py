#-------------------------------------------------------------------------------
# Name:        main
# Purpose:     Runs Prisoner's Dilemma
#
# Author:      David
#
# Created:     06/05/2013
#-------------------------------------------------------------------------------
from random import *

#Constants definining what happens after a single round
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
        self.turnsPlayed = 0
        self.pointsPerRound = 0.0
        self.avgGameLen = 0.0

    def __repr__(self):
        return  type(self).__name__ + ":" + str(self.id) + ":" + str(self.points)

    def reset(self):
        self.points=0
        self.roundsPlayed=0
        self.pointsPerRound=0.0

    #def calcPointsPerRound(self):
    #    self.pointsPerRound = float(self.points)/float(self.roundsPlayed)

class PermanentRetaliation(Player):
    """Permenant Retaliation player"""
    def __init__(self, id):
        super(PermanentRetaliation, self).__init__(id)
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

def getHash(schedule):
    hashCode = 0
    for pair in schedule:
        for player in pair:
            hashCode+=hash(player)
    return hashCode

def playRound(schedule, w):
    sum=0
    matches=0
    seed(getHash(schedule))
    for match in schedule:
        sum+=playGame(match[0], match[1], w)
        matches+=1
    return float(sum)/float(matches)

def playGame(player1, player2, w):
    rand = 100
    sum=0
    avg=0
    turns=0
    player1.turnsPlayed=0
    player2.turnsPlayed=0

    while(rand>(w*100)):
        playTurn(player1, player2)
        sum += (player1.turnsPlayed + player2.turnsPlayed)
        avg += float(sum)/2.0
        sum=0
        rand = randint(1, 100) % 100
        w=w**2
        turns += 1

    player1.roundsPlayed+=1
    player2.roundsPlayed+=1
    return float(avg)/float(turns)

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
    player1.turnsPlayed += 1
    player2.turnsPlayed += 1
    #player1.calcPointsPerRound()
    #player2.calcPointsPerRound()

def getNumPR(players):
    numPR=0
    for player in players:
        if type(player).__name__ == "PermanentRetaliation":
            numPR+=1
    return numPR

def getAvgPPR(players):
    sum=0
    for player in players:
        sum += player.points#PerRound
    return float(sum)/float(len(players))

def getStdDeviation(players, avg):
    sum=0
    for player in players:
        sum += (float(avg)-float(player.points))**2
    return (sum/float(len(players)))**(0.5)

def getAvgGameLen(players):
    sum=0
    for player in players:
        sum += player.roundsPlayed
    return float(sum)/float(len(players))

def main():
    numPlayers=input("Input the number of players: ")
    numPlayers=int(numPlayers)
    fractionPR=input("Input the % of players playing PR: ")
    fractionPR=float(fractionPR)
    w=input("What is the probability of another round occuring: ")
    w=float(w)
    numRounds=input("How many rounds should be played: ")
    numRounds=int(numRounds)

    players=[]

    numPR = int(float(numPlayers)*float(fractionPR))

    #Initialize Players
    for i in range(0, numPlayers):
        if i<numPR:
            players.append(PermanentRetaliation(i))
        else:
            players.append(AlwaysExploit(i))

    #Play rounds
    rounds=0
    nextRound='y'
    #while(nextRound == 'y' or nextRound =='Y'):
    for x in range(0,numRounds):
        #Round robin scheduling
        schedule = scheduleMatches(players)
        playRound(schedule, w)
        print("##############################")
        print("Round " + str(rounds) + " stats")
        print("##############################")
        avgPPR = getAvgPPR(players)
        print("\tNumber of Players: " + str(numPlayers))
        print("\tNumber playing PR: " + str(getNumPR(players)))
        print("\tAverage points: " + str(avgPPR))
        #nextRound=input("Should there be a new round? (y/n): ")
        if(nextRound == 'y' or nextRound == 'Y'):
            #players = sorted(players, key=lambda player: player.pointsPerRound)
            stdDev = getStdDeviation(players, avgPPR)
            i=0
            #prune below std. deviation
            belowStdDev=[]
            aboveStdDev=[]
            for player in players:
                if avgPPR-(1.55*stdDev) > player.points: #TODO: Play with these values more 0.3*
                    belowStdDev.append(player.id)
                elif avgPPR+(stdDev) <= player.points: #0.1*
                    aboveStdDev.append(player.id)

            #create new generation
            for i in range(0, len(belowStdDev)):
                if i<len(aboveStdDev):
                    if type(players[aboveStdDev[len(aboveStdDev)-(i+1)]]).__name__ == "PermanentRetaliation":
                        players[belowStdDev[i]] = PermanentRetaliation(belowStdDev[i])
                    elif type(players[aboveStdDev[len(aboveStdDev)-(i+1)]]).__name__ == "AlwaysExploit":
                        players[belowStdDev[i]] = AlwaysExploit(belowStdDev[i])
                else:
                    players[belowStdDev[i]] = AlwaysExploit(belowStdDev[i])

            for player in players:
                player.reset()
                if player.id in belowStdDev:
                    for player2 in players:
                        if type(player2).__name__ == "PermanentRetaliation":
                            if player.id in player2.beenExploited:
                                player2.beenExploited.remove(player.id)
                        else:
                            continue
                else:
                    continue
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