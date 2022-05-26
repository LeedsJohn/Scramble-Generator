"""
John Leeds
5/25/2022
Mover.py

Contains a class to apply moves to a Rubik's cube
Uses syntax from https://github.com/hkociemba/RubiksCube-TwophaseSolver
"""

class Mover:

  def __init__(self, cubestring):
    self.cubelist = list(cubestring)

  def swapStickers(self, movePattern):
    cubelistCopy = self.cubelist.copy()
    for piece in range(len(movePattern)):
      for i in range(len(movePattern[piece])):
        self.cubelist[movePattern[piece][i]] = cubelistCopy[movePattern[piece][i-1]]

  def move(self, dir):
    """
    move
    dir: str
      Which direction to rotate the cube. Valid directions: R, U, F, L, D, B
    """
    movePatterns = {"R": ((5, 48, 32, 23), (8, 45, 35, 26), (2, 51, 29, 20)),
                    "U": ((19, 37, 46, 10), (20, 38, 47, 11), (18, 36, 45, 9)),
                    "F": ((7, 12, 28, 41), (8, 15, 27, 38), (6, 9, 29, 44)),
                    "L": ((3, 21, 30, 50), (0, 18, 27, 53), (6, 24, 33, 47)),
                    "D": ((25, 16, 52, 43), (24, 15, 51, 42), (26, 17, 53, 44)),
                    "B": ((1, 39, 34, 14), (0, 42, 35, 11), (2, 36, 33, 17))}
    self.swapStickers(movePatterns[dir])

  def getCubestring(self):
    """
    Converts the cubelist to a cubestring to be used with the Kociemba solver
    """
    return "".join(self.cubelist)
