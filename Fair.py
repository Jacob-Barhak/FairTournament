##############################################################################
#Copyright (C) 2015 Jacob Barhak
# 
#This file is part of Fair Tournament. The Fair Tournament is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
#
#Fair Tournament is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
#See the GNU General Public License for more details.
#############################################################################


from __future__ import division
import sys
import copy
import random
from time import time
import inspyred


def CalculatePlayerSwaps(random, NumberOfPlayers):
    "Calculates a random set of player pair swaps"
    # Determine the number of swaps pairs - at least one 
    # and at most all players swap
    # note that odd numbers one player will always not sawp
    NumberOfSwapPairs = random.randint(1,NumberOfPlayers//2)
    # generate candidates
    PlayerPositions = list(range(NumberOfPlayers))
    Swaps = random.sample(PlayerPositions, NumberOfSwapPairs*2)
    # return a list of players swaped - each pair is a swap
    return Swaps


def Generator(random, args):
    "Generate solutions"
    TeamSizes = args['TeamSizes']
    MaxRounds = args['MaxRounds']
    NumberOfPlayers = sum(TeamSizes)
    GeneratedSwaps = [] 
    # Now calculate swaps for each round. Note that we need one kess
    # round of swaps then number of rounds since initial placing is
    # always 1:NumberPofPlayers
    for SwapNumber in range(MaxRounds-1):
        SwapsToNextRound = CalculatePlayerSwaps(random, NumberOfPlayers)
        GeneratedSwaps.append(SwapsToNextRound)
    return GeneratedSwaps

def ApplySwaps(CurrentPlayerVector,RoundSwaps):
    "Applies swaps to current player vector to deduce next round teams"
    RoundSwapsCopy = RoundSwaps[:]
    ReturnPlayerVector = CurrentPlayerVector[:]
    while RoundSwapsCopy != []:
        SwapPosition1 = RoundSwapsCopy.pop()
        SwapPosition2 = RoundSwapsCopy.pop()
        RememberPlayer1 = ReturnPlayerVector[SwapPosition1]
        ReturnPlayerVector[SwapPosition1] = ReturnPlayerVector[SwapPosition2]
        ReturnPlayerVector[SwapPosition2] = RememberPlayer1
    return ReturnPlayerVector




def PlayedWithPlayerCount(Player, TeamSizes, PreviousPlaysForPlayer, PlayerArrangementForRound):
    "Returns a vector of number of plays with player"
    # first locate the players team
    TeamStart = 0
    Team = None
    ReturnPlaysPerPlayer = PreviousPlaysForPlayer[:]
    for TeamSize in TeamSizes:
        Team = PlayerArrangementForRound[TeamStart:(TeamStart + TeamSize)]
        if Player in Team:
            for TeamPlayer in Team:
                ReturnPlaysPerPlayer[TeamPlayer] = ReturnPlaysPerPlayer[TeamPlayer] + 1
            break
        TeamStart = TeamStart + TeamSize
    assert Team != None
    return ReturnPlaysPerPlayer



def FullEvaluation(Candidate, TeamSizes, MaxRounds):
    "Score candidates composed of player swaps - output full results"
    NumberOfPlayers = sum(TeamSizes)    
    CurrentPlayerVector = list(range(NumberOfPlayers))
    Tournamentarrangement = [CurrentPlayerVector[:]]
    for RoundSwaps in Candidate:
        CurrentPlayerVector = ApplySwaps(CurrentPlayerVector,RoundSwaps)
        Tournamentarrangement.append(CurrentPlayerVector)
    # TBD, define score for tournament
    # first figure out who played with who how many times for each round
    # So create and initialize the tensor
    PlaysTensor = []
    for SwapNumber in range(MaxRounds):
        if SwapNumber == 0:
            PreviousPlays = [[0] * NumberOfPlayers]* NumberOfPlayers
        else:
            PreviousPlays = PlaysTensor[SwapNumber-1]
        PlaysMatrix = [ PlayedWithPlayerCount(Player, TeamSizes, PreviousPlays[Player], Tournamentarrangement[SwapNumber]) for Player in range(NumberOfPlayers)]
        PlaysTensor.append(PlaysMatrix)
    # Analyze the players tensor
    BestScoreForAllRounds = float('Inf')
    BestScoreRound = MaxRounds + 1
    ScoreBreakDownPerRound = []
    for SwapNumber in range(MaxRounds):
        # The base score is the round number to make sure that
        # the first round wiht the low score appears first
        BaseScore = SwapNumber
        # The second component of the score is checking if
        # every player is playing with another
        PlaysMatrix = PlaysTensor[SwapNumber]
        # At the same time collect information for the third criterion
        MaxPlays = 0
        MinPlays = MaxRounds+1
        for (Player,PlaysPerPlayer) in enumerate(PlaysMatrix):
            PlaysOfOtherPlayers = PlaysPerPlayer[:Player] + PlaysPerPlayer[Player+1:]
            for OtherPlayerCount in PlaysOfOtherPlayers:
                # use 100*MaxRounds squared since this is the most important 
                # condition to fulfill and we want it to to be significantly
                # Higer that other conditions
                BaseScore = BaseScore + (OtherPlayerCount == 0)*100*MaxRounds*MaxRounds
                MaxPlays = max(MaxPlays,OtherPlayerCount)
                MinPlays = min(MinPlays,OtherPlayerCount)            
        # The third component is the difference between plays
        # and  multiply it by MaxRounds to be higher than others
        BaseScore = BaseScore + (MaxPlays-MinPlays)*MaxRounds*10
        # Also register te score breakdown per round
        ScoreBreakDownPerRound.append([BaseScore,SwapNumber,PlaysMatrix,MaxPlays,MinPlays])
        if BaseScore < BestScoreForAllRounds:
            BestScoreForAllRounds = BaseScore
            # in human terms Round 1 is predetermined
            # therefore for SwapNumber zero we are calculating 
            # Round 2 - in other words, there is always a swap
            BestScoreRound = SwapNumber + 1
    return  (BestScoreForAllRounds, BestScoreRound, Tournamentarrangement, PlaysTensor, ScoreBreakDownPerRound)
    

@inspyred.ec.evaluators.evaluator
def Evaluator(Candidate, args):
    "Score candidtes composed of player swaps"
    # First recreate the team from the swaps
    TeamSizes = args['TeamSizes']
    MaxRounds = args['MaxRounds']
    # use full evaluation function
    (BestScoreForAllRounds, BestScoreRound, Tournamentarrangement, PlaysTensor, ScoreBreakDownPerRound) = FullEvaluation(Candidate, TeamSizes, MaxRounds)
    return BestScoreForAllRounds

@inspyred.ec.variators.crossover
def Crossover(random, Mom, Dad, args):
    "Crossover round swaps between two tournament solutions"
    Brother = copy.deepcopy(Dad[:])
    Sister = copy.deepcopy(Dad[:])
    for (Round, BrotherRoundSwaps) in enumerate(Brother):
        if random.random()<0.5:
            Brother[Round] = Sister[Round]
            Sister[Round] = BrotherRoundSwaps
    return Brother,Sister

@inspyred.ec.variators.mutator
def Mutator(random, Candidate, args):
    "Mutate swaps to add some variation"
    TeamSizes = args['TeamSizes']
    NumberOfPlayers = sum(TeamSizes)    
    MutationRate = args['mutation_rate']
    Mutated = copy.deepcopy(Candidate)
    for (Round, RoundSwaps) in enumerate(Mutated):
        if random.random() < MutationRate:
            Mutated[Round] = CalculatePlayerSwaps(random, NumberOfPlayers)
    return Mutated
   

def ApplyEvolutionaryComputation(TeamSizes,MaxRounds,RandomSeed):
    if RandomSeed is None:
        RandomSeedToUse = random.Random()
        RandomSeedToUse.seed(time()) 
    Players = list(range(sum(TeamSizes)))
    ea = inspyred.ec.EvolutionaryComputation(RandomSeedToUse)
    ea.selector = inspyred.ec.selectors.tournament_selection
    ea.variator = [Crossover, Mutator]
    ea.replacer = inspyred.ec.replacers.generational_replacement
    ea.terminator = inspyred.ec.terminators.generation_termination
    ea.observer = inspyred.ec.observers.stats_observer
    FinalPopulation = ea.evolve(generator=Generator,
                          evaluator=Evaluator,
                          pop_size=10000, 
                          bounder=inspyred.ec.DiscreteBounder(Players),
                          maximize=False,
                          tournament_size=7,
                          num_selected=2, 
                          num_elites=1,
                          max_generations=10000,
                          mutation_rate=0.1,
                          TeamSizes=TeamSizes,
                          MaxRounds=MaxRounds)
    BestCandidate = max(FinalPopulation) 
    (BestScoreForAllRounds, BestScoreRound, Tournamentarrangement, PlaysTensor, ScoreBreakDownPerRound) = FullEvaluation(BestCandidate.candidate, TeamSizes, MaxRounds)
    return ea,FinalPopulation, BestScoreForAllRounds, BestScoreRound, Tournamentarrangement, PlaysTensor, ScoreBreakDownPerRound

def PrintResults(TeamSizes,MaxRounds,AllEvolutionaryComuptationResults):
    "Output results nicely"    
    (ea,FinalPopulation, BestScoreForAllRounds, BestScoreRound, Tournamentarrangement, PlaysTensor, ScoreBreakDownPerRound) = AllEvolutionaryComuptationResults
    print '#'*70
    print '#'*70
    print 'Scores:'
    for [BaseScore,SwapNumber,PlaysMatrix,MaxPlays,MinPlays] in ScoreBreakDownPerRound:
        print 'Swap # %2i , Score %8g , Min Plays %2i , Max Plays %2i'% (SwapNumber,BaseScore,MinPlays,MaxPlays)
        print 'Full Play Matrix was:'
        for Row in PlaysMatrix:
            print Row
        # If we reached optimum solution do not show the rest
        if SwapNumber == BaseScore:
            print 'Assuming this is the optimal solution and not showing further rounds !!!'
            break
    print 
    print 'Best Score'
    print BestScoreForAllRounds
    print 'Achieved in round'
    print BestScoreRound
    if BestScoreForAllRounds <= MaxRounds :
        print 'This may very well be the optimal solution !!!'
    else:
        print 'This is not an optimal solution - increasing MaxRounds may improve result'

    for (SwapNumber,RoundPlacements) in enumerate(Tournamentarrangement):
        print '#'*70        
        print 'Round Number %i player arrangement:'%(SwapNumber+1)
        TeamStart = 0
        for (TeamEnum,TeamSize) in enumerate(TeamSizes):
            Team = RoundPlacements[TeamStart:(TeamStart + TeamSize)]
            print '  Team %2i: %s' % ((TeamEnum+1),str(Team))
            TeamStart = TeamStart + TeamSize
        if SwapNumber == BestScoreRound:
            print '$'*40
            print 'Use Above for Best Solution'
            if BestScoreForAllRounds <= MaxRounds:
                break
                print 'Assuming optimal solution - not printing anymore'
            print '$'*40
    print '#'*70        


if __name__ == '__main__':
    Args = sys.argv
    TeamSizes = eval(Args[1])
    MaxRounds = eval(Args[2])
    if len(Args) == 4:
        RandomSeed = eval(Args[3])
    else:
        RandomSeed = None
    AllEvolutionaryComuptationResults = ApplyEvolutionaryComputation(TeamSizes,MaxRounds,RandomSeed)
    PrintResults(TeamSizes,MaxRounds,AllEvolutionaryComuptationResults)

    
    

