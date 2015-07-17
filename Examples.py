##############################################################################
#Copyright (C) 2015 Jacob Barhak
# 
#This file is part of Fair Tournament. The Fair Tournament is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
#
#Fair Tournament is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
#See the GNU General Public License for more details.
#############################################################################


import subprocess
import shlex
import sys

# THis file contanes some test examples to show tournamet generations with 
# different sizes to test the program


if __name__ == '__main__':
    # if output files are requested for summary and long files then 
    # open these files 
    if len(sys.argv)>=2:
        LongOutputFile = open(sys.argv[1],'w')
    else:
        LongOutputFile = None
    if len(sys.argv)>=3:
        SummaryOutputFile = open(sys.argv[2],'w')
    else:
        SummaryOutputFile = None
    
    TeamSizesAndRoundNumbers = [
                 ([2,2],5),
                 ([2,3],5),
                 ([3,3],5),
                 ([-3,-3],5),
                 ([2,4],5),
                 ([3,4],5),
                 ([2,2,2,2],5),
                 ([4,4],5),
                 ([-4,-4],5),
                 ([5,5],5),
                 ([4,4,4],5),
                 ([3,3,3,3],5),
                 ([4,4,4,4],5),
                 ([2,2],20),
                 ([2,3],20),
                 ([3,3],20),
                 ([-3,-3],20),
                 ([3,4],20),
                 ([-3,-4],20),
                 ([2,2,2,2],20),
                 ([4,4],20),
                 ([-4,-4],20),
                 ([5,5],20),
                 ([-5,-5],20),
                 ([4,4,4],20),
                 ([-4,-4,-4],20),
                 ([3,3,3,3],20),
                 ([-3,-3,-3,-3],20),
                 ([4,4,4,4],20),
                 ([-4,-4,-4,-4],20),
    ]
    
    for (TeamsSize,NumberOfRounds) in TeamSizesAndRoundNumbers:
        Out = ''
        Out = Out + '='*70 + '\n'
        Out = Out + '='*70 + '\n'
        Out = Out + '='*70 + '\n'
        Out = Out + 'Solving for team size '+ str(TeamsSize) + ' with ' + str(NumberOfRounds) +  ' rounds \n'
        CommandLineArguments = 'python Fair.py "' + str(TeamsSize)+ '" ' + str(NumberOfRounds)
        SplitArguments = shlex.split(CommandLineArguments)
        Process = subprocess.Popen(SplitArguments, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (StdOut,StdErr) = Process.communicate('cmd')
        Out = Out + 'Running the command:\n'
        Out = Out + CommandLineArguments + '\n'
        if LongOutputFile != None:
            LongOutputFile.write(Out +  StdOut)
        # For short output locate the important Output information after the #
        LocationWhereResultsStart = StdOut.index('#'*70)
        Out = Out + ' Result Summary is:\n' + StdOut[LocationWhereResultsStart:]
        print Out
        if SummaryOutputFile != None:
            SummaryOutputFile.write(Out)
    if LongOutputFile != None:
        LongOutputFile.close()
    if SummaryOutputFile != None:
        SummaryOutputFile.close()
