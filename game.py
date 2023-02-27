import pygame
from settings import *
import random
import sys
import keyboard

pygame.init()


class Snake:
    def __init__(self):
        self.x = START_X
        self.y = START_Y
        self.dir = [1, 0]
        self.tail = [[self.x, self.y]]
        self.length = 1

    def update(self):
        self.x += self.dir[0] * CELL_W
        self.y += self.dir[1] * CELL_W
        self.tail.append([self.x, self.y])

        if len(self.tail) > self.length:
            del [self.tail[0]]

    def draw(self, gui):
        for x in self.tail:
            if x == [self.x, self.y]:
                pygame.draw.rect(gui, (175, 255, 0), [x[0], x[1], CELL_W, CELL_W])
            else:
                pygame.draw.rect(gui, (0, 255, 0), [x[0], x[1], CELL_W, CELL_W])
            pygame.draw.rect(gui, (120, 120, 120), [x[0], x[1], CELL_W, CELL_W], 2)


class Apple:
    def __init__(self):
        self.x = random.randint(0, NUM_CELLS - 1) * CELL_W
        self.y = random.randint(0, NUM_CELLS - 1) * CELL_W

    def draw(self, gui):
        pygame.draw.rect(gui, (255, 0, 100), [self.x, self.y, CELL_W, CELL_W])
        pygame.draw.rect(gui, (120, 120, 120), [self.x, self.y, CELL_W, CELL_W], 2)


class SnakeGame:
    def __init__(self):
        self.gui = pygame.display.set_mode((GUI, GUI))
        self.game_over = False
        self.score = 0
        self.snake = Snake()
        self.apple = Apple()
        self.timer = pygame.time.Clock()

    def relocateApple(self):
        # relocates the apple where the snake is not
        possible = []
        for i in range(0, GUI, CELL_W):
            for j in range(0, GUI, CELL_W):
                if not [i, j] in self.snake.tail:
                    possible.append([i, j])
        return random.choice(possible)

    def play(self):
        while not self.game_over:
            self.gui.fill((51, 51, 51))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            ret = self.checkForPress()
            if ret is not None:
                self.snake.dir = ret

            # self.snake.update()
            self.snake.draw(self.gui)
            self.apple.draw(self.gui)

            if self.snake.tail[-1] == [self.apple.x, self.apple.y]:
                # eaten!
                self.snake.length += 1
                newCoords = self.relocateApple()
                self.apple.x = newCoords[0]
                self.apple.y = newCoords[1]
                self.score += 1

            if self.checkForDeath() != 0:
                self.game_over = True

            pygame.display.set_caption(str(self.generate_inputs()))
            pygame.display.update()
            self.timer.tick(FPS)

    def generate_inputs(self):
        inps = []
        # directions
        directions = [
            [-1, -1],
            [0, -1],
            [1, -1],
            [1, 0],
            [1, 1],
            [0, 1],
            [-1, 1],
            [-1, 0],
        ]
        for direction in directions:
            wallDist = 1.0
            foodDist = 0.0
            snakeDist = 0.0
            # if I am touching the wall in every direction, walldist is 0
            x = self.snake.x + direction[0] * CELL_W
            y = self.snake.y + direction[1] * CELL_W
            if not (0 <= x <= GUI - CELL_W and 0 <= y <= GUI - CELL_W):
                wallDist = 0
            while 0 <= x <= GUI - CELL_W and 0 <= y <= GUI - CELL_W:
                if [x, y] == [self.apple.x, self.apple.y]:
                    foodDist = 1.0
                if [x, y] in self.snake.tail[0 : len(self.snake.tail) - 1]:
                    snakeDist = 1
                x += direction[0] * CELL_W
                y += direction[1] * CELL_W
            inps.append(wallDist)
            inps.append(foodDist)
            inps.append(snakeDist)
        # extra stuff :

        # head dir
        if self.snake.dir == [0, -1]:
            inps.append(1)
            inps.append(0)
            inps.append(0)
            inps.append(0)
        elif self.snake.dir == [-1, 0]:
            inps.append(0)
            inps.append(1)
            inps.append(0)
            inps.append(0)
        elif self.snake.dir == [0, 1]:
            inps.append(0)
            inps.append(0)
            inps.append(1)
            inps.append(0)
        elif self.snake.dir == [1, 0]:
            inps.append(0)
            inps.append(0)
            inps.append(0)
            inps.append(1)

        # tail dir
        if len(self.snake.tail) == 1:
            inps.append(0)
            inps.append(0)
            inps.append(0)
            inps.append(0)
        else:
            # calculate the direction of the tail
            print(self.snake.tail)
            tail = self.snake.tail[0]
            sec = self.snake.tail[1]
            x = sec[0] - tail[0]
            y = sec[1] - tail[1]

            if x == 0 and y == -CELL_W:  # up
                inps.append(1)
                inps.append(0)
                inps.append(0)
                inps.append(0)
            elif x == 0 and y == CELL_W:  # down
                inps.append(0)
                inps.append(0)
                inps.append(1)
                inps.append(0)
            elif x == -CELL_W and y == 0:  # left
                inps.append(0)
                inps.append(1)
                inps.append(0)
                inps.append(0)
            elif x == CELL_W and y == 0:  # right
                inps.append(0)
                inps.append(0)
                inps.append(0)
                inps.append(1)
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
    test = SnakeGame()

    test.apple.x = 60
    test.apple.y = 60
    print(len(test.generate_inputs()))
    test.play()
