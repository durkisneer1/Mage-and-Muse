import pygame as pg
from support import import_folder
from settings import *
import math

class Player(pg.sprite.Sprite):
    def __init__(self, pos, surface, jump_dust):
        super().__init__()

        # character variables
        self.char_import()
        self.char_frame = 0
        self.char_anim_speed = 0.1
        self.image = self.anims['idle'][self.char_frame]
        self.rect = self.image.get_rect(bottomleft = pos)

        # dust particles
        self.dust = import_folder('../graphics/character/dust_particles/run', 1)
        self.dust_frame = 0
        self.dust_anim_speed = 0.15
        self.display_surf = surface
        self.jump_dust = jump_dust

        # player movement
        self.direction = pg.math.Vector2(0, 0)
        self.gravity = 1.2
        self.jump_speed = -22
        self.dash_speed = 25
        self.flinch_distance = 80

        # player status
        self.status = 'idle'
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False
        self.jumped = False
        self.dashed = False
        self.stunned = False

        # wand
        self.wand = import_folder('../graphics/character/wand', 4)

        # sfx
        self.sfx = None

    def char_import(self):

        char_path = '../graphics/character/'
        self.anims = {'idle':[], 'run':[], 'jump':[], 'fall':[], 'hit':[]}

        for anim in self.anims.keys():
            full_path = char_path + anim
            self.anims[anim] = import_folder(full_path, 3)

    def char_anim(self):
        
        # loop over frame index
        char_anim = self.anims[self.status]
        self.char_frame += self.char_anim_speed
        if self.char_frame >= len(char_anim):
            self.char_frame = 0

        image = char_anim[int(self.char_frame)]
        if self.facing_right:
            self.image = image
        else:
            facing_left = pg.transform.flip(image, True, False)
            self.image = facing_left
        
        # set the rect
        if self.on_ground and self.on_right:
            self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
        elif self.on_ground and self.on_left:
            self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
        elif self.on_ground:
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)

        elif self.on_ceiling and self.on_right:
            self.rect = self.image.get_rect(topright = self.rect.topright)
        elif self.on_ceiling and self.on_left:
            self.rect = self.image.get_rect(topleft = self.rect.topleft)
        elif self.on_ceiling:
            self.rect = self.image.get_rect(midtop = self.rect.midtop)

    def dust_anim(self):

        if self.status == 'run' and self.on_ground:
            self.dust_frame += self.dust_anim_speed
            if self.dust_frame >= len(self.dust):
                self.dust_frame = 0

            dust_particle = self.dust[int(self.dust_frame)]

            if self.facing_right:
                pos = self.rect.bottomleft - pg.math.Vector2(6, 10)
                self.display_surf.blit(dust_particle, pos)
            else:
                pos = self.rect.bottomright - pg.math.Vector2(6, 10)
                flipped_dust = pg.transform.flip(dust_particle, True, False)
                self.display_surf.blit(flipped_dust, pos)

    def handle_wand(self, mouse_pos):

        wand = self.wand[0]
        wand = pg.transform.rotate(wand, -45)
        
        mouse_x, mouse_y = mouse_pos

        x, y = self.rect.center
        rel_x, rel_y = mouse_x - x, mouse_y - y
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)

        wand_copy = pg.transform.rotate(wand, angle)
        wand_rect = wand_copy.get_rect(center = (x, y))

        self.display_surf.blit(wand_copy, wand_rect)

    def get_input(self, events):

        keys = pg.key.get_pressed()

        if keys[pg.K_d]:
            self.direction.x = 1
            self.facing_right = True
        elif keys[pg.K_a]:
            self.direction.x = -1
            self.facing_right = False
        else:
            self.direction.x = 0

        if self.rect.bottom >= HEIGHT:
            self.jump()
            self.jump_dust(self.rect.midbottom)
            self.jumped = True

        if self.on_ground:
            self.dashed = False

        for event in events:
            if event.type == pg.KEYDOWN:

                if event.key == pg.K_SPACE and self.on_ground:
                    self.jump()
                    self.jump_dust(self.rect.midbottom)
                    self.jumped = True
                elif event.key == pg.K_SPACE and self.jumped == True and not self.on_ground:
                    self.jump()
                    self.jump_dust(self.rect.midbottom)
                    self.jumped = False
                
                if event.key == pg.K_LSHIFT and self.dashed == False:
                    if self.direction.x > 0:
                        self.direction.x = self.dash_speed
                    elif self.direction.x < 0:
                        self.direction.x = self.dash_speed * -1
                    self.dashed = True

    def get_status(self):

        if self.direction.y < 0 and self.stunned == False:
            self.status = 'jump'
        elif self.direction.y < 0 and self.stunned == True:
            self.status = 'hit'
        elif self.direction.y > 1:
            self.status = 'fall'
        else:
            if self.direction.x != 0:
                self.status = 'run'
            else:
                self.status = 'idle'

    def apply_gravity(self):

        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):

        self.direction.y = self.jump_speed
        self.stunned = False

    def stun(self):

        self.direction.y = self.jump_speed * (2 / 3)
        self.stunned = True

    def update(self, events):

        self.get_input(events)
        self.get_status()
        self.char_anim()
        self.dust_anim()

class Projectile(pg.sprite.Sprite):
    def __init__(self, surface, pos, mouse_pos):
        super().__init__()

        self.display_surf = surface

        self.x, self.y = pos
        self.mouse_x, self.mouse_y = mouse_pos
        self.speed = 15

        self.angle = math.atan2(self.y - self.mouse_y, self.x - self.mouse_x)
        self.x_vel = math.cos(self.angle) * self.speed
        self.y_vel = math.sin(self.angle) * self.speed

        self.sfx = pg.mixer.Sound(f'../sounds/shoot/shoot.mp3')
        self.sfx.set_volume(1.0)

    def update(self):

        self.x -= int(self.x_vel)
        self.y -= int(self.y_vel)

        if self.x > WIDTH or self.x < 0:
            self.kill()
        elif self.y > HEIGHT or self.y < 0:
            self.kill()

        pg.draw.circle(self.display_surf, (135, 225, 255), (self.x, self.y), 6)