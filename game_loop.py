import pygame as py
from camera import Camera
from player import Player
from tilemap import TileMap
from timer import Timer
from gameLLMController import GameLLMController

py.init()  # Initialize Pygame
py.font.init()  # Initialize Pygame font module
llm_controller = GameLLMController()  # inizializza il controller con nessun contesto


class GameLoop:
    
    WIDTH = 640
    HEIGHT = 320
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    font = py.font.SysFont("power clear", 28)
    clock = py.time.Clock()
    screen = py.display.set_mode((WIDTH, HEIGHT))
    py.display.set_caption("Game title")
    game_state = "intro"  # Initial game state

    @staticmethod
    def run(game_state):
        while game_state == "intro":
            game_state = GameLoop.intro()
        if game_state == "game":
            GameLoop.game()

    @staticmethod
    def intro():
        dialog_text = "Child...\n\n" \
                        "Child... Wake up...\n\n" \
                        "...\n\n" \
                        "...\n\n" \
                        "You can't see, child? Wait...\n\n" \
                        "This should work...\n\n"
        # Display the dialog text on the screen
        char_index = 0
        text_speed = 0.1  # Speed of text display
        text_complete = False

        GameLoop.screen.fill(GameLoop.BLACK)
        dialog_rect = py.Rect(50, 50, GameLoop.WIDTH - 100, GameLoop.HEIGHT - 100)
        while not text_complete:
            for event in py.event.get():
                if event.type == py.QUIT:
                    py.quit()
                    return

            GameLoop.screen.fill(GameLoop.BLACK)
            if char_index < len(dialog_text):
                char_index += text_speed
                if py.key.get_pressed()[py.K_RETURN]:
                    # If Enter is pressed, skip to the end of the text
                    char_index = len(dialog_text)
            else:
                text_complete = True
                game_state = "game"  # Change to game state after dialog
                return game_state

            # Render the current part of the dialog text
            rendered_text = GameLoop.font.render(dialog_text[:int(char_index)], True, GameLoop.WHITE)
            GameLoop.screen.blit(rendered_text, dialog_rect.topleft)

            py.display.flip()
            GameLoop.clock.tick(60)


    @staticmethod
    def game():
        input_mode = False #definisce se il giocatore ha richiesto di interagire con il LLM per inserire un nuovo comando
        user_input = "" #inseriremo qui dentro la richiesta dell'utente.
        new_function_key = None #qua va inserito il tasto a cui l'utente decide di voler associare la nuova funzione
        door_timer = Timer(30) #timer per il cambio di mappa
        #carica la mappa iniziale
        tilemap = TileMap("./maps/Mappa_0.tmx")
        #definisce il giocatore e la sua posizione all'interno della mappa (centro dello schermo)
        player_x,player_y = tilemap.get_player_start(0,0)
        camera = Camera(GameLoop.screen.get_size(), (tilemap.width, tilemap.height))
        player = Player(player_x, player_y, tilemap.get_scale())
        #game_surface = pygame.Surface((camera.rect.width, camera.rect.height))
        dt = GameLoop.clock.tick(60) / 1000.0  # Time in seconds

        #imposta il ciclo di esecuzione e lo stato del gioco
        running = True
        #imposta la chiusura dalla X della finestra
        while running:
            for event in py.event.get():
                if event.type == py.QUIT:
                    running = False
                if event.type == py.VIDEORESIZE:
                    GameLoop.screen = py.display.set_mode((event.w, event.h))
                if event.type == py.KEYDOWN:
                    if event.key == py.K_TAB:
                        input_mode = True

        #controlla il cambio di area e il caricamento di una nuova mappa

            if input_mode:
                #prendiamo allora in ingresso dal terminale la richiesta dell'utente
                user_input = input("Tell me child, how can I help you? \n")
                if user_input.lower() == "exit":
                    input_mode = False
                else:
                    print("Press the key you want to assign to this function")
                    #attende che l'utente prema un tasto
                    waiting_for_key = True
                    while waiting_for_key:
                        for event in py.event.get():
                            if event.type == py.KEYDOWN:
                                if event.key == py.K_ESCAPE:
                                    waiting_for_key = False
                                    input_mode = False
                                else:
                                    new_function_key = py.key.name(event.key)
                                    print(f"Okay child. I will do what I can... (the key '{new_function_key}' will be assigned to the function)")
                                    waiting_for_key = False
                                    llm_controller.controls_generation(user_input, new_function_key)
                                    input_mode = False
                        py.time.delay(10) #delay per evitare che il loop sia troppo veloce

            if door_timer.ready():
                tilemap, player = tilemap.load_next_map(player)
            #print("posizione del player: ", player.rect.center)
            #ottiene dalla mappa i rettangoli di collisione
            colliders = tilemap.get_colliders()
            llm_controller.set_game_context(player, colliders, dt) #temporanemente consideriamo solo i colliders, successivamente dovremo inserire anche altri elementi di gioco quali bottoni e porte da aprire
            #aggiorna la posizione del giocatore e della telecamera
            keys = py.key.get_pressed()
            player.update(keys, colliders, llm_controller.key_functions)
            camera.update(player.rect)
            #mostra a schermo la mappa e il giocatore
            tilemap.render(GameLoop.screen)
           
            player.draw(camera, GameLoop.screen, tilemap)
            py.display.flip()
            GameLoop.clock.tick(60)
        

        py.quit()
