import pygame as py
import pytmx
from pytmx.util_pygame import load_pygame
from player import Player
from pathlib import Path

class TileMap:
    #definisce una tilemap che abbia un .tmx con una dimensione dei tile e della mappa
    def __init__(self, filename):
        self.tmx_data = pytmx.load_pygame(filename)
        self.tilewidth = self.tmx_data.tilewidth
        self.tileheight = self.tmx_data.tileheight
        self.width = self.tmx_data.width * self.tilewidth
        self.height = self.tmx_data.height * self.tileheight
        self.scale = 1
        self.offset_x = 0
        self.offset_y = 0

#mostra la mappa a schermo, scalandola se necessario e controllando l'opacità dei layer
    def render(self, surface):

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

        #offset per centrare la mappa
        self.offset_x = (screen_width - scaled_map.get_width()) // 2
        self.offset_y = (screen_height - scaled_map.get_height()) // 2
        surface.fill((0, 0, 0))  # letterbox
        surface.blit(scaled_map, (self.offset_x, self.offset_y))

    def get_offset(self):
        """Restituisce l'offset della mappa, utile per centrare la mappa
        all'interno della finestra."""
        return self.offset_x, self.offset_y
#prende la posizione iniziale del giocatore dalla mappa
    def get_player_start(self, door_in, door_out):
        for obj in self.tmx_data.objects:
            if obj.name == f"player_pos{door_in}{door_out}":
                print(f"posizione del player: {obj.x}, {obj.y}")
                return int(obj.x), int(obj.y)
        print(f"posizione del player non trovata per la mappa {door_out} dalla mappa {door_in}")
        return 0, 0  # fallback

    def get_colliders(self):
        """crea dei rettangoli per tutti gli oggetti che hanno per nome
        collider, ovvero quegli oggetti che fanno parte della object layer
        di tiled e che sono collisioni."""
        colliders = []
        for obj in self.tmx_data.objects:
            if obj.name == "collider":
                rect =py.Rect(obj.x, 
                              obj.y, 
                              obj.width,
                              obj.height)
                              
                colliders.append(rect)
        return colliders

    # Restituisce la scala della mappa
    # che viene usata per scalare il player e le collisioni
    def get_scale(self):
        return self.scale
    
    # Carica la mappa successiva in base alla porta con cui il giocatore collide
    def load_next_map(self, player):
        #recupera le porte della mappa attuale
        doors = []
        for obj in self.tmx_data.objects:
            if obj.name and obj.name.startswith("door"):
                try:
                    door_in = int(obj.name[4:5])  # Assuming door names are like "door1", "door2", etc.
                    door_out = int(obj.name[5:6])
                except ValueError:
                    continue
                rect =py.Rect(obj.x*self.scale, 
                              obj.y*self.scale, 
                              obj.width*self.scale, 
                              obj.height*self.scale)
                doors.append((rect, door_in, door_out))

        # Controlla le collisioni con le porte
        for rect, door_in, door_out in doors:
            collision = player.rect.colliderect(rect)
            if collision:
                print(f"COLLISIONE AVVENUTA! sulla porta che fa accedere alla mappa {door_out} dalla mappa {door_in}")
                #carica la mappa successiva
                map_path = Path(f"maps/Mappa_{door_out}.tmx")
                if (map_path.exists() == False):
                    print(f"la mappa {door_out} non esiste")
                    return self, player
                new_tilemap = TileMap(map_path)
                player_x, player_y = new_tilemap.get_player_start(door_in, door_out)
                new_player = Player(player_x, player_y, new_tilemap.get_scale())
                return new_tilemap, new_player
        return self, player

