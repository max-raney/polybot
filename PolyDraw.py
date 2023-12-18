# PolyDraw.py
import pygame
import numpy as np
from PolyEntities import Map, Tile


class Drawer:
    IMAGES = {
        Tile.LandType.GRASS: pygame.image.load("Art/Terrain/Tiles/ground_1.png"),
        Tile.LandType.WATER: pygame.image.load("Art/Terrain/Tiles/ground_10.png"),
    }

    def __init__(self, dimensions, game_map):
        self.dimensions = dimensions
        self.game_map = game_map

    def _calculate_tile_coords(self, x, y, offset=[0, 0]):
        A = np.array([[0.4975, 0.4975], [-0.31, 0.31]])
        coordinate = np.array([[x], [y]])
        offset_v = np.array([[self.dimensions['camera_offset'][0] + offset[0]],
                             [self.dimensions['camera_offset'][1] + offset[1] + self.dimensions['screen_dims'][1] / 2]])
        resize_matrix = np.diag(self.dimensions['tile_size'])

        return np.floor(resize_matrix @ (A @ coordinate) + offset_v).astype(int)

    def _resize_images(self):
        resized_images = {}
        for land_type, image in self.IMAGES.items():
            resized_images[land_type] = pygame.transform.scale(
                image, self.dimensions['tile_size'].astype(int))
        return resized_images

    def _draw_map(self):
        map_surface = pygame.Surface(self.dimensions['screen'].get_size())
        resized_images = self._resize_images()

        for x in range(self.game_map.size - 1, -1, -1):
            for y in range(self.game_map.size):
                tile_coords = self._calculate_tile_coords(x, y)
                scaled_tile = resized_images[self.game_map.tiles[x][y].land_type]
                map_surface.blit(scaled_tile, tile_coords.T[0])

        self.dimensions['screen'].blit(map_surface, (0, 0))

    # Draws all units
    def _draw_units(self):
        for unit in self.game_map.units:
            coords = self._calculate_tile_coords(unit.x, unit.y, [8, -30])
            scaled_image = pygame.transform.scale(unit.unit_image, self.dimensions['unit_size'].astype(int))
            self.dimensions['screen'].blit(scaled_image, coords.T[0])

    def draw_frame(self):
        self._draw_map()
        self._draw_units()
        pygame.display.flip()