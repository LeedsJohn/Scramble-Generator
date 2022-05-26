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

  def move(self, dir):
    """
    move
    Rotates the cube
    dir: str
      Which direction to rotate the cube. Valid directions: R, U, F, L, D, B
    """
    movePatterns = {"R": ((5, 48, 32, 23), (8, 45, 35, 26), (2, 51, 29, 20)),
                    "U": ((19, 37, 46, 10), (20, 38, 47, 11), (18, 36, 45, 9)),
                    "F": ((7, 12, 28, 41), (8, 15, 27, 38), (6, 9, 29, 44)),
                    "L": ((3, 21, 30, 50), (0, 18, 27, 53), (6, 24, 33, 47)),
                    "D": ((25, 16, 52, 43), (24, 15, 51, 42), (26, 17, 53, 44)),
                    "B": ((1, 39, 34, 14), (0, 42, 35, 11), (2, 36, 33, 17))}
    self.__swapStickers(movePatterns[dir])

  def scramble(self, scramble):
    for i, c in enumerate(scramble):
      if c in "RUFLDB":
        rotationCount = 1
        if i == len(scramble) - 1:
          rotationCount = 1
        elif scramble[i+1] == '2':
          rotationCount = 2
        elif scramble[i+1] == "'":
          rotationCount = 3
        
        for j in range(rotationCount):
          self.move(c)

  def getCubestring(self):
    """
    Converts the cubelist to a cubestring to be used with the Kociemba solver
    """
    return "".join(self.cubelist)

  def __swapStickers(self, movePattern):
    """
    swapStickers
    Helper function for move
    Rotates the stickers around the cube
    """
    cubelistCopy = self.cubelist.copy()
    print(f"cubelist OLD:  {self.cubelist}\ncubelist COPY: {cubelistCopy}\n-----------------")
    for piece in range(len(movePattern)):
      for i in range(len(movePattern[piece])):
        self.cubelist[movePattern[piece][i]] = cubelistCopy[movePattern[piece][i-1]]