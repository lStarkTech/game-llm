import pygame as py
import pytmx
from pytmx.util_pygame import load_pygame

class TileMap:
    #definisce una tilemap che abbia un .tmx con una dimensione dei tile e della mappa
    def __init__(self, filename):
        self.scale = 0.75
        self.tmx_data = load_pygame(filename)
        self.tilewidth = self.tmx_data.tilewidth
        self.tileheight = self.tmx_data.tileheight
        self.width = self.tmx_data.width*self.tilewidth
        self.height = self.tmx_data.height*self.tileheight
    
    #renderizza la mappa per ogni layer e recupera l'immagine dal file gid, e definisce la posizione a schermo in
    #base alla posizione della mappa e alla posizione delle "videocamera"
    def render(self, surface, camera_rect):
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = self.tmx_data.get_tile_image_by_gid(gid)
                    if tile:
                        scaled_tile = py.transform.scale(tile,
                                                          (int(self.tilewidth *self.scale),
                                                           int(self.tileheight *self.scale)))
                        p_x = (x * self.tmx_data.tilewidth*self.scale) -camera_rect.x
                        p_y = (y * self.tmx_data.tileheight*self.scale) -camera_rect.y
    
                        surface.blit(scaled_tile, (p_x, p_y))
    
    #definisce le collisioni grazie al layer oggetto di tiled, devo ancora imparare come usarlo
    def get_colliders(self,):
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