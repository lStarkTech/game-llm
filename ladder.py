import pygame as py

class Ladder:

    def get_ladder_rects(self, tilemap):
        """Restituisce i rettangoli delle scale presenti nella mappa."""
        ladder_rects = []
        for obj in tilemap.tmx_data.objects:
            if obj.name.startswith("ladder"):
                rect = py.Rect(obj.x, obj.y, obj.width, obj.height)
                ladder_rects.append(rect)
        return ladder_rects