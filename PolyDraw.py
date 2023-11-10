# PolyDraw.py
import pygame
import numpy as np
from PolyEntities import Tile, City, Unit

def scaled_size(image, dimensions):
    return np.array([image.get_width(), image.get_height()]) // dimensions['scale']

def index_to_pixel(x, y, dimensions, offset = [0,0]):
    A = np.array([[0.4975, 0.4975],[-0.31, 0.31]])
    coordinate = np.array([[x], [y]])
    offset_v = np.array([[dimensions['camera_offset'][0] + offset[0]], [dimensions['camera_offset'][1] + offset[1] + dimensions['screen_dims'][1]/2]])
    resize_matrix = np.diag(dimensions['tile_size'])

    return np.floor(resize_matrix @ (A @ coordinate) + offset_v).astype(int)

class Drawer:
    def __init__(self, dimensions):
        self.dimensions = dimensions

    def draw_map(self, game_map):
        map_surface = pygame.Surface(self.dimensions['screen'].get_size())

        for x in range(game_map.size-1, -1, -1):
            for y in range(game_map.size):
                # Calculate the position of the tile on the screen
                tile_coords = index_to_pixel(x, y, self.dimensions)

                scaled_tile = pygame.transform.scale(game_map.tiles[x][y].image, self.dimensions['tile_size'].astype(int))

                # Draw the scaled tile image at the calculated position
                map_surface.blit(scaled_tile, tile_coords.T[0])

        self.dimensions['screen'].blit(map_surface, (0, 0))

    def draw_unit(self, unit):
        coords = index_to_pixel(unit.x, unit.y, self.dimensions, [8, -30])
        scaled_image = pygame.transform.scale(unit.unit_image, self.dimensions['unit_size'].astype(int))

        self.dimensions['screen'].blit(scaled_image, coords.T[0])

    def draw_frame(self):
        # Additional drawing logic goes here
        pygame.display.flip()
