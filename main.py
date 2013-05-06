#-------------------------------------------------------------------------------
# Name:        main
# Purpose:     Runs Prisoner's Dilemma
#
# Author:      David
#
# Created:     06/05/2013
#-------------------------------------------------------------------------------

class Player(object):
    """Base class for the two players"""
    def __init__(self, id):
        self.points=0
        self.id=id

    def __repr__(self):
        return  type(self).__name__ + " " + str(self.id)

class PermenantRetaliation(Player):
    """Permenant Retaliation player"""
    def __init__(self, id):
        super(PermenantRetaliation, self).__init__(id)
        self.beenExploited=[]

    def play(id):
        """plays a round against a player of id"""
        if(id in self.beenExploited):
            return True #Once exploited, returns true
        else:
            return False #Returns false until exploited

    def beenExploited(id):
        """plays a round against a player of id"""
        self.beenExploited.append(id)

class AlwaysExploit(Player):
    def __init__(self, id):
        super(AlwaysExploit, self).__init__(id)

    def play():
        return True #Always returns true

def playGame(player1, player2):
    #this will play a single round between 2 players
    pass

def scheduleMatches(players):
    schedule=[]
    for i in range(0, len(players)):
        for j in range(i+1, len(players)):
            schedule.append([players[i],players[j]])
    return schedule

def playRound(schedule):
    pass

def main():
    #Constants definining what happens after a single round
    BOTH_EXPLOIT=4
    BOTH_COOPERATE=11
    OPP_EXPLOIT=2
    OPP_COOPERATE=7

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