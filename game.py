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
        for i in range(0, GUI-CELL_W, CELL_W):
            for j in range(0, GUI-CELL_W, CELL_W):
                if not [i, j] in self.snake.tail:
                    possible.append([i, j])
        return random.choice(possible)

    def generate_inputs(self):
        """
        Generates inputs for the neural network.
        Inputs:
            - Normalized distances to wall, apple, and body in cardinal directions.
            - Relative position of the apple (x and y direction).
            - One-hot encoding of the snake's current direction.
        """
        inputs = []

        # Cardinal directions: right, down, left, up
        directions = [[1, 0], [0, 1], [-1, 0], [0, -1]]

        for direction in directions:
            x, y = self.snake.x, self.snake.y
            distance_to_wall = 0
            distance_to_apple = 0
            body_present = 0

            # Calculate distance to wall
            while 0 <= x < GUI and 0 <= y < GUI:
                x += direction[0] * CELL_W
                y += direction[1] * CELL_W
                distance_to_wall += 1

                # Check for apple
                if x == self.apple.x and y == self.apple.y and distance_to_apple == 0:
                    distance_to_apple = distance_to_wall

                # Check for body
                if [x, y] in self.snake.tail:
                    body_present = 1
                    break

            # Normalize distances
            inputs.append(1 / (distance_to_wall + 1))  # Avoid division by zero
            inputs.append(1 / (distance_to_apple + 1) if distance_to_apple > 0 else 0)
            inputs.append(body_present)

        # Add relative apple position
        relative_x = (self.apple.x - self.snake.x) / GUI
        relative_y = (self.apple.y - self.snake.y) / GUI
        inputs.extend([relative_x, relative_y])

        # Add current movement direction as one-hot encoding
        direction_one_hot = [
            int(self.snake.dir == [1, 0]),  # Right
            int(self.snake.dir == [0, 1]),  # Down
            int(self.snake.dir == [-1, 0]),  # Left
            int(self.snake.dir == [0, -1])   # Up
        ]
        inputs.extend(direction_one_hot)

        return inputs


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


