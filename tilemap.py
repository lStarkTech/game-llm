import pygame as py
import pytmx
from pytmx.util_pygame import load_pygame

class TileMap:
    #definisce una tilemap che abbia un .tmx con una dimensione dei tile e della mappa
    def __init__(self, filename):
        self.tmx_data = pytmx.load_pygame(filename)
        self.tilewidth = self.tmx_data.tilewidth
        self.tileheight = self.tmx_data.tileheight
        self.width = self.tmx_data.width * self.tilewidth
        self.height = self.tmx_data.height * self.tileheight
        self.scale = 1

    def render(self, surface, camera):
        map_surface = py.Surface((self.width, self.height), py.SRCALPHA)
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                layer_opacity = getattr(layer, "opacity",1.0)                
                for x, y, gid in layer:
                    tile = self.tmx_data.get_tile_image_by_gid(gid)
                    if tile:
                        if layer_opacity < 1.0:
                            tile = tile.copy()
                            tile.set_alpha(int(255*layer_opacity))
                        map_surface.blit(tile, (x * self.tilewidth, y * self.tileheight))

        # Scaling
        screen_width, screen_height = surface.get_size()
        scale = min(screen_width / self.width, screen_height / self.height)
        self.scale = scale

        scaled_map = py.transform.scale(map_surface, 
                                        (int(self.width * scale), int(self.height * scale)))

        offset_x = (screen_width - scaled_map.get_width()) // 2
        offset_y = (screen_height - scaled_map.get_height()) // 2
        surface.fill((0, 0, 0))  # letterbox
        surface.blit(scaled_map, (offset_x, offset_y))

    def get_player_start(self):
        for obj in self.tmx_data.objects:
            if obj.name == "player_pos":
                return int(obj.x), int(obj.y)
        return 0, 0  # fallback

    def get_colliders(self):
        """crea dei rettangoli per tutti gli oggetti che hanno per nome
        collision, ovvero quegli oggetti che fanno parte della object layer
        di tiled"""
        colliders = []
        for obj in self.tmx_data.objects:
            if obj.name == "collider":
                rect =py.Rect(obj.x*self.scale, 
                              obj.y*self.scale, 
                              obj.width*self.scale, 
                              obj.height*self.scale)
                              
                colliders.append(rect)
        return colliders

    def get_scale(self):
        return self.scale
            
