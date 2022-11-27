import pygame as pg

from settings import *
from support import import_folder


class Enemy(pg.sprite.Sprite):
    def __init__(self, surface):
        super().__init__()

        self.display_surf = surface
        self.hitbox()

        # imports
        self.enemy_import()

        # status
        self.up = False
        self.y_pos = 85
        self.enemy_easy = True

    def enemy_import(self):
        self.enemy_surf_easy_idle = import_folder('graphics/enemy/main/idle/easy', 4)
        self.enemy_surf_hard_idle = import_folder('graphics/enemy/main/idle/hard', 4)
        self.enemy_frame = 0
        self.enemy_anim_speed = 0.05

    def enemy_anim_easy(self):
        if self.enemy_easy:
            enemy_sprite = self.enemy_surf_easy_idle
        else:
            enemy_sprite = self.enemy_surf_hard_idle

        self.enemy_frame += self.enemy_anim_speed
        if self.enemy_frame >= len(enemy_sprite) and self.up == False:
            self.enemy_frame = 0
            self.y_pos = 95
            self.up = True
        elif self.enemy_frame >= len(enemy_sprite) and self.up == True:
            self.enemy_frame = 0
            self.y_pos = 85
            self.up = False

        self.enemy_image = enemy_sprite[int(self.enemy_frame)]
        self.display_surf.blit(self.enemy_image, (0, self.y_pos))

    def hit_box(self):
        self.hitbox_surf = pg.Surface((320, 100))
        self.hitbox_rect = self.hitbox_surf.get_rect(center=(WIDTH / 2, 255))

        self.display_surf.blit(self.hitbox_surf, self.hitbox_rect)

    def draw(self):
        self.hit_box()
        self.enemy_anim_easy()
