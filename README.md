Fair Tournament 
===============
This project demonstrates the use of Evolutionary Computation for a tournament planning optimization problem with a large solution space.

This system attempts to create a fair tournament with M teams with N1,N2..Nm players in each team.

We want to determine who is the best player by running at most MaxRounds rounds with all games played in parallel and rotating teams.

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

It seems like an NP hard problem with elements similar to the traveling salesman problem. Yet no reduction was attempted, so we cannot be sure.

The solution approach taken uses Evolutionary Computation using [Inpyred] (https://github.com/aarongarrett/inspyred).




USAGE:
------
python Fair.py TeamSizes MaxRounds [RandomSeed] [PopSize] [MaxGen]

The inputs are:
* TeamSizes - this list defines team sizes. For example the above example would show [2,2]. A negative team size means that there is a judge in that team that does not swap positions.
* MaxRounds - an integer defining the maximum number of rounds in the tournament
* RandomSeed - an optional parameter to set Random seed of computations - if missing timer is used
* PopSize - defines the population size - default 100"
* MaxGen - defines the number of generations - default 1000"

The output is:
* A list of player at each team for each tournament round
* Statistics about tournament fairness each round

EXAMPLE:
--------
To solve the 2 team problem above using the program type:
python Fair.py [2,2] 5


FILES:
------
Fair.py : Main file with calculations
Readme.md : The file that you are reading now
Examples.py : Test suit with examples that test the application


VERSION HISTORY:
----------------
Development started on 2nd July 2015.
Fixes towards PyCon Israel on 30th May 2018 and on 4th June 2018.


DEVELOPER CONTACT INFO:
-----------------------

Jacob Barhak Ph.D.

Email: jacob.barhak@gmail.com

http://sites.google.com/site/jacobbarhak/



ACKNOWLEDGEMENTS:
-----------------
Thanks to Aaron Garrett for bouncing ideas and creating Inspyred.
Thanks to Robert Myers who runs Julython that helped speed things up:
http://www.julython.org/

LICENSE
-------

Copyright (C) 2015, 2018 Jacob Barhak
 
This file is part of Fair Tournament. The Fair Tournament is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

Fair Tournament is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

See the GNU General Public License for more details.





