import random

import pygame


class Animal(pygame.sprite.Sprite):
    def __init__(self, maxHealth: int, damage: int, position: list, size: int) -> None:
        super().__init__()
        self.image = pygame.Surface([size, size])
        self.image.fill(
            (255, 255, 255)
        )
        self._maxHealth = maxHealth
        self._damage = damage
        self._position = position.copy()
        self.rect = self.image.get_rect(topleft=self._position)

    def move(
        self, dx: int, dy: int, screen_rect: pygame.Rect, group: pygame.sprite.Group
    ):
        """
        Attempt to move by (dx, dy). If the movement would cause a collision with the screen border or with any other sprite in the group, return to original position.
        """
        old_position = self._position.copy()

        self._position[0] += dx
        self._position[1] += dy
        self.rect.topleft = self._position

        if not screen_rect.contains(self.rect):
            self._position = old_position
            self.rect.topleft = self._position
            return

        for sprite in group:
            if sprite != self and self.rect.colliderect(sprite.rect):
                self._position = old_position
                self.rect.topleft = self._position
                return


class PrimaryConsumer(Animal):
    def __init__(self, maxHealth: int, damage: int, position: list, size: int) -> None:
        super().__init__(maxHealth, damage, position, size)
        self.speed = 2
        self.image.fill((0, 255, 0))

    def update(self, screen_rect: pygame.Rect, group: pygame.sprite.Group):
        dx, dy = random.choice(
            [(self.speed, 0), (-self.speed, 0), (0, self.speed), (0, -self.speed)]
        )
        self.move(dx, dy, screen_rect, group)


class SecondaryConsumer(Animal):
    def __init__(self, maxHealth: int, damage: int, position: list, size: int) -> None:
        super().__init__(maxHealth, damage, position, size)
        self.speed = 3
        self.image.fill((0, 0, 255))

    def update(self, screen_rect: pygame.Rect, group: pygame.sprite.Group):
        dx, dy = random.choice(
            [(self.speed, 0), (-self.speed, 0), (0, self.speed), (0, -self.speed)]
        )
        self.move(dx, dy, screen_rect, group)


class TertiaryConsumer(Animal):
    def __init__(self, maxHealth: int, damage: int, position: list, size: int) -> None:
        super().__init__(maxHealth, damage, position, size)
        self.speed = 4
        self.image.fill((255, 0, 0))

    def update(self, screen_rect: pygame.Rect, group: pygame.sprite.Group):
        dx, dy = random.choice(
            [(self.speed, 0), (-self.speed, 0), (0, self.speed), (0, -self.speed)]
        )
        self.move(dx, dy, screen_rect, group)
