import pygame as py
class Camera:
    def __init__(self, screen_size, world_size):
        self.rect = py.Rect(0, 0, *screen_size)
        self.world_width, self.world_height = world_size

    #applica i vari offset dei rettangoli in base alla posizione della telecamera
    def apply(self, rect, tilemap):
        map_offset_x, map_offset_y = tilemap.get_offset()
        scale = tilemap.get_scale()
        scaled_rect = rect.copy()
        scaled_rect.centerx = int(((rect.centerx - self.rect.x) * scale)+ map_offset_x)
        scaled_rect.centery = int(((rect.centery - self.rect.y) * scale) + map_offset_y)
        scaled_rect.width = int(rect.width * scale)
        scaled_rect.height = int(rect.height * scale)
        return scaled_rect

    #aggiorna la posizione della telecamera in base allo spostamento del target, ovvero il giocatore
    def update(self, target_rect):
        self.rect.center = target_rect.center
        self.rect.clamp_ip(py.Rect(0, 0, self.world_width, self.world_height))