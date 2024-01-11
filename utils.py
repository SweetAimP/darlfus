import math
import pygame as pg

def read_map_file(path):
    with open(path) as file:
        map_data = [[int(c) for c in row] for row in file.read().split('\n')]          
    return map_data

def cartisian_to_iso(cartisian, delta = 1):
    screen_pos = pg.Vector2()
    screen_pos.x = int(0.5 * (cartisian.x  - cartisian.y) * delta)
    screen_pos.y = int(0.25 * (cartisian.x  + cartisian.y) * delta) 
    return screen_pos
    
def isometric_to_cartisian(isometric):
    cartisian_pos =  pg.Vector2(isometric) - pg.Vector2(320,120)
    cartisian_pos.x = int((2 * isometric.y + isometric.x) / 2) 
    cartisian_pos.y = int((2 * isometric.y - isometric.x) / 2)
    return cartisian_pos

def check_facing(vector_to, vector_from):
        angle_radians = math.atan2(vector_to.y - vector_from.y, vector_to.x - vector_from.x)
        angle_degrees = math.degrees(angle_radians)

        if angle_degrees == 0:
            return 'se'
        elif angle_degrees == 180:
            return 'nw'
        elif angle_degrees == -90:
            return 'ne'
        else:
            return 'sw'