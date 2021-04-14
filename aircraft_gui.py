import pygame, sys
from pygame.locals import *

pygame.init()

DISPLAYSURF = pygame.display.set_mode((500,500))
pygame.display.set_caption('Plane Radar')
display_surface = pygame.display.set_mode((500, 500))

tail_number = ''
distance = ''
altitudae = ''

WHITE = (255,255,255)
GREEN = (0,255,0)
BLUE = (0,0,128)

font = pygame.font.Font('freesansbold.ttf',32)

tail_number_header = font.render('Tail number:', True, GREEN, BLUE)
tail_number_header_rect = tail_number_header.get_rect()
tail_number_header_rect.center = (100, 20)

distance_header = font.render('Distance (miles):', True, GREEN, BLUE)
distance_header_rect = distance_header.get_rect()
distance_header_rect.center = (134, 95)

altitude_header = font.render('Altitude (feet):', True, GREEN, BLUE)
altitude_header_rect = altitude_header.get_rect()
altitude_header_rect.center = (119, 170)

while True:
    
    display_surface.fill(WHITE)
 
    # copying the text surface object
    # to the display surface object
    # at the center coordinate.
    display_surface.blit(tail_number_header, tail_number_header_rect)
    display_surface.blit(distance_header, distance_header_rect)
    display_surface.blit(altitude_header, altitude_header_rect)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            

    pygame.display.update()
