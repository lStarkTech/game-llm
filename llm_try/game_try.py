import pygame  # Importa la funzione space dal file debug_function_code.py
# Inizializza pygame-ce
pygame.init()

import importlib.util
import types

def carica_modulo_llm(percorso="llm_try/debug_function_code.py") -> types.ModuleType:
    spec = importlib.util.spec_from_file_location("debug_function_code", percorso)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo

funzioni_llm = carica_modulo_llm()
# Costanti finestra
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Platform Player Test")

# Player properties
player_width, player_height = 40, 60
player_x, player_y = WIDTH // 2, HEIGHT - player_height  # in basso, centro
player_vel_x, player_vel_y = 0, 0
player_speed = 5
player_jump_height = 15
player_state = "idle"  # può essere: idle, running, jumping, falling

gravity = 1

clock = pygame.time.Clock()



running = True
while running:
    clock.tick(60)  # 60 FPS
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Input semplice: muovi il player con frecce
    keys = pygame.key.get_pressed()
    player_vel_x = 0
    if keys[pygame.K_LEFT]:
        player_vel_x = -player_speed
        player_state = "running"
    elif keys[pygame.K_RIGHT]:
        player_vel_x = player_speed
        player_state = "running"
    elif keys[pygame.K_SPACE] and player_state != "jumping" and player_state != "falling":
        if hasattr(funzioni_llm, 'space'):
            function = funzioni_llm.space()
            function()  # Chiama la funzione space
        else:
            print("La funzione 'space' non è stata trovata nel modulo.")
    else:
        player_state = "idle"


    # Applica la gravità
    player_vel_y += gravity
    
    # Muovi player
    player_x += player_vel_x
    player_y += player_vel_y
    
    # Collisione col "pavimento"
    if player_y > HEIGHT - player_height:
        player_y = HEIGHT - player_height
        player_vel_y = 0
        if player_state == "falling" or player_state == "jumping":
            player_state = "idle"
    
    # Schermo
    screen.fill((30, 30, 30))  # sfondo scuro
    
    # Disegna player
    pygame.draw.rect(screen, (255, 0, 0), (player_x, player_y, player_width, player_height))
    
    pygame.display.flip()

pygame.quit()
