import pygame
from settings import *
import random
import sys
import keyboard



class Snake:
    def __init__(self):
        self.x = START_X
        self.y = START_Y
        self.dir = [1, 0]
        self.tail = [[self.x-2*CELL_W, self.y], [self.x-CELL_W, self.y], [self.x, self.y]]
        self.length = 3

    def update(self):
        self.x += self.dir[0] * CELL_W
        self.y += self.dir[1] * CELL_W
        self.tail.append([self.x, self.y])

        if len(self.tail) > self.length:
            del [self.tail[0]]

    def draw(self, gui):
        for x in self.tail:
            if x == [self.x, self.y]:
                pygame.draw.rect(gui, (175, 255, 0), [x[0]+1, x[1]+1, CELL_W-1, CELL_W-1])
            else:
                pygame.draw.rect(gui, (0, 255, 0), [x[0]+1, x[1]+1, CELL_W-1, CELL_W-1])


class Apple:
    def __init__(self):
        self.x = random.randint(0, NUM_CELLS - 1) * CELL_W
        self.y = random.randint(0, NUM_CELLS - 1) * CELL_W

    def draw(self, gui):
        pygame.draw.rect(gui, (255, 0, 100), [self.x+1, self.y+1, CELL_W-1, CELL_W-1])


class SnakeGame:
    def __init__(self):
        self.gui = pygame.display.set_mode((GUI, GUI))
        self.game_over = False
        self.score = 0
        self.snake = Snake()
        self.apple = Apple()
        self.timer = pygame.time.Clock()
        self.numMoves = 100

    def relocateApple(self):
        # relocates the apple where the snake is not
        possible = []
        for i in range(0, GUI, CELL_W):
            for j in range(0, GUI, CELL_W):
                if not [i, j] in self.snake.tail:
                    possible.append([i, j])
        return random.choice(possible)

    def generate_inputs(self):
        inps = []
        directions = [[0, -1], [-1, 0], [0, 1], [1, 0]]#, [-1, -1], [1, -1], [1, 1], [-1, 1]]
        for d in directions:
            copySnake = self.snake.tail[-1].copy()
            copyHead = [d[0]*CELL_W + copySnake[0], d[1]*CELL_W + copySnake[1]]
            touchingWall = int(not (0 <= copyHead[0] < GUI and 0 <= copyHead[1] < GUI))
            touchingSelf = int(copyHead in self.snake.tail)
            inps.append(touchingWall)
            inps.append(touchingSelf)

            # extend until apple is found or wall is reached
            copyHead = self.snake.tail[-1].copy()
            appleFound = 0
            while(0 <= copyHead[0] < GUI and 0 <= copyHead[1] < GUI):
                if (copyHead[0] == self.apple.x and copyHead[1] == self.apple.y):
                    appleFound = 1
                    break
                copyHead[0] += d[0]*CELL_W
                copyHead[1] += d[1]*CELL_W
            inps.append(appleFound)

        if self.snake.dir == [0, -1]:
            inps.extend([1, 0, 0, 0])
        elif self.snake.dir == [-1, 0]:
            inps.extend([0, 1, 0, 0])
        elif self.snake.dir == [0, 1]:
            inps.extend([0, 0, 1, 0])
        elif self.snake.dir == [1, 0]:
            inps.extend([0, 0, 0, 1])

        return inps
            

    def checkForDeath(self):
        if not (
            0 <= self.snake.x <= GUI - CELL_W and 0 <= self.snake.y <= GUI - CELL_W
        ):
            return 1
        if [self.apple.x, self.apple.y] in self.snake.tail:
            return 2
        if [self.snake.x, self.snake.y] in self.snake.tail[
            0 : len(self.snake.tail) - 1
        ]:
            return 3
        if self.numMoves == 0:
            return 4
        return 0

    def checkForPress(self, key=None):
        if key is not None:
            if key == 0 and self.snake.dir != [0, 1]:
                return [0, -1]
            elif key == 1 and self.snake.dir != [1, 0]:
                return [-1, 0]
            elif key == 2 and self.snake.dir != [0, -1]:
                return [0, 1]
            elif key == 3 and self.snake.dir != [-1, 0]:
                return [1, 0]
            else:
                return None
        else:
            if keyboard.is_pressed("w"):
                return [0, -1]
            elif keyboard.is_pressed("a"):
                return [-1, 0]
            elif keyboard.is_pressed("s"):
                return [0, 1]
            elif keyboard.is_pressed("d"):
                return [1, 0]
            else:
                return None


if __name__ == "__main__":
    testGame = SnakeGame()
    print(testGame.generate_inputs())