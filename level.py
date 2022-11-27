import random

import pygame as pg

from UI import Health, BossHealth
from decoration import Decoration
from events import Notes, Pianos, Horns, LeftCymbal, RightCymbal
from particles import ParticleEffect
from player import Player, Projectile
from settings import *


class Level:
    def __init__(self, surface):

        # events
        self.SPAWN_RANDOM_OBS_EASY = pg.USEREVENT + 1
        self.SPAWN_RANDOM_OBS_HARD = pg.USEREVENT + 2
        pg.time.set_timer(self.SPAWN_RANDOM_OBS_EASY, 1300)
        pg.time.set_timer(self.SPAWN_RANDOM_OBS_HARD, 800)

        # variable setup
        self.display_surf = surface
        self.setup_level()
        self.current_x = 0
        self.player_hit = False

        # UI
        self.player_hp = Health(self.display_surf)

        # dust
        self.dust_sprite = pg.sprite.GroupSingle()
        self.player_on_ground = False

        # obstacle group
        self.obs_group = pg.sprite.Group()
        self.piano_sprite = None
        self.crash_played = False
        self.hit_played = False
        self.L_cymbal_sprite = None
        self.R_cymbal_sprite = None
        self.horn_sprite = None

        # timer
        self.player_hit_time = 0
        self.piano_kill_time = 0

        # projectiles
        self.projectile_group = pg.sprite.Group()
        self.shoot_delay = 0

        # enemy
        self.boss_hp = BossHealth(self.display_surf)

    def dust_jump(self, pos):
        if self.player.sprite.facing_right:
            pos -= pg.math.Vector2(10, 5)
        else:
            pos += pg.math.Vector2(10, -5)

        jump_particle = ParticleEffect(pos, 'jump')
        self.dust_sprite.add(jump_particle)

    def get_stand(self):
        if self.player.sprite.on_ground:
            self.player_on_ground = True
        else:
            self.player_on_ground = False

    def dust_land(self):
        if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites():
            if self.player.sprite.facing_right:
                offset = pg.math.Vector2(10, 15)
            else:
                offset = pg.math.Vector2(-10, 15)
            fall_particle = ParticleEffect(self.player.sprite.rect.midbottom - offset, 'land')
            self.dust_sprite.add(fall_particle)

    def decoration_draw(self):
        self.decor_group = pg.sprite.GroupSingle()
        self.decor_sprite = Decoration(self.display_surf)
        self.decor_group.add(self.decor_sprite)

    def hard_scenery(self):
        if self.boss_hp.health_remain <= 1250:
            self.decor_sprite.bg_easy = False
            self.decor_sprite.enemy_sprite.enemy_easy = False

    def random_obstacle(self, current_time, events):
        for event in events:
            if self.boss_hp.health_remain >= 1250:
                if event.type == self.SPAWN_RANDOM_OBS_EASY:

                    pick = random.randint(0, 3)
                    if pick == 0:
                        note_sprite = Notes(self.display_surf)
                        self.obs_group.add(note_sprite)
                        note_sprite.sfx.play()
                    elif pick == 1:
                        self.piano_sprite = Pianos(self.display_surf, self.decor_sprite.c_rect)
                        self.obs_group.add(self.piano_sprite)
                        self.crash_played = False
                    elif pick == 2:
                        self.horn_sprite = Horns(self.display_surf, self.decor_sprite.c_rect)
                        self.obs_group.add(self.horn_sprite)
                        self.horn_sprite.sfx.play()
                    elif pick == 3:
                        self.L_cymbal_sprite = LeftCymbal(self.display_surf)
                        self.R_cymbal_sprite = RightCymbal(self.display_surf)
                        self.obs_group.add(self.L_cymbal_sprite)
                        self.obs_group.add(self.R_cymbal_sprite)
                        self.hit_played = False
            else:
                if event.type == self.SPAWN_RANDOM_OBS_HARD:

                    pick = random.randint(0, 3)
                    if pick == 0:
                        note_sprite = Notes(self.display_surf)
                        self.obs_group.add(note_sprite)
                        note_sprite.sfx.play()
                    elif pick == 1:
                        self.piano_sprite = Pianos(self.display_surf, self.decor_sprite.c_rect)
                        self.obs_group.add(self.piano_sprite)
                        self.crash_played = False
                    elif pick == 2:
                        self.horn_sprite = Horns(self.display_surf, self.decor_sprite.c_rect)
                        self.obs_group.add(self.horn_sprite)
                        self.horn_sprite.sfx.play()
                    elif pick == 3:
                        self.L_cymbal_sprite = LeftCymbal(self.display_surf)
                        self.R_cymbal_sprite = RightCymbal(self.display_surf)
                        self.obs_group.add(self.L_cymbal_sprite)
                        self.obs_group.add(self.R_cymbal_sprite)
                        self.hit_played = False

        for sprite in self.obs_group:
            sprite.draw(current_time)
            if self.piano_sprite != None:
                if sprite == self.piano_sprite and self.crash_played == False:
                    if self.piano_sprite.landed == True:
                        self.piano_sprite.sfx.play()
                        self.crash_played = True
            if self.L_cymbal_sprite != None and self.R_cymbal_sprite != None:
                if sprite == self.L_cymbal_sprite and self.hit_played == False:
                    if self.L_cymbal_sprite.crashed == True:
                        self.L_cymbal_sprite.sfx.play()
                        self.hit_played = True

    def player_draw(self):
        self.player = pg.sprite.GroupSingle()
        self.player_sprite = Player((WIDTH / 2, HEIGHT / 2), self.display_surf, self.dust_jump)
        self.player.add(self.player_sprite)

    def setup_level(self):
        self.decoration_draw()
        self.player_draw()

    def limit(self):
        player = self.player.sprite
        direction_x = player.direction.x

        if player.rect.left <= 0 and direction_x < 0:
            player.speed = 0
            player.rect.left = 0
        elif player.rect.right >= WIDTH and direction_x > 0:
            player.speed = 0
            player.rect.right = WIDTH
        else:
            player.speed = 7

    def h_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        for sprite in self.decor_group:
            if sprite.c_rect.colliderect(player.rect):

                if player.direction.x < 0:
                    player.rect.left = sprite.c_rect.right

                elif player.direction.x > 0:
                    player.rect.right = sprite.c_rect.left

    def v_collision(self):
        player = self.player.sprite
        player.apply_gravity()

        for sprite in self.decor_group:
            if sprite.c_rect.colliderect(player.rect):

                if player.direction.y > 0:
                    player.rect.bottom = sprite.c_rect.top
                    player.direction.y = 0
                    player.on_ground = True

                elif player.direction.y < 0:
                    player.rect.top = sprite.c_rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True

        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0:
            player.on_ceiling = False

    def obs_collision(self, current_time):
        for sprite in self.obs_group:
            if sprite.rect.colliderect(self.player.sprite.rect) and self.player_hit == False:
                if self.horn_sprite != None and sprite == self.horn_sprite:
                    if pg.sprite.collide_mask(self.player.sprite, self.horn_sprite):
                        pick = random.randint(1, 3)
                        self.player.sprite.sfx = pg.mixer.Sound(f'sounds/hurt/{pick}.mp3')
                        self.player.sprite.sfx.set_volume(0.8)
                        self.player.sprite.sfx.play()
                        self.player.sprite.stun()
                        self.player_hit_time = pg.time.get_ticks()
                        self.player_hp.hit()
                        self.player_hit = True
                else:
                    pick = random.randint(1, 3)
                    self.player.sprite.sfx = pg.mixer.Sound(f'sounds/hurt/{pick}.mp3')
                    self.player.sprite.sfx.set_volume(0.8)
                    self.player.sprite.sfx.play()
                    self.player.sprite.stun()
                    self.player_hit_time = pg.time.get_ticks()
                    self.player_hp.hit()
                    self.player_hit = True

        if current_time - self.player_hit_time > 2000 and self.player_hit == True:
            self.player_hit = False

    def shooting(self, mouse_pos):
        if pg.mouse.get_pressed()[0]:
            self.shoot_delay += 1
            if self.shoot_delay >= 10:
                projectile = Projectile(self.display_surf, self.player.sprite.rect.center, mouse_pos)
                self.projectile_group.add(projectile)
                projectile.sfx.play()
                self.shoot_delay = 0

        for sprite in self.projectile_group:
            sprite.update()

    def enemy_manager(self):
        for sprite in self.projectile_group:
            if self.decor_sprite.enemy_sprite.hitbox_rect.collidepoint((sprite.x, sprite.y)):
                sprite.kill()
                self.boss_hp.hit()

        self.boss_hp.draw()

    def run(self, events, current_time, mouse_pos):
        # floor
        self.decor_sprite.draw()

        # dust particles
        self.dust_sprite.update()
        self.dust_sprite.draw(self.display_surf)

        # barriers
        self.limit()

        # events
        self.hard_scenery()
        self.random_obstacle(current_time, events)
        self.shooting(mouse_pos)
        self.obs_collision(current_time)

        # player
        self.player.update(events)
        self.h_collision()
        self.get_stand()
        self.v_collision()
        self.dust_land()
        self.player.draw(self.display_surf)
        self.player.sprite.handle_wand(mouse_pos)

        # foreground
        self.decor_sprite.foreground()

        # score
        self.player_hp.hp_blit()
        self.enemy_manager()
