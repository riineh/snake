import pygame
from random import randint
from conf import *

pygame.init()
screen = pygame.display.set_mode((game_area_width * square_len, game_area_height * square_len + menu_height))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()
initial_speed = 5
speed = initial_speed

running = True

current_state = STATE_MAIN_MENU

snake_direction = "down"
initial_snake = [(3, 3), (4, 3)]
snake = initial_snake
foods = [((randint(0, game_area_height - 1), randint(0, game_area_width - 1)), 1)]
score = 0
walls = [(8, 8)]

font = pygame.font.SysFont("monospace", 30)


def draw_info_bar():
    pygame.draw.rect(screen, GRAY, pygame.Rect(0, game_area_height * square_len, game_area_width * square_len,
                                               menu_height * square_len))
    draw_info_texts()


def draw_info_texts():
    score_lable = font.render("Score: " + str(score), 1, BLACK)
    screen.blit(score_lable, (20, game_area_height * square_len + 26))


def draw_snake():
    for el in snake:
        pygame.draw.rect(screen, WHITE, pygame.Rect(el[1] * square_len, el[0] * square_len, square_len, square_len))


def draw_food():
    for el in foods:
        pygame.draw.rect(screen, GREEN,
                         pygame.Rect(el[0][1] * square_len, el[0][0] * square_len, square_len, square_len))


def update_high_scores():
    f = open("high-scores.txt", "r+", encoding="utf-8")
    lines = f.readlines()

    # Leidsin siit: https://stackoverflow.com/questions/17126037/how-to-delete-only-the-content-of-file-in-python
    f.seek(0)
    f.truncate()

    existing_scores = []
    for line in lines:
        existing_scores.append(int(line.strip()))

    existing_scores.sort(reverse=True)

    if len(existing_scores) < 5:
        existing_scores.append(score)
    elif existing_scores[-1] < score:
        existing_scores = existing_scores[:-1]
        existing_scores.append(score)

    for existing_score in existing_scores:
        f.write(str(existing_score) + "\n")

    f.close()


def end_game():
    global current_state
    current_state = STATE_GAME_OVER
    update_high_scores()


def calculate_snake_position():
    global snake, snake_direction, current_state
    snake_head = snake[-1]
    new_snake_head = calculate_new_snake_head_pos(snake_direction, snake_head)
    if check_food_collision(new_snake_head):
        new_snake = snake[:]
    elif check_collision_with_itself(new_snake_head):
        end_game()
        return
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


def check_collision_with_itself(new_snake_head):
    global snake
    if new_snake_head in snake[1:]:
        return True


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


def draw_text_to_center(text, order):
    score_label = font.render(text, 1, BLACK)
    text_width, text_height = font.size(text)
    screen.blit(score_label, (game_area_width * square_len / 2 - text_width / 2, game_area_height * square_len / 2 + order * (text_height + 20)))


def draw_start_menu_info_texts():
    draw_text_to_center("To start the game press SPACE", -1)
    draw_text_to_center("To view the high-scores press H", 0)
    draw_text_to_center("To exit press ESC", 1)


def draw_game_over_info_texts():
    draw_text_to_center("GAME OVER!!!", -3)
    draw_text_to_center("Your score was: " + str(score), -2)
    draw_text_to_center("", -1)
    draw_text_to_center("To play again press SPACE", 0)
    draw_text_to_center("To view the high-scores press H", 1)
    draw_text_to_center("To exit press ESC", 2)


def draw_highscores():
    f = open("high-scores.txt", "r", encoding="utf-8")
    lines = f.readlines()
    f.close()
    scores = []
    for line in lines:
        scores.append(int(line.strip()))
    scores.sort(reverse=True)

    nr_of_scores = len(scores)
    vert_index = - (nr_of_scores + 2) // 2

    draw_text_to_center("TOP 5 SCORES", vert_index)
    draw_text_to_center("", vert_index + 1)
    vert_index += 2
    for i, high_score in enumerate(scores):
        draw_text_to_center("#" + str(i + 1) + ":   " + str(high_score), vert_index)
        vert_index += 1

    draw_text_to_center("Press ESC to main menu", vert_index)


def run_game():
    global running, snake_direction, current_state
    valid_key_pressed = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                current_state = STATE_MAIN_MENU
            if not valid_key_pressed:
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


def start_game():
    global current_state, initial_snake, speed, score, snake, snake_direction
    speed = initial_speed
    snake_direction = "down"
    score = 0
    snake = initial_snake
    current_state = STATE_GAME_STARTED


def run_start_menu():
    global running, current_state
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                start_game()
            elif event.key == pygame.K_h:
                current_state = STATE_HIGH_SCORES
            elif event.key == pygame.K_ESCAPE:
                running = False

    screen.fill(WHITE)
    draw_start_menu_info_texts()
    pygame.display.flip()
    clock.tick(speed)


def run_game_over():
    global running, current_state
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                start_game()
            elif event.key == pygame.K_h:
                current_state = STATE_HIGH_SCORES
            elif event.key == pygame.K_ESCAPE:
                running = False

    screen.fill(WHITE)
    draw_game_over_info_texts()
    pygame.display.flip()
    clock.tick(speed)


def run_high_scores():
    global running, current_state
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                current_state = STATE_MAIN_MENU

    screen.fill(WHITE)
    draw_highscores()
    pygame.display.flip()
    clock.tick(speed)


while running:
    if current_state == STATE_GAME_STARTED:
        run_game()
    elif current_state == STATE_MAIN_MENU:
        run_start_menu()
    elif current_state == STATE_GAME_OVER:
        run_game_over()
    elif current_state == STATE_HIGH_SCORES:
        run_high_scores()
