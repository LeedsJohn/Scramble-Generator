"""
John Leeds
5/25/2022
ScrambleGenerator.py

Takes a txt file of cube states and generates scrambles to that state.
Special thanks to hkociemba for his Rubik's Cube solver
https://github.com/hkociemba/RubiksCube-TwophaseSolver
"""

import json  # loading / dumping dictionaries
import random  # adding random moves before scrambles
import twophase.solver as sv  # https://github.com/hkociemba/RubiksCube-TwophaseSolver
import Mover

SOLVED_STATE = "UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB"
DATA_PATH = "./Data/"
MIN_MOVECOUNT = 8
NUM_SCRAMBLES = 3 # how many scrambles to generate for each case
VALID_MOVES = ("R", "U", "F", "L", "D", "B", "R'",
               "U'", "F'", "L'", "D'", "B'", "")
SOLVE_TIME = 1 # how long to give the solver to generate a solution
RANDOM_AUF = True # whether the orientation should be randomized

class ScrambleGenerator:
    def __init__(self, input_file, output_file):
        self.mover = Mover.Mover()
        self.input_file = input_file
        self.output_file = output_file
        self.states = self.getStates()
        self.scrambles = self.getScrambles()

    def getStates(self):
        """
        getStates
        Takes data from the input file and creates a list of states
        """
        with open(f"{DATA_PATH}{self.input_file}") as f:
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
                goalState = random.choice(self.states[state])
                scramble = self._getScramble(goalState, premoveCount)
                if self._scrambleLength(scramble) < MIN_MOVECOUNT or scramble not in scrambles[state]: # no duplicates
                    scrambles[state].append(scramble)
                    i += 1
                else:
                    premoveCount += 1
        return scrambles

    def writeScrambles(self):
        """
        Saves the scrambles json file
        """
        with open(f"{DATA_PATH}{self.output_file}", "w") as f:
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

        scramble = sv.solveto(SOLVED_STATE, updatedGoalstring, MIN_MOVECOUNT, SOLVE_TIME)
        scramble = self._fixScramble(scramble, postmoves)
        return scramble.strip()

    def _randomAUF(self, goalstring):
        """
        Performs a random number of U turns
        """
        self.mover.setCubelist(goalstring)
        for i in range(random.randrange(0,4)):
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

    def _fixScramble(self, scramble, postmoves):
        """
        Formats a scramble nicely
        """
        print(f"Scramble: {scramble}\tpostmoves: {postmoves}")
        # cut off the end (___f)
        scramble = scramble[:scramble.find("(")]
        scramble += postmoves
        scramble = scramble.split(" ")
        if "" in scramble:
            scramble.remove("")
        newScramble = []

        for move in scramble:
            print(f"newScramble: {newScramble}\tmove: {move}")
            if not newScramble:
                newScramble.append(move)
            elif not newScramble[-1] or newScramble[-1][0] != move[0]:
                suffix = self._rotationsToSuffix(self._turnsInAMove(move))
                newScramble.append(move[0] + suffix)
            else:
                totalTurns = self._turnsInAMove(
                    move) + self._turnsInAMove(newScramble[-1])
                if totalTurns % 4 == 0:
                    newScramble.pop()
                else:
                    newScramble[-1] = newScramble[-1][0] + self._rotationsToSuffix(totalTurns)

        for i, move in enumerate(newScramble): # TODO: this is a lazy fix
            if move[-1] == "3":
                newScramble[i] = move[0] + "'"
            elif move[-1] == "1":
                newScramble[i] = move[0]
        i = 0
        while True: # CROP LEADING U MOVES
            if newScramble[i][0] != 'U':
                return " ".join(newScramble[i:])
            i += 1

    def _turnsInAMove(self, move):
        """
        Determines how many times a cube face is rotated
        """
        if move[-1] == "2":
            return 2
        if move[-1] == "'" or move[-1] == '3':
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
