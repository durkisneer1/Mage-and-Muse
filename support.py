from os import walk
import pygame as pg


def import_folder(path, scale):
    surf_list = []
    for _, __, img_file in walk(path):
        for image in img_file:
            full_path = path + '/' + image
            image_surf = pg.image.load(full_path).convert_alpha()
            x, y = image_surf.get_size()
            image_surf = pg.transform.scale(image_surf, (x * scale, y * scale))
            surf_list.append(image_surf)

    return surf_list