import pygame
import collision as Collision
from character import Character

FRAME_WIDTH = 32
FRAME_HEIGHT = 36
ANIM_DELAY = 150  # millisecondi
COLLISION_HEIGHT = 20
COLLISION_WIDTH = 17
COLLISION_OFFSET_Y = 10
COLLISION_OFFSET_X = 5



class Player(Character) :
    def __init__(self, x, y, scale):
        super().__init__(frame_width = 32, frame_height = 36)
        # Carica frame
        self.animations = {
            "idle": self.load_animation(path = "./assets/player/player_idle.png", scale=scale),
            "running": self.load_animation(path ="./assets/player/player_run.png", scale=scale),
        }
        self.state = "idle"
        self.speed = 2.5*scale
        self.facing_right = True
        self.frame_index = 0
        self.image = self.animations[self.state][0]

        #variabili per fisica verticale
        self.gravity = 0.5 * scale  # Forza di gravità
        self.jump_power = -10 * scale  # spinta iniziale per il salto
        self.is_jumping = False
        self.velocity_y = 0
        self.is_falling = False
        self.on_ground = True

        #variabili per possibili interazione e attacchi
        self.is_attacking = False
        self.attack_cooldown = 0  # in millisecondi
        self.is_interacting = False
        self.interact_range = 50  # pixel

        
        self.rect = pygame.Rect(0, 0, COLLISION_WIDTH, COLLISION_HEIGHT)
        self.rect.center = (x, y + COLLISION_OFFSET_Y)  # applichi l'offset solo una volta qui
        self.visual_rect = self.image.get_rect(center=(x, y))
        self.last_update = pygame.time.get_ticks()


    #aggiorna la posizione del giocatore in base ai tasti premuti, verrà poi sostituita
    #con quello che deciderà la llm in base al prompt
    def update(self, keys, colliders, key_functions=None):
        dx = dy = 0
        if keys[pygame.K_a] or keys[pygame.K_d]:
            self.state = "running"
            if keys[pygame.K_a]:
                dx -= self.speed
                self.facing_right = False
            if keys[pygame.K_d]:
                dx += self.speed
                self.facing_right = True
            self.rect = Collision.handle_collision(self.rect, dx, dy, colliders)
            self.visual_rect.center = (self.rect.centerx, self.rect.centery - COLLISION_OFFSET_Y)


            #inseriamo momentaneamente come aggiunta tutto quello che viene dato dal LLM
        elif key_functions and isinstance(key_functions, dict):
            for key_name, function in key_functions.items():
                if len(key_name) == 1:
                    pygame_key = getattr(pygame, f"K_{key_name}", None)
                else:
                        pygame_key = getattr(pygame, f"K_{key_name.upper()}", None)
                if pygame_key and keys[pygame_key]:
                    function()
            #tiene conto delle collisioni
            self.rect = Collision.handle_collision(self.rect, dx, dy, colliders)
            self.visual_rect.center = (self.rect.centerx, self.rect.centery - COLLISION_OFFSET_Y)

        

        #controlla di aggiornare le animazioni di idle e run
        else:
            self.state = "idle"
        
        if hasattr(self, "velocity_y"):
            dy += self.velocity_y
    
        now = pygame.time.get_ticks()
        if now - self.last_update > ANIM_DELAY:
            self.frame_index = (self.frame_index + 1) % len(self.animations[self.state])
            self.image = self.animations[self.state][self.frame_index]
            self.last_update = now

    #disgna a schermo il giocaatore in base alla posizione, alla telecamera e in base
    #alla direzione in cui sta guardando
    def draw(self, camera, surface, tilemap):
        scale = tilemap.get_scale()
        if scale != 1:
            self.image =  pygame.transform.scale(self.image, (self.frame_width*scale, 
                                                              self.frame_height*scale))

        if self.facing_right:
            
            surface.blit(self.image, camera.apply(self.visual_rect, tilemap))
        else:
            flipped_image = pygame.transform.flip(self.image, True, False)
            surface.blit(flipped_image, camera.apply(self.visual_rect, tilemap))
        #debug_rect = camera.apply(self.rect, tilemap)
        #pygame.draw.rect(surface, (255,0,0), debug_rect, 2)