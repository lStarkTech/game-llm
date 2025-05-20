def handle_collision(player_rect, dx, dy, collision_rects):
    """Restituisce una posizione corretta per il player dopo la collisione."""
    # Sposta orizzontalmente
    player_rect.x += dx
    for rect in collision_rects:
        if player_rect.colliderect(rect):
            if dx > 0:
                player_rect.right = rect.left
            elif dx < 0:
                player_rect.left = rect.right

    # Sposta verticalmente
    player_rect.y += dy
    for rect in collision_rects:
        if player_rect.colliderect(rect):
            if dy > 0:
                player_rect.bottom = rect.top
            elif dy < 0:
                player_rect.top = rect.bottom

    return player_rect