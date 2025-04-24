import random


class InvalidDirectionError(Exception):
    pass


class Animal:
    """
    Base implementation of the animals that will be used for predators and prey


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
    def __init__(self, x:int, y:int, speed:int, health:int, strength:int) -> None:
        """
        Constructor method
        """
        self._position = [x, y]
        self._speed = speed
        self._max_health = health
        self._strength = strength

    
    def move(self, direction:str) -> list[int, int]:
        """
        Move the animal :attr:`self._speed` units in a certain direction

        Accepted directions are: ``"up"``, ``"down"``, ``"left"``, ``"right"``

        :param direction: The direction the animal moves towards
        :type direction: str
        :raises InvalidDirectionError: If **direction** is not one of the accepted ones
        :return: Coordinates of the animal after moving
        :rtype: list[int, int]
        """
        match direction:
            case "up":
                self._position[1] -= self._speed
            case "down":
                self._position[1] += self._speed
            case "left":
                self._position[0] -= self._speed
            case "right":
                self._position[0] += self._speed
            case _:
                raise InvalidDirectionError("Invalid direction (up, down, left, right)")
        return self._position
    
    def update(self) -> None:
        """
        Basic implementation for testing the animals

        TODO: implement neural network for animals 
        """
        # outputs = self.think(inputs)
        # self.move(direction = outputs[0], speed = outputs[1])
        self.move(random.choice(["up", "down", "right", "left"]))