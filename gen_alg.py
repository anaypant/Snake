import game
import nn
from settings import *
import pygame
import sys
import numpy as np

snake = []
ai = []

for i in range(NUM_POP):
    ai.append(nn.SnakeNN())
    snake.append(game.SnakeGame())

for cur_gen in range(1, NUM_GEN + 1):
    # play all games
    c = 0
    for i in snake:
        while not i.game_over:
            if not isinstance(i, game.SnakeGame):
                quit()
            if cur_gen > PYGAME_LOOK_AFTER_GEN: i.gui.fill((51, 51, 51))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            inps = i.generate_inputs()
            ai[c].forward(inps)

            ret = i.checkForPress(key=ai[c].key)
            if ret is not None:
                i.snake.dir = ret

            i.snake.update()

            if cur_gen > PYGAME_LOOK_AFTER_GEN:
                i.snake.draw(i.gui)
                i.apple.draw(i.gui)


            if i.snake.tail[-1] == [i.apple.x, i.apple.y]:
                # Apple eaten!
                i.snake.length += 1
                new_coords = i.relocateApple()
                i.apple.x, i.apple.y = new_coords
                i.score += 10  # Reward for eating apple
                i.numMoves += 100  # Extra moves for apple

            # Encourage movement toward the apple
            prev_distance = abs(i.snake.x - i.apple.x) + abs(i.snake.y - i.apple.y)
            cur_distance = abs(i.snake.tail[-1][0] - i.apple.x) + abs(i.snake.tail[-1][1] - i.apple.y)

            if cur_distance < prev_distance:
                i.score += 0.1  # Reward for getting closer
            else:
                i.score -= 0.1  # Penalty for moving away

            # Penalize spinning in place
            if len(i.snake.tail) > 3 and i.snake.tail[-1] == i.snake.tail[-3]:
                i.score -= 0.5  # Discourage repetitive moves

            

            if i.checkForDeath() != 0:
                i.game_over = True

            
            # display generation, iteration, and score
            if cur_gen > PYGAME_LOOK_AFTER_GEN:
                pygame.display.set_caption("Generation: " + str(cur_gen) + " | Iteration: " + str(c) + " | Score: " + str(i.score))
                pygame.display.update()
                i.timer.tick(FPS)
                print(i.generate_inputs())
            i.score += 1e-4
            i.numMoves -= 1

        c += 1

    # Adjust scoring mechanism
    for i in range(NUM_POP):
        for j in range(i + 1, NUM_POP):
            if snake[i].score < snake[j].score:
                snake[i], snake[j] = snake[j], snake[i]
                ai[i], ai[j] = ai[j], ai[i]

    print(f"Generation {cur_gen}: {snake[0].score}")

    # Improved selection mechanism
    new_gen = ai[:NUM_ELITES]
    while len(new_gen) < NUM_POP:
        parent1, parent2 = np.random.choice(ai[:NUM_POP//2], 2, replace=False)
        child = parent1.crossover(parent2)
        child.mutate()
        new_gen.append(child)

    ai = new_gen

    # Reset games
    snake = [game.SnakeGame() for _ in range(NUM_POP)]
   

print("Done")
