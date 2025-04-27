# tests\test_world.py

import random

import pygame

from src.modules.world import Map

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
MIN_CELL_SIZE = 1
MAX_CELL_SIZE = 50
DEFAULT_CELL_SIZE = 20
DEFAULT_MAP_WIDTH = 100
DEFAULT_MAP_HEIGHT = 75
DEFAULT_NUM_BIOMES = 10

WHITE = (0xFF, 0xFF, 0xFF)
BLACK = (0x00, 0x00, 0x00)
GRAY = (0xC8, 0xC8, 0xC8)
RED = (0xFF, 0x00, 0x00)
GREEN = (0x00, 0xFF, 0x00)
BLUE = (0x00, 0x00, 0xFF)
LIGHT_BLUE = (0xA0, 0xD0, 0xFF)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("World Test")

font = pygame.font.SysFont(None, 24)
small_font = pygame.font.SysFont(None, 20)


def get_min_cell_size(map_area_rect, map_width, map_height):
    min_cell_width = map_area_rect.width / map_width
    min_cell_height = map_area_rect.height / map_height
    return max(MIN_CELL_SIZE, min(min_cell_width, min_cell_height))


def clamp_camera(x, y, cell_size, view_rect, map_width, map_height):
    max_x = max(0, map_width - view_rect.width / cell_size)
    max_y = max(0, map_height - view_rect.height / cell_size)
    return max(0, min(x, max_x)), max(0, min(y, max_y))


def draw_slider(surface, rect, label, value, min_val, max_val, active=False):
    pygame.draw.rect(surface, LIGHT_BLUE if active else WHITE, rect)
    pygame.draw.rect(surface, BLACK, rect, 2)
    
    label_surface = small_font.render(f"{label}: {value}", True, BLACK)
    surface.blit(label_surface, (rect.x + 5, rect.y + 5))
    
    track_rect = pygame.Rect(rect.x + 10, rect.y + rect.height - 15, rect.width - 20, 6)
    pygame.draw.rect(surface, BLACK, track_rect)
    
    handle_pos = track_rect.x + (track_rect.width * (value - min_val)) / (max_val - min_val)
    handle_rect = pygame.Rect(handle_pos - 5, track_rect.y - 5, 10, 16)
    pygame.draw.rect(surface, BLUE if active else BLACK, handle_rect)
    
    return handle_rect


def main():
    global screen

    map_obj = None
    status_text = "Click 'Initialize' to create a map"
    error_text = ""
    seed = None
    use_random_seed = True

    map_width = DEFAULT_MAP_WIDTH
    map_height = DEFAULT_MAP_HEIGHT
    num_biomes = DEFAULT_NUM_BIOMES
    
    cell_size = DEFAULT_CELL_SIZE
    camera_x = 0
    camera_y = 0

    dragging = False
    drag_start = None
    drag_camera_start = None
    
    active_slider = None
    slider_width_rect = pygame.Rect(50, SCREEN_HEIGHT - 70, 180, 30)
    slider_height_rect = pygame.Rect(240, SCREEN_HEIGHT - 70, 180, 30)
    slider_biomes_rect = pygame.Rect(430, SCREEN_HEIGHT - 70, 180, 30)
    slider_width_handle = None
    slider_height_handle = None
    slider_biomes_handle = None

    clock = pygame.time.Clock()

    init_button = pygame.Rect(50, 20, 150, 30)
    gen_button = pygame.Rect(220, 20, 150, 30)
    noseed_button = pygame.Rect(390, 20, 150, 30)
    seed_button = pygame.Rect(560, 20, 150, 30)
    
    apply_button = pygame.Rect(620, SCREEN_HEIGHT - 70, 130, 30)

    map_area_rect = pygame.Rect(0, 70, SCREEN_WIDTH, SCREEN_HEIGHT - 150)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return SystemExit(0)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos

                if init_button.collidepoint(mouse_pos):
                    try:
                        map_obj = Map(map_width, map_height)
                        status_text = f"Map initialized with size {map_width}x{map_height}"
                        error_text = ""
                        camera_x = 0
                        camera_y = 0
                        cell_size = get_min_cell_size(map_area_rect, map_width, map_height)
                    except Exception as e:
                        error_text = str(e)

                elif gen_button.collidepoint(mouse_pos):
                    if not map_obj:
                        error_text = "Map not initialized. Click 'Initialize' first."
                    else:
                        try:
                            if use_random_seed:
                                seed = random.randint(1, 10000)
                            map_obj.generate_map(num_biomes, seed)
                            status_text = f"Map generated with {num_biomes} biomes and seed: {seed}"
                            error_text = ""
                            camera_x = 0
                            camera_y = 0
                            cell_size = get_min_cell_size(map_area_rect, map_width, map_height)
                        except Exception as e:
                            error_text = str(e)

                elif noseed_button.collidepoint(mouse_pos):
                    use_random_seed = True
                    seed = random.randint(1, 10000)
                    status_text = f"Random seed mode enabled: {seed}"

                elif seed_button.collidepoint(mouse_pos):
                    try:
                        seed_input = input("Enter seed (integer or string): ")
                        try:
                            seed = int(seed_input)
                        except ValueError:
                            seed = seed_input
                        use_random_seed = False
                        status_text = f"Custom seed set: {seed}"
                    except Exception as e:
                        error_text = str(e)
                
                elif apply_button.collidepoint(mouse_pos):
                    if map_obj:
                        try:
                            map_obj = Map(map_width, map_height)
                            if use_random_seed:
                                seed = random.randint(1, 10000)
                            map_obj.generate_map(num_biomes, seed)
                            status_text = f"Map updated: {map_width}x{map_height} with {num_biomes} biomes, seed: {seed}"
                            camera_x = 0
                            camera_y = 0
                            cell_size = get_min_cell_size(map_area_rect, map_width, map_height)
                        except Exception as e:
                            error_text = str(e)
                    else:
                        error_text = "Map not initialized. Click 'Initialize' first."
                
                if slider_width_handle and slider_width_handle.collidepoint(mouse_pos):
                    active_slider = "width"
                elif slider_height_handle and slider_height_handle.collidepoint(mouse_pos):
                    active_slider = "height"
                elif slider_biomes_handle and slider_biomes_handle.collidepoint(mouse_pos):
                    active_slider = "biomes"

                elif event.button == 4:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if map_area_rect.collidepoint((mouse_x, mouse_y)):
                        map_x = (mouse_x - map_area_rect.x) / cell_size + camera_x
                        map_y = (mouse_y - map_area_rect.y) / cell_size + camera_y

                        cell_size = min(cell_size + 2, MAX_CELL_SIZE)

                        camera_x = map_x - (mouse_x - map_area_rect.x) / cell_size
                        camera_y = map_y - (mouse_y - map_area_rect.y) / cell_size
                        camera_x, camera_y = clamp_camera(
                            camera_x, camera_y, cell_size, map_area_rect, map_width, map_height
                        )

                elif event.button == 5:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if map_area_rect.collidepoint((mouse_x, mouse_y)):
                        exact_fit_size = get_min_cell_size(map_area_rect, map_width, map_height)

                        if cell_size > exact_fit_size:
                            map_x = (mouse_x - map_area_rect.x) / cell_size + camera_x
                            map_y = (mouse_y - map_area_rect.y) / cell_size + camera_y

                            new_cell_size = max(cell_size - 2, exact_fit_size)

                            if abs(new_cell_size - exact_fit_size) < 0.5:
                                new_cell_size = exact_fit_size
                                camera_x = 0
                                camera_y = 0
                            else:
                                cell_size = new_cell_size
                                camera_x = (
                                    map_x - (mouse_x - map_area_rect.x) / cell_size
                                )
                                camera_y = (
                                    map_y - (mouse_y - map_area_rect.y) / cell_size
                                )
                                camera_x, camera_y = clamp_camera(
                                    camera_x, camera_y, cell_size, map_area_rect, map_width, map_height
                                )

                            cell_size = new_cell_size

                elif event.button == 1 and map_area_rect.collidepoint(mouse_pos):
                    if map_obj and map_obj.map:
                        exact_fit_size = get_min_cell_size(map_area_rect, map_width, map_height)
                        if cell_size > exact_fit_size:
                            dragging = True
                            drag_start = mouse_pos
                            drag_camera_start = (camera_x, camera_y)

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    dragging = False
                    active_slider = None

            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = event.pos
                
                if active_slider:
                    if active_slider == "width":
                        track_rect = pygame.Rect(slider_width_rect.x + 10, 
                                               slider_width_rect.y + slider_width_rect.height - 15, 
                                               slider_width_rect.width - 20, 6)
                        rel_x = max(0, min(1, (mouse_pos[0] - track_rect.x) / track_rect.width))
                        map_width = int(50 + rel_x * 150)
                    
                    elif active_slider == "height":
                        track_rect = pygame.Rect(slider_height_rect.x + 10, 
                                               slider_height_rect.y + slider_height_rect.height - 15, 
                                               slider_height_rect.width - 20, 6)
                        rel_x = max(0, min(1, (mouse_pos[0] - track_rect.x) / track_rect.width))
                        map_height = int(50 + rel_x * 150)
                    
                    elif active_slider == "biomes":
                        track_rect = pygame.Rect(slider_biomes_rect.x + 10, 
                                               slider_biomes_rect.y + slider_biomes_rect.height - 15, 
                                               slider_biomes_rect.width - 20, 6)
                        rel_x = max(0, min(1, (mouse_pos[0] - track_rect.x) / track_rect.width))
                        num_biomes = max(2, int(2 + rel_x * 28))
                
                elif dragging and map_obj and map_obj.map:
                    dx = (drag_start[0] - mouse_pos[0]) / cell_size
                    dy = (drag_start[1] - mouse_pos[1]) / cell_size
                    camera_x = drag_camera_start[0] + dx
                    camera_y = drag_camera_start[1] + dy

                    camera_x, camera_y = clamp_camera(
                        camera_x, camera_y, cell_size, map_area_rect, map_width, map_height
                    )

        keys = pygame.key.get_pressed()
        speed = 5 / cell_size
        if map_obj and map_obj.map:
            exact_fit_size = get_min_cell_size(map_area_rect, map_width, map_height)
            if cell_size > exact_fit_size:
                moved = False
                new_camera_x, new_camera_y = camera_x, camera_y

                if keys[pygame.K_LEFT]:
                    new_camera_x -= speed
                    moved = True
                if keys[pygame.K_RIGHT]:
                    new_camera_x += speed
                    moved = True
                if keys[pygame.K_UP]:
                    new_camera_y -= speed
                    moved = True
                if keys[pygame.K_DOWN]:
                    new_camera_y += speed
                    moved = True

                if moved:
                    camera_x, camera_y = clamp_camera(
                        new_camera_x, new_camera_y, cell_size, map_area_rect, map_width, map_height
                    )

        mouse_pos = pygame.mouse.get_pos()
        if map_obj and map_obj.map and map_area_rect.collidepoint(mouse_pos):
            mouse_x, mouse_y = mouse_pos
            tile_x = int((mouse_x - map_area_rect.x) / cell_size + camera_x)
            tile_y = int((mouse_y - map_area_rect.y) / cell_size + camera_y)

            if 0 <= tile_x < map_width and 0 <= tile_y < map_height:
                try:
                    terrain = map_obj.get_terrain_type(tile_x, tile_y)
                    color = map_obj.get_tile_colour(tile_x, tile_y)
                    status_text = f"Tile ({tile_x}, {tile_y}): {terrain.name} - RGB Color: {color}"
                except Exception as e:
                    error_text = str(e)

        screen.fill(GRAY)

        pygame.draw.rect(screen, WHITE, init_button)
        pygame.draw.rect(screen, BLACK, init_button, 2)
        init_text = font.render("Initialize Map", True, BLACK)
        screen.blit(init_text, (init_button.x + 20, init_button.y + 7))

        pygame.draw.rect(screen, WHITE, gen_button)
        pygame.draw.rect(screen, BLACK, gen_button, 2)
        gen_text = font.render("Generate Map", True, BLACK)
        screen.blit(gen_text, (gen_button.x + 20, gen_button.y + 7))

        pygame.draw.rect(screen, WHITE if use_random_seed else GRAY, noseed_button)
        pygame.draw.rect(screen, BLACK, noseed_button, 2)
        noseed_text = font.render("Random Seed", True, BLACK)
        screen.blit(noseed_text, (noseed_button.x + 20, noseed_button.y + 7))

        pygame.draw.rect(screen, WHITE if not use_random_seed else GRAY, seed_button)
        pygame.draw.rect(screen, BLACK, seed_button, 2)
        seed_text = font.render("Custom Seed", True, BLACK)
        screen.blit(seed_text, (seed_button.x + 20, seed_button.y + 7))

        pygame.draw.rect(screen, WHITE, map_area_rect)
        pygame.draw.rect(screen, BLACK, map_area_rect, 2)
        
        slider_width_handle = draw_slider(screen, slider_width_rect, "Width", map_width, 50, 200, active_slider == "width")
        slider_height_handle = draw_slider(screen, slider_height_rect, "Height", map_height, 50, 200, active_slider == "height")
        slider_biomes_handle = draw_slider(screen, slider_biomes_rect, "Biomes", num_biomes, 2, 30, active_slider == "biomes")
        
        pygame.draw.rect(screen, GREEN, apply_button)
        pygame.draw.rect(screen, BLACK, apply_button, 2)
        apply_text = font.render("Apply Changes", True, BLACK)
        screen.blit(apply_text, (apply_button.x + 10, apply_button.y + 7))

        if map_obj and map_obj.map:
            exact_fit_size = get_min_cell_size(map_area_rect, map_width, map_height)

            if abs(cell_size - exact_fit_size) < 0.01:
                tile_width = map_area_rect.width / map_width
                tile_height = map_area_rect.height / map_height
                
                surf = pygame.Surface((map_area_rect.width, map_area_rect.height))
                
                for y in range(map_height):
                    for x in range(map_width):
                        try:
                            color = map_obj.get_tile_colour(x, y)
                            rect = pygame.Rect(
                                x * tile_width,
                                y * tile_height,
                                tile_width + 0.5,
                                tile_height + 0.5
                            )
                            pygame.draw.rect(surf, color, rect)
                        except Exception:
                            pass
                
                screen.blit(surf, (map_area_rect.x, map_area_rect.y))
            else:
                view_width = map_area_rect.width
                view_height = map_area_rect.height

                visible_width_tiles = view_width / cell_size
                visible_height_tiles = view_height / cell_size

                visible_width_cells = int(visible_width_tiles) + 2
                visible_height_cells = int(visible_height_tiles) + 2

                start_x = int(camera_x)
                start_y = int(camera_y)

                offset_x = (camera_x - start_x) * cell_size
                offset_y = (camera_y - start_y) * cell_size

                surf = pygame.Surface((map_area_rect.width, map_area_rect.height))
                
                for y in range(visible_height_cells):
                    for x in range(visible_width_cells):
                        map_x = x + start_x
                        map_y = y + start_y

                        if 0 <= map_x < map_width and 0 <= map_y < map_height:
                            try:
                                color = map_obj.get_tile_colour(map_x, map_y)
                                
                                rect = pygame.Rect(
                                    x * cell_size - offset_x,
                                    y * cell_size - offset_y,
                                    cell_size + 0.5,
                                    cell_size + 0.5 
                                )
                                pygame.draw.rect(surf, color, rect)
                            except Exception:
                                pass
                
                screen.blit(surf, (map_area_rect.x, map_area_rect.y))

        status_area = pygame.Rect(0, SCREEN_HEIGHT - 30, SCREEN_WIDTH, 30)
        pygame.draw.rect(screen, WHITE, status_area)
        pygame.draw.rect(screen, BLACK, status_area, 2)

        exact_fit_size = get_min_cell_size(map_area_rect, map_width, map_height)
        zoom_text = f"Zoom: {cell_size:.1f}px/tile"
        if abs(cell_size - exact_fit_size) < 0.01:
            zoom_text += " (Full View)"
        zoom_surface = font.render(zoom_text, True, BLACK)
        screen.blit(
            zoom_surface,
            (SCREEN_WIDTH - zoom_surface.get_width() - 10, SCREEN_HEIGHT - 25),
        )

        status_surface = font.render(status_text, True, BLACK)
        screen.blit(status_surface, (10, SCREEN_HEIGHT - 25))

        if error_text:
            error_surface = font.render(error_text, True, RED)
            screen.blit(error_surface, (10, SCREEN_HEIGHT - 50))

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()