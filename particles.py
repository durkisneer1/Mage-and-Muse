import pygame as pg

from support import import_folder


class ParticleEffect(pg.sprite.Sprite):
    def __init__(self, pos, type):
        super().__init__()

        self.frame = 0
        self.anim_speed = 0.5

        if type == 'jump':
            self.frames = import_folder('graphics/character/dust_particles/jump', 1)
        elif type == 'land':
            self.frames = import_folder('graphics/character/dust_particles/land', 1)

        self.image = self.frames[self.frame]
        self.rect = self.image.get_rect(center=pos)

    def animate(self):
        self.frame += self.anim_speed

        if self.frame >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame)]

    def update(self):
        self.animate()
