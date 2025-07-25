import pygame
from pygame.locals import *  # noqa: F403

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
        self.standing_image = pygame.Surface([15, 35])
        self.crouch_image = pygame.Surface([15, 20])
        self.image = self.standing_image
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

        # Crouching variables
        self.crouched = False
        self.original_height = self.image.get_height()

    def update(self):
        # Apply gravity
        if not self.on_ground:
            self.velocity_y += GRAVITY

        # Horizontal movement
        keys = pygame.key.get_pressed()
        if keys[K_a]:  # noqa: F405
            self.rect.x -= self.speed
        if keys[K_d]:  # noqa: F405
            self.rect.x += self.speed

        # Jumping
        if keys[K_SPACE] and self.on_ground:  # noqa: F405
            self.velocity_y = -JUMP_POWER
            self.on_ground = False

        # Crouching
        if keys[K_s] and not self.crouched:  # noqa: F405
            self.crouched = True
            temp_bottom, temp_centerx = self.rect.bottom, self.rect.centerx
            self.image = self.crouch_image
            self.image.fill(WHITE)
            self.rect = self.image.get_rect()
            self.rect.bottom, self.rect.centerx = temp_bottom, temp_centerx

        # Uncrouching
        if not keys[K_s] and self.crouched:  # noqa: F405
            self.crouched = False
            temp_bottom, temp_centerx = self.rect.bottom, self.rect.centerx
            self.image = self.standing_image
            self.image.fill(WHITE)
            self.rect = self.image.get_rect()
            self.rect.bottom, self.rect.centerx = temp_bottom, temp_centerx

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
        if event.type == QUIT:  # noqa: F405
            pygame.quit()
            raise SystemExit(0)

    # Update sprites
    all_sprites.update()

    # Draw
    screen.fill(BLACK)
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)
