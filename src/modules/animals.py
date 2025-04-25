import random

import pygame
from pygame.sprite import Group, Sprite

from typing import Tuple

class InvalidDirectionError(Exception):
    pass


class Animal(Sprite):
    """
    Base implementation of the animals that will be used for predators and prey

    :param groups: The group to add the animal into
    :type groups: pygame.sprite.Group
    :param x: Starting x coordinate of the animal
    :type x: int
    :param y: Starting y coordinate of the animal
    :type y: int
    :param speed: Movement speed of the animal
    :type speed: int
    :param health: Max HP of the animal
    :type health: int
    :param strength: Damage per hit from the animal
    :type strength: int
    """

    @classmethod
    def set_bounds(cls, width: int, height: int) -> None:
        """
        Sets the screen bounds in every instance of the class, so animals can't leave the screen

        :param width: Screen width
        :type width: int
        :param height: Screen height
        :type height: int
        """
        cls._screen_width = width
        cls._screen_height = height

    def __init__(
        self,
        groups: Tuple[Group, ...],
        x: int,
        y: int,
        speed: int,
        health: int,
        strength: int,
        colour: Tuple[int, int, int]
    ) -> None:
        """
        Constructor method
        """
        super().__init__(groups)
        self.image = pygame.Surface([10, 10])
        self.image.fill(colour)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self._speed = speed
        self._max_health = health
        self._strength = strength

    def move(self, direction: str) -> None:
        """
        Move the animal :attr:`self._speed` units in a certain direction

        Accepted directions are: ``"up"``, ``"down"``, ``"left"``, ``"right"``

        :param direction: The direction the animal moves towards
        :type direction: str
        :raises InvalidDirectionError: If **direction** is not one of the accepted ones
        """
        match direction:
            case "up":
                self.rect.y -= self._speed
            case "down":
                self.rect.y += self._speed
            case "left":
                self.rect.x -= self._speed
            case "right":
                self.rect.x += self._speed
            case _:
                raise InvalidDirectionError("Invalid direction (up, down, left, right)")
            
        max_x = self._screen_width - self.rect.width
        max_y = self._screen_height - self.rect.height
        self.rect.x = max(0, min(self.rect.x, max_x))
        self.rect.y = max(0, min(self.rect.y, max_y))

    def update(self) -> None:
        """
        Basic implementation for testing the animals

        TODO: implement neural network for animals
        """
        # outputs = self.think(inputs)
        # self.move(direction = outputs[0], speed = outputs[1])
        self.move(random.choice(["up", "down", "right", "left"]))