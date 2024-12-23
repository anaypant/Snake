GUI = 600
NUM_CELLS = 15
CELL_W = int(GUI / NUM_CELLS)
START_X = CELL_W * (NUM_CELLS//2)  # GUI / 2
START_Y = CELL_W * (NUM_CELLS//2)   # GUI / 2
FPS = 15

NUM_POP = 100
NUM_GEN = 1000
PYGAME_LOOK_AFTER_GEN = 300
NUM_ELITES = 10
NUM_MUTATIONS = 10
NUM_OFFSPRING = 90
MOVE_INC = NUM_CELLS*10

assert NUM_POP == NUM_ELITES + NUM_OFFSPRING
assert NUM_MUTATIONS <= NUM_POP