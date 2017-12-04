import pygame, sys, random, time
from conf import *


pygame.init()
screen = pygame.display.set_mode((display_width * square_len, display_height * square_len))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

status = True

snake_direction = "down"
snake = [(0,0), (0, 1)]


def draw_snake():
    for el in snake:
        pygame.draw.rect(screen, WHITE, pygame.Rect(el[1] * square_len, el[0] * square_len, square_len, square_len))

def calculate_snake_position():
    global snake, snake_direction
    new_snake = snake[1:]
    snake_head = snake[-1]
    if snake_direction == "right":
        new_snake_head_row = snake_head[0]
        new_snake_head_col = snake_head[1] + 1
    elif snake_direction == "left":
        new_snake_head_row = snake_head[0]
        new_snake_head_col = snake_head[1] - 1
    elif snake_direction == "up":
        new_snake_head_row = snake_head[0] - 1
        new_snake_head_col = snake_head[1]
    else:
        new_snake_head_row = snake_head[0] + 1
        new_snake_head_col = snake_head[1]

    if new_snake_head_row > display_height:
        new_snake_head_row = 0
    elif new_snake_head_row < 0:
        new_snake_head_row = display_height
    elif new_snake_head_col > display_width:
        new_snake_head_col = 0
    elif new_snake_head_col < 0:
        new_snake_head_col = display_width



    new_snake_head = (new_snake_head_row, new_snake_head_col)
    new_snake.append(new_snake_head)
    snake = new_snake


while status:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            status = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and snake_direction != "right":
                snake_direction = "left"
            elif event.key == pygame.K_RIGHT and snake_direction != "left":
                snake_direction = "right"
            elif event.key == pygame.K_UP and snake_direction != "down":
                snake_direction = "up"
            elif event.key == pygame.K_DOWN and snake_direction != "up":
                snake_direction = "down"

    screen.fill(BLACK)
    draw_snake()
    calculate_snake_position()





    pygame.display.flip()
    clock.tick(5)
