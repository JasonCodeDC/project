import pygame
from pygame.locals import *

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
FPS = 60

# Colours
BLACK = (0x00, 0x00, 0x00)
WHITE = (0xFF, 0xFF, 0xFF)

# Physics constants
GRAVITY = 0.5
JUMP_POWER = 15


class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)

        # Pygame necessities
        self.image = pygame.Surface([15, 35])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()

        # Starting position
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 100

        # Character stats
        self.speed = 5

        # Physics variables
        self.velocity_y = 0
        self.on_ground = False

    def update(self):
        # Apply gravity
        if not self.on_ground:
            self.velocity_y += GRAVITY

        # Horizontal movement
        keys = pygame.key.get_pressed()
        if keys[K_a]:
            self.rect.x -= self.speed
        if keys[K_d]:
            self.rect.x += self.speed

        # Vertical movement
        if keys[K_SPACE] and self.on_ground:
            self.velocity_y = -JUMP_POWER
            self.on_ground = False

        # Apply vertical movement
        self.rect.y += self.velocity_y

        # Ensure on screen
        self.check_screen_collision()

    def check_screen_collision(self):
        # Side boundaries
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

        # Top and bottom boundaries
        if self.rect.top < 0:
            self.rect.top = 0
            self.velocity_y = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.velocity_y = 0
            self.on_ground = True


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
