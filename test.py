def move_away_from_player(enemy_position, player_position, max_cells_to_move):
    # Calcular la diferencia en las coordenadas x e y entre el jugador y el enemigo
    dx = enemy_position[0] - player_position[0]
    dy = enemy_position[1] - player_position[1]

    # Determinar la dirección a la que el enemigo debería moverse para alejarse del jugador
    move_direction = (1 if dx < 0 else -1, 1 if dy < 0 else -1)

    # Calcular la nueva posición del enemigo
    new_position = (
        enemy_position[0] + move_direction[0] * max_cells_to_move,
        enemy_position[1] + move_direction[1] * max_cells_to_move
    )

    return new_position

# Ejemplo de uso:
player_position = (2, 2)
enemy_position = (4, 4)
max_cells_to_move = 3

new_enemy_position = move_away_from_player(enemy_position, player_position, max_cells_to_move)

print(f"Posición original del enemigo: {enemy_position}")
print(f"Nueva posición del enemigo: {new_enemy_position}")
