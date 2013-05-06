#-------------------------------------------------------------------------------
# Name:        main
# Purpose:     Runs Prisoner's Dilemma
#
# Author:      David
#
# Created:     06/05/2013
#-------------------------------------------------------------------------------

class PermenantRetaliation():
    def __init__(self, beenExploited):
        self.beenExploited = beenExploited
        self.points=0

    def play():
        if(beenExploited):
            return True #Once exploited, returns true
        else: 
            return False #Returns false until exploited

class AlwaysExploit():
    def __init__(self):
        self.points=0

    def play():
        return True #Always returns true

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

    numPR = int(float(numPlayers)/float(fractionPR))

    #Initialize Players
    for i in range(0, numPlayers):
    if i<numPR:
        players[i]=PermenantRetaliation()
    else:
        players[i]=AlwaysExploit()
    #TODO: Play 1 Round
    #   TODO: Calc avg
    #   TODO: Calc std. deviation
    #TODO: Output 1 round
    pass

if __name__ == '__main__':
    main()