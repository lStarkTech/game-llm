import pygame 

class Character:

    #@classmethod 
    @staticmethod
    def load_animation(path, frame_width, frame_height):
        sheet = pygame.image.load(path).convert_alpha()
        sheet_width, sheet_height = sheet.get_size()
        frames = []
        for i in range(sheet_height // frame_height):
            frame = sheet.subsurface((0, i * frame_height, frame_width, frame_height))
            frames.append(frame)
        #print(f"Caricati {len(frames)} frame da {path}")
        return frames

    @classmethod
    #per definirla qui dentro devo modificarla
    def draw(self, camera, surface):
        
        if self.facing_right:
            
            surface.blit(self.image, camera.apply(self.visual_rect))
        else:
            flipped_image = pygame.transform.flip(self.image, True, False)
            surface.blit(flipped_image, camera.apply(self.visual_rect))
        debug_rect = camera.apply(self.rect)
        pygame.draw.rect(surface, (255,0,0), debug_rect, 2)