import numpy as np
from utils import *
def encontrar_puntos_entre_dos_puntos(punto1, punto2, cantidad_puntos):
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

# # Ejemplo de uso
# punto_inicial = (0, 1)
# punto_final = (0, 4)
# cantidad_puntos_deseados = 10

# puntos_intermedios = encontrar_puntos_entre_dos_puntos(punto_inicial, punto_final, cantidad_puntos_deseados)

# print("Punto inicial:", punto_inicial)
# print("Punto final:", punto_final)
# print("Puntos intermedios:", puntos_intermedios)
