import game
import nn
from settings import *
import pygame
import sys

snake = []
ai = []

for i in range(NUM_POP):
    ai.append(nn.snake_nn())
    snake.append(game.SnakeGame())

for cur_gen in range(1, 2):
    # play all games
    c = 0
    for i in snake:
        while not i.game_over:
            if not isinstance(i, game.SnakeGame):
                quit()
            i.gui.fill((51, 51, 51))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            inps = i.generate_inputs()
            ai[c].forward(inps)

            ret = i.checkForPress(key=ai[c].key)
            if ret is not None:
                i.snake.dir = ret

            i.snake.update()
            i.snake.draw(i.gui)
            i.apple.draw(i.gui)

            if i.snake.tail[-1] == [i.apple.x, i.apple.y]:
                # eaten!
                i.snake.length += 1
                newCoords = i.relocateApple()
                i.apple.x = newCoords[0]
                i.apple.y = newCoords[1]
                i.score += 1

            if i.checkForDeath() != 0:
                i.game_over = True

            pygame.display.set_caption(str(i.generate_inputs()))
            pygame.display.update()
            i.timer.tick(FPS)
        c += 1
