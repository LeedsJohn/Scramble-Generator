import twophase.solver as sv
import state_generators.ThreeStates as ThreeStates
import scramble_generators.ThreeScrambles as scrambler


def main():
    # algSets = {"PLL": "solved"}
    algSets = {"CMLL": "L4E", "COLL": "L4E", "ELL": "solved", "OLL": "PLL", "PLL": "solved", "WVLS_FL": "PLL", "WVLS": "PLL", "ZBLL_AS": "solved",
               "ZBLL_H": "solved", "ZBLL_L": "solved", "ZBLL_Pi": "solved", "ZBLL_S": "solved", "ZBLL_T": "solved", "ZBLL_U": "solved"}
    for algSet in algSets:
        print(algSet)
        state_gen = ThreeStates.StateGenerator(
            f"input/{algSet}.txt", f"states/{algSet}.json", algSets[algSet])
        state_gen.writeStates()

        scram_gen = scrambler.ScrambleGenerator(
            f"states/{algSet}.json", f"scrambles/{algSet}.json")
        scram_gen.writeScrambles()


if __name__ == "__main__":
    main()
