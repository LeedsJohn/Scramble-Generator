import state_generators.ThreeStates as ThreeStates
import state_generators.TwoStates as TwoStates
import scramble_generators.ThreeScrambles as ThreeScrambles
import scramble_generators.TwoScrambles as TwoScrambles


def main():
    three = {}
    # three = {"CMLL": "L4E", "COLL": "L4E", "ELL": "solved", "OLL": "PLL", "PLL": "solved", "WVLS_FL": "PLL", "WVLS": "PLL", "ZBLL_AS": "solved",
    #            "ZBLL_H": "solved", "ZBLL_L": "solved", "ZBLL_Pi": "solved", "ZBLL_S": "solved", "ZBLL_T": "solved", "ZBLL_U": "solved"}
    # two = ["bruh"]
    two = ["CLL", "EG-1", "EG-2", "Ortega_OLL", "Ortega_PBL"]
    for algSet in two:
        print(algSet)
        state_gen = TwoStates.StateGenerator(algSet)
        state_gen.writeStates()

        scram_gen = TwoScrambles.ScrambleGenerator(algSet)
        scram_gen.writeScrambles()

    for algSet in three:
        print(algSet)
        state_gen = ThreeStates.StateGenerator(algSet, three[algSet])
        state_gen.writeStates()

        scram_gen = ThreeScrambles.ScrambleGenerator(algSet)
        scram_gen.writeScrambles()


if __name__ == "__main__":
    main()
