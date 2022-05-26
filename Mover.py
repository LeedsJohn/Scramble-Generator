"""
John Leeds
5/25/2022
Mover.py

Contains a class to apply moves to a Rubik's cube
Uses syntax from https://github.com/hkociemba/RubiksCube-TwophaseSolver
"""


class Mover:
    def __init__(self, cubestring = ""):
        self.cubelist = list(cubestring)

    def __str__(self):
        stringCube = ""
        uCount = 0
        for row in range(3):
            stringCube += "    " + \
                "".join(self.cubelist[uCount:uCount + 3]) + '\n'
            uCount += 3

        lCount = 36
        fCount = 18
        rCount = 9
        bCount = 45
        for row in range(3):
            stringCube += ("".join(self.cubelist[lCount:lCount + 3]) + ' ' +
                           "".join(self.cubelist[fCount:fCount + 3]) + ' ' +
                           "".join(self.cubelist[rCount:rCount + 3]) + ' ' +
                           "".join(self.cubelist[bCount:bCount + 3]) + '\n')
            lCount += 3
            rCount += 3
            bCount += 3
            fCount += 3

        dCount = 27
        for row in range(3):
            stringCube += "    " + \
                "".join(self.cubelist[dCount:dCount + 3]) + '\n'
            dCount += 3

        return stringCube

    def move(self, dir):
        """
        move
        Rotates the cube
        dir: str
          Which direction to rotate the cube. Valid directions: R, U, F, L, D, B
        """
        movePatterns = {"R": (1, (5, 48, 32, 23), (8, 45, 35, 26), (2, 51, 29, 20)),
                        "U": (0, (19, 37, 46, 10), (20, 38, 47, 11), (18, 36, 45, 9)),
                        "F": (2, (7, 12, 28, 41), (8, 15, 27, 38), (6, 9, 29, 44)),
                        "L": (4, (3, 21, 30, 50), (0, 18, 27, 53), (6, 24, 33, 47)),
                        "D": (3, (25, 16, 52, 43), (24, 15, 51, 42), (26, 17, 53, 44)),
                        "B": (5, (1, 39, 34, 14), (0, 42, 35, 11), (2, 36, 33, 17))}
        self.__swapStickers(movePatterns[dir][1:], movePatterns[dir][0]*9)

    def scramble(self, scramble):
        """
        scramble
        receives a set of moves and applies them to the cube
        """
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

    def reverse(self, scramble):
        """
        Receives a set of moves and returns the inverse
        Ex: "R U D' L F2" --> "F2 L' D U' R'"
        """
        reversed = ""
        prev = "*"
        for c in scramble[::-1]:
            if c in "RUFLDB":
                reversed += c
                if prev == ' ':
                    reversed += "'"
                elif prev == "2":
                    reversed += "2"
                reversed += ' '
            prev = c
        return reversed.strip()

    def getCubestring(self):
        """
        Converts the cubelist to a cubestring to be used with the Kociemba solver
        """
        return "".join(self.cubelist)

    def setCubelist(self, cubestring):
        self.cubelist = list(cubestring)

    def __swapStickers(self, movePattern, start):
        """
        swapStickers
        Helper function for move
        Rotates the stickers around the cube
        """
        FACE_ROTATION = ((1, 5, 7, 3), (0, 2, 8, 6))

        cubelistCopy = self.cubelist.copy()
        for piece in range(len(movePattern)):
            for i in range(len(movePattern[piece])):
                self.cubelist[movePattern[piece][i]
                              ] = cubelistCopy[movePattern[piece][i-1]]

        for piece in range(2):
            for i in range(4):
                self.cubelist[FACE_ROTATION[piece][i] +
                              start] = cubelistCopy[FACE_ROTATION[piece][i-1] + start]
