import pygame

class Timer:
    def __init__(self, delay_ms):
        self.delay = delay_ms
        self.last_time = pygame.time.get_ticks()

    def ready(self):
        now = pygame.time.get_ticks()
        if now - self.last_time >= self.delay:
            self.last_time = now
            return True
        return False