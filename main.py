import pygame, sys, random, time
from conf import *


pygame.init()
screen = pygame.display.set_mode((display_width * square_len, display_height * square_len))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

status = True

snake = [(0,0), (0, 1)]


def draw_snake():
    for el in snake:
        pygame.draw.rect(screen, WHITE, pygame.Rect(el[1] * square_len, el[0] * square_len, square_len, square_len))

def calculate_snake_position():
    pass


while status:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            status = False
    screen.fill(BLACK)
    draw_snake()



    pygame.display.flip()
    clock.tick(5)
