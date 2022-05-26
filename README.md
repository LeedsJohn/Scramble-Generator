# Scramble-Generator
Generates scrambles to a specific state using Hebert Kociemba's two phase solver. This project would not be possible without his work which you can see here:

https://github.com/hkociemba/RubiksCube-TwophaseSolver

I wrote this project to generate scrambles to specific states for an algorithm trainer. 

# Usage
In the Data folder, create a .txt file containing the name of the algorithm and the algorithm on alternating lines:

![image](https://user-images.githubusercontent.com/94880155/170574452-0d9a23a7-c76c-4d87-aece-728392d319d9.png)

From this, you can use StateGenerator.py to create a file with the end states that you would like to generate scrambles to. These end states are represented in the same way that Herbert Kociemba represents Rubik's cubes 

![image](https://user-images.githubusercontent.com/94880155/170574572-b854104f-86e8-4e7f-802f-db70c87d90a8.png)

Finally, you can use this file to create a json file of scrambles using ScrambleGenerator.py:

![image](https://user-images.githubusercontent.com/94880155/170575088-457d5bb4-7199-4dc6-9469-c7d1c8ba3150.png)

# Options
In ScrambleGenerator.py, there are several options you can change.

NUM_SCRAMBLES: this number represents how many scrambles will be generated for each algorithm.

SOLVE_TIME: how much time you give the cube solver to find a solution

MOVE_COUNT: a desired move count - the cube solver stops once it finds a solution that is this length or shorter

RANDOM_AUF: whether a random auf should be applied to the cube (boolean)
