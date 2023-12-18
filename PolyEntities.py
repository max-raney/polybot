# PolyEntities
import pygame
import numpy as np

class Map:
    def __init__(self, size):
        # Initialize the map as a 2D array of tile types
        self.tiles = np.empty((size, size), dtype=Tile)
        self.size = size
        self.units = []

        for x in range(size):
            for y in range(size):
                # self.tiles[x][y] = Tile('grass')
                if (x + y) % 2 == 0:
                    self.tiles[x][y] = Tile('grass')
                else:
                    self.tiles[x][y] = Tile('water')

    def add_unit(self, unit, x, y):
        self.tiles[x][y].troop = unit
        self.units.append(unit)

class Tile:
    def __init__(self, land_type):
        self.land_type = land_type
        if land_type == 'grass':
            self.image = pygame.image.load("Art/Terrain/Tiles/ground_1.png")
        else:
            self.image = pygame.image.load("Art/Terrain/Tiles/ground_10.png")

class City:
    # Add City class details if needed
    pass

class Unit:
    unit_image = pygame.image.load('Art/Units/Imperius/Default/Imperius_Default_Scout.png')
    
    def __init__(self, x, y, map):
        self.x = x
        self.y = y
        map.add_unit(self, x, y)

class Warrior(Unit):
    attack = 2
    defense = 2
    movement = 1
    range = 1

    unit_image = pygame.image.load('Art/Units/Imperius/Default/Imperius_Default_Warrior.png')
    
    def __init__(self, x, y, map):
        self.health = 10
        super().__init__(x, y, map)


def scaled_size(image, dimensions):
    return np.array([image.get_width(), image.get_height()]) // dimensions['scale']

def index_to_pixel(x, y, dimensions, offset = [0,0]):
    A = np.array([[0.4975, 0.4975],[-0.31, 0.31]])
    coordinate = np.array([[x], [y]])
    offset_v = np.array([[dimensions['camera_offset'][0] + offset[0]], [dimensions['camera_offset'][1] + offset[1] + dimensions['screen_dims'][1]/2]])
    resize_matrix = np.diag(dimensions['tile_size'])

    return np.floor(resize_matrix @ (A @ coordinate) + offset_v).astype(int)