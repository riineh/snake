import pygame, sys, random, time

pygame.init()
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

#Colors
green = (0,128,0)
white = (255,255,255)
black = (0, 0, 0)
status = True
x_pos = 60
y_pos = 60

while status:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            status = False
    screen.fill(black)
    pygame.draw.rect(screen, white, pygame.Rect(x_pos, y_pos, 30, 30))
    x_pos += 30
    y_pos += 0

    if x_pos > 800:
        x_pos = 0
    pygame.display.flip()
    clock.tick(5)
