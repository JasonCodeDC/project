import math
import random


class Map:
    def __init__(self, width, height):
        self.map = [["" for _ in range(width)] for _ in range(height)]
        self._dimensions = [width, height]
        self._biomes = {
            "forest": {
                "weather": ["rain", "mist"],
                "temperature": "mild",
                "speed_mod": 0.7,
            },
            "desert": {
                "weather": ["sunny", "dusty"],
                "temperature": "hot",
                "speed_mod": 0.9,
            },
            "tundra": {
                "weather": ["snow", "blizzard"],
                "temperature": "cold",
                "speed_mod": 0.5,
            },
            "plains": {
                "weather": ["windy", "clear"],
                "temperature": "mild",
                "speed_mod": 1.0,
            },
            "mountains": {
                "weather": ["windy", "snow"],
                "temperature": "cold",
                "speed_mod": 0.3,
            },
        }
        self.biome_names = list(self._biomes.keys())

    def generate_map(self, random_seed=1, num_seeds=10):
        random.seed(random_seed)
        seeds = []
        for _ in range(num_seeds):
            x = random.randint(0, self._dimensions[0] - 1)
            y = random.randint(0, self._dimensions[1] - 1)
            biome = random.choice(self.biome_names)
            seeds.append((x, y, biome))

        for y in range(self._dimensions[1]):
            for x in range(self._dimensions[0]):
                chosen_biome = None
                for sx, sy, biome in seeds:
                    d = math.sqrt((x - sx) ** 2 + (y - sy) ** 2)
                    if d < min_dist:
                        min_dist = d
                        chosen_biome = biome
                self.map[y][x] = chosen_biome

    def get_cell_properties(self, x, y):
        return self._biomes.get(self.map[y][x], {})

    def print_map(self):
        for row in self.map:
            print(" ".join(row))


if __name__ == "__main__":
    import pygame

    map_width, map_height = 100, 50
    window_width, window_height = 800, 500
    cell_width = window_width // map_width
    cell_height = window_height // map_height
    game_map = Map(map_width, map_height)
    game_map.generate_map(random_seed=10023, num_seeds=8)
    game_map.print_map()
    biome_colors = {
        "forest": (34, 139, 34),
        "desert": (237, 201, 175),
        "tundra": (176, 196, 222),
        "plains": (124, 252, 0),
        "mountains": (139, 137, 137),
    }

    pygame.init()
    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Test visuals")
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        for y in range(map_height):
            for x in range(map_width):
                biome = game_map.map[y][x]
                color = biome_colors.get(biome, (0, 0, 0))
                rect = pygame.Rect(
                    x * cell_width, y * cell_height, cell_width, cell_height
                )
                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, (0, 0, 0), rect, 1)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
