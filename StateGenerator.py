"""
John Leeds
5/25/2022
StateGenerator.py

Takes a text file of scrambles and creates a text file of cubestrings
"""
import Mover

DATA_PATH = "./Data/"

class StateGenerator:
    def __init__(self):
        self.mover = Mover.Mover()
        self.input_file = input("Enter the name of your input file: ")
        self.output_file = input("Enter the name of your output file: ")
        self.scrambles = self.getScrambles()
        self.states = self.getStates()

    def getScrambles(self):
        """
        getScrambles
        Takes data from the input file and creates a list of scrambles
        """
        with open(f"{DATA_PATH}{self.input_file}") as f:
            scrambles = f.readlines()
        return scrambles
    
    def getStates(self):
        """
        getStates
        Turns the list of scrambles into a list of cubestrings by reversing the 
        scramble and applying it to a cube
        """
        SOLVED_STATE = "UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB"
        states = []
        for scramble in self.scrambles:
            self.mover.setCubelist(SOLVED_STATE)
            reversedScramble = self.mover.reverse(scramble)
            self.mover.scramble(reversedScramble)
            states.append(self.mover.getCubestring())
        return states

    def writeStates(self):
        """
        writeStates
        Creates a .txt file with one cubestring per line.
        """
        with open(f"{DATA_PATH}{self.output_file}", "w") as f:
            for state in self.states:
                f.write(f"{state}\n")