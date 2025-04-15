import pygame_sdl2
pygame_sdl2.import_as_pygame()
import sys
import pygame
from pygame.locals import *

pygame.init()
surface = pygame.display.set_mode((640, 480))

ball = pygame.image.load("pydroball.png")
ballrect = ball.get_rect()
clock = pygame.time.Clock()

width = surface.get_width()
height = surface.get_height()
exitg=False
speed = [14, 14]
while not exitg:
    for ev in pygame.event.get():
        if ev.type == QUIT:
            pygame.quit()
    a=pygame.mouse.get_pos()
    r=pygame.draw.rect(surface,(200,200,200),(a[0],a[1],200,15))
    pygame.display.update()
    
    surface.fill((0, 0, 0))
    ballrect = ballrect.move(speed)
    if ballrect.left < 0 or ballrect.right > width:
        speed[0] = -speed[0]
    if ballrect.top < 0 or r.colliderect(ballrect):
        speed[1] = -speed[1]
    if ballrect.bottom>height:
    	exitg=True
    surface.blit(ball, ballrect)
    pygame.display.flip()
    clock.tick(60)
