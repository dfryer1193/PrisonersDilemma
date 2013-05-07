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

    def reset(self):
        self.points=0
        self.roundsPlayed=0
        self.pointsPerRound=0.0

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

    def beenExploited(self, id):
        """plays a round against a player of id"""
        if (id not in self.beenExploited):
            self.beenExploited.append(id)

    def reset(self):
        super().reset()
        self.beenExploited=[]

class AlwaysExploit(Player):
    def __init__(self, id):
        super(AlwaysExploit, self).__init__(id)

    def play():
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
    #both exploit
    if (player1.play() and player2.play()):
        player1.points += BOTH_EXPLOIT
        player2.points += BOTH_EXPLOIT
    #both cooperate
    elif((not player1.play()) and (not player2.play())):
        player1.points += BOTH_COOPERATE
        player2.points += BOTH_COOPERATE
    #p1 exploit, p2 coop
    elif(player1.play() and (not player2.play())):
        player1.points += OPP_COOPERATE
        player2.points += OPP_EXPLOIT
        player2.beenExploited(player1.id)
    #p2 exploit, p1 coop
    else:
        player1.points += OPP_EXPLOIT
        player2.points += OPP_COOPERATE
        player1.beenExploited(player2.id)
    #increment the number of rounds played
    player1.roundsPlayed += 1
    player2.roundsPlayed += 1


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
    print(schedule)

    #TODO: Play rounds

    sum=0

    #   TODO: Calc avg
    #   TODO: Calc std. deviation
    #TODO: Output 1 round
    pass

if __name__ == '__main__':
    main()