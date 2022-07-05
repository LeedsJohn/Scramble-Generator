"""
John Leeds
5/25/2022
ScrambleGenerator.py

Takes a txt file of cube states and generates scrambles to that state.
Special thanks to hkociemba for his Rubik's Cube solver
https://github.com/hkociemba/Rubiks2x2x2-OptimalSolver
"""

import json  # loading / dumping dictionaries
import random  # adding random moves before scrambles
import solvers.TwoSolver.solver as sv # https://github.com/hkociemba/Rubiks2x2x2-OptimalSolver
import movers.twoMover as mv

SOLVED_STATE = "UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB"
DATA_PATH = "Data/"
MIN_MOVECOUNT = 6
NUM_SCRAMBLES = 5 # how many scrambles to generate for each case
VALID_MOVES = ("R", "U", "F", "R'",
               "U'", "F'", "")
RANDOM_AUF = True # whether the orientation should be randomized

class ScrambleGenerator:
    def __init__(self, name):
        self.mover = mv.Mover()
        self.input_file = f"{DATA_PATH}states/Two/{name}.json"
        self.output_file = f"{DATA_PATH}scrambles/Two/{name}.json"
        self.states = self.getStates()
        self.scrambles = self.getScrambles()

    def getStates(self):
        """
        getStates
        Takes data from the input file and creates a list of states
        """
        with open(self.input_file) as f:
            states = json.load(f)
        return states

    def getScrambles(self):
        """
        Takes the list of states and generates scrambles to each state
        """
        scrambles = {}
        for state in self.states:
            premoveCount = 0
            print(state)
            scrambles[state] = []
            i = 0
            while i < NUM_SCRAMBLES:
                addPremove = False
                goalState = random.choice(self.states[state])
                check = self._getScramble(goalState, premoveCount)
                for scramble in check:
                    if self._scrambleLength(scramble) >= MIN_MOVECOUNT and scramble not in scrambles[state]: # no duplicates
                        scrambles[state].append(scramble)
                        i += 1
                    else:
                        addPremove = True
                if addPremove:
                    premoveCount += 1
        return scrambles

    def writeScrambles(self):
        """
        Saves the scrambles json file
        """
        with open(self.output_file, "w") as f:
            json.dump(self.scrambles, f)

    def _getScramble(self, goalstring, premoveCount):
        """
        Generates a scramble to a state with several premoves appended
        """
        if RANDOM_AUF:
            goalstring = self._randomAUF(goalstring)
        premoves = self._getPremove(premoveCount)
        postmoves = self.mover.reverse(premoves)
        self.mover.setCubelist(goalstring)
        self.mover.scramble(premoves)
        updatedGoalstring = self.mover.getCubestring()

        scrambles = sv.solve(updatedGoalstring)
        scrambles = scrambles.split("\r\n")[:-1]
        fixed = []
        for scramble in scrambles:
            fixedScramble = self._fixScramble(scramble, premoves, True).strip()
            fixed.append(fixedScramble)
        return fixed

    def _randomAUF(self, goalstring):
        """
        Performs a random number of U turns
        """
        self.mover.setCubelist(goalstring)
        for i in range(random.randrange(0, 4)):
            self.mover.move("U")
        return self.mover.getCubestring()

    def _getPremove(self, numMoves=2):
        """
        Returns a string of a designated number of random moves
        """
        premoves = ""
        for i in range(numMoves):
            premoves += random.choice(VALID_MOVES)
            premoves += ' '
        return premoves.strip(' ')

    def _fixScramble(self, scramble, premoves, cropLeadingU = True):
        """
        Formats a scramble nicely
        """
        # cut off the end (___f)
        scramble = scramble[:scramble.find("(")]
        scramble = f"{premoves} {scramble}"
        scramble = scramble.split(" ")
        scramble = [move for move in scramble if move] # crop blank strings
        moveFormat = [[scramble[0][0], self._turnsInAMove(scramble[0])]]
        # turn scramble into a list of moves and how many times it was rotated
        for move in scramble[1:]:
            dir = move[0]
            turns = self._turnsInAMove(move)
            if dir == moveFormat[-1][0]:
                moveFormat[-1][1] += turns
            else:
                moveFormat.append([dir, turns])
        
        newScramble = []
        for move in moveFormat:
            turn = move[0] + self._rotationsToSuffix(move[1])
            newScramble.append(turn)


        print(f"before reverse: {' '.join(newScramble)}")
        newScramble = self.mover.reverse(" ".join(newScramble)).split(" ")
        print(f"After: {' '.join(newScramble)}")
        if cropLeadingU:
            i = 0
            while True:  # CROP LEADING U MOVES
                if newScramble[i][0] != 'U':
                    newScramble = " ".join(newScramble[i:])
                    break
                i += 1
        else:
            newScramble = " ".join(newScramble)
        
        return newScramble

    def _turnsInAMove(self, move):
        """
        Determines how many times a cube face is rotated
        """
        if move[-1].isnumeric():
            return int(move[-1])
        elif move[-1] == "'":
            return 3
        return 1

    def _rotationsToSuffix(self, numRotations):
        numRotations = numRotations % 4
        if numRotations == 0 or numRotations == 1:
            return ''
        if numRotations == 3:
            return "'"
        if numRotations == 2:
            return '2'

    def _scrambleLength(self, scramble):
        """
        _scrambleLength(scramble)
        Returns the move count of a scramble
        """
        moveCount = 0
        for c in scramble:
            if c in "RUFLDB":
                moveCount += 1
        return moveCount
