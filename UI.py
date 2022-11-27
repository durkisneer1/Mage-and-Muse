import pygame as pg

from settings import *


class Health:
    def __init__(self, surface):
        self.display_surf = surface
        self.health_remain = 3

        self.font = pg.font.Font('fonts/Kenney Pixel.ttf', 72)
        self.hp_count = self.font.render(f'Lives left: {self.health_remain}', True, 'white')
        self.hp_rect = self.hp_count.get_rect(bottomleft=(10, HEIGHT))

    def hit(self):
        self.health_remain -= 1
        self.hp_count = self.font.render(f'Lives left: {self.health_remain}', True, 'white')

    def hp_blit(self):
        self.display_surf.blit(self.hp_count, self.hp_rect)


class BossHealth:
    def __init__(self, surface):
        self.display_surf = surface
        self.health_remain = 3000

        self.font = pg.font.Font('fonts/Kenney Pixel.ttf', 72)
        self.hp_count = self.font.render(f'Boss HP: {self.health_remain}', True, 'white', 'black')
        self.hp_rect = self.hp_count.get_rect(midtop=(WIDTH / 2, 0))

    def hit(self):
        self.health_remain -= 10
        self.hp_count = self.font.render(f'Boss HP: {self.health_remain}', True, 'white', 'black')

    def draw(self):
        self.display_surf.blit(self.hp_count, self.hp_rect)
