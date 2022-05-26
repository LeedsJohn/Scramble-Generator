import twophase.solver as sv
import Mover
import StateGenerator
import ScrambleGenerator as scrambler

def main():
    state_gen = StateGenerator.StateGenerator()
    state_gen.writeStates()

    scram_gen = scrambler.ScrambleGenerator()
    scram_gen.writeScrambles()

if __name__ == "__main__":
    main()