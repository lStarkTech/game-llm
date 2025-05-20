import pygame
import collision as Collision
def load_animation(path, frame_width, frame_height):
    sheet = pygame.image.load(path).convert_alpha()
    sheet_width, sheet_height = sheet.get_size()
    frames = []
    for i in range(sheet_height // frame_height):
        frame = sheet.subsurface((0, i * frame_height, frame_width, frame_height))
        frames.append(frame)
    print(f"Caricati {len(frames)} frame da {path}")
    return frames

FRAME_WIDTH = 32
FRAME_HEIGHT = 48
ANIM_DELAY = 150  # millisecondi
COLLISION_HEIGHT = 30
COLLISION_WIDTH = 24
COLLISION_OFFSET_Y = 10

class Player:
    def __init__(self, x, y):
        # Carica frame
        self.animations = {
            "idle": load_animation("assets/player/B_witch_idle.png", FRAME_WIDTH, FRAME_HEIGHT),
            "run": load_animation("assets/player/B_witch_run.png", FRAME_WIDTH, FRAME_HEIGHT),
        }
        self.state = "idle"
        self.speed = 3
        self.facing_right = True
        self.frame_index = 0
        self.image = self.animations[self.state][0]
        initial_rect = self.image.get_rect(center=(x, y))
        self.rect = pygame.Rect(initial_rect.x, initial_rect.y, 
                                COLLISION_WIDTH, COLLISION_HEIGHT)
        self.last_update = pygame.time.get_ticks()


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
            self.rect = Collision.handle_collision(self.rect, dx, dy, colliders)
            
        else:
            self.state = "idle"
    
        now = pygame.time.get_ticks()
        if now - self.last_update > ANIM_DELAY:
            self.frame_index = (self.frame_index + 1) % len(self.animations[self.state])
            self.image = self.animations[self.state][self.frame_index]
            self.last_update = now

    def draw(self, camera, surface):
        if self.facing_right:
            surface.blit(self.image, camera.apply(self.rect))
        else:
            flipped_image = pygame.transform.flip(self.image, True, False)
            surface.blit(flipped_image, camera.apply(self.rect))