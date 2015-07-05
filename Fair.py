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
import random
from time import time
import inspyred


def CalculatePlayerSwaps(NumberOfPlayers):
    "Calculates a random set of player pair swaps"
    # Determine the number of swaps pairs - at least one 
    # and at most all players swap
    # note that odd numbers one player will always not sawp
    NumberOfSwapPairs = random.randint(1,NumberOfPlayers/2)
    # generate candidates
    Candidates = list(range(NumberOfPlayers))
    Swaps = random.sample(Candidates, NumberOfSwapPairs*2)
    # return a list of players swaped - each pair is a swap
    return Swaps


def Generator(Random, args):
    "Generate solutions"
    TeamSizes = args['TeamSizes']
    MaxRounds = args['MaxRounds']
    NumberOfPlayers = sum(TeamSizes)
    GeneratedSwaps = [] 
    # Now calculate swaps for each round. Note that we need one kess
    # round of swaps then number of rounds since initial placing is
    # always 1:NumberPofPlayers
    for RoundCount in range(MaxRounds-1):
        SwapsToNextRound = CalculatePlayerSwaps(NumberOfPlayers)
        GeneratedSwaps.append(SwapsToNextRound)
    return GeneratedSwaps


@inspyred.ec.evaluators.evaluator
def Evaluator(Candidate, args):
    "Custom evaluator"
    Error = 0
    return Error

@inspyred.ec.variators.crossover
def Crossover(Random, Mom, Dad, args):
    "Custom crossover"
    Brother,Sister = None,None
    return Brother,Sister

@inspyred.ec.variators.mutator
def Mutator(Random, Candidate, args):
    "Custom Mutator"
    Muteted = None
    return Muteted
   

def main(TeamSizes,MaxRounds,RandomSeed):
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
    final_pop = ea.evolve(generator=Generator,
                          evaluator=Evaluator,
                          pop_size=100, 
                          bounder=inspyred.ec.DiscreteBounder(Players),
                          maximize=False,
                          tournament_size=7,
                          num_selected=2, 
                          num_elites=1,
                          max_generations=300,
                          mutation_rate=0.1,
                          TeamSizes=TeamSizes,
                          MaxRounds=MaxRounds)

    return ea,final_pop

if __name__ == '__main__':
    Args = sys.argv
    TeamSizes = eval(Args[1])
    MaxRounds = eval(Args[2])
    if len(Args) == 3:
        RandomSeed = eval(Args[3])
    else:
        RandomSeed = None
    main(TeamSizes,MaxRounds,RandomSeed)

