import pygame
from camera import Camera
from player import Player
from tilemap import TileMap

#from LLM_npc import LLM

WIDTH = 640
HEIGHT = 320
to_scale = False
scale = 1
#starta pygame, crea la dimensione della finestra, ne da un titolo e setta il clock
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Game practice")
clock = pygame.time.Clock()

#llm_npc = LLM(64,64)

#carica la mappa
tilemap = TileMap("maps/Mappa_1.tmx")
#definisce il giocatore e la sua posizione all'interno della mappa (centro dello schermo)
player_x,player_y = tilemap.get_player_start()
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
#binda i tasti del computer, ottiene le collisioni
    keys = pygame.key.get_pressed()
    colliders = tilemap.get_colliders()
    player.update(keys, colliders)
    camera.update(player.rect)
    
    tilemap.render(screen, camera)
    player.draw(camera, screen, tilemap.get_scale())
    #scaled_surface = pygame.transform.scale(game_surface
    #                                        (camera.rect.width*scale, camera.rect.height*scale))
    #llm_npc.draw(screen, camera.rect, 1050, 200)
    #offset_x = (screen.get_width(), -scaled_surface.get_width())//2
    #offset_y = (screen.get_height(), -scaled_surface.get_height())//2
    #screen.fill((211,211,211))
    #screen.blit(scaled_surface, (offset_x, offset_y))
    pygame.display.flip()
    clock.tick(60)
    

pygame.quit()