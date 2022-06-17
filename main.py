import twophase.solver as sv
import StateGenerator
import ScrambleGenerator as scrambler

def main():
    state_gen = StateGenerator.StateGenerator("WV.txt", "WV_states.json", "PLL")
    state_gen.writeStates()

    scram_gen = scrambler.ScrambleGenerator("WV_states.json", "WV_scrambles.json")
    scram_gen.writeScrambles()

if __name__ == "__main__":
    main()