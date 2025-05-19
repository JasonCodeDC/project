import pygame
from pygame.locals import *

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
FPS = 60

# Colours
BLACK = (0x00, 0x00, 0x00)
WHITE = (0xFF, 0xFF, 0xFF)


class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)

        # Pygame necessities
        self.image = pygame.Surface([15, 35])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()

        # Character stats
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[K_w]:
            self.rect.y -= self.speed
        if keys[K_s]:
            self.rect.y += self.speed
        if keys[K_a]:
            self.rect.x -= self.speed
        if keys[K_d]:
            self.rect.x += self.speed


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Platformer shooter")
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
player = Player(all_sprites)

while True:
    # Event loop
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            raise SystemExit(0)

    # Update sprites
    all_sprites.update()

    # Draw
    screen.fill(BLACK)
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)
