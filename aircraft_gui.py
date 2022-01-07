#Title: Arc-Angel Aircraft tracking GUI Display
#Authors: Nickolas Gadomski, Samuel Njenga, Ben Deleuze, Colby Nicoletti, Neel Patel
#Purpose: Create a GUI for the user to interact with and have 
#a visual representation of his location compared to Local AirCraft

import pygame, sys
from pygame.locals import *
import aircraft_DF as my_calc
from time import sleep

#Initialize Pygame display surface for simple UI
pygame.init()
pygame.display.set_caption('Plane Radar')
display_surface = pygame.display.set_mode((500, 500))

WHITE = (255,255,255)
GREEN = (0,255,0)
BLUE = (0,0,128)
BLACK = (0,0,0)

font = pygame.font.Font('freesansbold.ttf',32)

#Create Headers for Aircraft Information to be displayed
tail_number_header = font.render('Tail number:', True, GREEN, BLUE)
tail_number_header_rect = tail_number_header.get_rect()
tail_number_header_rect.center = (100, 20)

distance_header = font.render('Distance (miles):', True, GREEN, BLUE)
distance_header_rect = distance_header.get_rect()
distance_header_rect.center = (134, 134)

altitude_header = font.render('Altitude (feet):', True, GREEN, BLUE)
altitude_header_rect = altitude_header.get_rect()
altitude_header_rect.center = (119, 170)

start_finding = my_calc.AircraftFilter(0,0)

#While Loop to update GUI diplay with updated aircraft information coming from the backend every 10 seconds
while True:
    
    start_finding.aircraft_dist_calc()
    tail_number_text = start_finding.get_tail_number()
    distance_text = start_finding.get_distance()
    altitude_text = start_finding.get_altitude()


    tail_value = font.render(str(tail_number_text), True, GREEN, BLUE)
    tail_value_rect = tail_value.get_rect()
    tail_value_rect.center = (300, 20)


    distance_value = font.render(str(round(distance_text,2)), True, GREEN, BLUE)
    distance_value_rect = distance_value.get_rect()
    distance_value_rect.center = (330, 134)
    

    altitude_value = font.render(str(altitude_text), True, GREEN, BLUE)
    altitude_value_rect = altitude_value.get_rect()
    altitude_value_rect.center = (300, 170)

    
    display_surface.fill(WHITE)

 
    # copying the text surface object
    # to the display surface object
    # at the center coordinate.
    display_surface.blit(tail_number_header, tail_number_header_rect)
    display_surface.blit(distance_header, distance_header_rect)
    display_surface.blit(altitude_header, altitude_header_rect)
    display_surface.blit(distance_value, distance_value_rect)
    display_surface.blit(altitude_value, altitude_value_rect)
    display_surface.blit(tail_value, tail_value_rect)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            

    pygame.display.update()
    sleep(10)
