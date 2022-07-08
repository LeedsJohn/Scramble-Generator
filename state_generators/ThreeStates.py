"""
John Leeds
5/25/2022
StateGenerator.py

Takes a text file of scrambles and creates a text file of cubestrings
"""
import json  # dumping dictionary
import movers.ThreeMover as ThreeMover

SOLVED_STATE = "UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB"
DATA_PATH = "Data/"


class StateGenerator:
    def __init__(self, file_name, solve_to):
        self.mover = ThreeMover.Mover()
        self.input_file = f"{DATA_PATH}input/Three/{file_name}.json"
        self.output_file = f"{DATA_PATH}states/Three/{file_name}.json"
        self.solve_to = solve_to
        self.scrambles = self.getScrambles()
        self.states = self.getStates()
        # specify what stage to solve the cube to - solved, PLL, L4E (last four edges)

    def getScrambles(self):
        """
        getScrambles
        Takes data from the input file and creates a dictionary of scrambles
        """
        with open(self.input_file) as f:
            scrambles = json.load(f)
        return {case: scrambles[case][0] for case in scrambles}

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
        with open(self.output_file, "w") as f:
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
