


def handle_collision(player, collision_rects):
    """Restituisce una posizione corretta per il player dopo la collisione."""
    # Sposta orizzontalmente
    #player.on_ground = False  # Reset on_ground status
    #player.rect.x += player.dx
    for rect in collision_rects:
        if player.rect.colliderect(rect):
            if player.dx > 0:
                player.rect.right = rect.left
            elif player.dx < 0:
                player.rect.left = rect.right

    # Sposta verticalmente
    #player.rect.y += player.dy
    for rect in collision_rects:
        if player.rect.colliderect(rect):
            if player.velocity_y > 0:
                player.rect.bottom = rect.top
                player.velocity_y = 0
                player.on_ground = True
            elif player.velocity_y < 0:
                player.rect.top = rect.bottom
"""
    #verifica se il player è a terra
        for rect in collision_rects:
            if player.rect.bottom == rect.top and player.rect.colliderect(rect):
                player.on_ground = True
"""
        