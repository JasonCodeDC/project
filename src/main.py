# main.py
import random
from typing import Tuple, TypedDict

import pygame
from pygame.locals import QUIT

from modules.animals import Animal
from modules.world import Map

WIDTH, HEIGHT = 1280, 720


class Settings(TypedDict):
    speed: int
    health: int
    strength: int
    colour: Tuple[int, int, int]


PRIMARY_SETTINGS: Settings = {
    "speed": 4,
    "health": 40,
    "strength": 15,
    "colour": (0xFF, 0x00, 0xFF),
}
SECONDARY_SETTINGS: Settings = {
    "speed": 10,
    "health": 80,
    "strength": 30,
    "colour": (0xFF, 0xFF, 0x00),
}
TERTIARY_SETTINGS: Settings = {
    "speed": 30,
    "health": 150,
    "strength": 50,
    "colour": (0xFF, 0x00, 0x00),
}


def spawn(group: pygame.sprite.Group, settings: Settings, amount: int):
    for _ in range(amount):
        Animal(
            group,
            random.randint(0, WIDTH),
            random.randint(0, HEIGHT),
            settings["speed"],
            settings["health"],
            settings["strength"],
            settings["colour"],
        )


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    Animal.set_bounds(WIDTH, HEIGHT)

    world = Map(640, 360)
    world.generate_map()

    tile_w = WIDTH // world._width
    tile_h = HEIGHT // world._height
    map_surface = pygame.Surface((WIDTH, HEIGHT))
    for y in range(world._height):
        for x in range(world._width):
            colour = world.get_tile_colour(x, y)
            rect = pygame.Rect(x * tile_w, y * tile_h, tile_w, tile_h)
            map_surface.fill(colour, rect)

    primary = pygame.sprite.Group()
    secondary = pygame.sprite.Group()
    tertiary = pygame.sprite.Group()

    spawn(primary, PRIMARY_SETTINGS, 10)
    spawn(secondary, SECONDARY_SETTINGS, 10)
    spawn(tertiary, TERTIARY_SETTINGS, 10)

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                raise SystemExit(0)

        primary.update()
        secondary.update()
        tertiary.update()

        screen.blit(map_surface, (0, 0))
        primary.draw(screen)
        secondary.draw(screen)
        tertiary.draw(screen)

        pygame.display.flip()
        clock.tick(5)
