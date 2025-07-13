"""File in cui verranno inserite le funzioni create dal LLM
Nonostante sia migliore non inserire delle variabili globali, per evitare che il LLM dimentichi di prendere
gli elementi corretti, li mettiamo come globali per essere comunque accessibili"""
import pygame
import collision

player = None #prenderà l'oggetto player per poterlo "manipolare"
game_objects = None #prenderà gli oggetti del gioco con cui il player può interagire
#dt = 0 #prenderà il delta time del gioco per poter calcolare le velocità e le accelerazioni

#funzione che verrà richiamata nel main del gameloop
def set_game_context(player_obj, game_objects_list):
    """Funzione per impostare il contesto del gioco, in modo che le funzioni
    generate dal LLM possano accedere agli oggetti del gioco."""
    global player, game_objects, dt
    player = player_obj
    game_objects = game_objects_list
    #dt = delta_time


