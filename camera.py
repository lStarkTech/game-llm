import pygame as py
class Camera:
    def __init__(self, screen_size, world_size):
        self.rect = py.Rect(0, 0, *screen_size)
        self.world_width, self.world_height = world_size

    def apply(self, rect, scale):
        scaled_rect = rect.copy()
        scaled_rect.centerx = int((rect.centerx - self.rect.x) * scale)
        scaled_rect.centery = int((rect.centery - self.rect.y) * scale)
        scaled_rect.width = int(rect.width * scale)
        scaled_rect.height = int(rect.height * scale)
        return scaled_rect

    def update(self, target_rect):
        self.rect.center = target_rect.center
        self.rect.clamp_ip(py.Rect(0, 0, self.world_width, self.world_height))