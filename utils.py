import math
import numpy as np
import pygame as pg

def find_interm_points(punto1, punto2, cantidad_puntos):
    x1, y1 = punto1
    x2, y2 = punto2

    # Paso 1: Encuentra el vector dirección
    direccion = np.array([x2 - x1, y2 - y1])

    # Paso 2: Normaliza el vector dirección
    direccion_unitaria = direccion / np.linalg.norm(direccion)

    # Calcula distancias equidistantes a lo largo de la dirección unitaria
    distancias = np.linspace(0, 1, cantidad_puntos + 2)[1:-1]
    puntos_intermedios = [(pg.Vector2(x1 + dist * direccion_unitaria[0], y1 + dist * direccion_unitaria[1])) for dist in distancias]

    return puntos_intermedios

def read_map_file(path):
    with open(path) as file:
        map_data = [[int(c) for c in row] for row in file.read().split('\n')]          
    return map_data

def cartisian_to_iso(cartisian, delta = 1):
    screen_pos = pg.Vector2()
    screen_pos.x = (0.5 * (cartisian.x  - cartisian.y) * delta)
    screen_pos.y = (0.25 * (cartisian.x  + cartisian.y) * delta) 
    return screen_pos
    
def isometric_to_cartisian(isometric):
    cartisian_pos =  pg.Vector2(isometric) - pg.Vector2(320,120)
    cartisian_pos.x = int((2 * isometric.y + isometric.x) / 2) 
    cartisian_pos.y = int((2 * isometric.y - isometric.x) / 2)
    return cartisian_pos

def distance_to(initial_pos, final_pos):
        initial_x, initial_y = initial_pos
        final_x, final_y = final_pos

        distance_x = abs(final_x - initial_x)
        distance_y = abs(final_y - initial_y)

        return int(distance_x + distance_y)

def extrac_imgs_from_sheet(sheet, frames, size):
    sheet_img = pg.image.load(sheet).convert_alpha()
    images = []
    for i in range(0,frames): 
        if i != 0:
             i+1
        temp_img = sheet_img.subsurface(
             (i*size,0),
             (size,size)
        )
        images.append(temp_img)
    return images

def check_facing(vector_to, vector_from):
        angle_radians = math.atan2(vector_to.y - vector_from.y, vector_to.x - vector_from.x)
        angle_degrees = math.degrees(angle_radians)

        if angle_degrees > -90 and angle_degrees <= 0:
            return 'se'
        elif (angle_degrees >135.0 and angle_degrees <= 180) or (angle_degrees >= -180.0 and angle_degrees < -135.0):
            return 'nw'
        elif angle_degrees >= -135.0 and angle_degrees <= -90:
            return 'ne'
        elif angle_degrees >= 45.0 and angle_degrees <= 135.0:
             return 'sw'
        else:
             return 'sw'