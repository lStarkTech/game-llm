import pygame
from camera import Camera
from player import Player
from tilemap import TileMap

#starta pygame, crea la dimensione della finestra, ne da un titolo e setta il clock
pygame.init()
screen = pygame.display.set_mode((960, 540), pygame.RESIZABLE)
pygame.display.set_caption("Game practice")
clock = pygame.time.Clock()
#definisce il giocatore e la sua posizione all'interno della mappa (centro dello schermo)
player = Player(480, 270)

#carica la mappa
tilemap = TileMap("maps/Testing.tmx")
camera = Camera(960,540);

#imposta il ciclo di esecuzionew
running = True
#imposta la chiusura dalla X della finestra
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

#binda i tasti del computer, ottiene le collisioni
    keys = pygame.key.get_pressed()
    colliders = tilemap.get_colliders()
    player.update(keys, colliders)
    camera.update(player, tilemap)
    screen.fill((0,0,0))
    tilemap.render(screen, camera.rect)
    player.draw(camera, screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()