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
            return True
        else:
            return False

class AlwaysExploit():
    def __init__(self):
        self.points=0

    def play():
        return True

def main():
    BOTH_EXPLOIT=4
    BOTH_COOPERATE=11
    OPP_EXPLOIT=2
    OPP_COOPERATE=7

    numPlayers=input("Input the number of players: ")
    print(numPlayers)
    fractionPR=input("Input the % of players playing PR: ")
    print(fractionPR)

    #TODO:Initialize Players
    #TODO: Play 1 Round
    #   TODO: Calc avg
    #   TODO: Calc std. deviation
    #TODO: Output 1 round
    pass

if __name__ == '__main__':
    main()