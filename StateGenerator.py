"""
John Leeds
5/25/2022
StateGenerator.py

Takes a text file of scrambles and creates a text file of cubestrings
"""
import json  # dumping dictionary
import Mover

SOLVED_STATE = "UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB"
DATA_PATH = "./Data/"


class StateGenerator:
    def __init__(self, input_file, output_file, solve_to):
        self.mover = Mover.Mover()
        self.input_file = input_file
        self.output_file = output_file
        self.solve_to = solve_to
        self.scrambles = self.getScrambles()
        self.states = self.getStates()
        # specify what stage to solve the cube to - solved, PLL, L4E (last four edges)

    def getScrambles(self):
        """
        getScrambles
        Takes data from the input file and creates a dictionary of scrambles
        """
        with open(f"{DATA_PATH}{self.input_file}") as f:
            scrambles = f.readlines()
        return {scrambles[i].strip(): scrambles[i+1].strip() for i in range(0, len(scrambles), 2)}

    def getStates(self):
        """
        getStates
        Turns the list of scrambles into a dictionary of cubestrings by reversing the 
        scramble and applying it to a cube
        """
        states = {}
        startMoves = [""] # every case should have the empty scramble applied
        if self.solve_to == "PLL":
            startMoves += self._getPLLs()
        elif self.solve_to == "L4E":
            startMoves += self._getEdgePLLs()

        for name in self.scrambles:
            reversedCase = self.mover.reverse(self.scrambles[name])
            goalstates = []
            for startMove in startMoves:
                self.mover.setCubelist(SOLVED_STATE)
                reversedStartMove = self.mover.reverse(startMove)
                self.mover.scramble(reversedStartMove, True)
                self.mover.scramble(reversedCase, True)
                goalstates.append(self.mover.getCubestring())
            states[name] = goalstates
        return states

    def writeStates(self):
        """
        writeStates
        Creates a .txt file with one cubestring per line.
        """
        with open(f"{DATA_PATH}{self.output_file}", "w") as f:
            json.dump(self.states, f)

    def _getPLLs(self):
        """
        _getPLLs()
        returns a list of scrambles to PLLs
        """
        pll = self._readPLL()
        return [pll[case].strip() + " " for case in pll]

    def _getEdgePLLs(self):
        """
        _getEdgePLLs()
        Returns a list of scrambles to edge PLLs
        """
        pll = self._readPLL()
        return [pll[case].strip() + " " for case in pll if case in ("Ua", "Ub", "Z", "H")]
    
    def _readPLL(self):
        """
        _readPLL()
        Reads the pll.txt file into a dictionary
        ["case name": solution]
        """
        with open('pll.txt') as f:
            text = f.readlines()
            return {text[i]: text[i+1] for i in range(0, len(text), 2)}
