Fair Tournament 
===============

This system attempts to create a fair tournament with M teams with N1,N2..Nm players in each team.

We want to determine who is the best player by running at most MaxRounds rounds with all games plated in parallel and rotating teams.

We want: 
 1. Each player to play with all other players, i.e. be on the same team with them. 
 2. Each player plays the same number of games with each other player. 
 3. Teams play in parallel and we want minimal number of games

For example for 2 teams of 2 players the solution is:

* Game 1:  
 Team 1: A B  
 Team 2: C D  

* Game 2:  
 Team 1: A D  
 Team 2: C B  

* Game 3:  
 Team 1: A C  
 Team 2: B D  

So each player plays 2 games with each other player and 3 rounds are required. 

It seems like an NP hard problem with elements simialr to the traveling salesman problem. Yet no reduction was attempted, so we cannot be sure.

The solution approach taken uses Evolutionary Computation using [Inpyred] (https://github.com/aarongarrett/inspyred).

The inputs are:
* TeamSizes vector - this list defines team sizes. For example the e=above example would show [2,2]
* MaxRounds - an integer defining the maximum number of rounds in the tournament

The output is:
A list of player swaps after each tournament round
Statistics about tournament fairness each round



DEVELOPER CONTACT INFO:
-----------------------

Jacob Barhak Ph.D.

Email: jacob.barhak@gmail.com

http://sites.google.com/site/jacobbarhak/



ACKNOWLEDGEMENTS:
-----------------
Thanks to Aaron Garrett for bouncing ideas and creating Inspyred.


LICENSE
-------

Copyright (C) 2015 Jacob Barhak
 
This file is part of Fair Tournament. The Fair Tournament is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

Fair Tournament is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

See the GNU General Public License for more details.





