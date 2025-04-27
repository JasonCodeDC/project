# modules\world.py

import random
from enum import Enum
from typing import Any, Optional, Tuple


class TerrainTypes(Enum):
    PLAINS = 0
    FOREST = 1
    OCEAN = 2
    MOUNTAIN = 3


class MapError(Exception):
    pass


class Map:
    """
    Represents a 2D grid composed of various terrain types

    :param width: Number of columns per row
    :type width: int
    :param height: Number of rows
    :type height: int
    """

    def __init__(self, width: int, height: int) -> None:
        """
        Constructor method
        """
        self._width = width
        self._height = height
        self.map = None

    def __str__(self) -> Optional[str]:
        """
        Converts the map to a string

        :return: A string which can be printed to console showing the current state of the map, if map has been generated
        :rtype: Optional[str]
        """
        if not self.map:
            return None
        return "\n".join(" ".join(str(terrain) for terrain in row) for row in self.map)

    def __repr__(self) -> str:
        """
        Return a representation of the Map object, useful for debugging

        :return: Representation of map object including dimensions and map data
        :rtype: str
        """
        return f"Map(width:{self._width}, height:{self._height}, map:{self.map})"

    def generate_map(self, seed: Any = None) -> None:
        """
        Placeholder random map generation

        TODO: replace with properly usable implementation

        :param seed: Seed to use with the random number generator
        :type seed: Any
        """
        random.seed(seed)
        self.map = [
            [TerrainTypes(random.randint(0, 3)) for _ in range(self._width)]
            for _ in range(self._height)
        ]

    def get_terrain_type(self, x: int, y: int):
        """
        Returns the terrain type at the given map coordinates

        Coordinates start at (0, 0), and end at (:attr:self._width - 1, :attr:self._height - 1)

        A map must have been generated already using :meth:`Map.generate_map`

        :param x: x coordinate of the tile
        :type x: int
        :param y: y coordinate of the tile
        :type y: int
        :raises MapError:
            * If map is not initialised\n
            * If one or both coordinates are out of bounds
        :return: The :class:`TerrainTypes` member at ``(x, y)``
        :rtype: TerrainTypes
        """
        if not self.map:
            raise MapError("Map not initialised")
        if not (0 <= x < self._width and 0 <= y < self._height):
            raise MapError("Value out of bounds")
        return self.map[y][x]

    def get_tile_colour(self, x: int, y: int) -> Tuple[int, int, int]:
        """ 
        Get the tile colour at a specific (x, y) coordinate

        :param x: x coordinate of the tile
        :type x: int
        :param y: y coordinate of the tile
        :type y: int
        :raises MapError: See :func:`get_terrain_type` for list of reasons
        :return: A tuple containing 3 integers, in RGB format
        :rtype: tuple[int, int, int] 

        """
        colours_dict = {
            TerrainTypes.PLAINS: (0x00, 0xFF, 0x33),
            TerrainTypes.FOREST: (0x11, 0x66, 0x22),
            TerrainTypes.OCEAN: (0x11, 0xBD, 0xD0),
            TerrainTypes.MOUNTAIN: (0xB1, 0xB1, 0xB1),
        }
        return colours_dict[self.get_terrain_type(x, y)]