# PolyEntities
import pygame
import numpy as np
from enum import Enum


class Map:

    def __init__(self, size):
        # Initialize the map as a 2D array of tile types
        self.tiles = np.empty((size, size), dtype=Tile)
        self.size = size
        self.units = []

        for x in range(size):
            for y in range(size):
                if (x + y) % 2 == 0:
                    self.tiles[x][y] = Tile(Tile.LandType.PLAINS)
                elif x % 3 == 0:
                    self.tiles[x][y] = Tile(Tile.LandType.MOUNTAINS)
                else:
                    self.tiles[x][y] = Tile(Tile.LandType.OCEAN)
    def add_unit(self, unit, x, y):
        self.tiles[x][y].troop = unit
        self.units.append(unit)


class Tile:
    class LandType(Enum):
        PLAINS = 'plains'
        MOUNTAINS = 'mountains'
        COAST = 'coast'
        OCEAN = 'water'

    def __init__(self, land_type, movement_penalty=1):
        self.land_type = land_type
        self.troop = None
        self.city = None
        self.movement_penalty = 1


class Plains(Tile):
    def __init__(self):
        super().__init__(Tile.LandType.PLAINS, 1)


class Mountains(Tile):
    def __init__(self):
        super().__init__(Tile.LandType.MOUNTAINS, 2)


class City:
    # Add City class details if needed
    pass


class Unit:
    class UnitType(Enum):
        SCOUT = 'scout'
        WARRIOR = 'warrior'

    def __init__(self, x, y, game_map):
        self.x = x
        self.y = y
        self.unit_type = Unit.UnitType.SCOUT
        game_map.add_unit(self, x, y)


class Warrior(Unit):
    attack = 2
    defense = 2
    movement = 1
    range = 1

    def __init__(self, x, y, game_map):
        self.health = 10
        super().__init__(x, y, game_map)
        self.unit_type = Unit.UnitType.WARRIOR
