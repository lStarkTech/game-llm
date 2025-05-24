import pygame
from camera import Camera
from player import Player
from tilemap import TileMap
from timer import Timer

WIDTH = 640
HEIGHT = 320

#starta pygame, crea la dimensione della finestra, ne da un titolo e setta il clock
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Game title")
clock = pygame.time.Clock()
door_timer = Timer(30) #timer per il cambio di mappa
#carica la mappa iniziale
tilemap = TileMap("maps/Mappa_0.tmx")
#definisce il giocatore e la sua posizione all'interno della mappa (centro dello schermo)
player_x,player_y = tilemap.get_player_start(0,0)
camera = Camera(screen.get_size(), (tilemap.width, tilemap.height))
player = Player(player_x, player_y, tilemap.get_scale())
#game_surface = pygame.Surface((camera.rect.width, camera.rect.height))

#imposta il ciclo di esecuzionew
running = True
#imposta la chiusura dalla X della finestra
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
#controlla il cambio di area e il caricamento di una nuova mappa
    if door_timer.ready():
        tilemap, player = tilemap.load_next_map(player)
    #print("posizione del player: ", player.rect.center)
    #ottiene dalla mappa i rettangoli di collisione
    colliders = tilemap.get_colliders()
    #aggiorna la posizione del giocatore e della telecamera
    keys = pygame.key.get_pressed()
    player.update(keys, colliders)
    camera.update(player.rect)
    #mostra a schermo la mappa e il giocatore
    tilemap.render(screen)
    """colliders = tilemap.get_colliders()
    for collider in colliders:
        pygame.draw.rect(screen, (255, 0, 0), camera.apply(collider, tilemap), 2)"""

    player.draw(camera, screen, tilemap)
    pygame.display.flip()
    clock.tick(60)
    

pygame.quit()