
def key_a_d_to_move(player, game_state):
    if game_state == "game":
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            player.rect.x -= player.speed
            player.visual_rect.x -= player.speed
            player.facing_right = False
        elif keys[pygame.K_d]:
            player.rect.x += player.speed
            player.visual_rect.x += player.speed
            player.facing_right = True
