import pygame as py
from character import Character

class LLM(Character): 

    def __init__(self, x, y):
        super().__init__()
        self.sprite = self.load_sprite("./assets/npcs/llm3.png")
        #self.sprite = py.transform.scale(self.sprite, (36, 36))
        self.rect = self.sprite.get_rect(center=(x,y))
        self.facing_right = False

    """funzione temporanea, utile finché non avrò un'animazione per lo sprite. Successivamente
    utile importare la funzione per l'animazione per la classe padre"""
    @staticmethod
    def load_sprite (path):
        sprite = py.image.load(path).convert_alpha()
        return sprite
    
    def draw (self, surface, camera_rect, x, y):
        surface.blit(self.sprite, (x-camera_rect.x,y-camera_rect.y))

        