import pygame, sys, time
from random import randint
from conf import *

pygame.init()
screen = pygame.display.set_mode((game_area_width * square_len, game_area_height * square_len + menu_height))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()
speed = 5


game_started = True


snake_direction = "down"
snake = [(0,0), (0, 1)]
foods = [((randint(0, game_area_height),randint(0,game_area_width)), 1)]
score = 0
walls = [(8, 8)]


def draw_info_bar():
    pygame.draw.rect(screen, GRAY, pygame.Rect(0, game_area_height * square_len, game_area_width * square_len, menu_height * square_len))
    draw_info_texts()


def draw_info_texts():
    myfont = pygame.font.SysFont("monospace", 30)
    score_lable = myfont.render("Score: " + str(score), 1, BLACK)
    screen.blit(score_lable, (20, game_area_height * square_len + 26))


def draw_snake():
    for el in snake:
        pygame.draw.rect(screen, WHITE, pygame.Rect(el[1] * square_len, el[0] * square_len, square_len, square_len))


def draw_food():
    for el in foods:
        pygame.draw.rect(screen, GREEN, pygame.Rect(el[0][1] * square_len, el[0][0] * square_len, square_len, square_len))


def calculate_snake_position():
    global snake, snake_direction, lives
    snake_head = snake[-1]
    new_snake_head = calculate_new_snake_head_pos(snake_direction, snake_head)
    if check_food_collision(new_snake_head):
        new_snake = snake[:]
    elif check_collision():
        new_snake = snake[:]
        #peab lõpetama
    else:
        new_snake = snake[1:]
    new_snake.append(new_snake_head)
    snake = new_snake


def check_food_collision(new_snake_head):
    global foods, score, speed
    for food in foods:
        if food[0] == new_snake_head:
            score += food[1]
            foods.remove(food)
            speed += 0.5
            return True
    return False

def check_collision():
    global snake
    if snake[0] in snake[1:]:
        return True
    # Iseendaga kokkupõrget peab kontrollima


def spawn_food(food_level):
    global foods
    new_food = ((randint(0, game_area_height - 1), randint(0, game_area_width - 1)), food_level)
    if new_food[0] in snake:
        spawn_food(food_level)
    else:
        foods.append(new_food)


def calculate_new_snake_head_pos(snake_direction, snake_head):
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
    if new_snake_head_row > game_area_height - 1:
        new_snake_head_row = 0
    elif new_snake_head_row < 0:
        new_snake_head_row = game_area_height - 1
    elif new_snake_head_col > game_area_width - 1:
        new_snake_head_col = 0
    elif new_snake_head_col < 0:
        new_snake_head_col = game_area_width - 1
    return (new_snake_head_row, new_snake_head_col)


while game_started:
    valid_key_pressed = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_started = False
        if not valid_key_pressed:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and snake_direction != "right":
                    snake_direction = "left"
                    valid_key_pressed = True
                elif event.key == pygame.K_RIGHT and snake_direction != "left":
                    snake_direction = "right"
                    valid_key_pressed = True
                elif event.key == pygame.K_UP and snake_direction != "down":
                    snake_direction = "up"
                    valid_key_pressed = True
                elif event.key == pygame.K_DOWN and snake_direction != "up":
                    snake_direction = "down"
                    valid_key_pressed = True

    screen.fill(BLACK)
    draw_info_bar()
    draw_snake()

    if len(foods) == 0:
        spawn_food(1)

    draw_food()
    calculate_snake_position()
    draw_info_bar()





    pygame.display.flip()
    clock.tick(speed)
