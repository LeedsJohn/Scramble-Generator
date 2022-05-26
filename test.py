import twophase.solver as sv
import Mover
import StateGenerator
import ScrambleGenerator as scrambler

# john = StateGenerator.StateGenerator()
# john.writeStates()

john = scrambler.ScrambleGenerator()
john.writeScrambles()


# solved = 'UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB'
# scramble = "F' L' U F2 R' U2 F R' L2 D2 L2 F2 U2 B D2 B U2 R2 F L2"
# john = Mover.Mover(solved)
# john.scramble(scramble)
# print(f"\n\nREVERSED: {john.reverse(scramble)}\n")
# john.scramble(john.reverse(scramble))
# print(john)
