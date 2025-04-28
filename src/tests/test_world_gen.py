import random

import pygame

from src.modules.world import Map

pygame.init()

SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720
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


def get_min_cell_size(
    map_area_rect: pygame.Rect, map_width: int, map_height: int
) -> float:
    """
    Return the cell size that makes the map fill the view area exactly.

    Ensures the aspect ratio is preserved and the map fits perfectly in at least one dimension.

    :param map_area_rect: Area of the window the map resides in
    :type map_area_rect: pygame.Rect
    :param map_width: Width of map in tiles
    :type map_width: int
    :param map_height: Height of map in tiles
    :type map_height: int
    :return: Size of a single cell that fills the view area
    :rtype: float
    """
    cell_width = map_area_rect.width / map_width
    cell_height = map_area_rect.height / map_height

    return min(cell_width, cell_height)


def clamp_camera(
    x: int,
    y: int,
    cell_size: int,
    view_rect: pygame.Rect,
    map_width: int,
    map_height: int,
) -> tuple[float, float]:
    """
    Ensure the camera position stays within valid bounds of the map.

    :param x: Current camera x position
    :type x: int
    :param y: Current camera y position
    :type y: int
    :param cell_size: Size of each map cell in pixels
    :type cell_size: int
    :param view_rect: Rectangle representing the viewable area
    :type view_rect: pygame.Rect
    :param map_width: Width of map in tiles
    :type map_width: int
    :param map_height: Height of map in tiles
    :type map_height: int
    :return: Clamped (x, y) coordinates
    :rtype: tuple[float, float]
    """
    visible_width_cells = view_rect.width / cell_size
    visible_height_cells = view_rect.height / cell_size

    max_x = max(0.0, map_width - visible_width_cells)
    max_y = max(0.0, map_height - visible_height_cells)

    return max(0.0, min(x, max_x)), max(0.0, min(y, max_y))


def draw_slider(
    surface: pygame.Surface,
    rect: pygame.Rect,
    label: str,
    value: int,
    min_val: int,
    max_val: int,
    active: bool = False,
) -> pygame.Rect:
    """
    Draw a slider control with label and handle.

    :param surface: Surface to draw on
    :type surface: pygame.Surface
    :param rect: Rectangle defining the slider area
    :type rect: pygame.Rect
    :param label: Text label for the slider
    :type label: str
    :param value: Current value of the slider
    :type value: int
    :param min_val: Minimum value of the slider
    :type min_val: int
    :param max_val: Maximum value of the slider
    :type max_val: int
    :param active: Whether the slider is currently active
    :type active: bool
    :return: Rectangle of the handle for hit detection
    :rtype: pygame.Rect
    """
    pygame.draw.rect(surface, LIGHT_BLUE if active else WHITE, rect)
    pygame.draw.rect(surface, BLACK, rect, 2)

    label_surface = small_font.render(f"{label}: {value}", True, BLACK)
    surface.blit(label_surface, (rect.x + 5, rect.y + 5))

    track_rect = pygame.Rect(rect.x + 10, rect.y + rect.height - 15, rect.width - 20, 6)
    pygame.draw.rect(surface, BLACK, track_rect)

    handle_pos = track_rect.x + (track_rect.width * (value - min_val)) / (
        max_val - min_val
    )
    handle_rect = pygame.Rect(handle_pos - 5, track_rect.y - 5, 10, 16)
    pygame.draw.rect(surface, BLUE if active else BLACK, handle_rect)

    return handle_rect


def draw_button(
    surface: pygame.Surface,
    rect: pygame.Rect,
    text: str,
    colour: tuple,
    active: bool = True,
) -> None:
    """
    Draw a button with text.

    :param surface: Surface to draw on
    :type surface: pygame.Surface
    :param rect: Rectangle defining the button area
    :type rect: pygame.Rect
    :param text: Text to display on the button
    :type text: str
    :param colour: Button colour
    :type colour: tuple
    :param active: Whether the button is currently active (changes background)
    :type active: bool
    """
    pygame.draw.rect(surface, colour if active else GRAY, rect)
    pygame.draw.rect(surface, BLACK, rect, 2)
    text_surface = font.render(text, True, BLACK)
    text_x = rect.x + (rect.width - text_surface.get_width()) // 2
    text_y = rect.y + (rect.height - text_surface.get_height()) // 2
    surface.blit(text_surface, (text_x, text_y))


def handle_map_zoom(
    map_obj: Map,
    map_area_rect: pygame.Rect,
    mouse_pos: tuple[int, int],
    scroll_direction: int,
    cell_size: float,
    camera_x: float,
    camera_y: float,
    map_width: int,
    map_height: int,
) -> tuple[float, float, float]:
    """
    Handle zooming in and out of the map with improved smoothness,
    maintaining the aspect ratio and preventing random lines.

    :param map_obj: The map object
    :type map_obj: Map
    :param map_area_rect: Area of the window the map resides in
    :type map_area_rect: pygame.Rect
    :param mouse_pos: Position of the mouse cursor
    :type mouse_pos: tuple[int, int]
    :param scroll_direction: Direction of mouse scroll (4 for up/zoom in, 5 for down/zoom out)
    :type scroll_direction: int
    :param cell_size: Current cell size in pixels
    :type cell_size: float
    :param camera_x: Current camera x position
    :type camera_x: float
    :param camera_y: Current camera y position
    :type camera_y: float
    :param map_width: Width of map in tiles
    :type map_width: int
    :param map_height: Height of map in tiles
    :type map_height: int
    :return: New cell size and camera position
    :rtype: tuple[float, float, float]
    """
    if not map_obj or not map_obj.map or not map_area_rect.collidepoint(mouse_pos):
        return cell_size, camera_x, camera_y

    mouse_x, mouse_y = mouse_pos
    view_x = mouse_x - map_area_rect.x
    view_y = mouse_y - map_area_rect.y

    world_x = camera_x + view_x / cell_size
    world_y = camera_y + view_y / cell_size

    zoom_factor = 1.1 if scroll_direction == 4 else 0.9
    new_cell_size = cell_size * zoom_factor

    exact_fit_size = get_min_cell_size(map_area_rect, map_width, map_height)

    min_size = max(MIN_CELL_SIZE, exact_fit_size)
    max_size = MAX_CELL_SIZE

    new_cell_size = max(min_size, min(new_cell_size, max_size))

    new_camera_x = world_x - view_x / new_cell_size
    new_camera_y = world_y - view_y / new_cell_size

    clamped_x, clamped_y = clamp_camera(
        new_camera_x,
        new_camera_y,
        new_cell_size,
        map_area_rect,
        map_width,
        map_height,
    )

    return new_cell_size, clamped_x, clamped_y


def handle_slider_drag(
    active_slider: str, mouse_pos: tuple[int, int], slider_rects: dict
) -> tuple[int, int, int] | None:
    """
    Handle dragging of sliders to change map parameters.

    :param active_slider: Which slider is currently being dragged
    :type active_slider: str
    :param mouse_pos: Current mouse position
    :type mouse_pos: tuple[int, int]
    :param slider_rects: Dictionary of slider rectangle data
    :type slider_rects: dict
    :return: Updated map_width, map_height, num_biomes values
    :rtype: tuple[int, int, int] | None
    """
    if not active_slider:
        return None

    map_width, map_height, num_biomes = slider_rects["values"]

    if active_slider == "width":
        rect = slider_rects["width"]
        track_rect = pygame.Rect(
            rect.x + 10,
            rect.y + rect.height - 15,
            rect.width - 20,
            6,
        )
        rel_x = max(0, min(1, (mouse_pos[0] - track_rect.x) / track_rect.width))
        map_width = int(50 + rel_x * 150)

    elif active_slider == "height":
        rect = slider_rects["height"]
        track_rect = pygame.Rect(
            rect.x + 10,
            rect.y + rect.height - 15,
            rect.width - 20,
            6,
        )
        rel_x = max(0, min(1, (mouse_pos[0] - track_rect.x) / track_rect.width))
        map_height = int(50 + rel_x * 150)

    elif active_slider == "biomes":
        rect = slider_rects["biomes"]
        track_rect = pygame.Rect(
            rect.x + 10,
            rect.y + rect.height - 15,
            rect.width - 20,
            6,
        )
        rel_x = max(0, min(1, (mouse_pos[0] - track_rect.x) / track_rect.width))
        num_biomes = max(2, int(2 + rel_x * 28))

    return map_width, map_height, num_biomes


def draw_status(
    screen: pygame.Surface,
    status_text: str,
    error_text: str,
    status_area: pygame.Rect,
    zoom_info: str,
) -> None:
    """
    Draw status information and error messages at the bottom of the screen.

    :param screen: Surface to draw on
    :type screen: pygame.Surface
    :param status_text: Status message to display
    :type status_text: str
    :param error_text: Error message to display
    :type error_text: str
    :param status_area: Rectangle defining the status area
    :type status_area: pygame.Rect
    :param zoom_info: Information about current zoom level
    :type zoom_info: str
    """
    pygame.draw.rect(screen, WHITE, status_area)
    pygame.draw.rect(screen, BLACK, status_area, 2)

    zoom_surface = font.render(zoom_info, True, BLACK)
    screen.blit(
        zoom_surface,
        (SCREEN_WIDTH - zoom_surface.get_width() - 10, SCREEN_HEIGHT - 25),
    )

    status_surface = font.render(status_text, True, BLACK)
    screen.blit(status_surface, (10, SCREEN_HEIGHT - 25))

    if error_text:
        error_surface = font.render(error_text, True, RED)
        screen.blit(error_surface, (10, SCREEN_HEIGHT - 50))


def handle_seed_input() -> tuple[str | int, bool, str]:
    """
    Handle user input for custom seed.

    :return: Tuple containing (seed value, use_random_seed flag, status message)
    :rtype: tuple[str | int, bool, str]
    """
    try:
        seed_input = input("Enter seed (integer or string): ")
        try:
            seed = int(seed_input)
        except ValueError:
            seed = seed_input
        use_random_seed = False
        status_text = f"Custom seed set: {seed}"
        return seed, use_random_seed, status_text
    except Exception as e:
        return None, True, f"Error setting seed: {str(e)}"


def draw_map(
    screen: pygame.Surface,
    map_obj: Map,
    map_area_rect: pygame.Rect,
    cell_size: float,
    camera_x: float,
    camera_y: float,
    map_width: int,
    map_height: int,
) -> None:
    """
    Draw the map with perfect aspect ratio and no random lines.

    :param screen: Surface to draw on
    :type screen: pygame.Surface
    :param map_obj: The map object to render
    :type map_obj: Map
    :param map_area_rect: Rectangle defining the map display area
    :type map_area_rect: pygame.Rect
    :param cell_size: Size of each map cell in pixels
    :type cell_size: float
    :param camera_x: Current camera x position
    :type camera_x: float
    :param camera_y: Current camera y position
    :type camera_y: float
    :param map_width: Width of map in tiles
    :type map_width: int
    :param map_height: Height of map in tiles
    :type map_height: int
    """
    if not map_obj or not map_obj.map:
        return

    surf = pygame.Surface((map_area_rect.width, map_area_rect.height))
    surf.fill(WHITE)

    start_x = int(camera_x)
    start_y = int(camera_y)

    visible_width_cells = int(map_area_rect.width / cell_size) + 2
    visible_height_cells = int(map_area_rect.height / cell_size) + 2

    offset_x = (camera_x - start_x) * cell_size
    offset_y = (camera_y - start_y) * cell_size

    for y in range(visible_height_cells):
        for x in range(visible_width_cells):
            map_x = x + start_x
            map_y = y + start_y

            if 0 <= map_x < map_width and 0 <= map_y < map_height:
                try:
                    colour = map_obj.get_tile_colour(map_x, map_y)

                    x_pos = x * cell_size - offset_x
                    y_pos = y * cell_size - offset_y

                    rect = pygame.Rect(
                        int(x_pos),
                        int(y_pos),
                        int(cell_size) + 1,
                        int(cell_size) + 1,
                    )
                    pygame.draw.rect(surf, colour, rect)
                except Exception:
                    pass

    screen.blit(surf, (map_area_rect.x, map_area_rect.y))


def main():
    """
    Main function that runs the world test application.
    """
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("World Test")

    global font, small_font
    font = pygame.font.SysFont(None, 24)
    small_font = pygame.font.SysFont(None, 20)

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

    map_area_rect = pygame.Rect(0, 70, SCREEN_WIDTH, SCREEN_HEIGHT - 150)
    status_area = pygame.Rect(0, SCREEN_HEIGHT - 30, SCREEN_WIDTH, 30)

    init_button = pygame.Rect(50, 20, 150, 30)
    gen_button = pygame.Rect(220, 20, 150, 30)
    noseed_button = pygame.Rect(390, 20, 150, 30)
    seed_button = pygame.Rect(560, 20, 150, 30)
    apply_button = pygame.Rect(620, SCREEN_HEIGHT - 70, 130, 30)

    slider_width_rect = pygame.Rect(50, SCREEN_HEIGHT - 70, 180, 30)
    slider_height_rect = pygame.Rect(240, SCREEN_HEIGHT - 70, 180, 30)
    slider_biomes_rect = pygame.Rect(430, SCREEN_HEIGHT - 70, 180, 30)

    slider_rects = {
        "width": slider_width_rect,
        "height": slider_height_rect,
        "biomes": slider_biomes_rect,
        "values": (map_width, map_height, num_biomes),
    }

    slider_handles = {"width": None, "height": None, "biomes": None}

    clock = pygame.time.Clock()

    target_cell_size = cell_size
    zoom_speed = 0.2

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()

        if abs(cell_size - target_cell_size) > 0.1:
            cell_size += (target_cell_size - cell_size) * zoom_speed
        else:
            cell_size = target_cell_size

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if init_button.collidepoint(mouse_pos):
                        try:
                            map_obj = Map(map_width, map_height)
                            status_text = (
                                f"Map initialized with size {map_width}x{map_height}"
                            )
                            error_text = ""
                            camera_x = 0
                            camera_y = 0
                            exact_fit_size = get_min_cell_size(
                                map_area_rect, map_width, map_height
                            )
                            cell_size = exact_fit_size
                            target_cell_size = exact_fit_size
                        except Exception as e:
                            error_text = str(e)

                    elif gen_button.collidepoint(mouse_pos):
                        if not map_obj:
                            error_text = (
                                "Map not initialized. Click 'Initialize' first."
                            )
                        else:
                            try:
                                if use_random_seed:
                                    seed = random.randint(1, 10000)
                                map_obj.generate_map(num_biomes, seed)
                                status_text = f"Map generated with {num_biomes} biomes and seed: {seed}"
                                error_text = ""
                                camera_x = 0
                                camera_y = 0
                                exact_fit_size = get_min_cell_size(
                                    map_area_rect, map_width, map_height
                                )
                                cell_size = exact_fit_size
                                target_cell_size = exact_fit_size
                            except Exception as e:
                                error_text = str(e)

                    elif noseed_button.collidepoint(mouse_pos):
                        use_random_seed = True
                        seed = random.randint(1, 10000)
                        status_text = f"Random seed mode enabled: {seed}"

                    elif seed_button.collidepoint(mouse_pos):
                        result = handle_seed_input()
                        if result:
                            seed, use_random_seed, status_text = result
                        if (
                            isinstance(result, tuple)
                            and len(result) == 3
                            and not result[0]
                        ):
                            error_text = result[2]

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
                                exact_fit_size = get_min_cell_size(
                                    map_area_rect, map_width, map_height
                                )
                                cell_size = exact_fit_size
                                target_cell_size = exact_fit_size
                                error_text = ""
                            except Exception as e:
                                error_text = str(e)
                        else:
                            error_text = (
                                "Map not initialized. Click 'Initialize' first."
                            )

                    for slider_name, handle in slider_handles.items():
                        if handle and handle.collidepoint(mouse_pos):
                            active_slider = slider_name
                            break

                    if (
                        map_area_rect.collidepoint(mouse_pos)
                        and map_obj
                        and map_obj.map
                    ):
                        dragging = True
                        drag_start = mouse_pos
                        drag_camera_start = (camera_x, camera_y)

                elif event.button in (4, 5):
                    target_cell_size, camera_x, camera_y = handle_map_zoom(
                        map_obj,
                        map_area_rect,
                        mouse_pos,
                        event.button,
                        cell_size,
                        camera_x,
                        camera_y,
                        map_width,
                        map_height,
                    )

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    dragging = False
                    active_slider = None

            elif event.type == pygame.MOUSEMOTION:
                if active_slider:
                    result = handle_slider_drag(active_slider, mouse_pos, slider_rects)
                    if result:
                        map_width, map_height, num_biomes = result
                        slider_rects["values"] = (map_width, map_height, num_biomes)

                elif dragging and map_obj and map_obj.map:
                    dx = (drag_start[0] - mouse_pos[0]) / cell_size
                    dy = (drag_start[1] - mouse_pos[1]) / cell_size
                    camera_x = drag_camera_start[0] + dx
                    camera_y = drag_camera_start[1] + dy

                    camera_x, camera_y = clamp_camera(
                        camera_x,
                        camera_y,
                        cell_size,
                        map_area_rect,
                        map_width,
                        map_height,
                    )

        keys = pygame.key.get_pressed()
        if map_obj and map_obj.map:
            moved = False
            speed = 5 / cell_size
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
                    new_camera_x,
                    new_camera_y,
                    cell_size,
                    map_area_rect,
                    map_width,
                    map_height,
                )

        if map_obj and map_obj.map and map_area_rect.collidepoint(mouse_pos):
            mouse_x, mouse_y = mouse_pos
            tile_x = int((mouse_x - map_area_rect.x) / cell_size + camera_x)
            tile_y = int((mouse_y - map_area_rect.y) / cell_size + camera_y)

            if 0 <= tile_x < map_width and 0 <= tile_y < map_height:
                try:
                    terrain = map_obj.get_terrain_type(tile_x, tile_y)
                    colour = map_obj.get_tile_colour(tile_x, tile_y)
                    movement_cost = map_obj.get_speed_multiplier(tile_x, tile_y)
                    visibility_multiplier = map_obj.get_visibility(tile_x, tile_y)
                    status_text = f"Tile ({tile_x}, {tile_y}): {terrain=} - {colour=}, {movement_cost=}, {visibility_multiplier=}"
                except Exception as e:
                    error_text = str(e)

        screen.fill(GRAY)

        draw_button(screen, init_button, "Initialize Map", WHITE)
        draw_button(screen, gen_button, "Generate Map", WHITE)
        draw_button(screen, noseed_button, "Random Seed", WHITE, use_random_seed)
        draw_button(screen, seed_button, "Custom Seed", WHITE, not use_random_seed)
        draw_button(screen, apply_button, "Apply Changes", GREEN)

        pygame.draw.rect(screen, WHITE, map_area_rect)
        pygame.draw.rect(screen, BLACK, map_area_rect, 2)

        slider_handles["width"] = draw_slider(
            screen,
            slider_width_rect,
            "Width",
            map_width,
            50,
            200,
            active_slider == "width",
        )
        slider_handles["height"] = draw_slider(
            screen,
            slider_height_rect,
            "Height",
            map_height,
            50,
            200,
            active_slider == "height",
        )
        slider_handles["biomes"] = draw_slider(
            screen,
            slider_biomes_rect,
            "Biomes",
            num_biomes,
            2,
            30,
            active_slider == "biomes",
        )

        draw_map(
            screen,
            map_obj,
            map_area_rect,
            cell_size,
            camera_x,
            camera_y,
            map_width,
            map_height,
        )

        exact_fit_size = get_min_cell_size(map_area_rect, map_width, map_height)
        zoom_percent = int((cell_size / exact_fit_size) * 100)
        zoom_text = f"Zoom: {zoom_percent}%"

        draw_status(screen, status_text, error_text, status_area, zoom_text)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
