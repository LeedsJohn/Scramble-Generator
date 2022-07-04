"""
John Leeds
7/4/twoMover.py

Contains a class to apply moves to a 2x2x2 Rubik's cube
Uses syntax from https://github.com/hkociemba/Rubiks2x2x2-OptimalSolver
"""


class Mover:
    def __init__(self, cubestring=""):
        self.cubelist = list(cubestring)

    def __str__(self):
        print(self.cubelist)
        stringCube = ""
        uCount = 0
        for row in range(2):
            stringCube += "   " + \
                "".join(self.cubelist[uCount:uCount + 2]) + '\n'
            uCount += 2

        lCount = 16
        fCount = 8
        rCount = 4
        bCount = 20
        for row in range(2):
            stringCube += ("".join(self.cubelist[lCount:lCount + 2]) + ' ' +
                           "".join(self.cubelist[fCount:fCount + 2]) + ' ' +
                           "".join(self.cubelist[rCount:rCount + 2]) + ' ' +
                           "".join(self.cubelist[bCount:bCount + 2]) + '\n')
            lCount += 2
            rCount += 2
            bCount += 2
            fCount += 2

        dCount = 12
        for row in range(2):
            stringCube += "   " + \
                "".join(self.cubelist[dCount:dCount + 2]) + '\n'
            dCount += 2

        return stringCube

    def move(self, dir):
        """
        move
        Rotates the cube
        dir: str
          Which direction to rotate the cube. Valid directions: R, U, F, L, D, B, 
          x, y, z
        """
        movePatterns = {"R": (1, (3, 20, 15, 11), (1, 22, 13, 9)),
                        "U": (0, (8, 16, 20, 4), (9, 17, 21, 5)),
                        "F": (2, (2, 4, 13, 19), (3, 6, 12, 17)),
                        "L": (4, (0, 8, 12, 23), (2, 10, 14, 21)),
                        "D": (3, (10, 6, 22, 18), (11, 7, 23, 19)),
                        "B": (5, (0, 18, 15, 5), (1, 16, 14, 7))}
        translations = {"y": "U D'", "x": "R L'", "z": "F B'"}

        if dir in "RUFLDB":
            self.__swapStickers(movePatterns[dir][1:], movePatterns[dir][0]*4)

        elif dir in "yxz":
            self.scramble(translations[dir])

    def scramble(self, scramble, orient = False):
        """
        scramble
        receives a set of moves and applies them to the cube
        """
        for i, c in enumerate(scramble):
            if c in "RUFLDBxyz":
                rotationCount = 1
                if i == len(scramble) - 1:
                    rotationCount = 1
                elif scramble[i+1] == '2':
                    rotationCount = 2
                elif scramble[i+1] == "'":
                    rotationCount = 3

                for j in range(rotationCount):
                    self.move(c)
        if orient:
            self.__orient()

    def reverse(self, scramble):
        """
        Receives a set of moves and returns the inverse
        Ex: "R U D' L F2" --> "F2 L' D U' R'"
        """
        reversed = ""
        prev = "*"
        for c in scramble[::-1]:
            if c in "RUFLDBxyz":
                reversed += c
                if prev == ' ' or prev == '*':
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

    def getNetRotations(self, scramble):
        """
        getNetRotations(scramble)
        Returns a string representing the rotations needed to get to the end
        orientation of the scramble.
        """
        rotations = []
        scramble = scramble.split()
        rotationDirections = {"x": ["x", "r", "l'", "M'"], "x'": ["x'", "r'", "l", "M"],
                              "x2": ["x2", "r2", "l2", "M2"], "y": ["y", "u", "d'", "E'"],
                              "y'": ["y'", "u'", "u", "E"], "y2": ["y2", "u2", "d2", "E2"],
                              "z": ["z", "f", "b'", "S"], "z'": ["z'", "f'", "b", "S'"],
                              "z2": ["z2", "f2", "b2", "S2"]}
        for move in scramble:
            for dir in rotationDirections:
                if move in rotationDirections[dir]:
                    rotations.append(dir)
                    break
        return " ".join(rotations)


    def __swapStickers(self, movePattern, start):
        """
        swapStickers
        Helper function for move
        Rotates the stickers around the cube
        """
        FACE_ROTATION = (0, 1, 3, 2)

        cubelistCopy = self.cubelist.copy()
        for piece in range(len(movePattern)):
            for i in range(len(movePattern[piece])):
                self.cubelist[movePattern[piece][i]
                              ] = cubelistCopy[movePattern[piece][i-1]]
                              
        for i in range(4):
            self.cubelist[FACE_ROTATION[i] +
                            start] = cubelistCopy[FACE_ROTATION[i-1] + start]