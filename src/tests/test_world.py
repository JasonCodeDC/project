import pygame
import random

from modules.world import Map

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
MIN_CELL_SIZE = 1
MAX_CELL_SIZE = 50
DEFAULT_CELL_SIZE = 20
MAP_WIDTH = 100
MAP_HEIGHT = 75
NUM_BIOMES = 10

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("World Test")

font = pygame.font.SysFont(None, 24)

def main():
    global screen

    map_obj = None
    status_text = "Click 'Initialize' to create a map"
    error_text = ""
    seed = None
    use_random_seed = True
    
    cell_size = DEFAULT_CELL_SIZE
    camera_x = 0
    camera_y = 0
    
    dragging = False
    drag_start = None
    drag_camera_start = None
    
    clock = pygame.time.Clock()
    
    init_button = pygame.Rect(50, 20, 150, 30)
    gen_button = pygame.Rect(220, 20, 150, 30)
    noseed_button = pygame.Rect(390, 20, 150, 30)
    seed_button = pygame.Rect(560, 20, 150, 30)
    
    map_area_rect = pygame.Rect(0, 70, SCREEN_WIDTH, SCREEN_HEIGHT - 100)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return SystemExit(0)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                
                if init_button.collidepoint(mouse_pos):
                    try:
                        map_obj = Map(MAP_WIDTH, MAP_HEIGHT)
                        status_text = f"Map initialized with size {MAP_WIDTH}x{MAP_HEIGHT}"
                        error_text = ""
                        camera_x = 0
                        camera_y = 0
                        cell_size = DEFAULT_CELL_SIZE
                    except Exception as e:
                        error_text = str(e)
                
                elif gen_button.collidepoint(mouse_pos):
                    if not map_obj:
                        error_text = "Map not initialized. Click 'Initialize' first."
                    else:
                        try:
                            if use_random_seed:
                                seed = random.randint(1, 10000)
                            map_obj.generate_map(NUM_BIOMES, seed)
                            status_text = f"Map generated with {NUM_BIOMES} biomes and seed: {seed}"
                            error_text = ""
                            camera_x = 0
                            camera_y = 0
                            cell_size = DEFAULT_CELL_SIZE
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
                
                elif event.button == 4:
                    if cell_size < MAX_CELL_SIZE:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        if map_area_rect.collidepoint((mouse_x, mouse_y)):
                            map_x = (mouse_x - map_area_rect.x) / cell_size + camera_x
                            map_y = (mouse_y - map_area_rect.y) / cell_size + camera_y
                            
                            cell_size = min(cell_size + 2, MAX_CELL_SIZE)
                            
                            camera_x = map_x - (mouse_x - map_area_rect.x) / cell_size
                            camera_y = map_y - (mouse_y - map_area_rect.y) / cell_size
                
                elif event.button == 5:
                    if cell_size > MIN_CELL_SIZE:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        if map_area_rect.collidepoint((mouse_x, mouse_y)):
                            map_x = (mouse_x - map_area_rect.x) / cell_size + camera_x
                            map_y = (mouse_y - map_area_rect.y) / cell_size + camera_y
                            
                            cell_size = max(cell_size - 2, MIN_CELL_SIZE)
                            
                            camera_x = map_x - (mouse_x - map_area_rect.x) / cell_size
                            camera_y = map_y - (mouse_y - map_area_rect.y) / cell_size
                
                elif event.button == 1 and map_area_rect.collidepoint(mouse_pos):
                    if map_obj and map_obj.map:
                        dragging = True
                        drag_start = mouse_pos
                        drag_camera_start = (camera_x, camera_y)
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    dragging = False
            
            elif event.type == pygame.MOUSEMOTION:
                if dragging and map_obj and map_obj.map:
                    mouse_pos = event.pos
                    dx = (drag_start[0] - mouse_pos[0]) / cell_size
                    dy = (drag_start[1] - mouse_pos[1]) / cell_size
                    camera_x = drag_camera_start[0] + dx
                    camera_y = drag_camera_start[1] + dy
                    
                    camera_x = max(0, min(camera_x, MAP_WIDTH - map_area_rect.width / cell_size))
                    camera_y = max(0, min(camera_y, MAP_HEIGHT - map_area_rect.height / cell_size))
        
        keys = pygame.key.get_pressed()
        speed = 5 / cell_size  
        if map_obj and map_obj.map:
            if keys[pygame.K_LEFT]:
                camera_x = max(0, camera_x - speed)
            if keys[pygame.K_RIGHT]:
                camera_x = min(MAP_WIDTH - map_area_rect.width / cell_size, camera_x + speed)
            if keys[pygame.K_UP]:
                camera_y = max(0, camera_y - speed)
            if keys[pygame.K_DOWN]:
                camera_y = min(MAP_HEIGHT - map_area_rect.height / cell_size, camera_y + speed)
        
        mouse_pos = pygame.mouse.get_pos()
        if map_obj and map_obj.map and map_area_rect.collidepoint(mouse_pos):
            mouse_x, mouse_y = mouse_pos
            tile_x = int((mouse_x - map_area_rect.x) / cell_size + camera_x)
            tile_y = int((mouse_y - map_area_rect.y) / cell_size + camera_y)
            
            if 0 <= tile_x < MAP_WIDTH and 0 <= tile_y < MAP_HEIGHT:
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
        
        if map_obj and map_obj.map:
            visible_width = int(map_area_rect.width / cell_size) + 1
            visible_height = int(map_area_rect.height / cell_size) + 1
            
            start_x = int(camera_x)
            start_y = int(camera_y)
            
            offset_x = int((camera_x - start_x) * cell_size)
            offset_y = int((camera_y - start_y) * cell_size)
            
            for y in range(visible_height):
                for x in range(visible_width):
                    map_x = x + start_x
                    map_y = y + start_y
                    
                    if 0 <= map_x < MAP_WIDTH and 0 <= map_y < MAP_HEIGHT:
                        try:
                            terrain = map_obj.get_terrain_type(map_x, map_y)
                            color = map_obj.get_tile_colour(map_x, map_y)
                            
                            rect = pygame.Rect(
                                map_area_rect.x + x * cell_size - offset_x,
                                map_area_rect.y + y * cell_size - offset_y,
                                cell_size, cell_size
                            )
                            pygame.draw.rect(screen, color, rect)
                            pygame.draw.rect(screen, BLACK, rect, 1)
                        except Exception:
                            ...
        
        status_area = pygame.Rect(0, SCREEN_HEIGHT - 30, SCREEN_WIDTH, 30)
        pygame.draw.rect(screen, WHITE, status_area)
        pygame.draw.rect(screen, BLACK, status_area, 2)
        
        zoom_text = f"Zoom: {cell_size}px/tile (Scroll to zoom, Drag to pan)"
        zoom_surface = font.render(zoom_text, True, BLACK)
        screen.blit(zoom_surface, (SCREEN_WIDTH - zoom_surface.get_width() - 10, SCREEN_HEIGHT - 25))
        
        status_surface = font.render(status_text, True, BLACK)
        screen.blit(status_surface, (10, SCREEN_HEIGHT - 25))
        
        if error_text:
            error_surface = font.render(error_text, True, RED)
            screen.blit(error_surface, (10, SCREEN_HEIGHT - 50))
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()