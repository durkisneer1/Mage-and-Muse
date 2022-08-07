import pygame as pg
import random
from settings import *
from support import import_folder

class Notes(pg.sprite.Sprite):
    def __init__(self, surface):
        super().__init__()

        self.display_surf = surface

        self.surf = import_folder('graphics/enemy/notes', 3)
        self.current_frame = 0
        self.anim_speed = 0.08

        self.image = self.surf[0]

        self.side = random.choice(['left', 'right'])
        if self.side == 'left':
            self.rect = self.image.get_rect(topright = (0, 550))
        elif self.side == 'right':
            self.rect = self.image.get_rect(topleft = (WIDTH, 550))

        self.speed = 12

        # soundfx
        self.pick = random.randint(1, 4)
        self.sfx = pg.mixer.Sound(f'sounds/scroll/{self.pick}.mp3')
        self.sfx.set_volume(0.5)

    def frames(self):

        self.current_frame += self.anim_speed
        if self.current_frame >= len(self.surf):
            self.current_frame = 0

        self.image = self.surf[int(self.current_frame)]

    def update(self):

        if self.side == 'left':
            self.rect.x += self.speed
            if self.rect.left >= WIDTH:
                self.kill()
        else:
            self.rect.x -= self.speed
            if self.rect.right <= 0:
                self.kill()

    def draw(self, _):
    
        self.frames()
        self.update()
        self.display_surf.blit(self.image, self.rect)

class Pianos(pg.sprite.Sprite):
    def __init__(self, surface, ground):
        super().__init__()

        self.ground_rect = ground
        self.display_surf = surface
         
        self.surf = import_folder('graphics/enemy/piano', 3.5)
        self.current_frame = 0
        self.anim_speed = 0.1

        self.image = self.surf[0]

        self.x = random.randint(150, WIDTH - 350)
        self.rect = self.image.get_rect(bottomleft = (self.x, 0))

        self.speed = 15
        self.random_landing = random.randint(0, 3)

        # timer
        self.current_time = 0
        self.kill_time = 0
        self.landed = False

        # soundfx
        self.pick = random.randint(1, 3)
        self.sfx = pg.mixer.Sound(f'sounds/crash/{self.pick}.mp3')
        self.sfx.set_volume(0.5)

    def frames(self):

        if self.speed > 0:
            self.current_frame += self.anim_speed
            if self.current_frame >= len(self.surf):
                self.current_frame = 0
        elif self.speed == 0:
            self.current_frame = self.random_landing

        self.image = self.surf[int(self.current_frame)]

    def update(self, current_time):
        
        self.rect.y += self.speed
        if self.ground_rect.colliderect(self.rect) and self.landed == False:
            self.kill_time = pg.time.get_ticks()
            self.speed = 0
            self.landed = True

        if self.kill_time > 0:
            if current_time - self.kill_time > 1000:
                self.rect.left = WIDTH
                self.kill()

        return self.landed

    def draw(self, current_time):
        
        self.frames()
        self.update(current_time)
        self.display_surf.blit(self.image, self.rect)

class Horns(pg.sprite.Sprite):
    def __init__(self, surface, ground):
        super().__init__()

        self.display_surf = surface
        self.ground_rect = ground

        self.surf = import_folder('graphics/enemy/horn', 2.2)

        self.image = self.surf[0]
        self.image = pg.transform.rotate(self.image, 45)

        self.side = random.choice(['left', 'right'])
        if self.side == 'left':
            self.image = pg.transform.flip(self.image, True, False)
            self.rect = self.image.get_rect(bottomright = (0, 0))
        elif self.side == 'right':
            self.rect = self.image.get_rect(bottomleft = (WIDTH, 0))

        self.mask = pg.mask.from_surface(self.image)

        self.speed = 10

        # soundfx
        self.pick = random.randint(1, 4)
        self.sfx = pg.mixer.Sound(f'sounds/horns/{self.pick}.mp3')
        self.sfx.set_volume(0.5)
        
    def update(self):

        if self.side == 'left':
            self.rect.x += self.speed
            self.rect.y += self.speed
            if self.ground_rect.collidepoint(self.rect.center):
                self.kill()
        else:
            self.rect.x -= self.speed
            self.rect.y += self.speed
            if self.ground_rect.collidepoint(self.rect.center):
                self.kill()

    def draw(self, _):

        self.update()
        self.display_surf.blit(self.image, self.rect)

class LeftCymbal(pg.sprite.Sprite):
    def __init__(self, surface):
        super().__init__()

        self.display_surf = surface

        self.surf = import_folder('graphics/enemy/cymbal/left', 3.5)
        self.image = self.surf[0]
        self.rect = self.image.get_rect(topright = (0, 550))

        self.speed = 13
        self.crashed = False

        # timer
        self.current_time = 0
        self.kill_time = 0

        # sfx
        self.pick = random.randint(1, 4)
        self.sfx = pg.mixer.Sound(f'sounds/cymbal/{self.pick}.mp3')
        self.sfx.set_volume(0.5)
    
    def update(self, current_time):

        self.rect.x += self.speed
        if self.rect.right >= WIDTH / 2 and self.crashed == False:
            self.rect.right = WIDTH / 2
            self.kill_time = pg.time.get_ticks()
            self.speed = 0
            self.crashed = True

        if self.kill_time > 0:
            if current_time - self.kill_time > 750:
                self.rect.left = WIDTH
                self.kill()

        return self.crashed

    def draw(self, current_time):

        self.update(current_time)
        self.display_surf.blit(self.image, self.rect)

class RightCymbal(pg.sprite.Sprite):
    def __init__(self, surface):
        super().__init__()

        self.display_surf = surface

        self.surf = import_folder('graphics/enemy/cymbal/right', 3.5)
        self.image = self.surf[0]
        self.rect = self.image.get_rect(topleft = (WIDTH, 550))

        self.speed = 13
        self.crashed = False

        # timer
        self.current_time = 0
        self.kill_time = 0

        # sfx
    
    def update(self, current_time):

        self.rect.x -= self.speed
        if self.rect.left <= WIDTH / 2 and self.crashed == False:
            self.rect.left = WIDTH / 2
            self.kill_time = pg.time.get_ticks()
            self.speed = 0
            self.crashed = True
        
        if self.kill_time > 0:
            if current_time - self.kill_time > 750:
                self.rect.left = WIDTH
                self.kill()
        
        return self.crashed

    def draw(self, current_time):

        self.update(current_time)
        self.display_surf.blit(self.image, self.rect)