import pygame 

class Character:
    def __init__(self, frame_width, frame_height):
        self.frame_width = frame_width
        self.frame_height = frame_height


    #@classmethod 
    def load_animation(self, path, scale):
        sheet = pygame.image.load(path).convert_alpha()
        sheet_width, sheet_height = sheet.get_size()
        frames = []
        for i in range(sheet_height // self.frame_height):
            frame = sheet.subsurface((0, i * self.frame_height, self.frame_width, self.frame_height))
            frame = pygame.transform.scale(frame, (self.frame_width*scale,
                                                   self.frame_height*scale))
            frames.append(frame)
        #print(f"Caricati {len(frames)} frame da {path}")
        return frames

    @classmethod
    #per definirla qui dentro devo modificarla
    def draw(self, camera, surface, tilemap):
        
        if self.facing_right:
            
            surface.blit(self.image, camera.apply(self.visual_rect, tilemap))
        else:
            flipped_image = pygame.transform.flip(self.image, True, False)
            surface.blit(flipped_image, camera.apply(self.visual_rect, tilemap))
        debug_rect = camera.apply(self.rect, tilemap)
        pygame.draw.rect(surface, (255,0,0), debug_rect, 2)