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
            "run": self.load_animation(path ="./assets/player/player_run.png", scale=scale),
        }
        self.state = "idle"
        self.speed = 2.5*scale
        self.facing_right = True
        self.frame_index = 0
        self.image = self.animations[self.state][0]
        
        self.rect = pygame.Rect(0, 0, COLLISION_WIDTH, COLLISION_HEIGHT)
        self.rect.center = (x, y + COLLISION_OFFSET_Y)  # applichi l'offset solo una volta qui
        self.visual_rect = self.image.get_rect(center=(x, y))
        self.last_update = pygame.time.get_ticks()


    #aggiorna la posizione del giocatore in base ai tasti premuti, verrà poi sostituita
    #con quello che deciderà la llm in base al prompt
    def update(self, keys, colliders):
        dx = dy = 0
        if keys[pygame.K_a] or keys[pygame.K_d] or keys[pygame.K_w] or keys[pygame.K_s]:
            self.state = "run"
            if keys[pygame.K_a]:
                dx -= self.speed
                self.facing_right = False
            if keys[pygame.K_d]:
                dx += self.speed
                self.facing_right = True
            if keys[pygame.K_w]:
                dy -= self.speed
            if keys[pygame.K_s]:
                dy += self.speed
            #tiene conto delle collisioni
            self.rect = Collision.handle_collision(self.rect, dx, dy, colliders)
            self.visual_rect.center = (self.rect.centerx, self.rect.centery - COLLISION_OFFSET_Y)

        #controlla di aggiornare le animazioni di idle e run
        else:
            self.state = "idle"
    
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