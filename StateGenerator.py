"""
John Leeds
5/25/2022
StateGenerator.py

Takes a text file of scrambles and creates a text file of cubestrings
"""
import json # dumping dictionary
import Mover

SOLVED_STATE = "UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB"
DATA_PATH = "./Data/"

class StateGenerator:
    def __init__(self):
        self.mover = Mover.Mover()
        self.input_file = input("STATE GENERATOR - Enter the name of your input file: ")
        self.output_file = input("STATE GENERATOR - Enter the name of your output file: ")
        self.scrambles = self.getScrambles()
        self.states = self.getStates()

    def getScrambles(self):
        """
        getScrambles
        Takes data from the input file and creates a dictionary of scrambles
        """
        with open(f"{DATA_PATH}{self.input_file}") as f:
            scrambles = f.readlines()
        return {scrambles[i].strip():scrambles[i+1].strip() for i in range(0, len(scrambles), 2)}
    
    def getStates(self):
        """
        getStates
        Turns the list of scrambles into a dictionary of cubestrings by reversing the 
        scramble and applying it to a cube
        """
        states = {}
        for name in self.scrambles:
            self.mover.setCubelist(SOLVED_STATE)
            reversedScramble = self.mover.reverse(self.scrambles[name])
            self.mover.scramble(reversedScramble)
            states[name] = self.mover.getCubestring()
        return states

    def writeStates(self):
        """
        writeStates
        Creates a .txt file with one cubestring per line.
        """
        with open(f"{DATA_PATH}{self.output_file}", "w") as f:
            json.dump(self.states, f)