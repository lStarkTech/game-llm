import pygame as py
from character import Character

class LLM(Character): 



    """funzione temporanea, utile finché non avrò un'animazione per lo sprite. Successivamente
    utile importare la funzione per l'animazione per la classe padre"""
    def load_sprite (path):
        sprite = py.image.load(path).convert_alpha()
        if(sprite):
            print(f"lo sprite è stato caricato correttamente")
        return sprite
    
    def draw ()