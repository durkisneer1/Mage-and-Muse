import pygame as pg
from settings import *

class Menu:
    def __init__(self, surface):

        self.display_surf = surface

        self.image = pg.image.load('../graphics/menu/title.png')
        self.rect = self.image.get_rect(topleft = (40, 75))

        self.font = pg.font.Font('../fonts/Kenney Pixel.ttf', 36)
        self.text = self.font.render('Created  by  durk#1224  and  Sjmarf#1894', True, 'white')
        self.text_rect = self.text.get_rect(bottomleft = (10, HEIGHT - 10))

        self.bg_image = pg.transform.scale(pg.image.load('../graphics/menu/bg.png'), (1200, 700))
        self.bg_rect = self.bg_image.get_rect(topleft = (0, 0))

    def update(self):

        self.display_surf.blit(self.bg_image, self.bg_rect)
        self.display_surf.blit(self.image, self.rect)
        self.display_surf.blit(self.text, self.text_rect)

class Win:
    def __init__(self, surface):

        self.display_surf = surface

        self.title_font = pg.font.Font('../fonts/Kenney Pixel.ttf', 72)
        self.sub_font = pg.font.Font('../fonts/Kenney Pixel.ttf', 48)
        self.win_info = self.title_font.render('YOU BEAT THE BEAT !', True, 'white')
        self.replay_info = self.sub_font.render('.Press ENTER to play again.', True, 'white')
        self.menu_info = self.sub_font.render('.or press ESC to return to menu.', True, 'white')
        self.win_rect = self.win_info.get_rect(center = (WIDTH / 2, HEIGHT / 2 - 20))
        self.replay_rect = self.replay_info.get_rect(center = (WIDTH / 2, HEIGHT / 2 + 20))
        self.menu_rect = self.menu_info.get_rect(center = (WIDTH / 2, HEIGHT / 2 + 60))

        self.bg_image = pg.transform.scale(pg.image.load('../graphics/menu/win.png'), (1200, 700))
        self.bg_rect = self.bg_image.get_rect(topleft = (0, 0))
    
    def update(self):

        self.display_surf.blit(self.bg_image, self.bg_rect)
        self.display_surf.blit(self.win_info, self.win_rect)
        self.display_surf.blit(self.replay_info, self.replay_rect)
        self.display_surf.blit(self.menu_info, self.menu_rect)

class Lose:
    def __init__(self, surface):

        self.display_surf = surface

        self.title_font = pg.font.Font('../fonts/Kenney Pixel.ttf', 72)
        self.sub_font = pg.font.Font('../fonts/Kenney Pixel.ttf', 48)
        self.death_info = self.title_font.render('YOU\'RE NOT SHARP ENOUGH !', True, 'white')
        self.replay_info = self.sub_font.render('.Press ENTER to start over.', True, 'white')
        self.menu_info = self.sub_font.render('.or press ESC to return to menu.', True, 'white')
        self.death_rect = self.death_info.get_rect(center = (WIDTH / 2, HEIGHT / 2 - 20))
        self.replay_rect = self.replay_info.get_rect(center = (WIDTH / 2, HEIGHT / 2 + 20))
        self.menu_rect = self.menu_info.get_rect(center = (WIDTH / 2, HEIGHT / 2 + 60))

        self.bg_image = pg.transform.scale(pg.image.load('../graphics/menu/lose.png'), (1200, 700))
        self.bg_rect = self.bg_image.get_rect(topleft = (0, 0))
    
    def update(self):

        self.display_surf.blit(self.bg_image, self.bg_rect)
        self.display_surf.blit(self.death_info, self.death_rect)
        self.display_surf.blit(self.replay_info, self.replay_rect)
        self.display_surf.blit(self.menu_info, self.menu_rect)

class Pause:
    def __init__(self, surface):

        self.display_surf = surface

        # box
        self.image = pg.Surface((WIDTH * (5 / 6), HEIGHT * (5 / 6)))
        self.image.fill('gray')
        self.rect = self.image.get_rect(center = (WIDTH / 2, HEIGHT / 2))

        self.x, self.y = self.rect.topleft

        # text
        self.font = pg.font.Font('../fonts/Kenney Pixel.ttf', 72)
        self.pause_info = self.font.render('PAUSED', True, 'black')
        self.pause_info_rect = self.pause_info.get_rect(center = (WIDTH / 2, 100))

        self.resume_fill = pg.Surface((190, 70))
        self.resume_fill.fill('white')
        self.resume_rect = self.resume_fill.get_rect(topleft = (WIDTH / 2 - 235, HEIGHT / 2 - 25))

        self.menu_fill = pg.Surface((190, 70))
        self.menu_fill.fill('white')
        self.menu_rect = self.menu_fill.get_rect(topleft = (WIDTH / 2 + 40, HEIGHT / 2 - 25))

    def update(self):

        self.display_surf.blit(self.image, self.rect)
        # window border
        pg.draw.rect(self.display_surf, 'black', pg.Rect(self.x, self.y, WIDTH * (5 / 6), HEIGHT * (5 / 6)), 6)
        pg.draw.rect(self.display_surf, 'white', pg.Rect(self.x, self.y, WIDTH * (5 / 6), HEIGHT * (5 / 6)), 3)
        
        # button borders
        self.display_surf.blit(self.resume_fill, self.resume_rect)
        pg.draw.rect(self.display_surf, 'black', pg.Rect(WIDTH / 2 - 235, HEIGHT / 2 - 25, 190, 70), 3)
        self.display_surf.blit(self.menu_fill, self.menu_rect)
        pg.draw.rect(self.display_surf, 'black', pg.Rect(WIDTH / 2 + 40, HEIGHT / 2 - 25, 190, 70), 3)

        self.display_surf.blit(self.pause_info, self.pause_info_rect)

class Controls:
    def __init__(self, surface):

        self.display_surf = surface

        self.title_font = pg.font.Font('../fonts/Kenney Pixel.ttf', 72)
        self.sub_font = pg.font.Font('../fonts/Kenney Pixel.ttf', 48)

        self.title_info = self.title_font.render('CONTROLS', True, 'white')
        self.wasd_info = self.sub_font.render('WASD - Movement', True, 'white')
        self.space_info = self.sub_font.render('SPACEBAR - Jump/Double-Jump', True, 'white')
        self.shift_info = self.sub_font.render('LSHIFT - Dash', True, 'white')
        self.click_info = self.sub_font.render('LCLICK - Hold to shoot at the boss', True, 'white')

        self.title_rect = self.title_info.get_rect(center = (WIDTH / 2, 100))
        self.wasd_rect = self.wasd_info.get_rect(center = (WIDTH / 2, 250))
        self.space_rect = self.space_info.get_rect(center = (WIDTH / 2, 350))
        self.shift_rect = self.shift_info.get_rect(center = (WIDTH / 2, 450))
        self.click_rect = self.click_info.get_rect(center = (WIDTH / 2, 550))

        self.bg_image = pg.transform.scale(pg.image.load('../graphics/menu/bg.png'), (1200, 700))
        self.bg_rect = self.bg_image.get_rect(topleft = (0, 0))
    
    def update(self):

        self.display_surf.blit(self.bg_image, self.bg_rect)
        self.display_surf.blit(self.title_info, self.title_rect)
        self.display_surf.blit(self.wasd_info, self.wasd_rect)
        self.display_surf.blit(self.space_info, self.space_rect)
        self.display_surf.blit(self.shift_info, self.shift_rect)
        self.display_surf.blit(self.click_info, self.click_rect)

class Button:
    def __init__(self, surface, pos, text, color):

        self.display_surf = surface

        font = pg.font.Font('../fonts/Kenney Pixel.ttf', 72)
        self.text = font.render(text, True, color)
        self.rect = self.text.get_rect(topleft = pos)

        self.clicked = False

    def draw(self):
        
        action = False
        pos = pg.mouse.get_pos()
        
        if self.rect.collidepoint(pos):
            if pg.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

        if pg.mouse.get_pressed()[0] == 0:
            self.clicked = False

        self.display_surf.blit(self.text, self.rect)

        return action