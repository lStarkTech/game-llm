import pygame as py
class Camera:
    def __init__(self, width, height):
        self.rect = py.Rect(0, 0, width, height)

    def apply(self, target_rect):
        # Sposta una superficie rispetto alla camera
        return target_rect.move(-self.rect.x, -self.rect.y)

    def update(self, target, tilemap):
        # Centra la camera sul target (es. player)
        self.rect.center = target.rect.center

        # Limita la camera ai bordi della mappa
        self.rect.x = max(0, min(self.rect.x, tilemap.width - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, tilemap.height - self.rect.height))