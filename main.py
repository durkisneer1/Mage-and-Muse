import pygame as pg

from level import Level
from screens import Lose, Pause, Win, Menu, Controls, Button
from settings import *

pg.mixer.pre_init(48000, -16, 2, 512)
pg.init()


class Game:
    def __init__(self):
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption('Mage and Muse')
        pg.display.set_icon(pg.image.load('graphics/character/wand/wand.png'))
        self.clock = pg.time.Clock()

        self.level = Level(self.screen)
        self.lose_screen = Lose(self.screen)
        self.pause_screen = Pause(self.screen)
        self.win_screen = Win(self.screen)
        self.menu_screen = Menu(self.screen)
        self.controls_screen = Controls(self.screen)

        # buttons
        self.start_button = Button(self.screen, (50, HEIGHT * (4 / 9) - 50), 'START', 'white')
        self.controls_button = Button(self.screen, (50, HEIGHT / 2 - 20), 'CONTROLS', 'white')
        self.exit_button = Button(self.screen, (50, HEIGHT * (5 / 9) + 10), 'EXIT', 'white')

        self.resume_button = Button(self.screen, (WIDTH / 2 - 225, HEIGHT / 2 - 20), 'RESUME', 'black')
        self.menu_button = Button(self.screen, (WIDTH / 2 + 75, HEIGHT / 2 - 20), 'MENU', 'black')

        # timer
        self.current_time = 0

        # music
        pg.mixer.music.load('sounds/music/music.wav')
        pg.mixer.music.set_volume(0.25)

    def menu(self):
        pg.mixer.music.stop()
        running = True
        while running:

            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    pg.quit()
                    raise SystemExit
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        pg.quit()
                        raise SystemExit

            self.menu_screen.update()

            if self.start_button.draw():
                self.game()
            if self.controls_button.draw():
                self.controls()
            if self.exit_button.draw():
                pg.quit()
                raise SystemExit

            pg.display.update()
            self.clock.tick(60)

    def game(self):
        pg.mixer.music.play(-1)
        pg.mixer.music.set_volume(0.25)

        running = True
        while running:

            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    pg.quit()
                    raise SystemExit
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.pause()

            self.current_time = pg.time.get_ticks()
            mouse_pos = pg.mouse.get_pos()

            self.level.run(events, self.current_time, mouse_pos)
            if self.level.player_hp.health_remain <= 0:
                self.lose()
            elif self.level.boss_hp.health_remain <= 0:
                self.win()

            pg.display.update()
            self.clock.tick(60)

    def win(self):
        pg.mixer.music.fadeout(1500)

        running = True
        while running:

            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    pg.quit()
                    raise SystemExit
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.level = Level(self.screen)
                        self.menu()
                    elif event.key == pg.K_RETURN:
                        self.level = Level(self.screen)
                        pg.mixer.music.play(-1)
                        running = False

            self.win_screen.update()

            pg.display.update()
            self.clock.tick(60)

    def lose(self):
        pg.mixer.music.fadeout(1500)

        running = True
        while running:

            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    pg.quit()
                    raise SystemExit
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.level = Level(self.screen)
                        self.menu()
                    elif event.key == pg.K_RETURN:
                        self.level = Level(self.screen)
                        pg.mixer.music.play(-1)
                        running = False

            self.lose_screen.update()

            pg.display.update()
            self.clock.tick(60)

    def pause(self):
        pg.mixer.music.set_volume(0.1)

        running = True
        while running:

            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    pg.quit()
                    raise SystemExit
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        pg.mixer.music.set_volume(0.25)
                        running = False

            self.pause_screen.update()
            if self.resume_button.draw():
                pg.mixer.music.set_volume(0.25)
                running = False
            elif self.menu_button.draw():
                self.level = Level(self.screen)
                self.menu()

            pg.display.update()
            self.clock.tick(60)

    def controls(self):
        running = True
        while running:

            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    pg.quit()
                    raise SystemExit
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        running = False

            self.controls_screen.update()

            pg.display.update()
            self.clock.tick(60)


if __name__ == '__main__':
    launch = Game()
    launch.menu()
