"""
John Leeds
5/25/2022
TwoStates.py

Takes a text file of scrambles and creates a text file of cubestrings.
Written for a 2x2x2 Rubik's Cube.
"""
import json  # dumping dictionary
import movers.twoMover as mv

SOLVED_STATE = "UUUURRRRFFFFDDDDLLLLBBBB"
DATA_PATH = "Data/"


class StateGenerator:
    def __init__(self, fileName):
        self.mover = mv.Mover()
        self.name = f"{fileName}.json"
        self.scrambles = self.getScrambles()
        self.states = self.getStates()

    def getScrambles(self):
        """
        getScrambles
        Takes data from the input file and creates a dictionary of scrambles
        """
        with open(f"{DATA_PATH}input/Two/{self.name}") as f:
            scrambles = json.load(f)
        return {case: scrambles[case][0] for case in scrambles}
        return {scrambles[i].strip(): scrambles[i+1].strip() for i in range(0, len(scrambles), 2)}

    def getStates(self):
        """
        getStates
        Turns the list of scrambles into a dictionary of cubestrings by reversing the 
        scramble and applying it to a cube
        """
        states = {}
        startMoves = [""] # every case should have the empty scramble applied
        for name in self.scrambles:
            reversedCase = f"{self.mover.getNetRotations(self.scrambles[name])} {self.mover.reverse(self.scrambles[name])}"
            goalstates = []
            for startMove in startMoves:
                self.mover.setCubelist(SOLVED_STATE)
                self.mover.scramble(startMove)
                self.mover.scramble(reversedCase)
                goalstates.append(self.mover.getCubestring())
            states[name] = goalstates
        return states

    def writeStates(self):
        """
        writeStates
        Creates a .txt file with one cubestring per line.
        """
        with open(f"{DATA_PATH}states/Two/{self.name}", "w") as f:
            json.dump(self.states, f)