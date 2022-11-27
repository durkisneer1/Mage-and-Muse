import pygame as pg
from settings import HEIGHT
from support import import_folder
from enemy import Enemy


class Decoration(pg.sprite.Sprite):
    def __init__(self, surface):
        super().__init__()

        self.display_surf = surface

        # imports
        self.bg_import()
        self.ground_import()
        self.enemy_sprite = Enemy(self.display_surf)

        self.bg_easy = True

    def ground_import(self):
        self.platform_back_easy = pg.transform.scale(pg.image.load('graphics/terrain/easy/midground.png'), (900, 75))
        self.platform_front_easy = pg.transform.scale(pg.image.load('graphics/terrain/easy/foreground.png'), (900, 75))
        self.platform_back_hard = pg.transform.scale(pg.image.load('graphics/terrain/hard/midground.png'), (900, 75))
        self.platform_front_hard = pg.transform.scale(pg.image.load('graphics/terrain/hard/foreground.png'), (900, 75))

    def mid_ground(self):
        if self.bg_easy:
            platform_back = self.platform_back_easy
        else:
            platform_back = self.platform_back_hard

        back_rect = platform_back.get_rect(bottomleft=(150, HEIGHT))
        self.display_surf.blit(platform_back, back_rect)

    def foreground(self):
        if self.bg_easy:
            platform_front = self.platform_front_easy
        else:
            platform_front = self.platform_front_hard

        front_rect = platform_front.get_rect(bottomleft = (150, HEIGHT))
        self.display_surf.blit(platform_front, front_rect)
        
    def collide_ground(self):
        self.c_image = pg.Surface((900, 50))
        self.c_rect = self.c_image.get_rect(bottomleft = (150, HEIGHT))
        self.display_surf.blit(self.c_image, self.c_rect)

    def bg_import(self):
        self.bg_surf_easy = import_folder('graphics/decoration/background/easy', 3)
        self.bg_surf_hard = import_folder('graphics/decoration/background/hard', 3)
        self.bg_frame = 0
        self.bg_anim_speed = 0.05

    def bg_anim(self):
        if self.bg_easy:
            bg_surf = self.bg_surf_easy
        else:
            bg_surf = self.bg_surf_hard

        self.bg_frame += self.bg_anim_speed
        if self.bg_frame >= len(bg_surf):
            self.bg_frame = 0

        bg = bg_surf[int(self.bg_frame)]
        self.display_surf.blit(bg, (0, 0))

    def draw(self):
        self.bg_anim()
        self.enemy_sprite.draw()
        self.collide_ground()
        self.mid_ground()
